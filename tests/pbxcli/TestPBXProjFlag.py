import os
import shutil
import sys
import unittest

import pbxproj.pbxcli.pbxproj_flag as pbxproj_flag
from pbxproj.pbxcli import open_project, PROJECT_PLACEHOLDER
from tests.pbxcli import SAMPLE_PROJECT_PATH, BASE_PROJECT_PATH


class TestPBXProjFlag(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile(BASE_PROJECT_PATH, SAMPLE_PROJECT_PATH)

    def tearDown(self):
        os.remove(SAMPLE_PROJECT_PATH)
        sys.stdout = sys.__stdout__

    def testAddFlags(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            '--delete': False,
            '--target': None,
            '--configuration': None,
            '<flag_name>': ['MYFLAG', 'MYFLAG'],
            '<flag_value>': ['-ObjC', '-all'],
        }

        project = open_project(args)

        for configuration in project.objects.get_configurations_on_targets(args['--target'], args['--configuration']):
            self.assertTrue('MYFLAG' not in configuration.buildSettings)

        result = pbxproj_flag.execute(project, args)
        self.assertEqual(result, 'Flags added successfully.')

        for configuration in project.objects.get_configurations_on_targets(args['--target'], args['--configuration']):
            self.assertTrue('MYFLAG' in configuration.buildSettings)
            self.assertListEqual(configuration.buildSettings['MYFLAG'], ['-ObjC', '-all'])

    def testRemoveFlags(self):
        args = {
            PROJECT_PLACEHOLDER: SAMPLE_PROJECT_PATH,
            '--delete': True,
            '--target': None,
            '--configuration': None,
            '<flag_name>': ['MYFLAG', 'MYFLAG'],
            '<flag_value>': ['-ObjC', '-all'],
        }

        project = open_project(args)
        project.add_flags('MYFLAG', ['-ObjC', '-all'])

        result = pbxproj_flag.execute(project, args)
        self.assertEqual(result, 'Flags removed successfully.')

        for configuration in project.objects.get_configurations_on_targets(args['--target'], args['--configuration']):
            self.assertTrue('MYFLAG' not in configuration.buildSettings)