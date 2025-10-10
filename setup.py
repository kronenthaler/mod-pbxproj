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
      url="http://github.com/kronenthaler/mod-pbxproj",
      version=find_version("pbxproj", "__init__.py"),
      packages=find_packages(exclude=['tests']))
