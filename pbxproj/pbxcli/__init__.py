import os
import argparse
from pbxproj.XcodeProject import XcodeProject


def open_project(args):
    if os.path.isdir(args.project):
        args.project += "/project.pbxproj"

    if not os.path.isfile(args.project):
        raise Exception("Project file not found")

    return XcodeProject.load(args.project)


def backup_project(project, args):
    if args.backup:
        return project.backup()
    return None


def resolve_backup(project, backup_file, args):
    project.save()
    # remove backup if everything was ok.
    if args.backup and backup_file:
        os.remove(backup_file)


def command_parser(command):
    def parser(args):
        project = open_project(args)
        backup_file = backup_project(project, args)
        print command(project, args)
        resolve_backup(project, backup_file, args)
    return parser


def standard_parameters(parser):
    parser.add_argument(u'project', help="project path")
    parser.add_argument(u'-t', u'--target', default=None, help="target to modify, if not specified affects all targets.")
    # parser.add_argument(u'-c', u'--configuration', choices=[u'Debug', u'Release'], default=None,
    #                     help="configuration to modify, if not specified affects all configurations.")
    parser.add_argument(u'-b', u'--backup', action=u'store_true', default=True,
                        help=u'create a temporary backup before modify.')


# import class files after the definitions here so the classes can use this definitions
from pbxproj.pbxcli.PBXCLIFile import *
