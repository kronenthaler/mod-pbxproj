import shutil
import datetime
from pbxproj import *
from pbxproj.pbxextensions import *


class XcodeProject(PBXGenericObject, ProjectFiles, ProjectFlags, ProjectGroups, Deprecations):
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

    def backup(self):
        backup_name = "%s_%s.backup" % (self._pbxproj_path, datetime.datetime.now().strftime('%d%m%y-%H%M%S'))

        shutil.copy2(self._pbxproj_path, backup_name)
        return backup_name

    def __repr__(self):
        return u'// !$*UTF8*$!\n' + super(XcodeProject, self).__repr__()

    @classmethod
    def load(cls, path):
        import openstep_parser as osp
        tree = osp.OpenStepDecoder.ParseFromFile(open(path, 'r'))
        return XcodeProject(tree, path)
