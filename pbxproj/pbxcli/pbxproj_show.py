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


def execute(project, args):
    # make a decision of what function to call based on the -D flag
    if args['--target']:
        return _target_info(project, args['--target'], args)
    else:
        return _summary(project, args)


def _summary(project, _):
    info = ''
    for target in project.objects.get_targets():
        configs = ', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)])
        info += f"{target.name}:\n" \
                f"\tTarget type: {target.isa}\n" \
                f"\tProduct name: {target.productName}\n" \
                f"\tConfigurations: {configs}\n" \

        for build_phase_id in target.buildPhases:
            build_phase = project.objects[build_phase_id]
            info += f"\t{build_phase._get_comment()} ({build_phase.isa}) file count: {build_phase.files.__len__()}\n"

        info += "\n"
    return info


def _target_info(project, target_name, args):
    build_phases = _process_parameters(args)

    info = ''
    for target in project.objects.get_targets(target_name):
        info += f"{target.name}:\n" \
                f"\tProduct name: {target.productName}\n"

        if args['--configurations']:
            configs = ', '.join([c.name for c in project.objects.get_configurations_on_targets(target.name)])
            info += f"\tConfigurations: {configs}\n"

        for build_phase_id in target.buildPhases:
            build_phase = project.objects[build_phase_id]
            if build_phase.isa in build_phases:
                info += f"\t{build_phase._get_comment()}: \n\t\t"
                files = []
                for build_file_id in build_phase.files:
                    build_file = project.objects[build_file_id]
                    files.append(project.objects[build_file.fileRef]._get_comment())
                formatted_files = "\n\t\t".join(sorted(files))
                info += f'{formatted_files}\n'
        info += '\n'
    return info


def _process_parameters(args):
    build_phases = []
    if args['--source-files']:
        build_phases += ['PBXSourcesBuildPhase']
    elif args['--header-files']:
        build_phases += ['PBXHeadersBuildPhase']
    elif args['--resource-files']:
        build_phases += ['PBXResourcesBuildPhase']
    elif args['--framework-files']:
        build_phases += ['PBXFrameworksBuildPhase']
    elif args['--build-phase-files']:
        build_phases += [args['--build-phase-files']]
    return build_phases
