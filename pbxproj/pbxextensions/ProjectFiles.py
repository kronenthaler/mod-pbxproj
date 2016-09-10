from pbxproj.pbxsections import *


class BuildOptions:
    CREATE_BUILD_FILE_FLAG = 1
    WEAK_LINK_FLAG = 1 << 1
    EMBED_FRAMEWORK = 1 << 2


class ProjectFiles:
    _FILE_TYPES = {
        u'.a': (u'archive.ar', u'PBXFrameworksBuildPhase'),
        u'.app': (u'wrapper.application', None),
        u'.s': (u'sourcecode.asm', u'PBXSourcesBuildPhase'),
        u'.c': (u'sourcecode.c.c', u'PBXSourcesBuildPhase'),
        u'.cpp': (u'sourcecode.cpp.cpp', u'PBXSourcesBuildPhase'),
        u'.framework': (u'wrapper.framework', u'PBXFrameworksBuildPhase'),
        u'.h': (u'sourcecode.c.h', None),
        u'.hpp': (u'sourcecode.c.h', None),
        u'.d': (u'sourcecode.dtrace', u'PBXSourcesBuildPhase'),
        u'.swift': (u'sourcecode.swift', u'PBXSourcesBuildPhase'),
        u'.icns': (u'image.icns', u'PBXResourcesBuildPhase'),
        u'.m': (u'sourcecode.c.objc', u'PBXSourcesBuildPhase'),
        u'.j': (u'sourcecode.c.objc', u'PBXSourcesBuildPhase'),
        u'.mm': (u'sourcecode.cpp.objcpp', u'PBXSourcesBuildPhase'),
        u'.nib': (u'wrapper.nib', u'PBXResourcesBuildPhase'),
        u'.plist': (u'text.plist.xml', u'PBXResourcesBuildPhase'),
        u'.json': (u'text.json', u'PBXResourcesBuildPhase'),
        u'.png': (u'image.png', u'PBXResourcesBuildPhase'),
        u'.rtf': (u'text.rtf', u'PBXResourcesBuildPhase'),
        u'.tiff': (u'image.tiff', u'PBXResourcesBuildPhase'),
        u'.txt': (u'text', u'PBXResourcesBuildPhase'),
        u'.xcodeproj': (u'wrapper.pb-project', None),
        u'.xib': (u'file.xib', u'PBXResourcesBuildPhase'),
        u'.strings': (u'text.plist.strings', u'PBXResourcesBuildPhase'),
        u'.bundle': (u'wrapper.plug-in', u'PBXResourcesBuildPhase'),
        u'.dylib': (u'compiled.mach-o.dylib', u'PBXFrameworksBuildPhase'),
        u'.xcdatamodeld': (u'wrapper.xcdatamodel', u'PBXSourcesBuildPhase'),
        u'.xcassets': (u'folder.assetcatalog', u'PBXResourcesBuildPhase'),
        u'.tbd': (u'sourcecode.text-based-dylib-definition', u'PBXFrameworksBuildPhase'),
    }
    _TREES = [
        u'<absolute>',
        u'<group>',
        u'BUILT_PRODUCTS_DIR',
        u'DEVELOPER_DIR',
        u'SDKROOT',
        u'SOURCE_ROOT',
    ]
    _SPECIAL_FOLDERS = [
        u'.bundle',
        u'.framework',
        u'.xcodeproj',
        u'.xcassets',
        u'.xcdatamodeld'
    ]

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_file(self, path, parent=None, tree='SOURCE_ROOT', target_name=None, ignore_unknown_type=False,
                 options=BuildOptions.CREATE_BUILD_FILE_FLAG|BuildOptions.EMBED_FRAMEWORK):
        """
        :param path: Path to the file to be added
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param target_name: Target name where the file should be added (none for every target)
        :param ignore_unknown_type: Stop insertion if the file type is unknown (Default is false)
        :param options: Bit mask options for the creation of the PBXBuildFile phase.
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """

        # decide the proper tree and path to add
        abs_path, path, tree = self._get_path_and_tree(path, tree)
        if path is None or tree is None:
            return []

        # create a PBXFileReference for the new file
        file_ref = PBXFileReference.create(path, tree)

        # determine the type of the new file:
        file_type, expected_build_phase = ProjectFiles._determine_file_type(file_ref, unknown_type_allowed=ignore_unknown_type)

        # set the file type on the file ref add the files
        file_ref.set_last_known_file_type(file_type)
        self.objects[file_ref.get_id()] = file_ref

        # determine the parent and add it to it
        self._get_parent_group(parent).add_child(file_ref.get_id())

        # no need to create the build_files, done
        if (options & BuildOptions.CREATE_BUILD_FILE_FLAG) == 0:
            return []

        attributes = [u'Weak'] if (options & BuildOptions.WEAK_LINK_FLAG) != 0 else None

        # get target to match the given name or all
        results = []
        for target in self.objects.get_targets(target_name):
            # determine if there is a suitable build phase created
            build_phases = target.get_or_create_build_phase(expected_build_phase)

            # if it's a framework and it needs to be embedded
            if (options & BuildOptions.EMBED_FRAMEWORK) != 0 and expected_build_phase == u'PBXFrameworksBuildPhase':
                build_phases.extend(target.get_or_create_build_phase(u'PBXCopyFilesBuildPhase', (PBXCopyFilesBuildPhase._EMBEDDED_FRAMEWORKS,)))

            # create the build file and add it to the phase
            for target_build_phase in build_phases:
                build_file = PBXBuildFile.create(file_ref, attributes)
                self.objects[build_file.get_id()] = build_file
                target_build_phase.add_build_file(build_file)

                results.append(build_file)

        # special case for the frameworks and libraries to update the search paths
        if tree != u'SOURCE_ROOT' or not os.path.isabs(file_ref.path):
            return results

        # the path is absolute and it's outside the scope of the project for linking purposes
        library_path = os.path.join(u'$(SRCROOT)', os.path.split(file_ref.path)[0])
        if os.path.isfile(file_ref.path):
            self.add_library_search_paths([library_path], recursive=False)
        else:
            self.add_framework_search_paths([library_path, u'$(inherited)'], recursive=False)

        return results

    @classmethod
    def _determine_file_type(cls, file_ref, unknown_type_allowed):
        ext = os.path.splitext(file_ref.name)[1]
        if os.path.isdir(file_ref.path) and ext not in ProjectFiles._SPECIAL_FOLDERS:
            file_type = 'folder'
            build_phase = None
            ext = ''
        else:
            file_type, build_phase = ProjectFiles._FILE_TYPES.get(ext, (None, u'PBXResourcesBuildPhase'))

        if not unknown_type_allowed and file_type is None:
            raise ValueError(u'Unknown file extension: {0}. Please add the extension and Xcode type to ProjectFiles._FILE_TYPES'\
                             .format(os.path.splitext(file_ref.name)[1]))

        return file_type, build_phase

    def _get_path_and_tree(self, path, tree):
        # returns the absolute path, the relative path and the tree
        abs_path = None
        if os.path.isabs(path):
            abs_path = path

            if not os.path.exists(path):
                return None, None, None

            if tree == 'SOURCE_ROOT':
                path = os.path.relpath(path, self._source_root)
            else:
                tree = '<absolute>'

        return abs_path, path, tree