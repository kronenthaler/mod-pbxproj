from pbxproj import PBXGenericObject


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
