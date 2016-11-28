import argparse
from pbxproj.pbxcli import *


def main():
    parser = argparse.ArgumentParser(u'Modify Xcode project executing commands')
    subcommands = parser.add_subparsers()
    add_command(subcommands)
    remove_command(subcommands)

    # parse and do the things
    args = parser.parse_args()
    args.func(args)


def add_command(command_parser):
    add_parser = command_parser.add_parser(u'add', help=u'Add objects to the project')
    subcommands = add_parser.add_subparsers()

    # add file parameters
    PBXCLIFile.add(subcommands)

    # flags options
    #flag_parser = subcommands.add_parser(u'flag', help=u'Add flags to the project')
    #folder_parser = subcommands.add_parser(u'folder', help=u'Add folders to the project')


def remove_command(command_parser):
    remove_parser = command_parser.add_parser(u'remove', help=u'Remove objects from the project')
    subcommands = remove_parser.add_subparsers()
    remove_file_parser = subcommands.add_parser(u'file', help=u'Remove files from the project')
    remove_flag_parser = subcommands.add_parser(u'flag', help=u'Remove flags from the project')
    remove_folder_parser = subcommands.add_parser(u'folder', help=u'Remove folders from the project')


if __name__ == "__main__":
    main()
