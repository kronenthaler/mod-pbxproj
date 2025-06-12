import unittest

from pbxproj.pbxsections.PBXFileSystemSynchronizedRootGroup import PBXFileSystemSynchronizedRootGroup


class PBXFileSystemSynchronizedRootGroupTests(unittest.TestCase):
    """
    Test suite for PBXFileSystemSynchronizedRootGroup class.
    
    PBXFileSystemSynchronizedRootGroup is a type of group in Xcode projects that's 
    synchronized with the file system. These tests verify the creation behavior 
    and special string representation formatting that's required for compatibility
    with Xcode project format.
    """
    def testCreate(self):
        """
        Tests the create method of PBXFileSystemSynchronizedRootGroup with 
        explicit file types, folders, path, and custom source tree parameter.
        Verifies that all attributes are correctly set in the created object.
        """
        explicit_file_types = ['file1', 'file2']
        explicit_folders = ['folder1', 'folder2']
        path = 'some/path'
        tree = 'SOURCE_ROOT'
        
        result = PBXFileSystemSynchronizedRootGroup.create(explicit_file_types, explicit_folders, path, tree)
        
        self.assertEqual(result.explicitFileTypes, explicit_file_types)
        self.assertEqual(result.explicitFolders, explicit_folders)
        self.assertEqual(result.path, path)
        self.assertEqual(result.sourceTree, tree)
        self.assertEqual(result.isa, 'PBXFileSystemSynchronizedRootGroup')
        self.assertIsNotNone(result._id)
    
    def testCreateWithDefaultTree(self):
        """
        Tests the create method of PBXFileSystemSynchronizedRootGroup with default tree parameter.
        Verifies that when no source tree is specified, it defaults to 'SOURCE_ROOT'.
        """
        explicit_file_types = ['file1', 'file2']
        explicit_folders = ['folder1', 'folder2']
        path = 'some/path'
        
        result = PBXFileSystemSynchronizedRootGroup.create(explicit_file_types, explicit_folders, path)
        
        self.assertEqual(result.sourceTree, 'SOURCE_ROOT')
        
    def testPrintObject(self):
        """
        Tests the _print_object method of PBXFileSystemSynchronizedRootGroup.
        Verifies that the object is printed in a single line format (no newlines)
        with correctly formatted attributes, overriding the parent class formatting.
        This special formatting is important for compatibility with Xcode project format.
        """
        obj = {
            '_id': 'test_id',
            'isa': 'PBXFileSystemSynchronizedRootGroup',
            'explicitFileTypes': ['file1', 'file2'],
            'explicitFolders': ['folder1', 'folder2'],
            'path': 'some/path',
            'sourceTree': 'SOURCE_ROOT'
        }
        dobj = PBXFileSystemSynchronizedRootGroup().parse(obj)
        
        # Test that _print_object method overrides the parent's formatting
        result = dobj._print_object()
        
        # Check that it's a single line representation (no newlines, compact format)
        self.assertNotIn('\n', result)
        self.assertIn('isa = PBXFileSystemSynchronizedRootGroup;', result)
        self.assertIn('explicitFileTypes = (', result)
        self.assertIn('file1', result)
        self.assertIn('file2', result)
        self.assertIn('explicitFolders = (', result)
        self.assertIn('folder1', result)
        self.assertIn('folder2', result)
        self.assertIn('path = some/path;', result)
        self.assertIn('sourceTree = SOURCE_ROOT;', result)
