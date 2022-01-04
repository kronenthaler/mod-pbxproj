from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXShellScriptBuildPhase(PBXGenericBuildPhase):

    @classmethod
    def create(cls, script, name=None, files=None, shell_path="/bin/sh", input_paths=None, output_paths=None,
               show_in_log='0', run_install_build=0):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'name': name,
            'files': files if files else [],
            'buildActionMask': 0x7FFFFFFF,
            'inputPaths': input_paths if input_paths else [],
            'outputPaths': output_paths if output_paths else [],
            'runOnlyForDeploymentPostprocessing': run_install_build,
            'shellPath': shell_path,
            'shellScript': script,
            'showEnvVarsInLog': show_in_log
        })

    def _get_comment(self):
        return getattr(self, 'name', 'ShellScript')
