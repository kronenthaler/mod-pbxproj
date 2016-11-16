from pbxproj import PBXGenericObject


class PBXContainerItemProxy(PBXGenericObject):
    def _get_comment(self):
        return u'PBXContainerItemProxy'
