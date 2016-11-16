from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXSourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Sources'
