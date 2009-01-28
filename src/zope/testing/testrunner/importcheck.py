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


class IndirectAttributeAccessChecker(types.ModuleType):

    def __init__(self, module):
        self.__import_checker_module = module

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
        if attr.__module__ != module.__name__:
            import_mod, real_mod = module.__name__, attr.__module__
            if (import_mod, name, real_mod) in WHITELIST:
                # No warning for things on the whitelist.
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
                print ("WARNING: indirect import of %s `%s.%s` (originally defined at `%s`)"
                        % (attr_type, import_mod, name, real_mod))
                frame = sys._getframe(1)
                file = frame.f_code.co_filename
                line = frame.f_lineno
                print "caused at %s:%s" % (file, line)
        return attr


class IndirectImportWarner(ihooks.ModuleImporter):

    def import_module(self, name, globals=None, locals=None,
            fromlist=None):
        result = ihooks.ModuleImporter.import_module(
            self, name, globals=globals, locals=locals, fromlist=fromlist)
        checker = IndirectAttributeAccessChecker(result)
        if not hasattr(result, '__all__'):
            checker.__all__ = [x for x in dir(result) if not
                    x.startswith('_')]
        return checker

    def import_it(self, partname, fqname, parent, force_load=0):
        result = ihooks.ModuleImporter.import_it(self, partname, fqname,
                parent, force_load)
        if result is not None:
            if hasattr(result, '__file__') and not '.' in os.path.basename(result.__file__):
                # Smells like a package which didn't get __init__.py
                # attached to its path.
                result.__file__ = os.path.join(result.__file__, '__init__.py')
        return result


class ImportChecker(zope.testing.testrunner.feature.Feature):
    """Monitor indirect imports and warn about them."""

    active = True

    def global_setup(self):
        ihooks.install(IndirectImportWarner())

    def global_teardown(self):
        ihooks.uninstall()
