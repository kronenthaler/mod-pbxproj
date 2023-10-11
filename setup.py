#!/usr/bin/env python
from setuptools import setup, find_packages


try:
    long_description = open("readme.rst").read()
except IOError:
    long_description = ""


def find_version(*file_paths):
    def read(*parts):
        import codecs
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(here, *parts), 'r') as fp:
            return fp.read()

    import re
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='pbxproj',
      author='Ignacio Calderon',
      description='XCode Project manipulation library for Python',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      entry_points={
        "console_scripts": [
            'pbxproj = pbxproj.__main__:main',
            'pbxproj-file = pbxproj.pbxcli.pbxproj_file:main',
            'pbxproj-flag = pbxproj.pbxcli.pbxproj_flag:main',
            'pbxproj-folder = pbxproj.pbxcli.pbxproj_folder:main'
        ]
      },
      url="http://github.com/kronenthaler/mod-pbxproj",
      version=find_version("pbxproj", "__init__.py"),
      license='MIT License',
      install_requires=['openstep_parser>=1.5.1', 'docopt'],
      python_requires='>=3.8',
      packages=find_packages(exclude=['tests']))
