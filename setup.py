#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# Inspired by the example at https://pytest.org/latest/goodpractises.html
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests', '-w', 'tests'])


class NoseTestCoverage(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests',
                            '--with-coverage',
                            '--cover-erase',
                            '--cover-branches',
                            '--cover-package=pbxproj',
                            '-w', 'tests'])


setup(name='pbxproj',
      author='Ignacio Calderon',
      description='XCode Project manipulation library for Python',
      entry_points={
        "console_scripts": [
            'pbxproj = pbxproj.__main__:main',
            'pbxproj-file = pbxproj.pbxcli.pbxproj_file:main',
            'pbxproj-flag = pbxproj.pbxcli.pbxproj_flag:main',
            'pbxproj-folder = pbxproj.pbxcli.pbxproj_folder:main'
        ]
      },
      url="http://github.com/kronenthaler/mod-pbxproj",
      version='2.0.0',
      license='MIT License',
      install_requires=['openstep_parser', 'docopt'],
      packages=find_packages(exclude=['tests']),
      setup_requires=['nose', 'coverage'],
      cmdclass={'test': NoseTestCommand, 'coverage': NoseTestCoverage})
