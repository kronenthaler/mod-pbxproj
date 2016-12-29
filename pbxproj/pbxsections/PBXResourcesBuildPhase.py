from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXResourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Resources'
