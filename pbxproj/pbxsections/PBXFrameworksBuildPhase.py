from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXFrameworksBuildPhase(PBXGenericBuildPhase):
    def _get_comment(self):
        return 'Frameworks'
