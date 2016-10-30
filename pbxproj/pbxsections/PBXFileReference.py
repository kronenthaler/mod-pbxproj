import os
from pbxproj import PBXGenericObject


class PBXFileReference(PBXGenericObject):
    @classmethod
    def create(cls, path, tree=u'SOURCE_ROOT'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'path': path,
            u'name': os.path.split(path)[1],
            u'sourceTree': tree
        })

    def set_explicit_file_type(self, file_type):
        if u'lastKnownFileType' in self:
            del self[u'lastKnownFileType']
        self[u'explicitFileType'] = file_type

    def set_last_known_file_type(self, file_type):
        if u'explicitFileType' in self:
            del self[u'explicitFileType']
        self[u'lastKnownFileType'] = file_type

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        return super(PBXFileReference, self)._print_object(u'', entry_separator=u' ', object_start=u'',
                                                     indentation_increment=u'')

