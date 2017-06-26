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

    def get_file_type(self):
        if u'explicitFileType' in self:
            return self.explicitFileType
        return self.lastKnownFileType

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        return super(PBXFileReference, self)._print_object(u'', entry_separator=u' ', object_start=u'',
                                                           indentation_increment=u'')

    def get_name(self):
        if hasattr(self, u'name'):
            return self.name
        if hasattr(self, u'path'):
            return self.path
        return None

    def remove(self, recursive=True):
        # search on the BuildFiles if there is a build file to be removed, and remove it
        # search for each phase that has a reference to the build file and remove it from it.
        # remove the file reference from it's parent
        pass

