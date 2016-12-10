"""
usage:
    pbxproj [--version] [--help] <command> [<args> ...]

options:
    -v, --version       Shows version of pbxproj running
    -h, --help          This message

commands:
    file                Manipulates files on a project
    flag                Manipulates compilation flags on the project
    folder              Manipulates folders or groups on a project

See pbxproj <command> --help, for more information about a specific command.
"""
from pbxproj.pbxcli import *
import pbxproj
from docopt import docopt


def main():
    args = docopt(__doc__, options_first=True, version=u'pbxproj version {0}'.format(pbxproj.__version__))
    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'file':
        import pbxproj.pbxcli.pbxproj_file as pbxproj_file
        command_parser(pbxproj_file.execute)(docopt(pbxproj_file.__doc__, argv=argv))
    elif args['<command>'] == 'flag':
        import pbxproj.pbxcli.pbxproj_flag as pbxproj_flag
        command_parser(pbxproj_flag.execute)(docopt(pbxproj_flag.__doc__, argv=argv))
    elif args['<command>'] == 'folder':
        import pbxproj.pbxcli.pbxproj_folder as pbxproj_folder
        command_parser(pbxproj_folder.execute)(docopt(pbxproj_folder.__doc__, argv=argv))


if __name__ == "__main__":
    main()
