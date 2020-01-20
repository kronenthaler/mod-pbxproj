from pbxproj.pbxsections.PBXGenericBuildPhase import PBXGenericBuildPhase


class PBXCopyFilesBuildPhaseNames:
    EMBEDDED_FRAMEWORKS = 'Embed Frameworks'


class PBXCopyFilesBuildPhase(PBXGenericBuildPhase):
    @classmethod
    def create(cls, name=None, files=None, dest_path='', dest_subfolder_spec='10'):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'name': name,
            'files': files if files else [],
            'buildActionMask': 0x7FFFFFFF,
            'dstSubfolderSpec': dest_subfolder_spec,
            'dstPath': dest_path,
            'runOnlyForDeploymentPostprocessing': 0
        })

    def _get_comment(self):
        comment = super(PBXCopyFilesBuildPhase, self)._get_comment()
        if comment is None:
            return 'CopyFiles'
        return comment
