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


setup(name='mod_pbxproj',
      author='Ignacio Calderon',
      description='XCode Project manipulation library for Python',
      url="http://github.com/kronenthaler/mod-pbxproj",
      version='2.0.0',
      license='BSD License',
      install_requires=['openstep_parser'],
      packages=find_packages(exclude=['tests']),
      setup_requires=['nose', 'coverage'],
      cmdclass={'test': NoseTestCommand, 'coverage': NoseTestCoverage})
