from pbxproj import PBXGenericObject


class PBXHeadersBuildPhase(PBXGenericObject):
    def _get_comment(self):
        return u'Headers'
