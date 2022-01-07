import unittest

from pbxproj.PBXKey import PBXKey


class PBXKeyTest(unittest.TestCase):
    def testGetComment(self):
        key = PBXKey("123", None)
        key._get_comment = lambda: "comment"

        self.assertEqual(key.__repr__(), "123 /* comment */")
