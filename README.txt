************
zope.testing
************

.. contents::

This package provides a number of testing frameworks.  It includes a
flexible test runner, and supports both doctest and unittest.

cleanup.py
  Provides a mixin class for cleaning up after tests that
  make global changes.

doctest.py
  Enhanced version of python's standard doctest.py.
  Better test count (one per block instead of one per docstring).
  See doctest.txt.

  (We need to merge this with the standard doctest module.)

doctestunit.py
  Provides a pprint function that always sorts dictionary entries
  (pprint.pprint from the standard library doesn't sort very short ones,
  sometimes causing test failures when the internal order changes).

formparser.py
  An HTML parser that extracts form information.

  This is intended to support functional tests that need to extract
  information from HTML forms returned by the publisher.

  See formparser.txt.

loggingsupport.py
  Support for testing logging code

  If you want to test that your code generates proper log output, you
  can create and install a handler that collects output.

loghandler.py
  Logging handler for tests that check logging output.

module.py
  Lets a doctest pretend to be a Python module.

  See module.txt.

renormalizing.py
  Regular expression pattern normalizing output checker.
  Useful for doctests.

server.py
  Provides a simple HTTP server compatible with the zope.app.testing
  functional testing API.  Lets you interactively play with the system
  under test.  Helpful in debugging functional doctest failures.

setupstack.py
  A simple framework for automating doctest set-up and tear-down.
  See setupstack.txt.

testrunner
  The test runner package.  This is typically wrapped by a test.py script that
  sets up options to run a particular set of tests.


Getting started
***************

zope.testing uses buildout.  To start, run ``python bootstrap.py``.  It will
create a number of directories and the ``bin/buildout`` script.  Next, run
``bin/buildout``.  It will create a test script for you.  Now, run ``bin/test``
to run the zope.testing test suite.
