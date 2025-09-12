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


long_description = read('README.rst') + '\n\n' + read('CHANGES.rst')
keywords = "zope testing doctest RENormalizing OutputChecker timeout logging"

setup(
    name='zope.testing',
    version='6.0',
    url='https://github.com/zopefoundation/zope.testing',
    license='ZPL-2.1',
    description='Zope testing helpers',
    long_description=long_description,
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Zope :: 3",
        "Framework :: Zope :: 4",
        "Framework :: Zope :: 5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords=keywords,
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
            'zope.testrunner >= 6.4',
        ],
        'docs': [
            'sphinx',
            'repoze.sphinx.autointerface',
            'zope.exceptions',
            'zope.interface',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
