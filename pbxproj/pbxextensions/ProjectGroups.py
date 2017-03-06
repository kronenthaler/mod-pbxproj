from pbxproj.pbxsections import *


class ProjectGroups:
    """
    This class provides separation of concerns, this class contains all methods related to groups manipulations.
    This class should not be instantiated on its own
    """

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_group(self, name, path=None, parent=None, source_tree=u'<group>'):
        """
        Add a new group with the given name and optionally path to the parent group. If parent is None, the group will
        be added to the 'root' group.
        Additionally the source tree type can be specified, normally it's group.
        :param name: Name of the group to be added (visible folder name)
        :param path: Path relative to the project where this group points to. If not present, name will match the path
            name
        :param parent: The PBXGroup that will be the parent of this group. If parent is None, the default 'root' group
            will be used as parent
        :param source_tree: The type of group to be created
        :return: PBXGroup created
        """
        group = PBXGroup.create(name=name, path=path, tree=source_tree)

        parent = self._get_parent_group(parent)

        parent.add_child(group)
        self.objects[group.get_id()] = group

        return group

    def remove_group_by_id(self, group_id, recursive=True):
        """
        Remove the group matching the given group_id. If recursive is True, all descendants of this group are also removed.
        :param group_id: The group id to be removed
        :param recursive: All descendants should be removed as well
        :return: True if the element was removed successfully, False if an error occured or there was nothing to remove.
        """
        group = self.objects[group_id]
        if group is None:
            return False

        result = True
        # iterate over the children and determine if they are file/group and call the right method.
        for subgroup_id in list(group.children):
            subgroup = self.objects[subgroup_id]
            if subgroup is None:
                return False

            if recursive and isinstance(subgroup, PBXGroup):
                result &= self.remove_group_by_id(subgroup.get_id(), recursive)
            if isinstance(subgroup, PBXFileReference):
                result &= self.remove_file_by_id(subgroup.get_id())

        if not result:
            return False

        del self.objects[group.get_id()]

        # remove the reference from any other group object that could be containing it.
        for other_group in self.objects.get_objects_in_section(u'PBXGroup'):
            other_group.remove_child(group)

        return True

    def remove_group_by_name(self, group_name, recursive=True):
        """
        Remove the groups matching the given name. If recursive is True, all descendants of this group are also removed.
        This method could cause the removal of multiple groups that not necessarily are intended to be removed, use with
        caution
        :param group_name: The group name to be removed
        :param recursive: All descendants should be removed as well
        :return: True if the element was removed successfully, False otherwise
        """
        groups = self.get_groups_by_name(name=group_name)

        if groups.__len__() == 0:
            return False

        for group in groups:
            if not self.remove_group_by_id(group.get_id(), recursive):
                return False

        return True

    def get_groups_by_name(self, name, parent=None):
        """
        Retrieve all groups matching the given name and optionally filtered by the given parent node.
        :param name: The name of the group that has to be returned
        :param parent: A PBXGroup object where the object has to be retrieved from. If None all matching groups are returned
        :return: An list of all matching groups
        """
        groups = self.objects.get_objects_in_section(u'PBXGroup')
        groups = [group for group in groups if group.get_name() == name]

        if parent:
            return [group for group in groups if parent.has_child(group)]

        return groups

    def get_groups_by_path(self, path, parent=None):
        """
        Retrieve all groups matching the given path and optionally filtered by the given parent node.
        The path is converted into the absolute path of the OS before comparison.
        :param path: The name of the group that has to be returned
        :param parent: A PBXGroup object where the object has to be retrieved from. If None all matching groups are returned
        :return: An list of all matching groups
        """
        groups = self.objects.get_objects_in_section(u'PBXGroup')
        groups = [group for group in groups if group.get_path() == path]

        if parent:
            return [group for group in groups if parent.has_child(group)]

        return groups

    def get_or_create_group(self, name, path=None, parent=None):
        if not name:
            return None

        groups = self.get_groups_by_name(name, parent)
        if groups.__len__() > 0:
            return groups[0]

        return self.add_group(name, path, parent)

    def _get_parent_group(self, parent):
        if parent is None:
            # search for the mainGroup of the project
            project = self.objects[self[u'rootObject']]
            if project:
                parent = self.objects[project[u'mainGroup']]
                if parent is not None:
                    return parent

            # search for the group without name
            parent = self.get_groups_by_name(None)

            # if there is no parent, create and empty parent group, add it to the objects
            if parent.__len__() > 0:
                return parent[0]

            parent = PBXGroup.create(path=None, name=None)
            self.objects[parent.get_id()] = parent
            return parent

        # it's not a group instance, assume it's an id
        if not isinstance(parent, PBXGroup):
            return self.objects[parent]

        return parent
