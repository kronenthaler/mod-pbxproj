"""
usage:
    pbxproj show [options] <project>
    pbxproj show [options] (--target <target>) <project>

positional arguments:
    <project>                      Project path to the .xcodeproj folder.

generic options:
    -h, --help                      This message.
    -t, --target <target>           Target name to be modified. If there is no target specified, all targets are
                                        modified.
    -b, --backup                    Creates a backup before start processing the command.

target options:
    -s, --source-files              Show the source files attached to the target
    -r, --resource-files            Show the resource files attached to the target
    -l, --library-files             Show the library files attached to the target
    -H, --header-files              Show the header files attached to the target
    -c, --configurations            Show the configurations attached to the target
"""

from pbxproj.pbxcli import *
from pbxproj.pbxextensions.ProjectFiles import FileOptions
from docopt import docopt


def execute(project, args):
    # make a decision of what function to call based on the -D flag
    if args[u'--target']:
        return _target_info(project, args[u'--target'], args)
    else:
        return _summary(project, args)


def _summary(project, args):
    info = ''
    for target in project.objects.get_targets():
        info += "{name}:\n" \
                "\tProduct Name: {productName}\n" \
                "\tConfigurations: {configs}\n" \
            .format(name=target.name,
                    productName=target.productName,
                    configs=', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)]),
                    )

        for build_phase_id in target.buildPhases:
            build_phase = project.objects[build_phase_id]
            info += "\t{name} Files Count: {count}\n"\
                .format(name=build_phase._get_comment(), count=build_phase.files.__len__())

        info += "\n"
    return info


def _target_info(project, target, args):
    return u'showing target options'