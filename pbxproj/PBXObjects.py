import uuid
from pbxproj import PBXGenericObject


class objects(PBXGenericObject):
    def __init__(self, parent=None):
        super(objects, self).__init__(parent)

        # sections: dict<isa, [tuple(id, obj)]>
        # sections get aggregated under the isa type. Each contains a list of tuples (id, obj) with every object defined
        self._sections = {}

    def parse(self, object_data):
        # iterate over the keys and fill the sections
        if isinstance(object_data, dict):
            for key, value in object_data.iteritems():
                key = self._parse_string(key)
                obj_type = key
                if 'isa' in value:
                    obj_type = value['isa']

                child = self._get_instance(obj_type, value)
                child[u'_id'] = key
                self[key] = child

            return self

        # safe-guard: delegate to the parent how to deal with non-object values
        return super(objects, self).parse(object_data)

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        # override to change the way the object is printed out
        result = u'{\n'
        for section in self.get_sections():
            phase = self._sections[section]
            phase.sort(key=lambda x: x.get_id())
            result += u'\n/* Begin {0} section */\n'.format(section)
            for value in phase:
                obj = value._print_object(indentation_depth + u'\t', entry_separator, object_start,
                                          indentation_increment)
                result += indentation_depth + u'\t{0} = {1};\n'.format(value.get_id().__repr__(), obj)
            result += u'/* End {0} section */\n'.format(section)
        result += indentation_depth + u'}'
        return result

    def get_keys(self):
        """
        :return: all the keys of the object (ids of objects)
        """
        keys = []
        for section in self.get_sections():
            phase = self._sections[section]
            for obj in phase:
                keys += obj.get_id()
        keys.sort()
        return keys

    def get_sections(self):
        sections = self._sections.keys()
        sections.sort()
        return sections

    def __getitem__(self, key):
        for section in self.get_sections():
            phase = self._sections[section]
            for obj in phase:
                if key == obj.get_id():
                    return obj
        return None

    def __setitem__(self, key, value):
        if value.isa not in self._sections:
            self._sections[value.isa] = []

        self._sections[value.isa].append(value)
        value._parent = self

    def __delitem__(self, key):
        obj = self[key]
        if obj is not None:
            phase = self._sections[obj.isa]
            phase.remove(obj)

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
            if section.endswith(u'Target'):
                targets += [value for value in self._sections[section]]

        if name is None:
            return targets

        for target in targets:
            if target.name == name:
                return [target]
        return []

    def get_configurations_on_targets(self, target_name=None, configuration_name=None):
        """
        Retrieves all configuration given a name on the specified target
        :param target_name: Searches for a specific target name, if None all targets are used
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
