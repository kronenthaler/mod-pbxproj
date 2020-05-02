import os
from pbxproj.XcodeProject import XcodeProject


def open_project(args):
    if os.path.isdir(args['<project>']):
        args['<project>'] += '/project.pbxproj'

    if not os.path.isfile(args['<project>']):
        raise Exception('Project file not found')

    return XcodeProject.load(args['<project>'])


def backup_project(project, args):
    if args['--backup']:
        return project.backup()
    return None


def resolve_backup(project, backup_file, args):
    # remove backup if everything was ok.
    if args['--backup'] and backup_file:
        os.remove(backup_file)


def command_parser(command, auto_save=True):
    def parser(args):
        try:
            project = open_project(args)
            backup_file = backup_project(project, args)
            print((command(project, args)))
            if auto_save:
                project.save()
            resolve_backup(project, backup_file, args)
        except Exception as ex:
            print(f'{ex}')
            exit(1)
    return parser
