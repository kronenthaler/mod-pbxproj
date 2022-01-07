import os

from pbxproj.XcodeProject import XcodeProject

PROJECT_PLACEHOLDER = '<project>'
PATH_PLACEHOLDER = '<path>'


def open_project(args):
    if os.path.isdir(args[PROJECT_PLACEHOLDER]):
        args[PROJECT_PLACEHOLDER] += '/project.pbxproj'

    if not os.path.isfile(args[PROJECT_PLACEHOLDER]):
        raise FileNotFoundError('Project file not found')

    return XcodeProject.load(args[PROJECT_PLACEHOLDER])


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
