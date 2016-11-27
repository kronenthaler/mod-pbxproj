from pbxproj import XcodeProject
from pbxproj.pbxextensions.ProjectFiles import TreeType

# def main():
#     import argparse
#     import os
#
#     parser = argparse.ArgumentParser("Modify an XCode project file using a single command at a time.")
#     parser.add_argument('project', help="Project path")
#     parser.add_argument('-t', '--target', help="Target to modify", default=None)
#     parser.add_argument('-c', '--configuration', help="Configuration to modify", choices=['Debug', 'Release'], default=None)
#     parser.add_argument('-af', help='Add a flag value, in the format key=value', action='append')
#     parser.add_argument('-rf', help='Remove a flag value, in the format key=value', action='append')
#     parser.add_argument('-b', '--backup', help='Create a temporary backup before modify', action='store_true')
#     args = parser.parse_args()
#
#     print args
#
#     # open the project file
#     if os.path.isdir(args.project):
#         args.project += "/project.pbxproj"
#
#     if not os.path.isfile(args.project):
#         raise Exception("Project File not found")
#
#     project = XcodeProject.load(args.project)
#     backup_file = None
#     if args.backup :
#         backup_file = project.backup()
#
#     # apply the commands
#     # add flags
#     if args.af:
#         pairs = {}
#         for flag in args.af:
#             tokens = flag.split("=")
#             project.add_flags(tokens[0], tokens[1],target_name=args.target, configuration_name=args.configuration)
#
#     # remove flags
#     if args.rf:
#         pairs = {}
#         for flag in args.rf:
#             tokens = flag.split("=")
#             project.remove_flags(tokens[0], tokens[1], target_name=args.target, configuration_name=args.configuration)
#
#     # save the file
#     project.save()
#
#     # remove backup if everything was ok.
#     if args.backup:
#         os.remove(backup_file)

def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(u'Modify Xcode project executing commands')
    # parser.add_argument(u'project', help="Project path")
    # parser.add_argument(u'-t', u'--target', help="Target to modify", default=None)
    # parser.add_argument(u'-c', u'--configuration', help="Configuration to modify", choices=[u'Debug', u'Release'],
    #                     default=None)

    subcommands = parser.add_subparsers()
    add_command(subcommands)
    remove_command(subcommands)

    #parser.print_help()
    # parse and do the things
    args = parser.parse_args()
    print args


    # pbxproj add file
    # pbxproj add flag
    # pbxproj remove file
    # pbxproj remove flag


def add_command(command_parser):
    add_parser = command_parser.add_parser(u'add', help=u'Add objects to the project')
    subcommands = add_parser.add_subparsers()

    # add file parameters
    file_parser = subcommands.add_parser(u'file', help=u'Add files to the project')
    standard_parameters(file_parser)
    file_parser.add_argument(u'path', help=u'file path to be added to the project')
    file_parser.add_argument(u'--tree', choices=TreeType.options(), default=TreeType.SOURCE_ROOT,
                             help=u'tree relative to the origin of the file to be added.')
    file_parser.add_argument(u'--weak', u'-w', action=u'store_true', help=u'link framework weakly.')
    file_parser.add_argument(u'--embed', u'-e', action=u'store_true', default=True,
                             help=u'embed framework on the application')
    file_parser.add_argument(u'--sign-on-copy', u'-csoc', action=u'store_true',
                             help=u'code sign frameworks when copied to the application.')
    file_parser.add_argument(u'--ignore-unknown-types', u'-i', action=u'store_true',
                             help=u'ignore unknown types and add the file regardless.')
    file_parser.add_argument(u'--create-build-files', u'-C', action=u'store_true', default=True,
                             help=u'when adding a file, create any associated build file section required.')

    # flags options
    flag_parser = subcommands.add_parser(u'flag', help=u'Add flags to the project')
    standard_parameters(flag_parser)

    folder_parser = subcommands.add_parser(u'folder', help=u'Add folders to the project')
    standard_parameters(folder_parser)


def remove_command(command_parser):
    remove_parser = command_parser.add_parser(u'remove', help=u'Remove objects from the project')
    subcommands = remove_parser.add_subparsers()
    remove_file_parser = subcommands.add_parser(u'file', help=u'Remove files from the project')
    remove_flag_parser = subcommands.add_parser(u'flag', help=u'Remove flags from the project')
    remove_folder_parser = subcommands.add_parser(u'folder', help=u'Remove folders from the project')


def standard_parameters(parser):
    parser.add_argument(u'project', help="project path")
    parser.add_argument(u'-t', u'--target', default=None, help="target to modify, if not specified affects all targets.")
    parser.add_argument(u'-c', u'--configuration', choices=[u'Debug', u'Release'], default=None,
                        help="configuration to modify, if not specified affects all configurations.")
    parser.add_argument(u'-b', u'--backup', action=u'store_true', default=True,
                        help=u'create a temporary backup before modify.')

if __name__ == "__main__":
    main()
