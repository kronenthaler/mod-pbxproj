# MIT License
#
# Copyright (c) [year] [fullname]
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

import os

class objects:
    pass

class XcodeProject:
    """
    Top level class, handles the project CRUD operations, new, load, save, delete. Also, exposes methods to manipulate
    the project's content, add/remove files, add/remove libraries/frameworks, query sections. For more advanced
    operations, underlying objects are exposed that can be manipulated using said objects.
    """
    def __init__(self, tree=None, path=None):
        if path is None:
            path = os.path.join(os.getcwd(), 'project.pbxproj')

        self._pbxproj_path = os.path.abspath(path)
        self._source_root = os.path.abspath(os.path.join(os.path.split(path)[0], '..'))

        # initialize the structure using the given tree
        self._parse(tree)

    def _parse(self, tree):
        # all top level objects are added as variables to this object
        for key, value in tree.iteritems():
            if not hasattr(self, key):
                # check if the key maps to a kind of object
                setattr(self, key, value)

        module = __import__("mod_pbxproj2")
        class_ = getattr(module, "objects")
        instance = class_()
        print instance

    def __repr__(self):
        # print all non-function and non-private ones
        return str([x for x in dir(self) if not x.startswith("_") and not hasattr(getattr(self, x), '__call__')])

    def save(self, path=None):
        if path is None:
            path = self._pbxproj_path

        # f = open(path, 'w')
        # f.write(self.__repr__())
        # f.close()

    @classmethod
    def load(cls, path, pure_python=False):
        if pure_python:
            import openstep_parser as osp

            tree = osp.OpenStepDecoder.ParseFromFile(open(path, 'r'))
        else:
            import plistlib
            import subprocess

            cls.plutil_path = os.path.join(os.path.split(__file__)[0], 'plutil')

            if not os.path.isfile(XcodeProject.plutil_path):
                cls.plutil_path = 'plutil'

            # load project by converting to xml and then convert that using plistlib
            p = subprocess.Popen([XcodeProject.plutil_path, '-convert', 'xml1', '-o', '-', path],
                                 stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()

            # If the plist was malformed, return code will be non-zero
            if p.returncode != 0:
                print stdout
                return None

            tree = plistlib.readPlistFromString(stdout)

        return XcodeProject(tree, path)


if __name__ == "__main__":
    print XcodeProject({"a": "b", "c": ["1", 2, 4]})