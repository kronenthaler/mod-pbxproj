from pbxproj.pbxsections.PBXBuildFile import *


class PBXGenericBuildPhase(PBXGenericObject):
    @classmethod
    def create(cls, name=None, files=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'name': name,
            u'files': files if files else [],
            u'buildActionMask': 0x7FFFFFFF,
            u'runOnlyForDeploymentPostprocessing': 0
        })

    def add_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.append(build_file.get_id())
        return True

    def remove_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.remove(build_file.get_id())
        del self.get_parent()[build_file.get_id()]

        return True
