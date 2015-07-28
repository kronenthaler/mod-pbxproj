from setuptools import setup, find_packages


setup(name='mod_pbxproj',
    author='Ignacio Calderon',
    description='XCode Project Generator for Python',
    url="http://github.com/kronenthaler/mod-pbxproj",
    version='1.3',
    license='BSD License',
    install_requires = ['openstep_parser'],
    packages=find_packages(exclude=['tests']))
