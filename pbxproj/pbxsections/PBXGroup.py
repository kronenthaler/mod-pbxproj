from pbxproj import PBXGenericObject
from pbxproj.pbxsections import PBXFileReference, PBXReferenceProxy


class PBXGroup(PBXGenericObject):
    @classmethod
    def create(cls, path=None, name=None, tree='<group>', children=None):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'children': children if children else [],
            'name': name,
            'path': path,
            'sourceTree': tree
        })

    def get_name(self):
        if 'name' in self:
            return self.name
        if 'path' in self:
            return self.path
        return None

    def get_path(self):
        if 'path' in self:
            return self.path
        if 'name' in self:
            return self.name
        return None

    def has_child(self, child):
        """
        Checks if the given child id
        :param child: The id to check if it's a child of the group
        :return: True if the given id it's a child of this group, False otherwise
        """
        if 'children' not in self:
            return False

        if not isinstance(child, str):
            child = child.get_id()

        return child in self.children

    def add_child(self, child):
        # if it's not the right type of children for the group
        if not isinstance(child, PBXGroup) \
                and not isinstance(child, PBXFileReference) \
                and not isinstance(child, PBXReferenceProxy):
            return False

        self.children.append(child.get_id())
        return True

    def remove_child(self, child):
        if self.has_child(child):
            self.children.remove(child.get_id())
            return True

        return False

    def remove(self, recursive=True):
        parent = self.get_parent()
        # remove from the objects reference
        del parent[self.get_id()]

        # remove children if necessary
        if recursive:
            for subgroup_id in self.children:
                subgroup = parent[subgroup_id]
                if subgroup is None or not subgroup.remove(recursive):
                    return False

        return True
