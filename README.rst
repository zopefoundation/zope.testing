=================
``zope.testing``
=================

.. image:: https://img.shields.io/pypi/v/zope.testing.svg
    :target: https://pypi.python.org/pypi/zope.testing/
    :alt: Latest Version

.. image:: https://github.com/zopefoundation/zope.testing/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/zope.testing/actions/workflows/tests.yml

.. image:: https://readthedocs.org/projects/zopetesting/badge/?version=latest
        :target: http://zopetesting.readthedocs.org/en/latest/
        :alt: Documentation Status

This package provides a number of testing frameworks.

cleanup
  Provides a mixin class for cleaning up after tests that
  make global changes.

formparser
  An HTML parser that extracts form information.

  **Python 2 only**

  This is intended to support functional tests that need to extract
  information from HTML forms returned by the publisher.

  See formparser.txt.

loggingsupport
  Support for testing logging code

  If you want to test that your code generates proper log output, you
  can create and install a handler that collects output.

loghandler
  Logging handler for tests that check logging output.

module
  Lets a doctest pretend to be a Python module.

  See module.txt.

renormalizing
  Regular expression pattern normalizing output checker.
  Useful for doctests.

server
  Provides a simple HTTP server compatible with the zope.app.testing
  functional testing API.  Lets you interactively play with the system
  under test.  Helpful in debugging functional doctest failures.

  **Python 2 only**

setupstack
  A simple framework for automating doctest set-up and tear-down.
  See setupstack.txt.

wait
  A small utility for dealing with timing non-determinism
  See wait.txt.

doctestcase
  Support for defining doctests as methods of ``unittest.TestCase``
  classes so that they can be more easily found by test runners, like
  nose, that ignore test suites.

.. contents::

Getting started developing zope.testing
=======================================

``zope.testing`` uses ``tox``.  To start, install ``tox`` using ``pip install tox``.
Now, run ``tox`` to run the ``zope.testing`` test suite.
