from pbxproj import PBXGenericObject


class PBXResourcesBuildPhase(PBXGenericObject):
    def _get_comment(self):
        return u'Resources'
