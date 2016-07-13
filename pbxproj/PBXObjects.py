import uuid
from pbxproj import PBXGenericObject


class objects(PBXGenericObject):
    def __init__(self, parent=None):
        super(type(self), self).__init__(parent)

        # sections: dict<isa, [tuple(id, obj)]>
        # sections get aggregated under the isa type. Each contains a list of tuples (id, obj) with every object defined
        self._sections = {}

    def parse(self, object):
        # iterate over the keys and fill the sections
        if isinstance(object, dict):
            for key, value in object.iteritems():
                key = self._parse_string(key)
                obj_type = key
                if 'isa' in value:
                    obj_type = value['isa']

                child = self._get_instance(obj_type, value)
                child[u'_id'] = key
                self[key] = child

            return self

        # safe-guard: delegate to the parent how to deal with non-object values
        return super(type(self), self).parse(object)

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        # override to change the way the object is printed out
        result = u'{\n'
        for section in self._get_keys():
            phase = self._sections[section]
            phase.sort(key=lambda x: x[0])
            result += u'\n/* Begin {0} section */\n'.format(section)
            for (key, value) in phase:
                obj = value._print_object(indentation_depth + u'\t', entry_separator, object_start,
                                          indentation_increment)
                result += indentation_depth + u'\t{0} = {1};\n'.format(key.__repr__(), obj)
            result += u'/* End {0} section */\n'.format(section)
        result += indentation_depth + u'}'
        return result

    def _get_keys(self):
        sections = self._sections.keys()
        sections.sort()
        return sections

    def __getitem__(self, key):
        for section in self._sections.iterkeys():
            phase = self._sections[section]
            for (target_key, value) in phase:
                if key == target_key:
                    return value
        return None

    def __setitem__(self, key, value):
        if value.isa not in self._sections:
            self._sections[value.isa] = []

        node = (key, value)
        self._sections[value.isa].append(node)
        value._parent = self

    def __delitem__(self, key):
        obj = self[key]
        phase = self._sections[obj.isa]
        phase.remove((obj._id, obj))

    def __contains__(self, item):
        return self[item] is not None

    def get_objects_in_section(self, name):
        if name in self._sections:
            return self._sections[name]
        return []

    def get_targets(self, name=None):
        """
        Retrieve all/one target objects
        :param name: name of the target to search for, None for everything
        :return: A list of target objects
        """
        targets = []
        for section in self._sections.iterkeys():
            if section.endswith(u'Target'):
                targets += [value for (key, value) in self._sections[section]]

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
