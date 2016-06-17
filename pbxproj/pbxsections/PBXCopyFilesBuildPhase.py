from pbxproj import PBXGenericObject


class PBXCopyFilesBuildPhase(PBXGenericObject):
    def _get_comment(self):
        comment = super(type(self), self)._get_comment()
        if comment is None:
            return u'CopyFiles'
        return comment
