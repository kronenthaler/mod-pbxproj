from pbxproj import PBXGenericObject


class PBXContainerItemProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, proxy_type=2):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'containerPortal': file_ref.get_id(),
            'proxyType': proxy_type,
            'remoteGlobalIDString': remote_ref.productReference,
            'remoteInfo': remote_ref.productName
        })

    def _get_comment(self):
        return 'PBXContainerItemProxy'

    def __getitem__(self, item):
        if item == 'remoteGlobalIDString':
            return getattr(self, item).__str__()
        return super().__getitem__(item)