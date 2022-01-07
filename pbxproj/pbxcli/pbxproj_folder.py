"""
usage:
    pbxproj folder [options] <project> <path> [--target <target>...]
                                              [--exclude <regex>...]
                                              [(--recursive | -r)]
                                              [(--no-create-groups | -G)]
                                              [(--weak | -w)]
                                              [(--no-embed | -E)]
                                              [(--sign-on-copy | -s)]
                                              [(--ignore-unknown-types | -i)]
                                              [(--no-create-build-files | -C)]
                                              [(--header-scope <scope> | -H <scope>)]
    pbxproj folder [options] (--delete | -D) <project> <path> [--tree <tree>]

positional arguments:
    <project>                      Project path to the .xcodeproj folder.
    <path>                         Path of the file to add to the project.

generic options:
    -h, --help                      This message.
    -t, --target <target>           Target name(s) to be modified. If there is no target specified, all targets are
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
    -H, --header-scope <scope>      Add header file using the given scope. Available options: public or private, project.
                                       [default: project]
"""
from docopt import docopt

from pbxproj.pbxcli import command_parser
from pbxproj.pbxextensions.ProjectFiles import FileOptions


def execute(project, args):
    # make a decision of what function to call based on the -D flag
    if args['--delete']:
        return _remove(project, args)
    else:
        return _add(project, args)


def _add(project, args):
    if '--header-scope' not in args or args['--header-scope'] not in ['public', 'private', 'project']:
        header_scope = 'project'
    else:
        header_scope = args['--header-scope']

    options = FileOptions(create_build_files=not args['--no-create-build-files'],
                          weak=args['--weak'],
                          ignore_unknown_type=args['--ignore-unknown-types'],
                          embed_framework=not args['--no-embed'],
                          code_sign_on_copy=args['--sign-on-copy'],
                          header_scope=header_scope.title())

    build_files = project.add_folder(args['<path>'], excludes=args['--exclude'], recursive=args['--recursive'],
                                     create_groups=not args['--no-create-groups'], target_name=args['--target'],
                                     file_options=options)
    # print some information about the build files created.
    if build_files is None:
        raise RuntimeError('No files were added to the project.')

    if not build_files:
        return 'Folder added to the project, no build file sections created.'

    info = {}
    for build_file in build_files:
        if build_file.isa not in info:
            info[build_file.isa] = 0
        info[build_file.isa] += 1

    summary = 'Folder added to the project.'
    for k in info:
        summary += f'\n{info[k]} {k} sections created.'
    return summary


def _remove(project, args):
    if project.remove_files_by_path(args['<path>'], tree=args['--tree'], target_name=args['--target']):
        return 'Folder removed from the project.'
    raise RuntimeError('An error occurred removing one of the files.')


def main():
    command_parser(execute)(docopt(__doc__))


if __name__ == '__main__':
    main()
