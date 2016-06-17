from pbxproj import PBXGenericObject


class PBXFileReference(PBXGenericObject):
    def _print_object(self, indentation_depth=u'', entry_separator=u'\n', object_start=u'\n', indentation_increment=u'\t'):
        return super(type(self), self)._print_object(u'', entry_separator=u' ', object_start=u'', indentation_increment=u'')