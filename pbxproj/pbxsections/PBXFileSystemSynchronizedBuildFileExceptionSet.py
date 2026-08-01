from pbxproj import PBXGenericObject


class PBXFileSystemSynchronizedBuildFileExceptionSet(PBXGenericObject):
    def _get_comment(self):
        return self.isa