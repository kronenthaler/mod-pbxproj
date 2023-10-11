import unittest

from pbxproj import PBXProject, PBXProvisioningTypes, PBXGenericObject


class PBXProjectTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXProject()
        assert obj._get_comment() == u'Project object'

    def testSetProvisioningTypeManual(self):
        obj = PBXProject()
        target = PBXGenericObject().parse({'_id': '1'})

        assert obj[u'attributes'] is None

        obj.set_provisioning_style(PBXProvisioningTypes.MANUAL, target)

        assert obj.attributes.TargetAttributes[u'1'].ProvisioningStyle == PBXProvisioningTypes.MANUAL

    def testSetProvisioningTypeAutomatic(self):
        obj = PBXProject()
        target = PBXGenericObject().parse({'_id': '1'})

        assert obj[u'attributes'] is None

        obj.set_provisioning_style(PBXProvisioningTypes.AUTOMATIC, target)

        assert obj.attributes.TargetAttributes[u'1'].ProvisioningStyle == PBXProvisioningTypes.AUTOMATIC

    def testRetainProjectReferences(self):
        obj = PBXProject().parse({'projectReferences': [
				{
					'ProductGroup': 'E248929D1CE31272000CB2D7',
					'ProjectRef': 'E248929C1CE31272000CB2D7'
				},
				{
					'ProductGroup': '15A8A4041834BDA200142BE0',
					'ProjectRef':'15A8A4031834BDA200142BE0'
				}
			]})

        assert obj.projectReferences.__len__() == 2
        assert obj.projectReferences[0].ProductGroup == 'E248929D1CE31272000CB2D7'
        assert obj.projectReferences[0].ProjectRef == 'E248929C1CE31272000CB2D7'
        assert obj.projectReferences[1].ProductGroup == '15A8A4041834BDA200142BE0'
        assert obj.projectReferences[1].ProjectRef == '15A8A4031834BDA200142BE0'
