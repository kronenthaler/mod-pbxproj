from pbxproj import PBXGenericObject


class XCLocalSwiftPackageReference(PBXGenericObject):
    @classmethod
    def create(cls, relative_path):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'relativePath': relative_path
        })

    def _get_comment(self):
        return f'XCLocalSwiftPackageReference "{self.relativePath}"'
