import unittest

from pbxproj.PBXObjects import objects


class PBXFileSystemSynchronizedBuildFileExceptionSetTests(unittest.TestCase):
    def testCommentsArePreservedInReferences(self):
        obj = {
            "AAAAAAAAAAAAAAAAAAAAAAAA": {
                "isa": "PBXFileSystemSynchronizedBuildFileExceptionSet",
                "membershipExceptions": [
                    "Sample.swift"
                ],
                "target": "BBBBBBBBBBBBBBBBBBBBBBBB"
            },
            "BBBBBBBBBBBBBBBBBBBBBBBB": {
                "isa": "PBXNativeTarget",
                "name": "Tests",
                "buildConfigurationList": "CCCCCCCCCCCCCCCCCCCCCCCC",
                "buildPhases": []
            },
            "CCCCCCCCCCCCCCCCCCCCCCCC": {
                "isa": "XCConfigurationList",
                "buildConfigurations": []
            },
            "DDDDDDDDDDDDDDDDDDDDDDDD": {
                "isa": "PBXFileSystemSynchronizedRootGroup",
                "exceptions": ["AAAAAAAAAAAAAAAAAAAAAAAA"],
                "explicitFileTypes": {},
                "explicitFolders": [],
                "path": "QuickAccept",
                "sourceTree": "<group>"
            }
        }

        dobj = objects(None).parse(obj)
        printed = dobj._print_object()

        assert "AAAAAAAAAAAAAAAAAAAAAAAA /* PBXFileSystemSynchronizedBuildFileExceptionSet */ =" in printed
        assert "exceptions = (AAAAAAAAAAAAAAAAAAAAAAAA /* PBXFileSystemSynchronizedBuildFileExceptionSet */, );" in printed
