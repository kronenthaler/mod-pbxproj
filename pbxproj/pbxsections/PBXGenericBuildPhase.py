from pbxproj.PBXGenericObject import *
from pbxproj.pbxsections import *


class PBXGenericBuildPhase(PBXGenericObject):
    def add_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.append(build_file.get_id())
        return True
