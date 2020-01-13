from pbxproj import PBXGenericObject


class PBXReferenceProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, tree='BUILT_PRODUCTS_DIR'):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'path': file_ref.path,
            'fileType': file_ref.get_file_type(),
            'remoteRef': remote_ref.get_id(),
            'sourceTree': tree
        })

    def get_file_type(self):
        return self.fileType

    def get_name(self):
        return self.path
