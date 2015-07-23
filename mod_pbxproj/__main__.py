from mod_pbxproj import XcodeProject


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser("Modify an xcode project file using a single command at a time.")
    parser.add_argument('project', help="Project path")
    parser.add_argument('configuration', help="Modify the flags of the given configuration", choices=['Debug', 'Release', 'All'])
    parser.add_argument('-af', help='Add a flag value, in the format key=value', action='append')
    parser.add_argument('-rf', help='Remove a flag value, in the format key=value', action='append')
    parser.add_argument('-b', '--backup', help='Create a temporary backup before modify', action='store_true')
    parser.add_argument('-pp', '--pure-python', help='Use the pure python parser', action='store_true')
    args = parser.parse_args()

    # open the project file
    if os.path.isdir(args.project) :
        args.project = args.project + "/project.pbxproj"

    if not os.path.isfile(args.project) :
        raise Exception("Project File not found")

    project = XcodeProject.Load(args.project, pure_python=args.pure_python)
    backup_file = None
    if args.backup :
        backup_file = project.backup()

    # apply the commands
    # add flags
    if args.af :
        pairs = {}
        for flag in args.af:
            tokens = flag.split("=")
            pairs[tokens[0]] = tokens[1]
        project.add_flags(pairs, args.configuration)

    # remove flags
    if args.rf :
        pairs = {}
        for flag in args.rf:
            tokens = flag.split("=")
            pairs[tokens[0]] = tokens[1]
        project.remove_flags(pairs, args.configuration)

    # save the file
    project.save()

    # remove backup if everything was ok.
    if args.backup :
        os.remove(backup_file)

if __name__ == "__main__":
    main()