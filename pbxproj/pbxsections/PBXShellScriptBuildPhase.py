from pbxproj import PBXGenericObject


class PBXShellScriptBuildPhase(PBXGenericObject):
    @classmethod
    def create(cls, script, shell_path=u"/bin/sh", files=[], input_paths=[], output_paths=[], show_in_log='0'):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'files': files,
            'buildActionMask': 0x7FFFFFFF,
            'inputPaths': input_paths,
            'outputPaths': output_paths,
            'runOnlyForDeploymentPostprocessing': 0,
            'shellPath': shell_path,
            'shellScript': script,
            'showEnvVarsInLog': show_in_log
        })

    def _get_comment(self):
        return u'ShellScript'

