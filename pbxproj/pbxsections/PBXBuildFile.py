from pbxproj import PBXGenericObject
from pbxproj.pbxsections.PBXSourcesBuildPhase import *
from pbxproj.pbxsections.PBXResourcesBuildPhase import *
from pbxproj.pbxsections.PBXFrameworksBuildPhase import *


class PBXBuildFile(PBXGenericObject):
    def _print_object(self, indentation_depth="", entry_separator='\n', object_start='\n', indentation_increment='\t'):
        return super(type(self), self)._print_object("", entry_separator=' ', object_start='', indentation_increment='')

    def _get_comment(self):
        return "{0} in {1}".format(self.fileRef._get_comment(), self._get_section())

    def _get_section(self):
        objects = self._parent
        target = objects.indexOf(self)

        for (key, obj) in objects.get_objects_in_section('PBXSourcesBuildPhase') + \
                          objects.get_objects_in_section('PBXResourcesBuildPhase') + \
                          objects.get_objects_in_section('PBXCopyFilesBuildPhase') + \
                          objects.get_objects_in_section('PBXFrameworksBuildPhase'):
            if target in obj.files:
                return obj._get_comment()
