import unittest
from pbxproj.pbxsections.PBXProject import *


class PBXProjectTest(unittest.TestCase):
    def testGetComment(self):
        obj = PBXProject()
        self.assertEqual(obj._get_comment(), u'Project object')
