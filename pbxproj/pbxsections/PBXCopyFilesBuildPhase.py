from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXCopyFilesBuildPhaseNames:
    EMBEDDED_FRAMEWORKS = u'Embed Frameworks'


class PBXCopyFilesBuildPhase(PBXGenericBuildPhase):
    @classmethod
    def create(cls, name=None, files=None, dest_path=u'', dest_subfolder_spec=10):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'name': name,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'dstSubfolderSpec': dest_subfolder_spec,
            u'dstPath': dest_path,
            u'runOnlyForDeploymentPostprocessing': 0
        })

    def _get_comment(self):
        comment = super(PBXCopyFilesBuildPhase, self)._get_comment()
        if comment is None:
            return u'CopyFiles'
        return comment
