from pbxproj import PBXGenericObject


class PBXTargetDependency(PBXGenericObject):
    def _get_comment(self):
        return u'PBXTargetDependency'
