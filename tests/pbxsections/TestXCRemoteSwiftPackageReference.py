import unittest
from pbxproj.pbxsections.XCRemoteSwiftPackageReference import *


class TestXCRemoteSwiftPackageReference(unittest.TestCase):
    def testGetComment(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', {})
        self.assertEqual(obj._get_comment(), 'XCRemoteSwiftPackageReference "some-package"')

    def testGetCommentWithoutGitExtension(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package.git', {})
        self.assertEqual(obj._get_comment(), 'XCRemoteSwiftPackageReference "some-package"')

    def testRequirementIsNotNone(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', {})
        self.assertIsNotNone(obj['requirement'])

    def testRequirementIsPopulated(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', { "kind": "branch" })
        self.assertEqual(obj['requirement']['kind'], 'branch')
