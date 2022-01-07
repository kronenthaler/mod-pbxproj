import os

from pbxproj import PBXGenericObject


class PBXFileReference(PBXGenericObject):
    @classmethod
    def create(cls, path, tree='SOURCE_ROOT'):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'path': path,
            'name': os.path.split(path)[1],
            'sourceTree': tree
        })

    def set_explicit_file_type(self, file_type):
        if 'lastKnownFileType' in self:
            del self['lastKnownFileType']
        self['explicitFileType'] = file_type

    def set_last_known_file_type(self, file_type):
        if 'explicitFileType' in self:
            del self['explicitFileType']
        self['lastKnownFileType'] = file_type

    def get_file_type(self):
        if 'explicitFileType' in self:
            return self.explicitFileType
        return self.lastKnownFileType

    def _print_object(self, indent_depth='', entry_separator='\n', object_start='\n',
                      indent_increment='\t'):
        return super(PBXFileReference, self)._print_object('', entry_separator=' ', object_start='',
                                                           indent_increment='')

    def get_name(self):
        if hasattr(self, 'name'):
            return self.name
        return self.path

    def remove(self, recursive=True):
        parent = self.get_parent()
        # search on the BuildFiles if there is a build file to be removed, and remove it
        build_files = [build_file for build_file in parent.get_objects_in_section('PBXBuildFile')
                       if build_file.fileRef == self.get_id()]
        for build_file in build_files:
            build_file.remove(recursive)

        # search for each group that has a reference to the build file and remove it from it.
        for group in parent.get_objects_in_section('PBXGroup'):
            if self.get_id() in group.children:
                group.remove_child(self)

        # remove the file reference from it's parent
        del parent[self.get_id()]

        return True
