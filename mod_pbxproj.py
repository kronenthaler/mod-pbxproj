# MIT License
#
# Copyright (c) 2016 Ignacio Calderon aka kronenthaler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This is a backwards-compatibility file. For Unity developers this is the only file it needs to be added to the Unity
# project.
# This file will install the proper python package into the user's python's local space, if it's not present at run-time
# of this script. Afterwards, it will import all necessary modules to the developer to make his/her own script work as
# before.

from setuptools import setup
import site

__author__ = 'kronenthaler'
__version__ = '2.0.1'
__package_name__ = 'mod_pbxproj_installer'

try:
    # check if file exists
    from pbxproj import XcodeProject
except:
    # install it if not present
    print('Installing package...')
    setup(name=__package_name__,
          license='MIT License',
          install_requires=['pbxproj'],
          script_args=['install', '--user', '--force', '--record', '.uninstall_files'])

# force the refresh of the packages
reload(site)

# expose import publicly
from pbxproj import *
