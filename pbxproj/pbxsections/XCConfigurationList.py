from pbxproj import PBXGenericObject


class XCConfigurationList(PBXGenericObject):
    def _get_comment(self):
        info = self._get_section()
        return 'Build configuration list for {0} "{1}"'.format(*info)

    def _get_section(self):
        # search for the section where this config is used and get the isa and name
        return ('PBXNativeTarget', "X")