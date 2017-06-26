from pbxproj import PBXGenericObject


class PBXContainerItemProxy(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, remote_ref, proxy_type=2):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'containerPortal': file_ref.get_id(),
            u'proxyType': proxy_type,
            u'remoteGlobalIDString': remote_ref.productReference,
            u'remoteInfo': remote_ref.productName
        })

    def _get_comment(self):
        return u'PBXContainerItemProxy'
