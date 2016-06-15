from pbxproj import PBXGenericObject


class PBXBuildFile(PBXGenericObject):
    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        return super(type(self), self)._print_object("", entry_separator=' ', object_start='', indentation_increment='')

    def _get_comment(self):
        return "{0} in {1}".format(self.fileRef._get_comment(), self._get_section())

    def _get_section(self):
        objects = self._parent
        target = objects.indexOf(self)

        for section in objects._get_keys():
            for (key, obj) in objects.get_objects_in_section(section):
                if 'files' in obj and target in obj.files:
                    return obj._get_comment()
