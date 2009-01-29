# vim:fileencoding=utf-8
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import ihooks
import os.path
import sys
import types
import zope.testing.testrunner.feature
import inspect


WHITELIST = [('re', 'match', 'sre'),
             ('os', 'error', 'exceptions')]

wrapper_cache = {}
seen = set()


class IndirectAttributeAccessChecker(types.ModuleType):

    def __init__(self, module, options):
        self.__import_checker_module = module
        self.__import_checker_options = options

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
        if getattr(attr, '__module__', None) is None:
            return attr
        if attr.__module__ == module.__name__:
            return attr

        frame = sys._getframe(1)
        show_only_from = self.__import_checker_options.indirect_source
        if show_only_from:
            for include in show_only_from:
                if frame.f_globals['__name__'].startswith(include):
                    break
            else:
                # This warning was caused in a module not under the
                # `indirect source` parameter.
                return attr

        import_mod, real_mod = module.__name__, attr.__module__
        if (import_mod, name, real_mod) in WHITELIST:
            # No warning for things on the whitelist.
            pass
        elif real_mod in ['doctest', 'zope.testing.doctest']:
            # doctest regularly sticks stuff somewhere else. We
            # ignore those.
            pass
        elif import_mod == 'sys' and name in ['stdin', 'stdout']:
            # Those are redirected regularly.
            pass
        elif import_mod == 'os' and real_mod == 'posix':
            pass
        elif name == '__class__' and real_mod == '__builtin__':
            pass
        elif (import_mod == 'types' or
              import_mod.startswith('xml.dom')) and real_mod == '__builtin__':
            # No warning for the types from the type module that
            # really originate from builtins
            pass
        elif import_mod.split('.') == real_mod.split('.')[:-1]:
            # Don't warn if the package of a module re-exports a
            # symbol.
            pass
        elif real_mod in sys.modules and hasattr(sys.modules[real_mod], '__file__') and not sys.modules[real_mod].__file__.endswith('.py'):
            # The real module seems to be a C-Module which is
            # regularly masked using another Python module in front
            # of it.
            pass
        elif real_mod.split('.')[-1] == '_' + import_mod.split('.')[-1]:
            # Looks like an internal module, prefixed with _ was
            # exported to the same module name without an _
            pass
        elif real_mod.startswith('_') and real_mod == import_mod.split('.')[-1]:
            # Looks like a C-module which doesn't declare its
            # package path correctly.
            pass
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
