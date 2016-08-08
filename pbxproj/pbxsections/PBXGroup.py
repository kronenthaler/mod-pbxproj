from pbxproj.PBXGenericObject import *
from pbxproj.pbxsections import *


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
        if u'path' in self:
            return self.path
        return None

    def get_path(self):
        if u'path' in self:
            return self.path
        if u'name' in self:
            return self.name
        return None

    def has_child(self, child):
        if u'children' not in self:
            return False

        return child in self.children

    def add_child(self, children):
        # if it's not the right type of children for the group
        if not isinstance(children, PBXGroup) and not isinstance(children, PBXFileReference):
            return False

        self.children.append(children.get_id())
        return True

    def remove_child(self, children):
        if self.has_child(children.get_id()):
            self.children.remove(children.get_id())
            return True

        return False

    def remove(self, recursive=True):
        # remove from the objects reference
        del self._parent[self.get_id()]

        # remove children if necessary
        if recursive:
            for subgroup_id in self.children:
                subgroup = self._parent[subgroup_id]
                if subgroup is None or not subgroup.remove(recursive):
                    return False

        return True
