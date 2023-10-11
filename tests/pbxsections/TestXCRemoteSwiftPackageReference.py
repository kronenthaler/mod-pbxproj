import unittest
from pbxproj.pbxsections.XCRemoteSwiftPackageReference import *


class TestXCRemoteSwiftPackageReference(unittest.TestCase):
    def testGetComment(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', {})
        assert obj._get_comment() == 'XCRemoteSwiftPackageReference "some-package"'

    def testGetCommentWithoutGitExtension(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package.git', {})
        assert obj._get_comment() == 'XCRemoteSwiftPackageReference "some-package"'

    def testRequirementIsNotNone(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', {})
        assert obj['requirement'] is not None

    def testRequirementIsPopulated(self):
        obj = XCRemoteSwiftPackageReference.create('http://myrepo.com/some-package', { "kind": "branch" })
        assert obj['requirement']['kind'] == 'branch'
