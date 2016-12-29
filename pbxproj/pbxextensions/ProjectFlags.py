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
        Removes the given flags from the flag_name section of the target on the configurations
        :param flag_name: name of the flag to be removed the values from
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_flags(flag_name, flags)

    def add_other_cflags(self, flags, target_name=None, configuration_name=None):
        """
        Adds flag values to the OTHER_CFLAGS flag.
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_flags(XCBuildConfigurationFlags.OTHER_CFLAGS, flags, target_name, configuration_name)

    def remove_other_cflags(self, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags from the OTHER_CFLAGS section of the target on the configurations
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_flags(XCBuildConfigurationFlags.OTHER_CFLAGS, flags, target_name, configuration_name)

    def add_other_ldflags(self, flags, target_name=None, configuration_name=None):
        """
        Adds flag values to the OTHER_LDFLAGS flag.
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_flags(XCBuildConfigurationFlags.OTHER_LDFLAGS, flags, target_name, configuration_name)

    def remove_other_ldflags(self, flags, target_name=None, configuration_name=None):
        """
        Removes the given flags from the OTHER_LDFLAGS section of the target on the configurations
        :param flags: A string or array of strings. If none, removes all values from the flag.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_flags(XCBuildConfigurationFlags.OTHER_LDFLAGS, flags, target_name, configuration_name)

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
        Removes the given search paths from the path_type section of the target on the configurations
        :param path_type: name of the path type to be removed the values from
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        for configuration in self.objects.get_configurations_on_targets(target_name, configuration_name):
            configuration.remove_search_paths(path_type, paths)

    def add_header_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        """
        Adds paths to the HEADER_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.HEADER_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_header_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the HEADER_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.HEADER_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_library_search_paths(self, paths, recursive=True, escape=False, target_name=None, configuration_name=None):
        """
        Adds paths to the LIBRARY_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.LIBRARY_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_library_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the LIBRARY_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.LIBRARY_SEARCH_PATHS, paths, target_name, configuration_name)

    def add_framework_search_paths(self, paths, recursive=True, escape=False, target_name=None,
                                   configuration_name=None):
        """
        Adds paths to the FRAMEWORK_SEARCH_PATHS configuration.
        :param paths: A string or array of strings
        :param recursive: Add the paths as recursive ones
        :param escape: Escape the path in case it contains spaces
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.add_search_paths(XCBuildConfigurationFlags.FRAMEWORK_SEARCH_PATHS, paths, recursive, escape, target_name,
                              configuration_name)

    def remove_framework_search_paths(self, paths, target_name=None, configuration_name=None):
        """
        Removes the given search paths from the FRAMEWORK_SEARCH_PATHS section of the target on the configurations
        :param paths: A string or array of strings
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return: void
        """
        self.remove_search_paths(XCBuildConfigurationFlags.FRAMEWORK_SEARCH_PATHS, paths, target_name, configuration_name)

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

            self.objects[shell.get_id()] = shell
            target.add_build_phase(shell, 0 if insert_before_compile else None)

    def remove_run_script(self, script, target_name=None):
        """
        Removes the given script string from the given target
        :param script: The script string to be removed from the target
        :param target_name: Target name to add the flag to or None for every target
        :return:
        """
        for target in self.objects.get_targets(target_name):
            for build_phase_id in target.buildPhases:
                build_phase = self.objects[build_phase_id]
                if not isinstance(build_phase, PBXShellScriptBuildPhase):
                    continue

                if build_phase.shellScript == script:
                    del self.objects[build_phase_id]
                    target.remove_build_phase(build_phase)

    def add_code_sign(self, code_sign_identity, development_team, provisioning_profile_uuid,
                      provisioning_profile_specifier, target_name=None, configuration_name=None):
        """
        Adds the code sign information to the project and creates the appropriate flags in the configuration.
        In xcode 8+ the provisioning_profile_uuid becomes optional, and the provisioning_profile_specifier becomes
        mandatory. Contrariwise, in xcode 8< provisioning_profile_uuid becomes mandatory and
        provisioning_profile_specifier becomes optional.

        :param code_sign_identity: Code sign identity name. Usually formatted as: 'iPhone Distribution[: <Company name> (MAAYFEXXXX)]'
        :param development_team: Development team identifier string. Usually formatted as: 'MAAYFEXXXX'
        :param provisioning_profile_uuid: Provisioning profile UUID string. Usually formatted as: '6f1ffc4d-xxxx-xxxx-xxxx-6dc186280e1e'
        :param provisioning_profile_specifier: Provisioning profile specifier (a.k.a. name) string.
        :param target_name: Target name to add the flag to or None for every target
        :param configuration_name: Configuration name to add the flag to or None for every configuration
        :return:
        """
        self.add_flags(u'CODE_SIGN_IDENTITY[sdk=iphoneos*]', code_sign_identity, target_name, configuration_name)
        self.add_flags(u'DEVELOPMENT_TEAM', development_team, target_name, configuration_name)
        self.add_flags(u'PROVISIONING_PROFILE', provisioning_profile_uuid, target_name, configuration_name)
        self.add_flags(u'PROVISIONING_PROFILE_SPECIFIER', provisioning_profile_specifier, target_name, configuration_name)

        for target in self.objects.get_targets(target_name):
            self.objects[self.rootObject].set_provisioning_style(PBXProvioningTypes.MANUAL, target)
