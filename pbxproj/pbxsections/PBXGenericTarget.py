from pbxproj.PBXGenericObject import *


class PBXGenericTarget(PBXGenericObject):
    def add_build_phase(self, build_phase, position=None):
        if position is None:
            position = self.buildPhases.__len__()

        self.buildPhases.insert(position, build_phase.get_id())

    def remove_build_phase(self, build_phase):
        self.buildPhases.remove(build_phase)
