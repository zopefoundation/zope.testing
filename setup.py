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


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


chapters = [
    read((os.path.join('src', 'zope', 'testing', name)))
    for name in [
        'formparser.txt',
        'loggingsupport.txt',
        'renormalizing.txt',
        'setupstack.txt',
        'wait.txt',
        'doctestcase.txt',
    ]
]


long_description = '\n\n'.join(
    [read('README.rst')] +
    chapters +
    [read('CHANGES.rst')]
)
keywords = "zope testing doctest RENormalizing OutputChecker timeout logging"

setup(
    name='zope.testing',
    version='4.6.2',
    url='https://github.com/zopefoundation/zope.testing',
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
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Framework :: Zope3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords=keywords,
    packages=[
        "zope",
        "zope.testing",
    ],
    package_dir={'': 'src'},
    namespace_packages=['zope'],
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='zope.testing.tests.test_suite',
)
