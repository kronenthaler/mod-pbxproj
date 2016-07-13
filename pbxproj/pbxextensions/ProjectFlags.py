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

    def add_search_paths(self, path_type, paths, recursive=True, escape=False, target_name=None,
                         configuration_name=None):
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
        self.add_search_paths(XCBuildConfiguration._HEADER_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_header_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._HEADER_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_library_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        self.add_search_paths(XCBuildConfiguration._LIBRARY_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_library_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._LIBRARY_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_framework_search_paths(self, paths, recursive=True, escape=False, target_name=None,
                                   configuration_name=None):
        self.add_search_paths(XCBuildConfiguration._FRAMEWORK_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_framework_search_paths(self, paths, target_name=None, configuration_name=None):
        self.remove_search_paths(XCBuildConfiguration._FRAMEWORK_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_run_script(self, script, target_name=None, insert_before_compile=False):
        """
        Adds a run script phase into the given target, optionally before compilation phase
        :param script: Script to be inserted on the run script
        :param target_name: Target name to add the flag to or None for every target
        :param insert_before_compile: Insert the run script phase before the compilation of the source files. By default,
        it's added at the end.
        :return:
        """
        for target in self.objects.get_targets(target_name):
            shell = PBXShellScriptBuildPhase.create(script)

            self.objects[shell._id] = shell
            if insert_before_compile:
                # insert before compile
                target.buildPhases.insert(0, shell._id)
            else:
                # append to the buildPhases of the target
                target.buildPhases.append(shell._id)

    def remove_run_script(self, script, target_name=None):
        """
        Removes the given script string from the given target
        :param script: The script string to be removed from the target
        :param target_name: Target name to add the flag to or None for every target
        :return:
        """
        for target in self.objects.get_targets(target_name):
            for buildPhase in target.buildPhases:
                if self.objects[buildPhase].isa != u'PBXShellScriptBuildPhase':
                    continue

                if self.objects[buildPhase].shellScript == script:
                    del self.objects[buildPhase]
                    target.buildPhases.remove(buildPhase)