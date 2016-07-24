from pbxproj.pbxsections import *


class ProjectGroups:
    def add_group(self, name, path=None, parent=None):
        # question: is it possible to create multiple groups with the same name under the same parent?
        pass

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
        path = os.path.abspath(path)
        groups = self.objects.get_objects_in_section(u'PBXGroup')
        groups = [group for group in groups if os.path.abspath(group.psth) == path]

        if parent:
            return [group for group in groups if parent.has_child(group)]

        return groups

