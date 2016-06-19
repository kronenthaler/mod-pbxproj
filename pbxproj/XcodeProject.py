import os
from pbxproj import *
from pbxproj.pbxextensions import *


class XcodeProject(PBXGenericObject, ProjectFlags):
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
        return u'// !$*UTF8*$!\n' + super(type(self), self).__repr__()

    @classmethod
    def load(cls, path, pure_python=False):
        import openstep_parser as osp
        tree = osp.OpenStepDecoder.ParseFromFile(open(path, 'r'))
        return XcodeProject(tree, path)