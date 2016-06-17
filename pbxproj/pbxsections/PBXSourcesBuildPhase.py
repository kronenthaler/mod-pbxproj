from pbxproj import PBXGenericObject


class PBXSourcesBuildPhase(PBXGenericObject):
    def _get_comment(self):
        return u'Sources'
