import unittest

from pbxproj import XcodeProject, PBXProvisioningTypes
from pbxproj.pbxextensions import ProjectFlags
import pytest

LS_LA_COMMAND = u'ls -la'
PATH_TO_SEARCH_PATTERN = 'path/to/search/**'


class ProjectFlagsTest(unittest.TestCase):

    def setUp(self):
        self.obj = {
            'objects': {
                '0': {'isa': 'PBXProject', 'buildConfigurationList': '4a'},
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3',
                      'buildPhases': ['compile']},
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': ['compile']},
                '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '4a': {'isa': 'XCConfigurationList', 'buildConfigurations': ['9', '10']},
                '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'buildSettings': {'base': 'a'}},
                '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                '9': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '9'},
                '10': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '10', 'buildSettings': {'base': 'x'}},
            },
            'rootObject': '0'
        }

    def testInit(self):
        with pytest.raises(EnvironmentError, match='^This class cannot be instantiated directly'):
            ProjectFlags()

    def testAddFlags(self):
        project = XcodeProject(self.obj)
        project.add_flags('flag', '-flag')

        assert project.objects['5'].buildSettings.flag == '-flag'
        assert project.objects['6'].buildSettings.flag == '-flag'
        assert project.objects['7'].buildSettings.flag == '-flag'
        assert project.objects['8'].buildSettings.flag == '-flag'

    def testAddProjectFlags(self):
        project = XcodeProject(self.obj)
        project.add_project_flags('flag', '-flag')

        assert project.objects['9'].buildSettings.flag == '-flag'
        assert project.objects['10'].buildSettings.flag == '-flag'

    def testRemoveFlags(self):
        project = XcodeProject(self.obj)
        project.remove_flags('base', 'a')

        assert project.objects['5'].buildSettings['base'] is None

    def testRemoveProjectFlags(self):
        project = XcodeProject(self.obj)
        project.remove_project_flags('base', 'x')

        assert project.objects['10'].buildSettings['base'] is None

    def testAddOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')

        assert project.objects['5'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['6'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['7'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['8'].buildSettings.OTHER_CFLAGS == '-ObjC'

    def testAddOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')

        assert project.objects['5'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['6'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['7'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['8'].buildSettings.OTHER_LDFLAGS == '-ObjC'

    def testRemoveOtherCFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_cflags('-ObjC')
        assert project.objects['5'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['6'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['7'].buildSettings.OTHER_CFLAGS == '-ObjC'
        assert project.objects['8'].buildSettings.OTHER_CFLAGS == '-ObjC'

        project.remove_other_cflags('-ObjC')

        assert project.objects['5'].buildSettings['OTHER_CFLAGS'] is None
        assert project.objects['6'].buildSettings['OTHER_CFLAGS'] is None
        assert project.objects['7'].buildSettings['OTHER_CFLAGS'] is None
        assert project.objects['8'].buildSettings['OTHER_CFLAGS'] is None

    def testRemoveOtherLDFlags(self):
        project = XcodeProject(self.obj)
        project.add_other_ldflags('-ObjC')
        assert project.objects['5'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['6'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['7'].buildSettings.OTHER_LDFLAGS == '-ObjC'
        assert project.objects['8'].buildSettings.OTHER_LDFLAGS == '-ObjC'

        project.remove_other_ldflags('-ObjC')

        assert project.objects['5'].buildSettings['OTHER_LDFLAGS'] is None
        assert project.objects['6'].buildSettings['OTHER_LDFLAGS'] is None
        assert project.objects['7'].buildSettings['OTHER_LDFLAGS'] is None
        assert project.objects['8'].buildSettings['OTHER_LDFLAGS'] is None

    def testAddHeaderSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_header_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

    def testAddLibrarySearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_library_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

    def testAddFrameworkSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_framework_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

    def testRemoveHeaderSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_header_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.HEADER_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

        project.remove_header_search_paths(PATH_TO_SEARCH_PATTERN)
        assert project.objects['5'].buildSettings['HEADER_SEARCH_PATHS'] is None
        assert project.objects['6'].buildSettings['HEADER_SEARCH_PATHS'] is None
        assert project.objects['7'].buildSettings['HEADER_SEARCH_PATHS'] is None
        assert project.objects['8'].buildSettings['HEADER_SEARCH_PATHS'] is None

    def testRemoveLibrarySearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_library_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.LIBRARY_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

        project.remove_library_search_paths(PATH_TO_SEARCH_PATTERN)
        assert project.objects['5'].buildSettings['LIBRARY_SEARCH_PATHS'] is None
        assert project.objects['6'].buildSettings['LIBRARY_SEARCH_PATHS'] is None
        assert project.objects['7'].buildSettings['LIBRARY_SEARCH_PATHS'] is None
        assert project.objects['8'].buildSettings['LIBRARY_SEARCH_PATHS'] is None

    def testRemoveFrameworkSearchPaths(self):
        project = XcodeProject(self.obj)
        project.add_framework_search_paths('path/to/search')

        assert project.objects['5'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['6'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['7'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN
        assert project.objects['8'].buildSettings.FRAMEWORK_SEARCH_PATHS == PATH_TO_SEARCH_PATTERN

        project.remove_framework_search_paths(PATH_TO_SEARCH_PATTERN)
        assert project.objects['5'].buildSettings['FRAMEWORK_SEARCH_PATHS'] is None
        assert project.objects['6'].buildSettings['FRAMEWORK_SEARCH_PATHS'] is None
        assert project.objects['7'].buildSettings['FRAMEWORK_SEARCH_PATHS'] is None
        assert project.objects['8'].buildSettings['FRAMEWORK_SEARCH_PATHS'] is None

    def testAddRunScriptBeforeCompile(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND, insert_before_compile=True)

        assert project.objects[project.objects['1'].buildPhases[0]].shellScript == LS_LA_COMMAND
        assert project.objects[project.objects['2'].buildPhases[0]].shellScript == LS_LA_COMMAND

    def testAddRunScriptAfterCompile(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND)

        assert project.objects[project.objects['1'].buildPhases[1]].shellScript == LS_LA_COMMAND
        assert project.objects[project.objects['2'].buildPhases[1]].shellScript == LS_LA_COMMAND

    def testAddRunScriptWithInputFiles(self):
        project = XcodeProject(self.obj)
        script = u'ls -la ${SCRIPT_INPUT_FILE_0} ${SCRIPT_INPUT_FILE_1} > ${SCRIPT_OUTPUT_FILE_0}'
        project.add_run_script(script, input_files=['a.txt', '/tmp/b.txt'], output_files=['../output.log'])

        assert project.objects[project.objects['1'].buildPhases[1]].shellScript == script
        assert project.objects[project.objects['1'].buildPhases[1]].inputPaths == ['a.txt', '/tmp/b.txt']
        assert project.objects[project.objects['1'].buildPhases[1]].outputPaths == ['../output.log']
        assert project.objects[project.objects['2'].buildPhases[1]].shellScript == script
        assert project.objects[project.objects['2'].buildPhases[1]].inputPaths == ['a.txt', '/tmp/b.txt']
        assert project.objects[project.objects['2'].buildPhases[1]].outputPaths == ['../output.log']

    def testRemoveRunScript(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND, insert_before_compile=True)

        assert project.objects[project.objects['1'].buildPhases[0]].shellScript == LS_LA_COMMAND
        assert project.objects[project.objects['2'].buildPhases[0]].shellScript == LS_LA_COMMAND

        project.remove_run_script(LS_LA_COMMAND)
        assert project.objects['1'].buildPhases[0] == u'compile'
        assert project.objects['2'].buildPhases[0] == u'compile'

    def testRemoveRunScriptNotFound(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND, insert_before_compile=True)

        assert project.objects[project.objects['1'].buildPhases[0]].shellScript == LS_LA_COMMAND
        assert project.objects[project.objects['2'].buildPhases[0]].shellScript == LS_LA_COMMAND

        project.remove_run_script(u'ls')
        assert project.objects[project.objects['1'].buildPhases[0]].shellScript == LS_LA_COMMAND
        assert project.objects[project.objects['2'].buildPhases[0]].shellScript == LS_LA_COMMAND

    def testAddRunScriptWithoutInstallBuild(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND, run_install_build=0)

        assert project.objects[project.objects['2'].buildPhases[1]].runOnlyForDeploymentPostprocessing == 0

    def testAddRunScriptWithInstallBuild(self):
        project = XcodeProject(self.obj)
        project.add_run_script(LS_LA_COMMAND, run_install_build=1)

        assert project.objects[project.objects['1'].buildPhases[1]].runOnlyForDeploymentPostprocessing == 1

    def testAddCodeSignAllTargetAllConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name')

        assert project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle == PBXProvisioningTypes.MANUAL
        assert project.objects['0'].attributes.TargetAttributes[u'2'].ProvisioningStyle == \
                         PBXProvisioningTypes.MANUAL

        assert project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'
        assert project.objects['6'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'
        assert project.objects['7'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'
        assert project.objects['8'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'

        assert project.objects['5'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'
        assert project.objects['6'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'
        assert project.objects['7'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'
        assert project.objects['8'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'

        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'
        assert project.objects['6'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'
        assert project.objects['7'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'
        assert project.objects['8'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'

        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
        assert project.objects['6'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
        assert project.objects['7'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
        assert project.objects['8'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'

    def testAddCodeSignOneTargetAllConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name', target_name='app')

        assert project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle == \
                         PBXProvisioningTypes.MANUAL
        assert project.objects['0'].attributes.TargetAttributes[u'2'] is None

        assert project.objects['7']['buildSettings'] is None
        assert project.objects['8']['buildSettings'] is None

        assert project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'
        assert project.objects['6'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'

        assert project.objects['5'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'
        assert project.objects['6'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'


        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'
        assert project.objects['6'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'

        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
        assert project.objects['6'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'

    def testAddCodeSignAllTargetOneConfigurations(self):
        project = XcodeProject(self.obj)

        project.add_code_sign('iPhone Distribution', 'MYTEAM', '0x0x0x0x0', 'Provisioning name', configuration_name='Release')

        assert project.objects['0'].attributes.TargetAttributes[u'1'].ProvisioningStyle == PBXProvisioningTypes.MANUAL
        assert project.objects['0'].attributes.TargetAttributes[u'2'].ProvisioningStyle == \
                         PBXProvisioningTypes.MANUAL

        assert project.objects['6']['buildSettings'] is None
        assert project.objects['8']['buildSettings'] is None
        assert project.objects['5'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'
        assert project.objects['7'].buildSettings['CODE_SIGN_IDENTITY[sdk=iphoneos*]'] == 'iPhone Distribution'

        assert project.objects['5'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'
        assert project.objects['7'].buildSettings['DEVELOPMENT_TEAM'] == 'MYTEAM'

        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'
        assert project.objects['7'].buildSettings['PROVISIONING_PROFILE'] == '0x0x0x0x0'

        assert project.objects['5'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
        assert project.objects['7'].buildSettings['PROVISIONING_PROFILE_SPECIFIER'] == 'Provisioning name'
