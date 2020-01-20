from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXSourcesBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return 'Sources'
