from pbxproj import PBXGenericObject


class PBXFileSystemSynchronizedBuildFileExceptionSet(PBXGenericObject):
    def _get_comment(self):
        comment = super(PBXFileSystemSynchronizedBuildFileExceptionSet, self)._get_comment()
        if comment is None:
            return 'PBXFileSystemSynchronizedBuildFileExceptionSet'
        return comment