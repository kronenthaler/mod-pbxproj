"""
usage:
    pbxproj folder [options] <project> <path> [--exclude <regex>...]
                                              [(--recursive | -r)]
                                              [(--no-create-groups | -G)]
                                              [(--weak | -w)]
                                              [(--no-embed | -E)]
                                              [(--sign-on-copy | -s)]
                                              [(--ignore-unknown-types | -i)]
                                              [(--no-create-build-files | -C)]
    pbxproj folder [options] (--delete | -D) <project> <path> [--tree <tree>]

positional arguments:
    <project>                      Project path to the .xcodeproj folder.
    <path>                         Path of the file to add to the project.

generic options:
    -h, --help                      This message.
    -t, --target <target>           Target name to be modified. If there is no target specified, all targets are
                                        modified.
    -b, --backup                    Creates a backup before start processing the command.

delete options:
    -D, --delete                    Delete the file.
    --tree <tree>                   Tree to add the file relative to. Available options: <absolute>, <group>,
                                        SOURCE_ROOT, SDKROOT, DEVELOPER_DIR, BUILT_PRODUCTS_DIR. [default: SOURCE_ROOT]

add options:
    -e, --exclude <regex>           Pattern to exclude during the insertion of a folder. The pattern applies to file
                                        names and folder names.
    -r, --recursive                 Add folders and files recursively.
    -G, --no-create-groups          Add the folder as a file reference instead of creating group(s).
    -w, --weak                      Add the weak flag when libraries or frameworks are added. Linking optional.
    -E, --no-embed                  Do not embed frameworks when added.
    -s, --sign-on-copy              Sign frameworks when copied/embedded.
    -i, --ignore-unknown-types      Ignore unknown file types when added.
    -C, --no-create-build-files     Do not create build file phases when adding a file.
"""

# Future addition to the command line:
# pbxproj folder (--delete | -D) (--group | -G) <project> <path>

from pbxproj.pbxcli import *
from pbxproj.pbxextensions.ProjectFiles import FileOptions
from docopt import docopt


def execute(project, args):
    # make a decision of what function to call based on the -D flag
    if args[u'--delete']:
        return _remove(project, args)
    else:
        return _add(project, args)


def _add(project, args):
    options = FileOptions(create_build_files=not args[u'--no-create-build-files'],
                          weak=args[u'--weak'],
                          ignore_unknown_type=args[u'--ignore-unknown-types'],
                          embed_framework=not args[u'--no-embed'],
                          code_sign_on_copy=args[u'--sign-on-copy'])

    build_files = project.add_folder(args[u'<path>'], excludes=args[u'--exclude'], recursive=args[u'--recursive'],
                                     create_groups=not args[u'--no-create-groups'], target_name=args[u'--target'],
                                     file_options=options)
    # print some information about the build files created.
    if build_files is None:
        raise Exception(u'No files were added to the project.')

    if not build_files:
        return u'Folder added to the project, no build file sections created.'

    info = {}
    for build_file in build_files:
        if build_file.isa not in info:
            info[build_file.isa] = 0
        info[build_file.isa] += 1

    summary = u'Folder added to the project.'
    for k in info:
        summary += u'\n{0} {1} sections created.'.format(info[k], k)
    return summary


def _remove(project, args):
    if project.remove_files_by_path(args[u'<path>'], tree=args[u'--tree'], target_name=args[u'--target']):
        return u'Folder removed from the project.'
    raise Exception(u'An error occurred removing one of the files.')


def main():
    command_parser(execute)(docopt(__doc__))


if __name__ == '__main__':
    main()
