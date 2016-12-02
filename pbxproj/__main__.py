import argparse
from pbxproj.pbxcli import *


def main():
    parser = argparse.ArgumentParser(u'pbxproj', description=u'PBXProject (Xcode) manipulation command line.')
    subcommands = parser.add_subparsers()

    PBXCLIFile(subcommands)
    PBXCLIFlag(subcommands)
    PBXCLIFolder(subcommands)

    # parse and trigger the parser
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
