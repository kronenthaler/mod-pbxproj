from pbxproj import PBXGenericObject


class PBXFileSystemSynchronizedRootGroup(PBXGenericObject):
    @classmethod
    def create(cls, explicit_file_types, explicit_folders, path, tree='SOURCE_ROOT'):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'explicitFileTypes': explicit_file_types,
            'explicitFolders': explicit_folders,
            'path': path,
            'sourceTree': tree
        })
    
    def _print_object(self, indent_depth='', entry_separator='\n', object_start='\n', indent_increment='\t'):
        return super(PBXFileSystemSynchronizedRootGroup, self)._print_object('', entry_separator=' ', object_start='', indent_increment='')
