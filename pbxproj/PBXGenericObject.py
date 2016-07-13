import re
import uuid

from pbxproj.PBXKey import PBXKey


class PBXGenericObject(object):
    """
    Generic class that creates internal attributes to match the structure of the tree used to create the element.
    Also, prints itself using the openstep format. Extensions might be required to insert comments on right places.
    """
    _VALID_KEY_REGEX = '[a-zA-Z0-9\\._/]*'

    def __init__(self, parent=None):
        self._parent = parent

    def parse(self, value):
        if isinstance(value, dict):
            return self._parse_dict(value)

        if isinstance(value, basestring):
            return self._parse_string(value)

        if isinstance(value, list):
            return self._parse_list(value)

        return value

    def _parse_dict(self, obj):
        # all top level objects are added as variables to this object
        for key, value in obj.iteritems():
            key = self._parse_string(key)
            if not hasattr(self, key):
                setattr(self, key, self._get_instance(key, value))

        return self

    def _parse_list(self, obj):
        ret = []
        for item in obj:
            ret.append(self.parse(item))

        return ret

    def _parse_string(self, obj):
        if re.match('([0-9A-F]{24})', obj) is not None:
            return PBXKey(obj, self)

        return obj

    def _get_instance(self, type, content):
        # check if the key maps to a kind of object
        module = __import__(u'pbxproj')
        if hasattr(module, type):
            class_ = getattr(module, type)
            return class_(self).parse(content)

        return PBXGenericObject(self).parse(content)

    def __repr__(self):
        return self._print_object()

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n', indentation_increment=u'\t'):
        ret = u'{' + object_start

        for key in self._get_keys():
            value = self._format(getattr(self, key), indentation_depth, entry_separator, object_start, indentation_increment)

            # use key decorators, could simplify the generation of the comments.
            ret += indentation_depth + u'{3}{0} = {1};{2}'.format(PBXGenericObject._escape(key), value, entry_separator, indentation_increment)
        ret += indentation_depth + u'}'
        return ret

    def _print_list(self, obj, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n', indentation_increment=u'\t'):
        ret = u'(' + object_start
        for item in obj:
            value = self._format(item, indentation_depth, entry_separator, object_start, indentation_increment)

            ret += indentation_depth + u'{1}{0},{2}'.format(value, indentation_increment, entry_separator)
        ret += indentation_depth + u')'
        return ret

    def _format(self, value, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n', indentation_increment=u'\t'):
        if hasattr(value, u'_print_object'):
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
            value = PBXGenericObject._escape(value.__str__())

        return value

    def _get_keys(self):
        fields = list([x for x in dir(self) if not x.startswith(u'_') and not hasattr(getattr(self, x), '__call__')])
        if u'isa' in fields:
            fields.remove(u'isa')
            fields = sorted(fields)
            fields.insert(0, u'isa')
        else:
            fields = sorted(fields)

        return fields

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

        return None

    def __setitem__(self, key, value):
        if isinstance(value, list):
            if value.__len__() == 1:
                value = value[0]
            if value.__len__() == 0:
                delattr(self, key)
                return

        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, item):
        return hasattr(self, item)

    def _resolve_comment(self, key):
        if key in self:
            return self[key]._get_comment()

        if self._parent is None:
            return None

        return self._parent._resolve_comment(key)

    def _get_comment(self):
        if hasattr(self, u'name'):
            return self.name
        if hasattr(self, u'path'):
            return self.path

        return None

    @classmethod
    def _generate_id(cls):
        return ''.join(str(uuid.uuid4()).upper().split('-')[1:])

    @classmethod
    def _escape(cls, item):
        if item.__len__() == 0 or re.match(cls._VALID_KEY_REGEX, item).group(0) != item:
            return u'"{0}"'.format(item.replace(u'\n', u'\\n').replace(u'\"', u'\\"').replace(u'\0', u'\\0'))
        return item