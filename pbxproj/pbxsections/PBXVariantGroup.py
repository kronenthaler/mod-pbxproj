from pbxproj.PBXGenericObject import *
from pbxproj.pbxsections.PBXFileReference import *


class PBXVariantGroup(PBXGenericObject):
    @classmethod
    def create(cls, name, children=None, source_tree=u'<group>'):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'children': children if children else [],
            u'name': name,
            u'sourceTree': source_tree
        })

    def add_variant(self, file_ref):
        if not isinstance(file_ref, PBXFileReference):
            return False

        self.children.append(file_ref.get_id())
        return True

    def remove_variant(self, file_ref):
        if not isinstance(file_ref, PBXFileReference):
            return False

        self.children.remove(file_ref.get_id())
        del self.get_parent()[file_ref.get_id()]

        return True
