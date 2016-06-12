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
        target = ''
        for key in objects.keys():
            if objects[key] == self:
                target = key
                break

        # TODO: ask object for the specific sections!
        for key in objects.keys():
            obj = objects[key]
            if isinstance(obj, PBXSourcesBuildPhase) or \
               isinstance(obj, PBXResourcesBuildPhase) or \
               isinstance(obj, PBXFrameworksBuildPhase):
                if target in obj.files:
                    return obj._get_comment()
