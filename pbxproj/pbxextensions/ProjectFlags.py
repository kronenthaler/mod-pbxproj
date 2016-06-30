from pbxproj.pbxsections import *


class ProjectFlags:
    """
    This class provides separation of concerns, this class contains all methods related to flags manipulations.
    This class should not be instantiated on its own
    """

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_flags(self, flag_name, flags, target_name=None, configuration_name=None):
        """
        Adds the given flags to the flag_name section of the target on the configurations
        :param flag_name: name of the flag to be added the values to
        :param flags: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.add_flags(flag_name, flags)

    def remove_flags(self, flag_name, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags to the flag_name section of the target on the configurations
        :param flag_name: name of the flag to be removed the values from
        :param flags: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_flags(flag_name, flags)

    def add_other_cflags(self, flags, target_name=None, configuration_name=None):
        self.add_flags(XCBuildConfiguration._OTHER_CFLAGS, flags, target_name, configuration_name)

    def remove_other_cflags(self, flags, target_name=None, configuration_name=None):
        self.remove_flags(XCBuildConfiguration._OTHER_CFLAGS, flags, target_name, configuration_name)

    def add_other_ldflags(self, flags, target_name=None, configuration_name=None):
        self.add_flags(XCBuildConfiguration._OTHER_LDFLAGS, flags, target_name, configuration_name)

    def remove_other_ldflags(self, flags, target_name=None, configuration_name=None):
        self.remove_flags(XCBuildConfiguration._OTHER_LDFLAGS, flags, target_name, configuration_name)

    def add_search_paths(self, path_type, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        """
        Adds the given search paths to the path type section of the target on the configurations
        :param path_type: name of the flag to be added the values to
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.add_search_paths(path_type, paths, recursive, escape)

    def remove_search_paths(self, path_type, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths to the path_type section of the target on the configurations
        :param path_type: name of the path type to be removed the values from
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_search_paths(path_type, paths)

    def add_header_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        self.add_search_paths(XCBuildConfiguration._HEADER_SEARCH_PATHS, paths, recursive, escape, target_name, configuration_name)

    def remove_header_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._HEADER_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_library_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        self.add_search_paths(XCBuildConfiguration._LIBRARY_SEARCH_PATHS, paths, recursive, escape, target_name, configuration_name)

    def remove_library_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._LIBRARY_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_framework_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        self.add_search_paths(XCBuildConfiguration._FRAMEWORK_SEARCH_PATHS, paths, recursive, escape, target_name, configuration_name)

    def remove_framework_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._FRAMEWORK_SEARCH_PATHS, paths, target_name, configuration_name)

