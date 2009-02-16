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
"""Test harness for the test runner itself.

$Id: __init__.py 86215 2008-05-03 14:08:12Z ctheune $
"""

import re
import gc
import os
import sys
import unittest

from zope.testing import doctest
from zope.testing import renormalizing


checker = renormalizing.RENormalizing([
    # 2.5 changed the way pdb reports exceptions
    (re.compile(r"<class 'exceptions.(\w+)Error'>:"),
                r'exceptions.\1Error:'),

    (re.compile('^> [^\n]+->None$', re.M), '> ...->None'),
    (re.compile(r"<module>"),(r'?')),
    (re.compile(r"<type 'exceptions.(\w+)Error'>:"),
                r'exceptions.\1Error:'),
    (re.compile("'[A-Za-z]:\\\\"), "'"), # hopefully, we'll make Windows happy
    (re.compile(r'\\\\'), '/'), # more Windows happiness
    (re.compile(r'\\'), '/'), # even more Windows happiness
    (re.compile('/r'), '\\\\r'), # undo damage from previous
    (re.compile(r'\r'), '\\\\r\n'),
    (re.compile(r'\d+[.]\d\d\d seconds'), 'N.NNN seconds'),
    (re.compile(r'\d+[.]\d\d\d s'), 'N.NNN s'),
    (re.compile(r'\d+[.]\d\d\d{'), 'N.NNN{'),
    (re.compile('( |")[^\n]+testrunner-ex'), r'\1testrunner-ex'),
    (re.compile('( |")[^\n]+testrunner.py'), r'\1testrunner.py'),
    (re.compile(r'> [^\n]*(doc|unit)test[.]py\(\d+\)'),
                r'\1test.py(NNN)'),
    (re.compile(r'[.]py\(\d+\)'), r'.py(NNN)'),
    (re.compile(r'[.]py:\d+'), r'.py:NNN'),
    (re.compile(r' line \d+,', re.IGNORECASE), r' Line NNN,'),
    (re.compile(r' line {([a-z]+)}\d+{', re.IGNORECASE), r' Line {\1}NNN{'),

    # omit traceback entries for unittest.py or doctest.py from
    # output:
    (re.compile(r'^ +File "[^\n]*(doc|unit)test.py", [^\n]+\n[^\n]+\n',
                re.MULTILINE),
     r''),
    (re.compile(r'^{\w+} +File "{\w+}[^\n]*(doc|unit)test.py{\w+}", [^\n]+\n[^\n]+\n',
                re.MULTILINE),
     r''),
    (re.compile('^> [^\n]+->None$', re.M), '> ...->None'),
    (re.compile('import pdb; pdb'), 'Pdb()'), # Py 2.3
    ])


def setUp(test):
    test.globs['saved-sys-info'] = (
        sys.path[:],
        sys.argv[:],
        sys.modules.copy(),
        gc.get_threshold(),
        )
    test.globs['this_directory'] = os.path.split(__file__)[0]
    test.globs['testrunner_script'] = sys.argv[0]


def tearDown(test):
    sys.path[:], sys.argv[:] = test.globs['saved-sys-info'][:2]
    gc.set_threshold(*test.globs['saved-sys-info'][3])
    sys.modules.clear()
    sys.modules.update(test.globs['saved-sys-info'][2])


def test_suite():
    suites = [
        doctest.DocFileSuite(
        'testrunner-arguments.txt',
        'testrunner-coverage.txt',
        'testrunner-debugging-layer-setup.test',
        'testrunner-debugging.txt',
        'testrunner-edge-cases.txt',
        'testrunner-errors.txt',
        'testrunner-layers-ntd.txt',
        'testrunner-layers.txt',
        'testrunner-layers-api.txt',
        'testrunner-progress.txt',
        'testrunner-colors.txt',
        'testrunner-simple.txt',
        'testrunner-test-selection.txt',
        'testrunner-verbose.txt',
        'testrunner-wo-source.txt',
        'testrunner-repeat.txt',
        'testrunner-gc.txt',
        'testrunner-knit.txt',
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
        checker=checker),
        doctest.DocTestSuite('zope.testing.testrunner'),
        doctest.DocTestSuite('zope.testing.testrunner.coverage'),
        doctest.DocTestSuite('zope.testing.testrunner.options'),
        doctest.DocTestSuite('zope.testing.testrunner.find'),
        ]

    if sys.platform == 'win32':
        suites.append(
            doctest.DocFileSuite(
            'testrunner-coverage-win32.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
            checker=checker))

    # Python <= 2.4.1 had a bug that prevented hotshot from running in
    # non-optimize mode
    if sys.version_info[:3] > (2,4,1) or not __debug__:
        # some Linux distributions don't include the profiling module (which
        # hotshot.stats depends on)
        try:
            import hotshot.stats
        except ImportError:
            pass
        else:
            suites.append(
                doctest.DocFileSuite(
                    'testrunner-profiling.txt',
                    setUp=setUp, tearDown=tearDown,
                    optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
                    checker = renormalizing.RENormalizing([
                        (re.compile(r'tests_profile[.]\S*[.]prof'),
                         'tests_profile.*.prof'),
                        ]),
                    )
                )
        try:
            import cProfile
            import pstats
        except ImportError:
            pass
        else:
            suites.append(
                doctest.DocFileSuite(
                    'testrunner-profiling-cprofiler.txt',
                    setUp=setUp, tearDown=tearDown,
                    optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
                    checker = renormalizing.RENormalizing([
                        (re.compile(r'tests_profile[.]\S*[.]prof'),
                         'tests_profile.*.prof'),
                        ]),
                    )
                )


    if hasattr(sys, 'gettotalrefcount'):
        suites.append(
            doctest.DocFileSuite(
            'testrunner-leaks.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
            checker = renormalizing.RENormalizing([
              (re.compile(r'\d+[.]\d\d\d seconds'), 'N.NNN seconds'),
              (re.compile(r'sys refcount=\d+ +change=\d+'),
               'sys refcount=NNNNNN change=NN'),
              (re.compile(r'sum detail refcount=\d+ +'),
               'sum detail refcount=NNNNNN '),
              (re.compile(r'total +\d+ +\d+'),
               'total               NNNN    NNNN'),
              (re.compile(r"^ +(int|type) +-?\d+ +-?\d+ *\n", re.M),
               ''),
              ]),

            )
        )
    else:
        suites.append(
            doctest.DocFileSuite(
            'testrunner-leaks-err.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
            checker=checker,
            )
        )
    return unittest.TestSuite(suites)
