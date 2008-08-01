##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Sample test layers

$Id$
"""

import os
import unittest


class TestLayer:

    __bases__ = ()

    def __init__(self, module, name):
        self.__module__ = module
        self.__name__ = name


class UnitTest(unittest.TestCase):

    def test(self):
        from zope.testing import testrunner
        this_directory = os.path.dirname(__file__)
        defaults = [
            '--path', this_directory,
            '--tests-pattern', '^innertests$',
            ]
        print "-- inner test run starts --"
        testrunner.run(defaults)
        print "-- inner test run ends --"


class LayeredTest(unittest.TestCase):

    layer = TestLayer(__name__, 'HardToAccessTestLayer')

    def test(self):
        pass


def test_suite():
    return unittest.TestSuite([unittest.makeSuite(UnitTest),
                               unittest.makeSuite(LayeredTest)])

