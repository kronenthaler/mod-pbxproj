import warnings
from pbxproj.pbxsections import *
from pbxproj.pbxextensions import ProjectFiles


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    def new_func(*args, **kwargs):
        warnings.filterwarnings('default', category=DeprecationWarning)
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


class Deprecations:
    """
    This class contains all methods that will be deprecated in the near future.
    It provides a compatibility layer meanwhile using old methods signatures as an alias of the new version available.
    """

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    @classmethod
    @deprecated
    def Load(cls, path, pure_python=False):
        return cls.load(path)

    @deprecated
    def remove_group(self, group_id, recursive=True):
        return self.remove_group_by_id(group_id, recursive)

    @deprecated
    def add_run_script_all_targets(self, script=None):
        self.add_run_script(script, target=None)

    @deprecated
    def add_single_valued_flag(self, flag, value, configuration='All'):
        self.add_flags(flag, value, target_name=None, configuration_name=configuration)

    @deprecated
    def remove_single_valued_flag(self, flag, configuration='All'):
        self.remove_flags(flag, None, target_name=None, configuration_name=configuration)

    @deprecated
    def add_flags(self, pairs, configuration='All'):
        for flag_name in pairs:
            self.add_flags(flag_name, pairs[flag_name], target_name=None, configuration_name=configuration)

    @deprecated
    def remove_flags(self, pairs, configuration='All'):
        for flag_name in pairs:
            self.remove_flags(flag_name, pairs[flag_name], target_name=None, configuration_name=configuration)

    @deprecated
    def get_groups_by_os_path(self, path):
        return self.get_groups_by_path(path)

    @deprecated
    def get_files_by_os_path(self, os_path, tree='SOURCE_ROOT'):
        return self.get_files_by_path(os_path, tree)

    @deprecated
    def remove_file(self, file_id, recursive=True):
        return self.remove_file_by_id(file_id)

    @deprecated
    def get_file_id_by_path(self, path):
        file_ref = self.get_file_id_by_path(path)[0]
        if file_ref is not None:
            return file_ref.get_id()
        return None

    @deprecated
    def get_keys_for_files_by_name(self, name):
        return map(lambda x: x.get_id(), self.get_files_by_name(name))

    @deprecated
    def get_build_files(self, file_id):
        return self.get_build_files_for_file(file_id)

    @deprecated
    def get_build_phases(self, phase_name):
        return self.get_build_phases_by_name(phase_name)

    @deprecated
    def add_file_if_doesnt_exist(self, f_path, parent=None, tree='SOURCE_ROOT', create_build_files=True, weak=False,
                                 ignore_unknown_type=False, target=None):
        file_options = ProjectFiles.FileOptions(create_build_files=create_build_files, weak=weak,
                                                ignore_unknown_type=ignore_unknown_type)
        return self.add_file(f_path, parent=parent, tree=tree, force=False, target_name=target,
                             file_options=file_options)
