import unittest

from pbxproj import PBXContainerItemProxy


class PBXContainerItemProxyTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXContainerItemProxy()
        self.assertEqual(obj._get_comment(), u'PBXContainerItemProxy')
