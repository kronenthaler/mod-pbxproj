import re
import uuid
import copy

from pbxproj.PBXKey import PBXKey


class PBXGenericObject(object):
    """
    Generic class that creates internal attributes to match the structure of the tree used to create the element.
    Also, prints itself using the openstep format. Extensions might be required to insert comments on right places.
    """
    _VALID_KEY_REGEX = re.compile(r'^[a-zA-Z0-9\\._/]*$')
    _ESCAPE_REPLACEMENTS = [
        ('\\', '\\\\'),
        ('\n', '\\n'),
        ('\"', '\\"'),
        ('\0', '\\0'),
        ('\t', '\\\t'),
        ('\'', '\\\''),
    ]

    def __init__(self, parent=None):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def parse(self, value):
        if isinstance(value, dict):
            return self._parse_dict(value)

        if isinstance(value, str):
            return self._parse_string(value)

        if isinstance(value, list):
            return self._parse_list(value)

        return value

    def _parse_dict(self, obj):
        # all top level objects are added as variables to this object
        for key, value in obj.items():
            if value is None:
                continue

            key = self._parse_string(key)
            setattr(self, key, self._get_instance(key, value))

        return self

    def _parse_list(self, obj):
        ret = []
        for item in obj:
            ret.append(copy.copy(self).parse(item))

        return ret

    def _parse_string(self, obj):
        if re.match('([0-9A-F]{24})', obj) is not None:
            return PBXKey(obj, self)

        return obj

    def _get_instance(self, class_type, content):
        # check if the key maps to a kind of object
        return self._get_class_reference(class_type)(self).parse(content)

    @classmethod
    def _get_class_reference(cls, class_type):
        module = __import__('pbxproj')
        return getattr(module, class_type, PBXGenericObject)

    def __repr__(self):
        return self._print_object()

    def _print_object(self, indent_depth='', entry_separator='\n', object_start='\n', indent_increment='\t'):
        ret = f"{'{'}{object_start}"
        for key in self.get_keys():
            value = self._format(self[key], indent_depth, entry_separator, object_start,
                                 indent_increment)

            # use key decorators, could simplify the generation of the comments.
            ret += f'{indent_depth}{indent_increment}{PBXGenericObject._escape(key)} = {value};{entry_separator}'

        ret += f"{indent_depth}{'}'}"
        return ret

    def _print_list(self, obj, indentation_depth='', entry_separator='\n', object_start='\n',
                    indentation_increment='\t'):
        ret = f'({object_start}'
        for item in obj:
            value = self._format(item, indentation_depth, entry_separator, object_start, indentation_increment)

            ret += f'{indentation_depth}{indentation_increment}{value},{entry_separator}'
        ret += f'{indentation_depth})'
        return ret

    def _format(self, value, indentation_depth='', entry_separator='\n', object_start='\n', indentation_increment='\t'):
        if hasattr(value, '_print_object'):
            value = value._print_object(indentation_depth + indentation_increment,
                                        entry_separator,
                                        object_start,
                                        indentation_increment)
        elif isinstance(value, list):
            value = self._print_list(value, indentation_depth + indentation_increment,
                                     entry_separator,
                                     object_start,
                                     indentation_increment)
        elif isinstance(value, PBXKey):
            value = value.__repr__()
        else:
            value = PBXGenericObject._escape(value.__str__(), exclude=['\''])

        return value

    def get_keys(self):
        fields = [field for field in list(self.__dict__.keys()) if field[0] != '_']
        if 'isa' in fields:
            fields.remove('isa')
            fields = sorted(fields)
            fields.insert(0, 'isa')
        else:
            fields = sorted(fields)

        return fields

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key, default):
        return getattr(self, key, default)

    def __setitem__(self, key, value):
        if type(value) is list:
            if value.__len__() == 1:
                value = value[0]
            if value.__len__() == 0:
                if hasattr(self, key):
                    delattr(self, key)
                return

        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, item):
        return hasattr(self, item)

    def __lt__(self, other):
        return self.get_id() < other.get_id()

    def _resolve_comment(self, key):
        parent = self.get_parent()
        if key in self:
            return self[key]._get_comment()

        if parent is None:
            return None

        return parent._resolve_comment(key)

    def get_id(self):
        return self['_id']

    def _get_comment(self):
        if hasattr(self, 'name'):
            return self.name
        if hasattr(self, 'path'):
            return self.path

        return None

    @classmethod
    def _generate_id(cls):
        return ''.join(str(uuid.uuid4()).upper().split('-')[1:])

    @classmethod
    def _escape(cls, item, exclude=None):
        exclude = set() if exclude is None else set(exclude)
        if len(item) != 0 and cls._VALID_KEY_REGEX.match(item) is not None:
            return item

        escaped = item
        for unescaped_value, escaped_value in cls._ESCAPE_REPLACEMENTS:
            if unescaped_value in exclude:
                continue
            escaped = escaped.replace(unescaped_value, escaped_value)

        return '"'+escaped+'"'

