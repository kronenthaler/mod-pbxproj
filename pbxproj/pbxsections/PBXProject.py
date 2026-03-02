from pbxproj import PBXGenericObject, PBXList


class PBXProvisioningTypes:
    MANUAL = 'Manual'
    AUTOMATIC = 'Automatic'


class PBXProject(PBXGenericObject):
    def _get_comment(self):
        return 'Project object'

    def set_provisioning_style(self, provisioning_type, target):
        if 'attributes' not in self:
            self['attributes'] = PBXGenericObject()

        if 'TargetAttributes' not in self.attributes:
            self.attributes['TargetAttributes'] = PBXGenericObject()

        if target.get_id() not in self.attributes.TargetAttributes:
            self.attributes.TargetAttributes[target.get_id()] = PBXGenericObject()

        self.attributes.TargetAttributes[target.get_id()]['ProvisioningStyle'] = provisioning_type

    def add_known_asset_tags(self, tags):
        if not isinstance(tags, list):
            tags = [tags]

        if 'attributes' not in self:
            self['attributes'] = PBXGenericObject()

        if 'KnownAssetTags' not in self.attributes:
            self.attributes['KnownAssetTags'] = PBXList()

        for tag in tags:
            if tag not in self.attributes.KnownAssetTags:
                self.attributes.KnownAssetTags.append(tag)

    def remove_known_asset_tags(self, tags):
        if 'attributes' not in self or 'KnownAssetTags' not in self.attributes:
            return False

        if not isinstance(tags, list):
            tags = [tags]

        for tag in tags:
            if tag in self.attributes.KnownAssetTags:
                self.attributes.KnownAssetTags.remove(tag)

        if self.attributes.KnownAssetTags.__len__() == 0:
            del self.attributes['KnownAssetTags']

        if self.attributes.get_keys().__len__() == 0:
            del self['attributes']

        return True
