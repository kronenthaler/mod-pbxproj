import unittest
import shutil
import sys
from pbxproj.pbxcli import *
import pbxproj.pbxcli.pbxproj_show as pbxproj_show

class PBXProjShowTest(unittest.TestCase):
    def setUp(self):
        # copy the project.pbxproj, into a file that can be used by the tests
        shutil.copyfile('samplescli/project.pbxproj', 'samplescli/test.pbxproj')

    def tearDown(self):
        os.remove('samplescli/test.pbxproj')
        sys.stdout = sys.__stdout__

    def testShowAllTargetsInfo(self):
        args = {
            u'<project>': u'samplescli/test.pbxproj',
            u'--target': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('testUITests:', result)
        self.assertIn('Product name: testUITests', result)
        self.assertIn('Configurations: Debug, Release', result)
        self.assertIn('Sources (PBXSourcesBuildPhase) file count: 1', result)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Configurations: Debug, Release', result)
        self.assertIn('Sources (PBXSourcesBuildPhase) file count: 2', result)

    def testShowTargetBasicInfo(self):
        args = {
            u'<project>': u'samplescli/test.pbxproj',
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertNotIn('testUITests:', result)
        self.assertNotIn('Product name: testUITests', result)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)

    def testShowTargetConfigurations(self):
        args = {
            u'<project>': u'samplescli/test.pbxproj',
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': True,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Configurations: Debug, Release\n', result)

    def testShowTargetSources(self):
        args = {
            u'<project>': u'samplescli/test.pbxproj',
            u'--target': u'test',
            u'--source-files': True,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Sources:', result)
        self.assertIn('AppDelegate.swift', result)
        self.assertIn('VīęwČøntröłler.swift', result)

    def testShowTargetResources(self):
        args = {
            u'<project>': u'samplescli/test.pbxproj',
            u'--target': u'test',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': True,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('test:', result)
        self.assertIn('Product name: test\n', result)
        self.assertIn('Resources:', result)
        self.assertIn('Assets.xcassets', result)
        self.assertIn('LaunchScreen.storyboard', result)
        self.assertIn('Main.storyboard', result)

    def testShowTargetHeaders(self):
        args = {
            u'<project>': u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': True,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Headers:', result)
        self.assertIn('doit.h', result)
        self.assertIn('helloworld.h', result)

    def testShowTargetFrameworks(self):
        args = {
            u'<project>': u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': True,
            u'--configurations': None,
            u'--build-phase-files': None
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Frameworks:', result)
        self.assertIn('AppKit.framework', result)

    def testShowTargetExplicitBuildPhase(self):
        args = {
            u'<project>': u'samplescli/dependency.xcodeproj/project.pbxproj',
            u'--target': u'helloworld',
            u'--source-files': None,
            u'--header-files': None,
            u'--resource-files': None,
            u'--framework-files': None,
            u'--configurations': None,
            u'--build-phase-files': u'PBXFrameworksBuildPhase'
        }
        project = open_project(args)
        result = pbxproj_show.execute(project, args)

        self.assertIn('helloworld:', result)
        self.assertIn('Product name: helloworld\n', result)
        self.assertIn('Frameworks:', result)
        self.assertIn('AppKit.framework', result)
