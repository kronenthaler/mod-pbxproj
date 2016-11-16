from pbxproj import PBXGenericObject


class rootObject(PBXGenericObject):
    def _resolve_comment(self, key):
        return self.get_parent().objects._resolve_comment(key)
