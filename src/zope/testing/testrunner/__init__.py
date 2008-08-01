##############################################################################
#
# Copyright (c) 2004-2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test runner

$Id$
"""

import sys
import unittest


import zope.testing.testrunner.interfaces



def run(defaults=None, args=None):
    # This function is here to make the whole test runner compatible before
    # the large refactoring.
    # XXX Bah. Lazy import to avoid circular/early import problems
    from zope.testing.testrunner.runner import Runner
    runner = Runner(defaults, args)
    runner.run()
    if runner.failed and runner.options.exitwithstatus:
        sys.exit(1)
    return runner.failed


###############################################################################
# Install 2.4 TestSuite __iter__ into earlier versions

if sys.version_info < (2, 4):
    def __iter__(suite):
        return iter(suite._tests)
    unittest.TestSuite.__iter__ = __iter__
    del __iter__

# Install 2.4 TestSuite __iter__ into earlier versions
###############################################################################

if __name__ == '__main__':
    # allow people to try out the test runner with
    # python -m zope.testing.testrunner --test-path .
    run()
