"""
usage:
    pbxproj show [options] <project>
    pbxproj show [options] (--target <target>...) <project> [(-s | --source-files) |
                                                             (-H | --header-files) |
                                                             (-r | --resource-files) |
                                                             (-f | --framework-files) |
                                                             (--build-phase-files <build_phase_type>)]

positional arguments:
    <project>                      Project path to the .xcodeproj folder.

generic options:
    -h, --help                      This message.
    -t, --target <target>           Target name to be modified. If there is no target specified, all targets are used.
    -b, --backup                    Creates a backup before start processing the command.

target options:
    -s, --source-files              Show the source files attached to the target
    -r, --resource-files            Show the resource files attached to the target
    -f, --framework-files           Show the library files attached to the target
    -H, --header-files              Show the header files attached to the target
    -c, --configurations            Show the configurations attached to the target
    -B, --build-phase-files <type>  Show the files associated to the build phase of the given type.
"""

from pbxproj.pbxcli import *


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
                "\tTarget type: {type}\n" \
                "\tProduct name: {productName}\n" \
                "\tConfigurations: {configs}\n" \
            .format(name=target.name,
                    productName=target.productName,
                    type=target.isa,
                    configs=', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)]),
                    )

        for build_phase_id in target.buildPhases:
            build_phase = project.objects[build_phase_id]
            info += "\t{name} ({type}) file count: {count}\n"\
                .format(name=build_phase._get_comment(), type=build_phase.isa, count=build_phase.files.__len__())

        info += "\n"
    return info


def _target_info(project, target_name, args):
    build_phases = []
    if args[u'--source-files']:
        build_phases += [u'PBXSourcesBuildPhase']
    elif args[u'--header-files']:
        build_phases += [u'PBXHeadersBuildPhase']
    elif args[u'--resource-files']:
        build_phases += [u'PBXResourcesBuildPhase']
    elif args[u'--framework-files']:
        build_phases += [u'PBXFrameworksBuildPhase']
    elif args[u'--build-phase-files']:
        build_phases += [args[u'--build-phase-files']]

    info = ''
    for target in project.objects.get_targets(target_name):
        info += "{name}:\n" \
                "\tProduct name: {productName}\n" \
            .format(name=target.name,
                    productName=target.productName,
                    configs=', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)]),
                    )

        if args[u'--configurations']:
            info += "\tConfigurations: {configs}\n" \
                .format(configs=', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)]))

        for build_phase_id in target.buildPhases:
            build_phase = project.objects[build_phase_id]
            if build_phase.isa in build_phases:
                info += "\t{name}: \n\t\t".format(name=build_phase._get_comment())
                files = []
                for build_file_id in build_phase.files:
                    build_file = project.objects[build_file_id]
                    files.append(project.objects[build_file.fileRef]._get_comment())
                info += '{files}\n'.format(files="\n\t\t".join(sorted(files)))
        info += '\n'
    return info
