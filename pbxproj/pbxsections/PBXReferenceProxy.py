from pbxproj import PBXGenericObject


class PBXReferenceProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, tree=u'BUILT_PRODUCTS_DIR'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'path': file_ref.path,
            u'fileType': file_ref.get_file_type(),
            u'remoteRef': remote_ref.get_id(),
            u'sourceTree': tree
        })

    def get_file_type(self):
        return self.fileType

    def get_name(self):
        return self.path
