from pbxproj import PBXGenericObject


class XCRemoteSwiftPackageReference(PBXGenericObject):
    @classmethod
    def create(cls, repositoryURL, requirement={}):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'repositoryURL': repositoryURL,
            'requirement': PBXGenericObject().parse(requirement)
        })

    def _get_comment(self):
        name = None
        if hasattr(self, 'repositoryURL'):
            name = self.repositoryURL.split('/')[-1]
            if name.endswith('.git'):
                name = name[:-4]
        return f'XCRemoteSwiftPackageReference "{name}"'
