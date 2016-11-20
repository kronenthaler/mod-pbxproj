from pbxproj import PBXGenericObject


class PBXProvioningTypes:
    MANUAL=u'Manual'
    AUTOMATIC=u'Automatic'


class PBXProject(PBXGenericObject):
    def _get_comment(self):
        return u'Project object'

    def set_provisioning_style(self, provisioning_type, target):
        if u'attributes' not in self:
            self[u'attributes'] = PBXGenericObject()

        if u'TargetAttributes' not in self.attributes:
            self.attributes[u'TargetAttributes'] = PBXGenericObject()

        if target.get_id() not in self.attributes.TargetAttributes:
            self.attributes.TargetAttributes[target.get_id()] = PBXGenericObject()

        self.attributes.TargetAttributes[target.get_id()][u'ProvisioningStyle'] = provisioning_type
