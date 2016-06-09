from pbxproj import XcodeProject
import sys
import os


if __name__ == "__main__":
    stdout = sys.stdout
    files = os.listdir('../mod_pbxproj/tests/samples/')
    for file in files:
        stdout.write('parsing {0}\n'.format(file))
        stdout.flush()

        sys.stdout = open('../test-{0}'.format(file), 'w')
        obj = XcodeProject.load('../mod_pbxproj/tests/samples/{0}'.format(file), pure_python=True)
        print obj
        sys.stdout.close()