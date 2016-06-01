from pbxproj import PBXGenericObject


class PBXBuildFile(PBXGenericObject):
    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        return super(type(self), self)._print_object("", entry_separator=' ', object_start='', indentation_increment='')