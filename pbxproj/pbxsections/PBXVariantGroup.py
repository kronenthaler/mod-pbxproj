from pbxproj.pbxsections import PBXFileReference, PBXGroup


class PBXVariantGroup(PBXGroup):
    def add_child(self, child):
        # Note: PBXVariantGroup is typically used for Localizable.strings
        #       If other children type is needed e.g. PBXFileReference, edit this
        #       function.
        if not isinstance(child, PBXFileReference):
            return False

        self.children.append(child.get_id())
        return True
