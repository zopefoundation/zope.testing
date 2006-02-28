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

try:
    from setuptools import setup
except ImportException, e:
    from distutils.core import setup
    
setup(name='zope_testing',
      version='3.0',

      url='http://svn.zope.org/zope.testing',
      license='ZPL 2.1',
      description='Zope testing framework, including the testrunner script.',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      
      packages=["zope", "zope.testing"],
      package_dir = {'': 'src'},

      include_package_data = True,
      zip_safe = False,
      )
