import pbxproj
from pbxproj import *


class PBXBuildFile(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, attributes=None, compiler_flags=None):
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            'fileRef': file_ref.get_id(),
            'settings': cls._get_settings(attributes, compiler_flags)
        })

    @classmethod
    def _get_settings(cls, attributes=None, compiler_flags=None):
        if attributes is None and compiler_flags is None:
            return None

        settings = {}
        if attributes is not None:
            if not isinstance(attributes, list):
                attributes = [attributes]
            settings['ATTRIBUTES'] = attributes

        if compiler_flags is not None:
            if not isinstance(compiler_flags, list):
                compiler_flags = [compiler_flags]
            settings['COMPILER_FLAGS'] = ' '.join(compiler_flags)

        return settings

    def _print_object(self, indentation_depth='', entry_separator='\n', object_start='\n',
                      indentation_increment='\t'):
        return super(PBXBuildFile, self)._print_object('', entry_separator=' ', object_start='',
                                                       indentation_increment='')

    def _get_comment(self):
        comment = '(null)'
        if hasattr(self, 'fileRef'):
            comment = self.fileRef._get_comment()
        return '{0} in {1}'.format(comment, self._get_section())

    def _get_section(self):
        objects = self.get_parent()
        target = self.get_id()

        def fill_cache_during_save(cache):
            for section in objects.get_sections():
                for obj in objects.get_objects_in_section(section):
                    file_ids = obj['files']
                    if file_ids is not None:
                        comment = obj._get_comment()
                        for file_id in file_ids:
                            cache[file_id] = comment

        # Do a special behavior here while saving to avoid the linear lookup below and therefore
        # be significantly faster.
        if pbxproj.is_in_save(self):
            return pbxproj.get_from_cache_during_save(self, 'FILE_HOLDERS', objects, fill_cache_during_save, target)

        # It's not safe to do the above optimization "normally" (outside of saving) since the objects
        # may have been modified by the user, and the cache may therefore be invalid. So we fall back
        # to a linear search.
        for section in objects.get_sections():
            for obj in objects.get_objects_in_section(section):
                if 'files' in obj and target in obj.files:
                    return obj._get_comment()

    def get_attributes(self):
        if 'settings' not in self:
            return None

        if 'ATTRIBUTES' not in self.settings:
            return None

        return self.settings['ATTRIBUTES']

    def get_compiler_flags(self):
        if 'settings' not in self or 'COMPILER_FLAGS' not in self.settings:
            return None

        return self.settings['COMPILER_FLAGS']

    def add_attributes(self, attributes):
        if not isinstance(attributes, list):
            attributes = [attributes]

        if 'settings' not in self:
            self['settings'] = PBXGenericObject()

        if 'ATTRIBUTES' not in self.settings:
            self.settings['ATTRIBUTES'] = PBXList()

        # append, if it's assigned and the list only has 1 element it will turn it into a string
        self.settings.ATTRIBUTES += attributes

    def remove_attributes(self, attributes):
        if 'settings' not in self or 'ATTRIBUTES' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(attributes, list):
            attributes = [attributes]

        for attribute in self.settings.ATTRIBUTES:
            self.settings.ATTRIBUTES.remove(attribute)

        return self._clean_up_settings()

    def add_compiler_flags(self, compiler_flags):
        if isinstance(compiler_flags, list):
            compiler_flags = ' '.join(compiler_flags)

        if 'settings' not in self:
            self['settings'] = PBXGenericObject()

        if 'COMPILER_FLAGS' not in self.settings:
            self.settings['COMPILER_FLAGS'] = ''

        self.settings['COMPILER_FLAGS'] += ' ' + compiler_flags
        self.settings['COMPILER_FLAGS'] = self.settings['COMPILER_FLAGS'].strip()

    def remove_compiler_flags(self, compiler_flags):
        if 'settings' not in self or 'COMPILER_FLAGS' not in self.settings:
            # nothing to remove
            return False

        if not isinstance(compiler_flags, list):
            compiler_flags = [compiler_flags]

        for flag in compiler_flags:
            self.settings['COMPILER_FLAGS'] = self.settings['COMPILER_FLAGS'].replace(flag, '')
        self.settings['COMPILER_FLAGS'] = self.settings['COMPILER_FLAGS'].strip()

        return self._clean_up_settings()

    def _clean_up_settings(self):
        # no attributes remain, remove the element
        if 'ATTRIBUTES' in self.settings and self.settings.ATTRIBUTES.__len__() == 0:
            del self.settings['ATTRIBUTES']

        # no flags remain, remove the element
        if 'COMPILER_FLAGS' in self.settings and self.settings.COMPILER_FLAGS.__len__() == 0:
            del self.settings['COMPILER_FLAGS']

        if self.settings.get_keys().__len__() == 0:
            del self['settings']

        return True
