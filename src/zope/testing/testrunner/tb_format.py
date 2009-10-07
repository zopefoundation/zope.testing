##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Set up testing environment

$Id: __init__.py 68482 2006-06-04 14:58:55Z jim $
"""

import sys
import traceback
import zope.exceptions.exceptionformatter
import zope.testing.testrunner.feature


def format_exception(t, v, tb, limit=None):
    fmt = zope.exceptions.exceptionformatter.TextExceptionFormatter(
        limit=None, with_filenames=True)
    return fmt.formatException(t, v, tb)


def print_exception(t, v, tb, limit=None, file=None):
    if file is None:
        file = sys.stdout
    file.writelines(format_exception(t, v, tb, limit))


class Traceback(zope.testing.testrunner.feature.Feature):

    active = True

    def global_setup(self):
        self.old_format = traceback.format_exception
        traceback.format_exception = format_exception

        self.old_print = traceback.print_exception
        traceback.print_exception = print_exception

    def global_teardown(self):
        traceback.format_exception = self.old_format
        traceback.print_exception = self.old_print
