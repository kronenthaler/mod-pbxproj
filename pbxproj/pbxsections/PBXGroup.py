from pbxproj.PBXGenericObject import *


class PBXGroup(PBXGenericObject):
    @classmethod
    def create(cls, path=None, name=None, tree=u'<group>', children=[]):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'children': children,
            u'name': name,
            u'path': path,
            u'sourceTree': tree
        })

    def get_name(self):
        if u'name' in self:
            return self.name
        return self.path

    def has_child(self, child):
        if u'children' not in self:
            return False

        return child in self.children