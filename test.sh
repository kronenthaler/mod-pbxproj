#!/usr/bin/python
from mod_pbxproj import XcodeProject
import sys
import os

if __name__ == '__main__':
	#copy the base part of the prime31 file
	proj = XcodeProject.LoadFromXML('project.xml')
	
	proj.add_run_script(target='Distributable')