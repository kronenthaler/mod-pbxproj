from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXHeadersBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return u'Headers'
