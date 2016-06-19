import os
from pbxproj import PBXGenericObject


class XCBuildConfiguration(PBXGenericObject):
    _OTHER_CFLAGS = u'OTHER_CFLAGS'
    _OTHER_LDFLAGS = u'OTHER_LDFLAGS'

    def add_flags(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        current_flags = self.buildSettings[flag_name]
        if current_flags is None:
            if isinstance(flags, list) and flags.__len__() == 1:
                flags = flags[0]
            self.buildSettings[flag_name] = flags
            return

        if not isinstance(current_flags, list):
            self.buildSettings[flag_name] = [current_flags]

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] += flags

    def remove_flags(self, flag_name, flags):
        if u'buildSettings' not in self or self.buildSettings[flag_name] is None:
            # nothing to remove
            return

        current_flags = self.buildSettings[flag_name]
        if not isinstance(current_flags, list):
            current_flags = [current_flags]

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] = [x for x in current_flags if x not in flags]

        if self.buildSettings[flag_name].__len__() == 1:
            self.buildSettings[flag_name] = self.buildSettings[flag_name][0]
        elif self.buildSettings[flag_name].__len__() == 0:
            del self.buildSettings[flag_name]

    def add_search_paths(self, paths, key, recursive=False, escape=False):
        # TODO: check if the escape parameter is necessary at all (formatting is taking care of necessary escaping)
        if not isinstance(paths, list):
            paths = [paths]

        # build the recursive/escaped strings and add the flags accordingly
        flags = []
        for path in paths:
            if path == '$(inherited)':
                escape = False
                recursive = False

            if recursive and not path.endswith('/**'):
                path = os.path.join(path, '**')

            if escape:
                path = u'"{0}"'.format(path)
            flags.append(path)

        self.add_flags(key, flags)

    def remove_search_paths(self, paths, key):
        self.remove_flags(key, paths)
