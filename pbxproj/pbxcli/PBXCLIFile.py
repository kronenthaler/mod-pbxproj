from pbxproj.pbxcli import *
from pbxproj.pbxextensions.ProjectFiles import TreeType, FileOptions


class PBXCLIFile:
    def __init__(self, parser):
        file_parser = parser.add_parser(u'file', help=u'Manipulate files in the project')
        # common parameters
        standard_parameters(file_parser)
        file_parser.add_argument(u'path', help=u'file path to be added to the project')
        file_parser.add_argument(u'--tree', choices=TreeType.options(), default=TreeType.SOURCE_ROOT,
                                 help=u'tree relative to the origin of the file to be added.')

        # remove parameters
        remove_parser = file_parser.add_argument_group(u'Remove file options')
        remove_parser.add_argument(u'--delete', u'-D', action=u'store_true', help=u'')

        # add parameters
        add_parser = file_parser.add_argument_group(u'Add file options')
        add_parser.add_argument(u'--weak', u'-w', action=u'store_true', help=u'link framework weakly.')
        add_parser.add_argument(u'--no-embed', u'-E', action=u'store_false', dest=u'embed',
                                help=u'do not embed framework on the application')
        add_parser.add_argument(u'--sign-on-copy', u'-csoc', action=u'store_true', dest=u'code_sign_on_copy',
                                help=u'code sign frameworks when copied to the application.')
        add_parser.add_argument(u'--ignore-unknown-types', u'-i', action=u'store_true', dest=u'ignore_unknown_types',
                                help=u'ignore unknown types and add the file regardless.')
        add_parser.add_argument(u'--no-create-build-files', u'-C', action=u'store_false', dest=u'create_build_files',
                                help=u'when adding a file, do not create any associated build file section required.')

        file_parser.set_defaults(func=command_parser(PBXCLIFile._process_command))

    @classmethod
    def _process_command(cls, project, args):
        if args.delete:
            return PBXCLIFile._remove_file(project, args)
        else:
            return PBXCLIFile._add_file(project, args)

    @classmethod
    def _add_file(cls, project, args):
        options = FileOptions(create_build_files=args.create_build_files,
                              weak=args.weak,
                              ignore_unknown_type=args.ignore_unknown_types,
                              embed_framework=args.embed,
                              code_sign_on_copy=args.code_sign_on_copy)
        build_files = project.add_file_if_doesnt_exist(args.path, tree=args.tree, target_name=args.target,
                                                       file_options=options)
        # print some information about the build files created.
        if build_files is None:
            return u'No files were added to the project'

        if build_files is []:
            return u'File added to the project, no build file sections created.'

        info = {}
        for build_file in build_files:
            if build_file.isa not in info:
                info[build_file.isa] = 0
            info[build_file.isa] += 1

        summary = u'File added to the project.'
        for k in info:
            summary += u'\n{0} {1} sections created'.format(info[k], k)
        return summary

    @classmethod
    def _remove_file(cls, project, args):
        if project.remove_files_by_path(args.path, tree=args.tree, target_name=args.target):
            return u'File removed from the project'
        return u'An error occurred removing one of the files.'
