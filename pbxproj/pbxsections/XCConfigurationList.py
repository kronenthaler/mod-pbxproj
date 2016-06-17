from pbxproj import PBXGenericObject


class XCConfigurationList(PBXGenericObject):
    def _get_comment(self):
        info = self._get_section()
        return u'Build configuration list for {0} "{1}"'.format(*info)

    def _get_section(self):
        objects = self._parent
        target = objects.indexOf(self)

        for (key, obj) in objects.get_objects_in_section(u'PBXNativeTarget') + \
                          objects.get_objects_in_section(u'PBXAggregateTarget'):
            if target in obj.buildConfigurationList:
                return obj.isa, obj.name

        for (key, obj) in objects.get_objects_in_section(u'PBXProject'):
            if target in obj.buildConfigurationList:
                return obj.isa, objects[obj.targets[0]].productName

        return u'', u''
