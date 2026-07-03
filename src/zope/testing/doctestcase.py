r"""Doctests in TestCase classes

"""
import doctest
import inspect
import io
import os
import re
import sys
import types
import unittest
import warnings


warnings.warn(
    'zope.testing.doctestcase is deprecated and will be removed in a '
    'future release. Use plain doctest (e.g. doctest.DocTestSuite or '
    'doctest.DocFileSuite) instead.',
    DeprecationWarning,
    stacklevel=2)


__all__ = [
    'doctestmethod',
    'method',

    'docteststring',
    'string',

    'doctestfile',
    'file',

    'doctestfiles',
    'files',
]

_parser = doctest.DocTestParser()


def _testify(name):
    if not name.startswith('test'):
        name = 'test_' + name
    return name


def doctestmethod(test=None, optionflags=0, checker=None):
    """Define a doctest from a method within a unittest.TestCase.

    The method's doc string provides the test source. Its body is
    called before the test and may perform test-specific setup.

    You can pass doctest option flags and a custon checker.

    Variables defined in the enclosing module are available in the test.

    If a test case defines a globs attribute, it must be a dictionary
    and its contents are added to the test globals.

    The test object is available as the variable ``self`` in the test.
    """
    if test is None:
        return lambda test: _doctestmethod(test, optionflags, checker)

    return _doctestmethod(test, optionflags, checker)


#: Alias of `doctestmethod`
method = doctestmethod


def _doctestmethod(test, optionflags, checker):
    doc = test.__doc__
    if not doc:
        raise ValueError(test, "has no docstring")
    setup = test
    name = test.__name__
    path = inspect.getsourcefile(test)
    lineno = inspect.getsourcelines(test)[1]

    fglobs = sys._getframe(3).f_globals

    def test_method(self):
        setup(self)
        _run_test(self, doc, fglobs.copy(), name, path,
                  optionflags, checker, lineno=lineno)

    test_method.__name__ = _testify(name)

    return test_method


def docteststring(test, optionflags=0, checker=None, name=None):
    """Define a doctest from a string within a unittest.TestCase.

    You can pass doctest option flags and a custon checker.

    Variables defined in the enclosing module are available in the test.

    If a test case defines a globs attribute, it must be a dictionary
    and its contents are added to the test globals.

    The test object is available as the variable ``self`` in the test.
    """
    fglobs = sys._getframe(2).f_globals

    def test_string(self):
        _run_test(self, test, fglobs.copy(), '<string>', '<string>',
                  optionflags, checker)
    if name:
        test_string.__name__ = _testify(name)

    return test_string


#: Alias of `docteststring`
string = docteststring

_not_word = re.compile(r'\W')


def doctestfile(path, optionflags=0, checker=None):
    """Define a doctest from a test file within a unittest.TestCase.

    The file path may be relative or absolute. If its relative (the
    common case), it will be interpreted relative to the directory
    containing the referencing module.

    You can pass doctest option flags and a custon checker.

    If a test case defines a globs attribute, it must be a dictionary
    and its contents are added to the test globals.

    The test object is available as the variable ``test`` in the test.

    The resulting object can be used as a function decorator. The
    decorated method is called before the test and may perform
    test-specific setup. (The decorated method's doc string is ignored.)
    """
    base = os.path.dirname(os.path.abspath(
        sys._getframe(2).f_globals['__file__']
    ))
    path = os.path.join(base, path)
    with open(path) as f:
        test = f.read()
    name = os.path.basename(path)

    def test_file(self):
        if isinstance(self, types.FunctionType):
            setup = self

            def test_file_w_setup(self):
                setup(self)
                _run_test(self, test, {}, name, path, optionflags, checker,
                          'test')

            test_file_w_setup.__name__ = _testify(setup.__name__)
            test_file_w_setup.filepath = path
            test_file_w_setup.filename = os.path.basename(path)
            return test_file_w_setup

        _run_test(self, test, {}, name, path, optionflags, checker, 'test')

    test_file.__name__ = name_from_path(path)
    test_file.filepath = path
    test_file.filename = os.path.basename(path)

    return test_file


#: Alias of `doctestfile`
file = doctestfile


def doctestfiles(*paths, **kw):
    """Define doctests from test files in a decorated class.

    Multiple files can be specified. A member is added to the
    decorated class for each file.

    The file paths may be relative or absolute. If relative (the
    common case), they will be interpreted relative to the directory
    containing the referencing module.

    You can pass doctest option flags and a custon checker.

    If a test case defines a globs attribute, it must be a dictionary
    and its contents are added to the test globals.

    The test object is available as the variable ``test`` in the test.

    The resulting object must be used as a class decorator.
    """
    def doctestfiles_(class_):
        for path in paths:
            name = name_from_path(path)
            test = doctestfile(path, **kw)
            test.__name__ = name
            setattr(class_, name, test)

        return class_

    return doctestfiles_


#: Alias of `doctestfiles`
files = doctestfiles


def name_from_path(path):
    return _testify(
        _not_word.sub('_', os.path.splitext(os.path.basename(path))[0])
    )


def _run_test(self, test, globs, name, path,
              optionflags, checker, testname='self', lineno=0):
    # This deliberately avoids DocTestCase.run()/.runTest(), which (as of
    # Python 3.15) report each example as a separate subtest of the
    # enclosing unittest result, rather than raising on failure. We want
    # the whole doctest to be run in one go, with any failures raised
    # here so that they become a failure of *this* test.
    globs.update(getattr(self, 'globs', ()))
    globs[testname] = self
    optionflags |= doctest.IGNORE_EXCEPTION_DETAIL
    if not (optionflags & doctest.REPORTING_FLAGS):
        optionflags |= getattr(doctest, '_unittest_reportflags', 0)

    dtest = _parser.get_doctest(test, globs, name, path, lineno)
    runner = doctest.DocTestRunner(
        optionflags=optionflags, checker=checker, verbose=False)
    out = io.StringIO()
    old_stdout = sys.stdout
    try:
        runner.DIVIDER = "-" * 70
        results = runner.run(dtest, out=out.write, clear_globs=False)
        # TestResults.skipped was only added in Python 3.13.
        if hasattr(results, 'skipped') and (
                results.skipped == results.attempted):
            raise unittest.SkipTest("all examples were skipped")
    finally:
        sys.stdout = old_stdout

    if results.failed:
        lineno = ('unknown line number' if dtest.lineno is None
                  else str(dtest.lineno))
        lname = dtest.name.rsplit('.', 1)[-1]
        raise self.failureException(
            'Failed doctest test for %s\n'
            '  File "%s", line %s, in %s\n\n%s'
            % (dtest.name, dtest.filename, lineno, lname,
               out.getvalue().rstrip('\n')))
