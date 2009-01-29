# vim:fileencoding=utf-8
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

# XXX: Is there *any* way to detect instances that are shuffled around?

import ihooks
import os.path
import sys
import types
import zope.testing.testrunner.feature
import inspect


WHITELIST = [('re', 'match', 'sre'),
             ('new', 'module', '__builtin__'),
             ('os', 'error', 'exceptions')]

wrapper_cache = {}
seen = set()


def guess_package_name(frame):
    """Guess which package a code frame originated from."""
    if '__name__' in frame.f_globals:
        return frame.f_globals['__name__']
    filename = frame.f_globals['__file__']
    for mod in sys.modules.values():
        if not hasattr(mod, '__file__'):
            continue
        if os.path.dirname(mod.__file__) == os.path.dirname(filename):
            return mod.__name__
    raise RuntimeError("Can't guess module name for %r" % frame)


def rule_whitelist(import_mod, name, real_mod):
    # No warning for things on the whitelist.
    return (import_mod, name, real_mod) in WHITELIST


def rule_doctest(import_mod, name, real_mod):
    # doctest regularly sticks stuff somewhere else. We
    # ignore those.
    return real_mod in ['doctest', 'zope.testing.doctest']


def rule_stdlib_and_builtins(import_mod, name, real_mod):
    # Some builtins are redirected within the stdlib (and vice versa)
    if import_mod == 'sys' and name in ['stdin', 'stdout']:
        return True
    if import_mod == 'os' and real_mod == 'posix':
        return True
    if name == '__class__' and real_mod == '__builtin__':
        return True
    if import_mod == '__builtin__' and real_mod == 'exceptions':
        return True
    if (import_mod == 'types' or
          import_mod.startswith('xml.dom')) and real_mod == '__builtin__':
        # No warning for the types from the type module that
        # really originate from builtins
        return True


def rule_intra_package_reimport(import_mod, name, real_mod):
    # Don't warn if the package of a module re-exports a symbol.
    return import_mod.split('.') == real_mod.split('.')[:-1]


def rule_intra_package_reimport2(import_mod, name, real_mod):
    # Don't warn if symbols of an underscore module are reimported
    # by a module belonging to the same package.
    real_path = real_mod.split('.')
    real_module = real_path[-1]
    base = '.'.join(real_path[:-1]) + '.'
    return real_module.startswith('_') and import_mod.startswith(base)


def rule_unclean_c_module(import_mod, name, real_mod):
    # The real module seems to be a C-Module which is regularly masked using
    # another Python module in front of it.
    if (real_mod in sys.modules and
            hasattr(sys.modules[real_mod], '__file__')):
        real_file = sys.modules[real_mod].__file__
        extension = os.path.splitext(real_file)[1]
        if not extension.startswith('.py'):
            return True
    if real_mod.startswith('_') and real_mod == import_mod.split('.')[-1]:
        # Looks like a C-module which doesn't declare its
        # package path correctly.
        return True


def rule_zope_deferredimport(import_mod, name, real_mod):
    if real_mod == 'zope.deferredimport.deferredmodule':
        return True


def rule_internal_underscore_reimport(import_mod, name, real_mod):
    # Looks like an internal module, prefixed with _ was exported to the same
    # module name without an _
    return real_mod.split('.')[-1] == '_' + import_mod.split('.')[-1]



RULES = [func for name, func in locals().items()
         if name.startswith('rule_')]


class IndirectAttributeAccessChecker(types.ModuleType):

    def __init__(self, module, options):
        self.__import_checker_module = module
        self.__import_checker_options = options

    def __eq__(self, other):
        if isinstance(other, IndirectAttributeAccessChecker):
            other = (
                other._IndirectAttributeAccessChecker__import_checker_module)
        return other == self._IndirectAttributeAccessChecker__import_checker_module

    def __setattr__(self, name, value):
        if name.startswith('_IndirectAttributeAccessChecker__import_checker_'):
            object.__setattr__(self, name.replace('_IndirectAttributeAccessChecker', ''), value)
        else:
            module = self.__import_checker_module
            setattr(module, name, value)

    def __getattribute__(self, name):
        if name.startswith('_IndirectAttributeAccessChecker__import_checker_'):
            return object.__getattribute__(self, name.replace('_IndirectAttributeAccessChecker', ''))
        module = self.__import_checker_module
        attr = getattr(module, name)
        if not isinstance(attr,
                (types.ClassType, types.TypeType, types.FunctionType)):
            return attr
        if attr.__module__ == module.__name__:
            return attr

        frame = sys._getframe(1)
        show_only_from = self.__import_checker_options.indirect_source
        if show_only_from:
            for include in show_only_from:
                if guess_package_name(frame).startswith(include):
                    break
            else:
                # This warning was caused in a module not under the
                # `indirect source` parameter.
                return attr

        import_mod, real_mod = module.__name__, attr.__module__
        for rule in RULES:
            # Warning suppression rules: if no rule matches, we display
            # a warning.
            if rule(import_mod, name, real_mod):
                break
        else:
            attr_type = type(attr).__name__
            file = frame.f_code.co_filename
            line = frame.f_lineno
            signature = (import_mod, name, real_mod, file, line)
            if signature not in seen:
                print ("WARNING: indirect import of %s `%s.%s` (originally defined at `%s`)"
                        % (attr_type, import_mod, name, real_mod))
                print "caused at %s:%s" % (file, line)
                seen.add(signature)

        return attr


class IndirectImportWarner(ihooks.ModuleImporter):

    def __init__(self, options):
        ihooks.ModuleImporter.__init__(self)
        self.options = options

    def import_module(self, name, globals=None, locals=None,
            fromlist=None):
        result = ihooks.ModuleImporter.import_module(
            self, name, globals=globals, locals=locals, fromlist=fromlist)
        if id(result) not in wrapper_cache:
            checker = IndirectAttributeAccessChecker(
                result, self.options)
            if not hasattr(result, '__all__'):
                # Support * imports
                checker.__all__ = [x for x in dir(result) if not
                        x.startswith('_')]
            wrapper_cache[id(result)] = checker
        return wrapper_cache[id(result)]

    def import_it(self, partname, fqname, parent, force_load=0):
        result = ihooks.ModuleImporter.import_it(self, partname, fqname,
                parent, force_load)
        if result is not None:
            if hasattr(result, '__file__') and not '.' in os.path.basename(result.__file__):
                # Smells like a package which didn't get __init__.py
                # attached to its path.
                result.__file__ = os.path.join(result.__file__, '__init__.py')
        return result

    def determine_parent(self, globals):
        if not globals or not "__name__" in globals:
            return None
        pname = globals['__name__']
        if "__path__" in globals:
            parent = self.modules[pname]
            # XXX The original class used to use an `assert` here which
            # conflicts with doctest creating copys of the globs.
            # assert globals is parent.__dict__
            return parent
        if '.' in pname:
            i = pname.rfind('.')
            pname = pname[:i]
            parent = self.modules[pname]
            assert parent.__name__ == pname
            return parent
        return None


class ImportChecker(zope.testing.testrunner.feature.Feature):
    """Monitor indirect imports and warn about them."""

    active = True

    def global_setup(self):
        if self.runner.options.indirect_imports:
            ihooks.install(IndirectImportWarner(self.runner.options))

    def global_teardown(self):
        if self.runner.options.indirect_imports:
            ihooks.uninstall()
