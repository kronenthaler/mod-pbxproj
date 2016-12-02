from pbxproj.pbxcli import *
from pbxproj.pbxextensions.ProjectFiles import TreeType, FileOptions


class PBXCLIFlag:
    def __init__(self, parser):
        flag_parser = parser.add_parser(u'flag', help=u'Manipulate flags in the project')
        # common parameters
        standard_parameters(flag_parser)
        flag_parser.add_argument(u'flag_name', help=u'flag name to modify')
        flag_parser.add_argument(u'value', help=u'flag value')
        flag_parser.add_argument(u'-c', u'--configuration', choices=[u'Debug', u'Release'], default=None,
                                 help="configuration to modify, if not specified affects all configurations.")

        # remove parameters
        remove_parser = flag_parser.add_argument_group(u'Remove flag options')
        remove_parser.add_argument(u'--delete', u'-D', action=u'store_true', help=u'')

        # add parameters
        add_parser = flag_parser.add_argument_group(u'Add flag options')

        flag_parser.set_defaults(func=command_parser(PBXCLIFlag._process_command))

    @classmethod
    def _process_command(cls, project, args):
        if args.delete:
            return cls._remove(project, args)
        else:
            return cls._add(project, args)

    @classmethod
    def _add(cls, project, args):
        project.add_flags(args.flag_name, args.value, target_name=args.target, configuration_name=args.configuration)
        return u'Flags added successfully'

    @classmethod
    def _remove(cls, project, args):
        project.remove_flags(args.flag_name, args.value, target_name=args.target, configuration_name=args.configuration)
        return u'Flags removed successfully'
