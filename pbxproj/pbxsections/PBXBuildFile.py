import sys

from pbxproj import PBXGenericObject, PBXList


class PBXBuildFile(PBXGenericObject):
    def __init__(self, parent=None):
        self._parent = parent
        self._section = None

    @classmethod
    def create(cls, file_ref, attributes=None, compiler_flags=None, is_product=False):
        ref_key = 'productRef' if is_product else 'fileRef'
        return cls().parse({
            '_id': cls._generate_id(),
            'isa': cls.__name__,
            ref_key: file_ref.get_id(),
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

    def _print_object(self, indent_depth='', entry_separator='\n', object_start='\n', indent_increment='\t'):
        return super(PBXBuildFile, self)._print_object('', entry_separator=' ', object_start='', indent_increment='')

    def _get_comment(self):
        comment = '(null)'
        if hasattr(self, 'fileRef'):
            comment = self.fileRef._get_comment()
        if hasattr(self, 'productRef'):
            comment = self.productRef._get_comment()
        return f'{comment} in {self._get_section()}'

    def _get_section(self):
        if self._section is not None:
            return self._section

        print('[WARNING] falling back to slow mechanism', file=sys.stderr)
        objects = self.get_parent()
        target = self.get_id()

        for section in objects.get_sections():
            for obj in objects.get_objects_in_section(section):
                if 'files' in obj and target in obj.files:
                    self._section = obj._get_comment()
                    break
        return self._section

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

        for attribute in attributes:
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

    def remove(self, recursive=True):
        if recursive:
            build_phases = [build_phase for build_phase in self.get_parent().get_sections() if build_phase.endswith('BuildPhase')]
            for build_phase in self.get_parent().get_objects_in_section(*build_phases):
                # if this build_phase contains a reference to this build_file...
                if 'files' in build_phase and self.get_id() in build_phase.files:
                    build_phase.remove_build_file(self)

        del self.get_parent()[self.get_id()]
        return True