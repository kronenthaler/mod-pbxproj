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
