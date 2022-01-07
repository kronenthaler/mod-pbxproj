from pbxproj.PBXGenericObject import PBXGenericObject
from pbxproj.pbxsections.PBXBuildFile import PBXBuildFile


class PBXGenericBuildPhase(PBXGenericObject):
    @classmethod
    def create(cls, name=None, files=None):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'name': name,
            'files': files if files else [],
            'buildActionMask': 0x7FFFFFFF,
            'runOnlyForDeploymentPostprocessing': 0
        })

    def add_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.append(build_file.get_id())

        # update the build_file section
        build_file._section = self._get_comment()

        return True

    def remove_build_file(self, build_file):
        if not isinstance(build_file, PBXBuildFile):
            return False

        self.files.remove(build_file.get_id())
        del self.get_parent()[build_file.get_id()]

        # update the build_file section
        build_file._section = None

        return True
