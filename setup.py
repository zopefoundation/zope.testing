##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Setup for zope.testing package

$Id$
"""

import os

try:
    from setuptools import setup
    extra = dict(
        namespace_packages=['zope',],
        install_requires = ['setuptools',
                            'zope.interface'],
        extras_require={'zope_tracebacks': 'zope.exceptions'},
        include_package_data = True,
        zip_safe = False,
        )
except ImportError, e:
    from distutils.core import setup
    extra = {}

chapters = '\n'.join([
    open(os.path.join('src', 'zope', 'testing', 'testrunner', name)).read()
    for name in (
        'testrunner.txt',
        'testrunner-simple.txt',
        'testrunner-layers-api.txt',
        'testrunner-layers.txt',
        'testrunner-arguments.txt',
        'testrunner-verbose.txt',
        'testrunner-test-selection.txt',
        'testrunner-progress.txt',

        # The following seems to cause weird unicode in the output: :(
        ##     'testrunner-errors.txt',

        'testrunner-debugging.txt',
        'testrunner-layers-ntd.txt',
        'testrunner-coverage.txt',
        'testrunner-profiling.txt',
        'testrunner-wo-source.txt',
        'testrunner-repeat.txt',
        'testrunner-gc.txt',
        'testrunner-leaks.txt',
        'testrunner-knit.txt',
    )])

chapters += '\n'.join([
    open(os.path.join('src', 'zope', 'testing', name)).read()
    for name in (
        'formparser.txt',
        'setupstack.txt',
    )])

long_description=(
    open('README.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' + chapters
    )

open('documentation.txt', 'w').write(long_description)

setup(
    name='zope.testing',
    version='3.7.3dev',
    url='http://pypi.python.org/pypi/zope.testing',
    license='ZPL 2.1',
    description='Zope testing framework, including the testrunner script.',
    long_description=long_description,
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',

    packages=["zope", "zope.testing"],
    package_dir = {'': 'src'},

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Zope3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        ],

    **extra)
