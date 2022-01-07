import os
import shutil
import unittest

from pbxproj import XcodeProject


class XCodeProjectTest(unittest.TestCase):
    def setUp(self):
        self.obj = {
            'objects': {
                '0': {'isa': 'PBXGroup', 'children': ['group1'], 'sourceTree': "<group>"},
                '1': {'isa': 'PBXNativeTarget', 'name': 'app', 'buildConfigurationList': '3',
                      'buildPhases': ['compile1']},
                '2': {'isa': 'PBXAggregateTarget', 'name': 'report', 'buildConfigurationList': '4',
                      'buildPhases': ['compile']},
                '3': {'isa': 'XCConfigurationList', 'buildConfigurations': ['5', '6']},
                '4': {'isa': 'XCConfigurationList', 'buildConfigurations': ['7', '8']},
                '5': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'buildSettings': {'base': 'a'}},
                '6': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '6'},
                '7': {'isa': 'XCBuildConfiguration', 'name': 'Release', 'id': '7'},
                '8': {'isa': 'XCBuildConfiguration', 'name': 'Debug', 'id': '8'},
                # groups
                'group1': {'isa': 'PBXGroup', 'name': 'root', 'children': ['group2', 'group3']},
                'group2': {'isa': 'PBXGroup', 'name': 'app', 'children': ['file1', 'file2']},
                'group3': {'isa': 'PBXGroup', 'name': 'app', 'children': ['file3', 'group4', 'file4']},
                'group4': {'isa': 'PBXGroup', 'name': 'app', 'children': []},
                'file1': {'isa': 'PBXFileReference', 'name': 'file', 'path':'file', 'sourceTree': 'SOURCE_ROOT'},
                'file2': {'isa': 'PBXFileReference', 'name': 'file', 'path':'file', 'sourceTree': 'SOURCE_ROOT'},
                'file3': {'isa': 'PBXFileReference', 'name': 'file', 'path':'file', 'sourceTree': 'SDKROOT'},
                'file4': {'isa': 'PBXFileReference', 'name': 'file1', 'path': 'file1', 'sourceTree': 'SOURCE_ROOT'},
                'build_file1': {'isa': 'PBXBuildFile', 'fileRef': 'file1'},
                'build_file2': {'isa': 'PBXBuildFile', 'fileRef': 'file2'},
                'compile': {'isa': 'PBXGenericBuildPhase', 'files': ['build_file1']},
                'compile1': {'isa': 'PBXGenericBuildPhase', 'files': ['build_file2']}
            }
        }

        # create tmp directory for results
        if not os.path.exists("results"):
            os.mkdir("results")

    def tearDown(self):
        # remove tmp directory
        shutil.rmtree('results')

    def testSaveOnGivenPath(self):
        XcodeProject().save("results/sample")

        self.assertTrue(os.path.exists("results/sample"))

    def testSaveOnDefaultPath(self):
        XcodeProject({}, "results/default").save()

        self.assertTrue(os.path.exists("results/default"))

    def testBackup(self):
        project = XcodeProject({}, 'results/default')
        project.save('results/default')
        backup_name = project.backup()

        self.assertRegex(backup_name, r'_[0-9]{6}-[0-9]{6}\.backup')

    def testGetIds(self):
        project = XcodeProject({'objects':{'1':{'isa':'a'}, '2':{'isa':'a'}}})

        self.assertListEqual(project.get_ids(), ['1', '2'])

    def testGetBuildFilesForFile(self):
        project = XcodeProject(self.obj)

        build_files = project.get_build_files_for_file('file1')
        self.assertListEqual(build_files, [project.objects['build_file1']])

    def testGetTargetByNameExisting(self):
        project = XcodeProject(self.obj)

        target = project.get_target_by_name('app')
        self.assertEqual(target, project.objects['1'])

    def testGetTargetByNameNonExisting(self):
        project = XcodeProject(self.obj)

        target = project.get_target_by_name('non-existing')
        self.assertIsNone(target)

    def testGetBuildPhasesByName(self):
        project = XcodeProject(self.obj)

        build_phases = project.get_build_phases_by_name('PBXGenericBuildPhase')
        self.assertEqual(build_phases.__len__(), 2)

    def testGetBuildConfigurationsByTarget(self):
        project = XcodeProject(self.obj)

        build_configurations = project.get_build_configurations_by_target(
            'app')
        self.assertListEqual(build_configurations, ['Release', 'Debug'])

    def testGetBuildConfigurationsByTargetNotExistent(self):
        project = XcodeProject(self.obj)

        build_configurations = project.get_build_configurations_by_target(
            'appThatDoesNotExists')
        self.assertIsNone(build_configurations)

    def testConsistency(self):
        with open('samplescli/massive.pbxproj', 'r') as file:
            original = file.read()
            project = XcodeProject.load('samplescli/massive.pbxproj')
            saved = project.__repr__() + '\n'

            self.assertEqual(saved, original)

