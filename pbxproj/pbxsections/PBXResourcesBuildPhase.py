from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXResourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return 'Resources'
