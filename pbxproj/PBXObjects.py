import pbxproj
import bisect
from pbxproj import PBXGenericObject


class objects(PBXGenericObject):
    def __init__(self, parent=None):
        super(objects, self).__init__(parent)

        # sections: dict<isa, [tuple(id, obj)]>
        # sections get aggregated under the isa type. Each contains a list of tuples (id, obj) with every object defined
        self._sections = {}

        # keep a dict indexed by obj.get_id() in order to do fast lookup while saving the file or in general
        # this means that the structure needs to be kept in sync whenever an object is added or removed to the _sections
        # dict.
        self._objects_by_id = {}

    def parse(self, object_data):
        # iterate over the keys and fill the sections
        if isinstance(object_data, dict):
            for key, value in object_data.items():
                key = self._parse_string(key)
                obj_type = key
                if 'isa' in value:
                    obj_type = value['isa']

                child = self._get_instance(obj_type, value)
                child['_id'] = key
                self[key] = child

            return self

        # safe-guard: delegate to the parent how to deal with non-object values
        return super(objects, self).parse(object_data)

    def _print_object(self, indent_depth='', entry_separator='\n', object_start='\n',
                      indent_increment='\t'):
        # override to change the way the object is printed out
        result = '{\n'
        for section in self.get_sections():
            phase = self._sections[section]
            result += f'\n/* Begin {section} section */\n'
            for value in phase:
                obj = value._print_object(indent_depth + '\t', entry_separator, object_start,
                                          indent_increment)
                result += f'{indent_depth}\t{value.get_id().__repr__()} = {obj};\n'
            result += f'/* End {section} section */\n'
        result += f'{indent_depth}{"}"}'
        return result

    def get_keys(self):
        """
        :return: all the keys of the object (ids of objects)
        """
        keys = list(self._objects_by_id.keys())
        keys.sort()
        return keys

    def get_sections(self):
        sections = list(self._sections.keys())
        sections.sort()
        return sections

    def __getitem__(self, key):
        # retrieve the element from the dict representation for faster access.
        return self._objects_by_id.get(key, None)

    def __setitem__(self, key, value):
        if value.isa not in self._sections:
            self._sections[value.isa] = []

        # use the bisect module to keep the list sorted at all times.
        bisect.insort(self._sections[value.isa], value)

        # add to the fast lookup dict
        self._objects_by_id[value.get_id()] = value

        value._parent = self

    def __delitem__(self, key):
        obj = self[key]
        if obj is not None:
            phase = self._sections[obj.isa]
            phase.remove(obj)
            # remove from the fast lookup dict
            del self._objects_by_id[obj.get_id()]

            # remove empty phases
            if phase.__len__() == 0:
                del self._sections[obj.isa]

    def __contains__(self, item):
        return self[item] is not None

    def __len__(self):
        return sum([section.__len__() for section in self._sections])

    def get_objects_in_section(self, *sections):
        result = []
        for name in sections:
            if name in self._sections:
                result.extend(self._sections[name])
        return result

    def get_targets(self, name=None):
        """
        Retrieve all/one target objects
        :param name: name of the target to search for, None for everything
        :return: A list of target objects
        """
        targets = []
        for section in self.get_sections():
            if section.endswith('Target'):
                targets += [value for value in self._sections[section]]

        if name is None:
            return targets

        if not isinstance(name, list):
            name = [name]

        return [target for target in targets if target.name in name]

    def get_buildphases_on_target(self, target_name=None):
        for target in self.get_targets(target_name):
            for build_phase_id in target.buildPhases:
                yield (target, self[build_phase_id])

    def get_configurations_on_targets(self, target_name=None, configuration_name=None):
        """
        Retrieves all configuration given a name on the specified target
        :param target_name: Searches for a specific target name or a list of target names. If None all targets are used
        :param configuration_name: Searches for a specific configuration, if None all configuration of the target
            are used
        :return: A generator of configurations objects matching the target and configuration given (or all if nothing is
            specified)
        """
        for target in self.get_targets(target_name):
            configuration_list = self[target.buildConfigurationList]
            for configuration in configuration_list.buildConfigurations:
                if configuration_name is None or self[configuration].name == configuration_name:
                    yield self[configuration]

    def get_project_configurations(self, configuration_name=None):
        """
        Retrieves all configuration given a name on the root project
        :param configuration_name: Searches for a specific configuration, if None all configuration of the target
            are used
        :return: A generator of configurations objects from the root project the given configuration name (or all if
            nothing is specified)
        """
        project = self[self._parent.rootObject]
        configuration_list = self[project.buildConfigurationList]
        for configuration in configuration_list.buildConfigurations:
            if configuration_name is None or self[configuration].name == configuration_name:
                yield self[configuration]