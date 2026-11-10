import sys
import unittest
from io import StringIO

from pbxproj.__main__ import main


class PBXMainUnknownCommandTest(unittest.TestCase):
    def setUp(self):
        self.argv = sys.argv
        self.stderr = sys.stderr

    def tearDown(self):
        sys.argv = self.argv
        sys.stderr = self.stderr

    def testUnknownCommandExitsNonZero(self):
        sys.argv = ['pbxproj', 'boguscmd']
        sys.stderr = StringIO()
        with self.assertRaises(SystemExit) as ctx:
            main()
        self.assertNotEqual(ctx.exception.code, 0)
        self.assertIn('boguscmd', sys.stderr.getvalue())

    def testNoCommandExitsNonZero(self):
        sys.argv = ['pbxproj']
        sys.stderr = StringIO()
        with self.assertRaises(SystemExit) as ctx:
            main()
        self.assertNotEqual(ctx.exception.code, 0)
