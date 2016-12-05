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
from docopt import docopt

# Usage:
#     pbxproj file (--delete | -D) project path [--tree tree] [(--target | -t) target]
#     pbxproj file project path [--tree tree] [(--target | -t) target] [--weak | -w] [--no-embed | -E] [--sign-on-copy | -csoc] [--ignore-unknown-types | -i] [--no-create-build-files | -C]
#     pbxproj flag (--delete | -D) project flag value [(--target | -t) target] [(--configuration | -c) configuration]
#     pbxproj flag project flag value [(--target | -t) target] [(--configuration | -c) configuration]
#     pbxproj folder (--delete | -D) project path [(--target | -t) target]
#     pbxproj folder project path [(--target | -t) target] [(--exclude | -e) regex] [--recursive | -r] [--no-create-groups | -G] [--weak | -w] [--no-embed | -E] [--sign-on-copy | -s] [--ignore-unknown-types | -i] [--no-create-build-files | -C]

if __name__ == "__main__":
    args = docopt(__doc__, options_first=True, version=u'pbxproj version 2.0.0')
    print('global arguments:')
    print(args)
    print('command arguments:')

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'file':
        import pbxproj.pbxcli.pbxproj_file as pbxproj_file
        command_parser(pbxproj_file.main)(docopt(pbxproj_file.__doc__, argv=argv))
    elif args['<command>'] == 'flag':
        pass
    elif args['<command>'] == 'folder':
        pass
