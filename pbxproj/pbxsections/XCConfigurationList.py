from pbxproj import PBXGenericObject


class XCConfigurationList(PBXGenericObject):
    def _get_comment(self):
        info = self._get_section()
        return f'Build configuration list for {info[0]} "{info[1]}"'

    def _get_section(self):
        objects = self.get_parent()
        target = self.get_id()

        for obj in objects.get_objects_in_section('PBXNativeTarget', 'PBXAggregateTarget'):
            if target in obj.buildConfigurationList:
                return obj.isa, obj.name

        for obj in objects.get_objects_in_section('PBXProject'):
            if target in obj.buildConfigurationList:
                if hasattr(objects[obj.targets[0]], 'name'):
                    return obj.isa, objects[obj.targets[0]].name
                return obj.isa, objects[obj.targets[0]].productName

        return '', ''
