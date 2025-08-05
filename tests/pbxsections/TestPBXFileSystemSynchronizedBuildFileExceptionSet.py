import unittest

from pbxproj.pbxsections.PBXFileSystemSynchronizedBuildFileExceptionSet import PBXFileSystemSynchronizedBuildFileExceptionSet


class PBXFileSystemSynchronizedBuildFileExceptionSetTests(unittest.TestCase):
    """
    Test suite for PBXFileSystemSynchronizedBuildFileExceptionSet class.
    
    PBXFileSystemSynchronizedBuildFileExceptionSet is a type of group in Xcode projects that's 
    synchronized with the file system. These tests verify the creation behavior 
    and special string representation formatting that's required for compatibility
    with Xcode project format.
    """
        
    def testPrintObject(self):
        """
        Tests the _print_object method of PBXFileSystemSynchronizedBuildFileExceptionSet.
        Verifies that the object is printed in a single line format (no newlines)
        with correctly formatted attributes, overriding the parent class formatting.
        This special formatting is important for compatibility with Xcode project format.
        """
        obj = {
            '_id': 'test_id',
            'isa': 'PBXFileSystemSynchronizedBuildFileExceptionSet',
            'membershipExceptions': ['Foo.swift', 'Bar.swift'],
            'target': "test_target_id /* FooTests */",
        }
        dobj = PBXFileSystemSynchronizedBuildFileExceptionSet().parse(obj)
        
        # Test that _print_object method overrides the parent's formatting
        result = dobj._print_object()
        
        self.assertIn('isa = PBXFileSystemSynchronizedBuildFileExceptionSet;', result)
        self.assertIn('Foo.swift', result)
        self.assertIn('Bar.swift', result)
        self.assertIn("test_target_id /* FooTests */", result)
