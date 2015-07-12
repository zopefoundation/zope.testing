r"""Doctests in TestCase classes

The original doctest unittest integration was based on unittest test
suites, which have falled out of favor. This module provides a way to
define doctests inside of unittest TestCase classes. It also provides
better integration with unittest test fixtures, because doctests use
setup provided by the containing test case class.

You can define doctests in 4 ways:

- references to named files

- strings

- decorated functions with docstrings

- reference to named files decorating test-specific setup functions

Here are some examples::

    import unittest
    from zope.testing.doctestcase import DocTest

    class MyTest(unittest.TestCase):

        test1 = DocTest('test1.txt')

        test2 = DocTest('''
        >>> 1 + 1
        2
        ''')

        @DocTest
        def test3(self):
            '''
            >>> test.x
            3
            '''
            self.x = 3

        @DocTest('test4.txt')
        def test4(self):
            self.y = 5

The exampe illustrates some additional points:

- the test case ``self`` argument is exposed to the doctest as the
  ``test`` global variable.  This gives the test access to any
  attributes defined in the test case.

- The body of a function who's docstring defines a doctest is run before
  the test, providing test-specific setup, if desired.

- A the return value of the doctest function can be used to decorate a
  function.  The decorated function is run before the test is executed.
  This provides a way to provide some test-specfic setup, if desired.

  Note that the docstring, of any, of the decorated function is ignored.

Also note that, unlike regular unit tests, module globals from the
module defining the tests are't included in the test globals.

"""
import doctest as standard_doctest
import inspect
import os
import re
import sys
import types

non_identifier_sub = re.compile('[^a-zA-Z_0-9]').sub

def DocTest(test=None, **kw):
    """Define a doctest within a unittest.TestCase

    You can pass doctest option flags and a custon checker.
    """
    if test is None:
        return lambda test: DocTest(test, **kw)
    return DTMaker(test, **kw).test_func

class DTMaker:
    parser = standard_doctest.DocTestParser()

    def __init__(self, test, optionflags=0, checker=None):
        self.optionflags = (
            optionflags | standard_doctest.IGNORE_EXCEPTION_DETAIL)
        self.checker = checker
        self.setups = []

        if isinstance(test, str):
            if '\n' not in test:
                base = os.path.dirname(os.path.abspath(
                    sys._getframe(2).f_globals['__file__']
                    ))
                path = os.path.join(base, test)
                self.test = open(path).read()
                self.name = os.path.basename(path)
                self.path = path
            else:
                self.test = test
                self.name = self.path = '<string>'
            self.lineno = 0
        else:
            # func
            self.setups.append(test)
            doc = test.__doc__
            if doc:
                self.test = doc
                self.name = test.__name__
                self.path = inspect.getsourcefile(test)
                self.lineno = inspect.getsourcelines(test)[1]
            else:
                raise ValueError(test, "has no docstring")
            self.name = test.__name__

        def test_func(test):
            if isinstance(test, types.FunctionType):
                self.setups.append(test)
                return self.test_func

            for setup in self.setups:
                setup(test)

            standard_doctest.DocTestCase(
                self.parser.get_doctest(
                    self.test,
                    dict(test=test),
                    self.name,
                    self.path,
                    self.lineno,
                    ),
                optionflags = self.optionflags,
                checker = self.checker,
                ).runTest()

        self.test_func = test_func
