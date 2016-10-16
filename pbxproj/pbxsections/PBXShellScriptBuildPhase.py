from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXShellScriptBuildPhase(PBXGenericBuildPhase):
    @classmethod
    def create(cls, script, shell_path=u"/bin/sh", files=None, input_paths=None, output_paths=None, show_in_log='0'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'inputPaths': input_paths if input_paths else [],
            u'outputPaths': output_paths if output_paths else [],
            u'runOnlyForDeploymentPostprocessing': 0,
            u'shellPath': shell_path,
            u'shellScript': script,
            u'showEnvVarsInLog': show_in_log
        })

    def _get_comment(self):
        return u'ShellScript'
