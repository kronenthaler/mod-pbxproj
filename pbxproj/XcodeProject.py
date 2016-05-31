import os

from pbxproj import PBXGenericObject


class XcodeProject(PBXGenericObject):
    """
    Top level class, handles the project CRUD operations, new, load, save, delete. Also, exposes methods to manipulate
    the project's content, add/remove files, add/remove libraries/frameworks, query sections. For more advanced
    operations, underlying objects are exposed that can be manipulated using said objects.
    """
    def __init__(self, tree=None, path=None):
        self._parent = None

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

    def __repr__(self):
        return "// !$*UTF8*$!\n" + super(type(self), self).__repr__()

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