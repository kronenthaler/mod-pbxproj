from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXHeadersBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return 'Headers'
