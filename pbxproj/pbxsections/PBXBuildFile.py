from pbxproj import *


class PBXBuildFile(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, attributes=None, compiler_flags=None):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'fileRef': file_ref.get_id(),
            u'settings': cls._get_settings(attributes, compiler_flags)
        })

    @classmethod
    def _get_settings(cls, attributes=None, compiler_flags=None):
        if attributes is None and compiler_flags is None:
            return None

        settings = {}
        if attributes is not None:
            if not isinstance(attributes, list):
                attributes = [attributes]
            settings[u'ATTRIBUTES'] = attributes

        if compiler_flags is not None:
            if not isinstance(compiler_flags, list):
                compiler_flags = [compiler_flags]
            settings[u'COMPILER_FLAGS'] = u' '.join(compiler_flags)

        return settings

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n',
                      indentation_increment=u'\t'):
        return super(PBXBuildFile, self)._print_object(u'', entry_separator=u' ', object_start=u'',
                                                       indentation_increment=u'')

    def _get_comment(self):
        return u'{0} in {1}'.format(self.fileRef._get_comment(), self._get_section())

    def _get_section(self):
        objects = self.get_parent()
        target = self.get_id()

        for section in objects.get_sections():
            for obj in objects.get_objects_in_section(section):
                if u'files' in obj and target in obj.files:
                    return obj._get_comment()

    def add_attributes(self, attributes):
        if not isinstance(attributes, list):
            attributes = [attributes]

        if u'settings' not in self:
            self[u'settings'] = PBXGenericObject()

        if u'ATTRIBUTES' not in self.settings:
            self.settings[u'ATTRIBUTES'] = PBXList()

        # append, if it's assigned and the list only has 1 element it will turn it into a string
        self.settings.ATTRIBUTES += attributes

    def remove_attributes(self, attributes):
        if u'settings' not in self or u'ATTRIBUTES' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(attributes, list):
            attributes = [attributes]

        for attribute in self.settings.ATTRIBUTES:
            self.settings.ATTRIBUTES.remove(attribute)

        return self._clean_up_settings()

    def add_compiler_flags(self, compiler_flags):
        if isinstance(compiler_flags, list):
            compiler_flags = u' '.join(compiler_flags)

        if u'settings' not in self:
            self[u'settings'] = PBXGenericObject()

        if u'COMPILER_FLAGS' not in self.settings:
            self.settings[u'COMPILER_FLAGS'] = u''

        self.settings[u'COMPILER_FLAGS'] += u' ' + compiler_flags
        self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].strip()

    def remove_compiler_flags(self, compiler_flags):
        if u'settings' not in self or u'COMPILER_FLAGS' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(compiler_flags, list):
            compiler_flags = [compiler_flags]

        for flag in compiler_flags:
            self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].replace(flag, u'')
        self.settings[u'COMPILER_FLAGS'] = self.settings[u'COMPILER_FLAGS'].strip()

        return self._clean_up_settings()

    def _clean_up_settings(self):
        # no attributes remain, remove the element
        if u'ATTRIBUTES' in self.settings and self.settings.ATTRIBUTES.__len__() == 0:
            del self.settings[u'ATTRIBUTES']

        # no flags remain, remove the element
        if u'COMPILER_FLAGS' in self.settings and self.settings.COMPILER_FLAGS.__len__() == 0:
            del self.settings[u'COMPILER_FLAGS']

        if self.settings.get_keys().__len__() == 0:
            del self[u'settings']

        return True
