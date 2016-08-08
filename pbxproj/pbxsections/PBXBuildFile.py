from pbxproj import PBXGenericObject


class PBXBuildFile(PBXGenericObject):
    @classmethod
    def create(cls, file_ref, weak=False):
        return cls().parse({
            u'_id': cls._generate_id(),
            u'isa': cls.__name__,
            u'fileRef': file_ref.get_id(),
            u'settings': {u'ATTRIBUTES': [u'Weak']} if weak else None
        })

    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n', indentation_increment=u'\t'):
        return super(type(self), self)._print_object(u'', entry_separator=u' ', object_start=u'', indentation_increment=u'')

    def _get_comment(self):
        return u'{0} in {1}'.format(self.fileRef._get_comment(), self._get_section())

    def _get_section(self):
        objects = self._parent
        target = self.get_id()

        for section in objects._get_keys():
            for obj in objects.get_objects_in_section(section):
                if u'files' in obj and target in obj.files:
                    return obj._get_comment()

    # todo: add attributes (weak)
    # todo: remove attributes (weak)
    # todo: add compiler flag
    # todo: remove compiler flag
