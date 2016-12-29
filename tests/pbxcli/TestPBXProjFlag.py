import unittest
import os
import sys
import shutil
from pbxproj.pbxcli import *
import pbxproj.pbxcli.pbxproj_flag as pbxproj_flag


class TestPBXProjFlag(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile('samplescli/project.pbxproj', 'samplescli/test.pbxproj')

    def tearDown(self):
        os.remove('samplescli/test.pbxproj')
        sys.stdout = sys.__stdout__

    def testAddFlags(self):
        args = {
            '<project>': 'samplescli/test.pbxproj',
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
            '<project>': 'samplescli/test.pbxproj',
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