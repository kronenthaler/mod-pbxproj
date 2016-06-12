from pbxproj import PBXGenericObject


class PBXShellScriptBuildPhase(PBXGenericObject):
    def _get_comment(self):
        return "ShellScript"
