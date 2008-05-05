##############################################################################
#
# Copyright (c) 2004-2008 Zope Corporation and Contributors.
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
"""Subprocess support.

$Id: __init__.py 86218 2008-05-03 14:17:26Z ctheune $
"""

import sys
import time
import zope.testing.testrunner.feature


class SubProcess(zope.testing.testrunner.feature.Feature):
    """Lists all tests in the report instead of running the tests."""

    def __init__(self, runner):
        super(SubProcess, self).__init__(runner)
        self.active = bool(runner.options.resume_layer)

    def global_setup(self):
        self.original_stderr = sys.stderr
        sys.stderr = sys.stdout
        self.runner.options.verbose = False

    def report(self):
        sys.stdout.close()
        # Communicate with the parent.  The protocol is obvious:
        print >> self.original_stderr, self.runner.ran, \
                len(self.runner.failures), len(self.runner.errors)
        for test, exc_info in self.runner.failures:
            print >> self.original_stderr, ' '.join(str(test).strip().split('\n'))
        for test, exc_info in self.runner.errors:
            print >> self.original_stderr, ' '.join(str(test).strip().split('\n'))
