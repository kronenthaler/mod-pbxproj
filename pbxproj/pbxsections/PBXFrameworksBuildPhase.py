from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXFrameworksBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Frameworks'
