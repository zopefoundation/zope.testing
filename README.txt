========================================
zope.testing package Readme
========================================

This package provides a flexible testing framework.  It includes a
flexible test runner, and supports both doctest and unittest.

Additional Zope-specific testing features are in the zope.app.testing
package.


cleanup.py
-----------

Provides a mixin class for cleaning up after tests that
make global changes.

doctest.py
-----------

Enhanced version of python's standard doctest.py.
Better test count (one per block instead of one per docstring).

formparser.py
--------------

An HTML parser that extracts form information.

This is intended to support functional tests that need to extract
information from HTML forms returned by the publisher.

See *formparser.txt* for documentation.

loggingsupport.py
-----------------------

Support for testing logging code

If you want to test that your code generates proper log output, you
can create and install a handler that collects output.


loghandler.py
-------------

Logging handler for tests that check logging output.


renormalizing.py
-----------------

Regular expression pattern normalizing output checker.
Useful for doctests.


testrunner.py
--------------

The test runner module.  This is typically wrapped by a test.py script that
sets up options to run a particular set of tests.

For overview of usage, see testrunner.txt.

tests.py
---------

Test script for the testing package. Invokes testrunner.


Changes
-------

See CHANGES.txt.


Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.testing/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.testing/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.testing/trunk

- Note that the 'src/zope/testing' package is acutally a 'svn:externals' link
  to the corresponding package in the Zope3 trunk (or to a specific tag,
  for released versions of the package).
