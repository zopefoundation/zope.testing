##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.testing package
"""

import os
from setuptools import setup
import sys
if sys.version > '3':
    extras = dict(
    use_2to3 = True,
    convert_2to3_doctests = ['src/zope/testing/doctest.txt',
                             'src/zope/testing/formparser.txt',
                             'src/zope/testing/module.txt',
                             'src/zope/testing/setupstack.txt',
                             ],
    dependency_links = ['.'], # Only until zope.interface 3.6 and zope.exception 3.6 has been released.
    )
else:
    extras = {}

chapters = '\n'.join([
    open(os.path.join('src', 'zope', 'testing', name)).read()
    for name in (
    'formparser.txt',
    'loggingsupport.txt',
    'renormalizing.txt',
    'setupstack.txt',
    'wait.txt',
    )])

long_description=(
    open('README.txt').read()
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' + chapters
    + '\n' + open('CHANGES.txt').read()
    )

setup(
    name='zope.testing',
    version = '4.1.1',
    url='http://pypi.python.org/pypi/zope.testing',
    license='ZPL 2.1',
    description='Zope testing helpers',
    long_description=long_description,
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        ],

    packages=["zope",
              "zope.testing",
              "zope.testing.doctest",
              "zope.testing.renormalizing"],
    package_dir = {'': 'src'},
    namespace_packages=['zope',],
    install_requires = ['setuptools',
                        'zope.exceptions',
                        'zope.interface'],
    include_package_data = True,
    zip_safe = False,
    test_suite = 'zope.testing.tests.test_suite',
    **extras
)
