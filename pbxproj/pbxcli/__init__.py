import os
from pbxproj.XcodeProject import XcodeProject


def open_project(args):
    if os.path.isdir(args[u'<project>']):
        args[u'<project>'] += "/project.pbxproj"

    if not os.path.isfile(args[u'<project>']):
        raise Exception("Project file not found")

    return XcodeProject.load(args[u'<project>'])


def backup_project(project, args):
    if args[u'--backup']:
        return project.backup()
    return None


def resolve_backup(project, backup_file, args):
    project.save()
    # remove backup if everything was ok.
    if args[u'--backup'] and backup_file:
        os.remove(backup_file)


def command_parser(command):
    def parser(args):
        try:
            project = open_project(args)
            backup_file = backup_project(project, args)
            print command(project, args)
            resolve_backup(project, backup_file, args)
        except Exception as ex:
            print ex.message
            exit(1)
    return parser
