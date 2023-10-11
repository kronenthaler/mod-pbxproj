import unittest

from pbxproj import PBXContainerItemProxy


class PBXContainerItemProxyTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXContainerItemProxy()
        assert obj._get_comment() == u'PBXContainerItemProxy'
