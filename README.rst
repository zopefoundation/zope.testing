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

For complete documentation, see https://zopetesting.readthedocs.io

cleanup
  Provides a mixin class for cleaning up after tests that
  make global changes.

  See `zope.testing.cleanup`

formparser
  An HTML parser that extracts form information.

  This is intended to support functional tests that need to extract
  information from HTML forms returned by the publisher.

  See `zope.testing.formparser`

loggingsupport
  Support for testing logging code

  If you want to test that your code generates proper log output, you
  can create and install a handler that collects output.

  See `zope.testing.loggingsupport`

module
  Lets a doctest pretend to be a Python module.

  See `zope.testing.module`

renormalizing
  Regular expression pattern normalizing output checker.
  Useful for doctests.

  See `zope.testing.renormalizing`

setupstack
  A simple framework for automating doctest set-up and tear-down.

  See `zope.testing.setupstack`

wait
  A small utility for dealing with timing non-determinism

  See `zope.testing.wait`

doctestcase
  Support for defining doctests as methods of `unittest.TestCase`
  classes so that they can be more easily found by test runners, like
  nose, that ignore test suites.

  See `zope.testing.doctestcase`

Getting started developing zope.testing
=======================================

``zope.testing`` uses ``tox``.  To start, install ``tox`` using ``pip install tox``.
Now, run ``tox`` to run the ``zope.testing`` test suite.
