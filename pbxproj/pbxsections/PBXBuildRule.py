from pbxproj import PBXGenericObject


class PBXBuildRule(PBXGenericObject):
    def _get_comment(self):
        return 'PBXBuildRule'
