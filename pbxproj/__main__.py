"""
usage:
    pbxproj [--version] [--help] <command> [<args> ...]

options:
    -v, --version       Shows version of pbxproj running
    -h, --help          This message

commands:
    show                Displays information about the project targets
    file                Manipulates files on a project
    flag                Manipulates compilation flags on the project
    folder              Manipulates folders or groups on a project

See pbxproj <command> --help, for more information about a specific command.
"""

from docopt import docopt

import pbxproj
from pbxproj.pbxcli import command_parser


def main():
    args = docopt(__doc__, options_first=True, version=f'{pbxproj.__version__}')
    cmd = args['<command>']
    argv = [cmd] + args['<args>']

    if cmd == 'file':
        import pbxproj.pbxcli.pbxproj_file as pbxproj_file
        command_parser(pbxproj_file.execute)(docopt(pbxproj_file.__doc__, argv=argv))
    elif cmd == 'flag':
        import pbxproj.pbxcli.pbxproj_flag as pbxproj_flag
        command_parser(pbxproj_flag.execute)(docopt(pbxproj_flag.__doc__, argv=argv))
    elif cmd == 'folder':
        import pbxproj.pbxcli.pbxproj_folder as pbxproj_folder
        command_parser(pbxproj_folder.execute)(docopt(pbxproj_folder.__doc__, argv=argv))
    elif cmd == 'show':
        import pbxproj.pbxcli.pbxproj_show as pbxproj_show
        command_parser(pbxproj_show.execute, auto_save=False)(docopt(pbxproj_show.__doc__, argv=argv))


if __name__ == '__main__':
    main()
