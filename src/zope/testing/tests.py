##############################################################################
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
"""Tests for the testing framework.
"""

import sys
import re
import unittest
import warnings
from zope.testing import renormalizing

# Yes, it is deprecated, but we want to run tests on it here.
warnings.filterwarnings("ignore", "zope.testing.doctest is deprecated",
                        DeprecationWarning, __name__, 0)

from zope.testing import doctest


def test_suite():
    suite = unittest.TestSuite((
        doctest.DocTestSuite('zope.testing.loggingsupport'),
        doctest.DocTestSuite('zope.testing.renormalizing'),
        doctest.DocTestSuite('zope.testing.server'),
        doctest.DocFileSuite('doctest.txt'),
        doctest.DocFileSuite('formparser.txt'),
        doctest.DocFileSuite(
            'module.txt',
            # when this test is run in isolation, the error message shows the
            # module name as fully qualified; when it is run as part of the
            # full test suite, the error message shows the module name as
            # relative.
            checker=renormalizing.RENormalizing([
                (re.compile('No module named zope.testing.unlikelymodulename'),
                 'No module named unlikelymodulename')])),
        doctest.DocFileSuite('setupstack.txt'),
        ))

    if sys.version < '3':
        suite.addTests(doctest.DocFileSuite('unicode.txt'))
    return suite
