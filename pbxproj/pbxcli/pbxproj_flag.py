"""
usage:
    pbxproj flag [options] <project> [--target <target>...] [--] (<flag_name> <flag_value>)...
    pbxproj flag [options] (--delete | -D) <project> [--] (<flag_name> <flag_value>)...

positional arguments:
    <project>                               Project path to the .xcodeproj folder.
    <flag_name>                             Flag name to be modified in the project's configuration(s).
    <flag_value>                            Flag value to be modified in the project's configuration(s).

generic options:
    --                                      Force to read the flag_value's and flag_name's as they are, otherwise they
                                                might be interpreted as an option and detected as such. Use when a
                                                flag_value starts with -, like -ObjC
    -h, --help                              This message.
    -t, --target <target>                   Target name(s) to be modified. If there is no target specified, all targets
                                                are modified.
    -b, --backup                            Creates a backup before start processing the command.
    -c, --configuration <configuration>     Configuration name to modify the flags. If no configuration name is
                                                provided, all configurations are affected.

delete options:
    -D, --delete                            Removes the given flag_value's from the pairing flag_name.
"""

# Future addition to the command line:
# pbxproj flag [options] (--delete | -D) (--all | -A) <project> [--] <flag_name>...
from docopt import docopt

from pbxproj.pbxcli import command_parser


def execute(project, args):
    # make a decision of what function to call based on the -D flag
    if args['--delete']:
        return _remove(project, args)
    else:
        return _add(project, args)


def _add(project, args):
    for (flag_name, flag_value) in zip(args['<flag_name>'], args['<flag_value>']):
        project.add_flags(flag_name, flag_value, target_name=args['--target'],
                          configuration_name=args['--configuration'])
    return 'Flags added successfully.'


def _remove(project, args):
    for (flag_name, flag_value) in zip(args['<flag_name>'], args['<flag_value>']):
        project.remove_flags(flag_name, flag_value, target_name=args['--target'],
                             configuration_name=args['--configuration'])
    return 'Flags removed successfully.'


def main():
    command_parser(execute)(docopt(__doc__))


if __name__ == '__main__':
    main()

