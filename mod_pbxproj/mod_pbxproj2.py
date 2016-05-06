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
import re


class DynamicObject(object):
    """
    Generic class that creates internal attributes to match the structure of the tree used to create the element.
    Also, prints itself using the openstep format. Extensions might be required to insert comments on right places.
    """
    _VALID_KEY_REGEX = '[a-zA-Z0-9\\._/-]*'

    def parse(self, value):
        if isinstance(value, dict):
            return self._parse_dict(value)

        return value

    def _parse_dict(self, obj):
        # all top level objects are added as variables to this object
        for key, value in obj.iteritems():
            if not hasattr(self, key):
                # check if the key maps to a kind of object
                module = __import__("mod_pbxproj2")
                if hasattr(module, key):
                    class_ = getattr(module, key)
                    instance = class_().parse(value)
                else:
                    instance = DynamicObject().parse(value)

                setattr(self, key, instance)

        return self

    def __repr__(self):
        return self.print_object("")

    def print_object(self, indent):
        ret = "{\n"
        for key in [x for x in dir(self) if not x.startswith("_") and not hasattr(getattr(self, x), '__call__')]:
            value = getattr(self, key)
            if hasattr(value, 'print_object'):
                value = value.print_object(indent + "\t")
            elif isinstance(value, list):
                value = self._print_list(value, indent+"\t")
            else:
                value = DynamicObject._escape(value.__str__())

            ret += indent+"\t{0} = {1};\n".format(DynamicObject._escape(key), value)
        ret += indent+"}"
        return ret

    def _print_list(self, value, indent):
        ret = "(\n"
        for item in value:
            ret += indent+"\t{0},\n".format(item)
        ret += indent+")"
        return ret

    @classmethod
    def _escape(cls, item):
        if re.match(cls._VALID_KEY_REGEX, item).group(0) != item:
            return '"{0}"'.format(item)
        return item


class objects(DynamicObject):
    def __init__(self):
        self._sections = {}
        # during parsing time the section will be aggregated under the same isa key.
        # this will allow do queries and retrieve especific sections far more easily
        # printing the object should iterate over said sections.

    def print_object(self, indent):
        # override to change the way the object is printed out
        return super(type(self), self).print_object(indent)


class XcodeProject(DynamicObject):
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
        self.parse(tree)

    def save(self, path=None):
        if path is None:
            path = self._pbxproj_path

        f = open(path, 'w')
        f.write(self.__repr__())
        f.close()

    @classmethod
    def load(cls, path, pure_python=False):
        if pure_python:
            import openstep_parser as osp

            tree = osp.OpenStepDecoder.ParseFromFile(open(path, 'r'))
        else:
            import plistlib
            import subprocess

            plutil_path = os.path.join(os.path.split(__file__)[0], 'plutil')

            if not os.path.isfile(plutil_path):
                plutil_path = 'plutil'

            # load project by converting to xml and then convert that using plistlib
            p = subprocess.Popen([plutil_path, '-convert', 'xml1', '-o', '-', path], stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()

            # If the plist was malformed, return code will be non-zero
            if p.returncode != 0:
                print stdout
                return None

            tree = plistlib.readPlistFromString(stdout)

        return XcodeProject(tree, path)


if __name__ == "__main__":
    print XcodeProject({"a": "b", "c": {"1": 2},"z":[1,2,4]})
    print XcodeProject.load('../tests/samples/cloud-search.pbxproj')