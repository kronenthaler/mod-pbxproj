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
                if child.isa not in self._sections:
                    self._sections[child.isa] = []

                node = (key, child)
                self._sections[child.isa].append(node)

            return self

        # safe-guard: delegate to the parent how to deal with non-object values
        return super(type(self), self).parse(object)

    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        # override to change the way the object is printed out
        result = "{\n"
        for section in self._get_keys():
            phase = self._sections[section]
            phase.sort(key=lambda x: x[0])
            result += "\n/* Begin {0} section */\n".format(section)
            for (key, value) in phase:
                obj = value._print_object(indentation_depth + "\t", entry_separator, object_start, indentation_increment)
                result += indentation_depth + "\t{0} = {1};\n".format(key.__repr__(), obj)
            result += "/* End {0} section */\n".format(section)
        result += indentation_depth + "}"
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

    def __contains__(self, item):
        return self[item] is not None

    def keys(self):
        keys = []
        for section in self._sections.iterkeys():
            phase = self._sections[section]
            for (target_key, value) in phase:
                keys.append(target_key)
        return keys
