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

from pbxproj.PBXGenericObject import PBXGenericObject
from pbxproj.XcodeProject import XcodeProject
from pbxproj.PBXObjects import objects


class PBXBuildFile(PBXGenericObject):
    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        return super(type(self), self)._print_object("", entry_separator=' ', object_start='', indentation_increment='')


class PBXFileReference(PBXGenericObject):
    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        return super(type(self), self)._print_object("", entry_separator=' ', object_start='', indentation_increment='')


if __name__ == "__main__":
    # print XcodeProject({"a": "b", "c": {"1": 2},"z":[1,2,4]})
    obj = XcodeProject.load('../mod_pbxproj/tests/samples/cloud-search.pbxproj')
    print obj