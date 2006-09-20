************
zope.testing
************

.. contents::

This package provides a flexible testing framework.  It includes a
flexible test runner, and supports both doctest and unittest.

cleanup.py
  Provides a mixin class for cleaning up after tests that
  make global changes.

doctest.py
  Enhanced version of python's standard doctest.py.
  Better test count (one per block instead of one per docstring).

  (We need to merge this with the standard doctest module.)

formparser.py
  An HTML parser that extracts form information.

  This is intended to support functional tests that need to extract
  information from HTML forms returned by the publisher.

loggingsupport.py
  Support for testing logging code

  If you want to test that your code generates proper log output, you
  can create and install a handler that collects output.

loghandler.py
  Logging handler for tests that check logging output.

renormalizing.py
  Regular expression pattern normalizing output checker.
  Useful for doctests.

testrunner.py
  The test runner module.  This is typically wrapped by a test.py script that
  sets up options to run a particular set of tests.
