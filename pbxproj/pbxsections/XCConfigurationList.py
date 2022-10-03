from pbxproj import PBXGenericObject


class XCConfigurationList(PBXGenericObject):
    def _get_comment(self):
        info = self._get_section()
        return f'Build configuration list for {info[0]} "{info[1]}"'

    def _get_section(self):
        objects = self.get_parent()
        target_id = self.get_id()

        for obj in objects.get_objects_in_section('PBXNativeTarget', 'PBXLegacyTarget', 'PBXAggregateTarget'):
            if target_id in obj.buildConfigurationList:
                return obj.isa, obj.name

        projects = filter(lambda o: target_id in o.buildConfigurationList, objects.get_objects_in_section('PBXProject'))
        project = projects.__next__()
        target = objects[project.targets[0]]
        name = target.name if hasattr(target, 'name') else target.productName
        return project.isa, name
