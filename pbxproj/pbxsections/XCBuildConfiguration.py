from pbxproj import PBXGenericObject


class XCBuildConfiguration(PBXGenericObject):
    OTHER_CFLAGS = u'OTHER_CFLAGS'
    OTHER_LDFLAGS = u'OTHER_LDFLAGS'

    def add_other_cflags(self, flags):
        self._add_flags(XCBuildConfiguration.OTHER_CFLAGS, flags)

    def remove_other_cflags(self, flags):
        self._remove_flags(XCBuildConfiguration.OTHER_CFLAGS, flags)

    def add_other_ldflags(self, flags):
        self._add_flags(XCBuildConfiguration.OTHER_LDFLAGS, flags)

    def remove_other_ldflags(self, flags):
        self._remove_flags(XCBuildConfiguration.OTHER_LDFLAGS, flags)

    def _add_flags(self, flag_name, flags):
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

    def _remove_flags(self, flag_name, flags):
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
