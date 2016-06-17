from pbxproj import PBXGenericObject


class PBXProject(PBXGenericObject):
    def _get_comment(self):
        return u'Project object'
