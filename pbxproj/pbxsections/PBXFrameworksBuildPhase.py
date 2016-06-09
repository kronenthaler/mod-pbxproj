from pbxproj import PBXGenericObject


class PBXFrameworksBuildPhase(PBXGenericObject):
    def _get_comment(self):
        return 'Frameworks'
