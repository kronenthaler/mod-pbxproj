from pbxproj import PBXGenericObject


class XCSwiftPackageProductDependency(PBXGenericObject):
    @classmethod
    def create(cls, package_ref, product_name):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'package': package_ref.get_id(),
            'productName': product_name
        })

    def _get_comment(self):
        if hasattr(self, 'productName'):
            return self.productName

        return None
