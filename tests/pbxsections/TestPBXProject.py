import unittest
from pbxproj.pbxsections.PBXProject import *


class PBXProjectTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXProject()
        self.assertEqual(obj._get_comment(), u'Project object')

    def testSetProvisioningTypeManual(self):
        obj = PBXProject()
        target = PBXGenericObject().parse({'_id': '1'})

        self.assertIsNone(obj[u'attributes'])

        obj.set_provisioning_style(PBXProvioningTypes.MANUAL, target)

        self.assertEqual(obj.attributes.TargetAttributes[u'1'].ProvisioningStyle, PBXProvioningTypes.MANUAL)

    def testSetProvisioningTypeAutomatic(self):
        obj = PBXProject()
        target = PBXGenericObject().parse({'_id': '1'})

        self.assertIsNone(obj[u'attributes'])

        obj.set_provisioning_style(PBXProvioningTypes.AUTOMATIC, target)

        self.assertEqual(obj.attributes.TargetAttributes[u'1'].ProvisioningStyle, PBXProvioningTypes.AUTOMATIC)

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

        self.assertEqual(obj.projectReferences.__len__(), 2)
        self.assertEqual(obj.projectReferences[0].ProductGroup, 'E248929D1CE31272000CB2D7')
        self.assertEqual(obj.projectReferences[0].ProjectRef, 'E248929C1CE31272000CB2D7')
        self.assertEqual(obj.projectReferences[1].ProductGroup, '15A8A4041834BDA200142BE0')
        self.assertEqual(obj.projectReferences[1].ProjectRef, '15A8A4031834BDA200142BE0')
