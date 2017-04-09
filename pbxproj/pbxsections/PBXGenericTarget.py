from pbxproj.PBXGenericObject import *
from pbxproj.pbxsections.PBXGenericBuildPhase import *


class PBXGenericTarget(PBXGenericObject):
    def get_or_create_build_phase(self, build_phase_type, search_parameters=None, create_parameters=()):
        result = []
        parent = self.get_parent()
        search_parameters = search_parameters if search_parameters is not None else {}

        if build_phase_type is None:
            return result

        for build_phase_id in self.buildPhases:
            target_build_phase = parent[build_phase_id]
            current_build_phase = target_build_phase.isa

            if current_build_phase == build_phase_type and \
                    all(key in target_build_phase and target_build_phase[key] == search_parameters[key] for key in search_parameters):
                result.append(target_build_phase)

        if result.__len__() == 0:
            build_phase = self._get_class_reference(build_phase_type).create(*create_parameters)
            parent[build_phase.get_id()] = build_phase
            self.add_build_phase(build_phase)
            result.append(build_phase)

        return result

    def add_build_phase(self, build_phase, position=None):
        if position is None:
            position = self.buildPhases.__len__()

        self.buildPhases.insert(position, build_phase.get_id())

    def remove_build_phase(self, build_phase):
        if not isinstance(build_phase, PBXGenericBuildPhase):
            return False

        self.buildPhases.remove(build_phase.get_id())
        del self.get_parent()[build_phase.get_id()]

        return True
