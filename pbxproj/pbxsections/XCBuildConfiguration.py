from pbxproj import PBXGenericObject


class XCBuildConfiguration(PBXGenericObject):
    def add_other_cflags(self, flags):
        self._add_flag(u'OTHER_CFLAGS', flags)

    def add_other_ldflags(self, flags):
        self._add_flag(u'OTHER_LDFLAGS', flags)

    def _add_flag(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        current_flags = self.buildSettings[flag_name]
        if current_flags is None:
            self.buildSettings[flag_name] = flags
            return

        if not isinstance(current_flags, list):
            self.buildSettings[flag_name] = [current_flags]

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] += flags
