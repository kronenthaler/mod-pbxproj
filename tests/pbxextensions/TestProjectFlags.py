import unittest
from pbxproj.XcodeProject import *


class ProjectFlagsTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                '0': {'isa': 'PBXProject'},
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3',
                      'buildPhases': ['compile']},
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': ['compile']},
                '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'buildSettings': {'base': 'a'}},
                '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
            },
            'rootObject': '0'
        }

    def testInit(self):
        with self.assertRaisesRegex(EnvironmentError, '^This class cannot be instantiated directly'):
            ProjectFlags()

    def testAddFlags(self):
        project = XcodeProject(self.obj)
        project.add_flags('flag', '-flag')

        self.assertEqual(project.objects['5'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['6'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['7'].buildSettings.flag, '-flag')
        self.assertEqual(project.objects['8'].buildSettings.flag, '-flag')

    def testRemoveFlags(self):
        project = XcodeProject(self.obj)
        project.remove_flags('base', 'a')

        self.assertIsNone(project.objects['5'].buildSettings['base'])

    def testAddOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')

        self.assertEqual(project.objects['5'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_CFLAGS, '-ObjC')

    def testAddOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')

        self.assertEqual(project.objects['5'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_LDFLAGS, '-ObjC')

    def testRemoveOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')
        self.assertEqual(project.objects['5'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_CFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_CFLAGS, '-ObjC')

        project.remove_other_cflags('-ObjC')

        self.assertIsNone(project.objects['5'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['6'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['7'].buildSettings['OTHER_CFLAGS'])
        self.assertIsNone(project.objects['8'].buildSettings['OTHER_CFLAGS'])

    def testRemoveOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')
        self.assertEqual(project.objects['5'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['6'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['7'].buildSettings.OTHER_LDFLAGS, '-ObjC')
        self.assertEqual(project.objects['8'].buildSettings.OTHER_LDFLAGS, '-ObjC')

        project.remove_other_ldflags('-ObjC')

        self.assertIsNone(project.objects['5'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['6'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['7'].buildSettings['OTHER_LDFLAGS'])
        self.assertIsNone(project.objects['8'].buildSettings['OTHER_LDFLAGS'])

    def testAddHeaderSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_header_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')

    def testAddLibrarySearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_library_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')

    def testAddFrameworkSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_framework_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')

    def testRemoveHeaderSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_header_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.HEADER_SEARCH_PATHS, 'path/to/search/**')

        project.remove_header_search_paths('path/to/search/**')
        self.assertIsNone(project.objects['5'].buildSettings['HEADER_SEARCH_PATHS'])
        self.assertIsNone(project.objects['6'].buildSettings['HEADER_SEARCH_PATHS'])
        self.assertIsNone(project.objects['7'].buildSettings['HEADER_SEARCH_PATHS'])
        self.assertIsNone(project.objects['8'].buildSettings['HEADER_SEARCH_PATHS'])

    def testRemoveLibrarySearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_library_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS, 'path/to/search/**')

        project.remove_library_search_paths('path/to/search/**')
        self.assertIsNone(project.objects['5'].buildSettings['LIBRARY_SEARCH_PATHS'])
        self.assertIsNone(project.objects['6'].buildSettings['LIBRARY_SEARCH_PATHS'])
        self.assertIsNone(project.objects['7'].buildSettings['LIBRARY_SEARCH_PATHS'])
        self.assertIsNone(project.objects['8'].buildSettings['LIBRARY_SEARCH_PATHS'])

    def testRemoveFrameworkSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_framework_search_paths('path/to/search')

        self.assertEqual(project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')
        self.assertEqual(project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS, 'path/to/search/**')

        project.remove_framework_search_paths('path/to/search/**')
        self.assertIsNone(project.objects['5'].buildSettings['FRAMEWORK_SEARCH_PATHS'])
        self.assertIsNone(project.objects['6'].buildSettings['FRAMEWORK_SEARCH_PATHS'])
        self.assertIsNone(project.objects['7'].buildSettings['FRAMEWORK_SEARCH_PATHS'])
        self.assertIsNone(project.objects['8'].buildSettings['FRAMEWORK_SEARCH_PATHS'])

    def testAddRunScriptBeforeCompile(self):
        project = XcodeProject(self.obj)
        project.add_run_script(u'ls -la', insert_before_compile=True)

        self.assertEqual(project.objects[project.objects['1'].buildPhases[0]].shellScript, u'ls -la')
        self.assertEqual(project.objects[project.objects['2'].buildPhases[0]].shellScript, u'ls -la')

    def testAddRunScriptAfterCompile(self):
        project = XcodeProject(self.obj)
        project.add_run_script(u'ls -la')

        self.assertEqual(project.objects[project.objects['1'].buildPhases[1]].shellScript, u'ls -la')
        self.assertEqual(project.objects[project.objects['2'].buildPhases[1]].shellScript, u'ls -la')

    def testRemoveRunScript(self):
        project = XcodeProject(self.obj)
        project.add_run_script(u'ls -la', insert_before_compile=True)

        self.assertEqual(project.objects[project.objects['1'].buildPhases[0]].shellScript, u'ls -la')
        self.assertEqual(project.objects[project.objects['2'].buildPhases[0]].shellScript, u'ls -la')

        project.remove_run_script(u'ls -la')
        self.assertEqual(project.objects['1'].buildPhases[0], u'compile')
        self.assertEqual(project.objects['2'].buildPhases[0], u'compile')

    def testRemoveRunScriptNotFound(self):
        project = XcodeProject(self.obj)
        project.add_run_script(u'ls -la', insert_before_compile=True)

        self.assertEqual(project.objects[project.objects['1'].buildPhases[0]].shellScript, u'ls -la')
        self.assertEqual(project.objects[project.objects['2'].buildPhases[0]].shellScript, u'ls -la')

        project.remove_run_script(u'ls')
        self.assertEqual(project.objects[project.objects['1'].buildPhases[0]].shellScript, u'ls -la')
        self.assertEqual(project.objects[project.objects['2'].buildPhases[0]].shellScript, u'ls -la')

    def testAddCodeSignAllTargetAllConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name')

        self.assertEqual(project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle, PBXProvioningTypes.MANUAL)
        self.assertEqual(project.objects['0'].attributes.TargetAttributes[u'2'].ProvisioningStyle,
                         PBXProvioningTypes.MANUAL)

        self.assertEqual(project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')
        self.assertEqual(project.objects['6'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')
        self.assertEqual(project.objects['7'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')
        self.assertEqual(project.objects['8'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')

        self.assertEqual(project.objects['5'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')
        self.assertEqual(project.objects['6'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')
        self.assertEqual(project.objects['7'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')
        self.assertEqual(project.objects['8'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')

        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')
        self.assertEqual(project.objects['6'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')
        self.assertEqual(project.objects['7'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')
        self.assertEqual(project.objects['8'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')

        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')
        self.assertEqual(project.objects['6'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')
        self.assertEqual(project.objects['7'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')
        self.assertEqual(project.objects['8'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')

    def testAddCodeSignOneTargetAllConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name', target_name='app')

        self.assertEqual(project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle,
                         PBXProvioningTypes.MANUAL)
        self.assertIsNone(project.objects['0'].attributes.TargetAttributes[u'2'])

        self.assertIsNone(project.objects['7']['buildSettings'])
        self.assertIsNone(project.objects['8']['buildSettings'])

        self.assertEqual(project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')
        self.assertEqual(project.objects['6'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')

        self.assertEqual(project.objects['5'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')
        self.assertEqual(project.objects['6'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')


        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')
        self.assertEqual(project.objects['6'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')

        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')
        self.assertEqual(project.objects['6'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')

    def testAddCodeSignAllTargetOneConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name', configuration_name='Release')

        self.assertEqual(project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle, PBXProvioningTypes.MANUAL)
        self.assertEqual(project.objects['0'].attributes.TargetAttributes[u'2'].ProvisioningStyle,
                         PBXProvioningTypes.MANUAL)

        self.assertIsNone(project.objects['6']['buildSettings'])
        self.assertIsNone(project.objects['8']['buildSettings'])
        self.assertEqual(project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')
        self.assertEqual(project.objects['7'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'], 'iPhone Distribution')

        self.assertEqual(project.objects['5'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')
        self.assertEqual(project.objects['7'].buildSettings['DEVELOPMENT_TEAM'], 'MYTEAM')

        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')
        self.assertEqual(project.objects['7'].buildSettings['PROVISIONING_PROFILE'], '0x0x0x0x0')

        self.assertEqual(project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')
        self.assertEqual(project.objects['7'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'], 'Provisioning name')

