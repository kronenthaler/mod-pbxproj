from pbxproj.pbxsections import *


class TreeType:
    ABSOLUTE = u'<absolute>'
    GROUP = u'<group>'
    BUILT_PRODUCT_DIR = u'BUILT_PRODUCTS_DIR'
    DEVELOPER_DIR = u'DEVELOPER_DIR'
    SDKROOT = u'SDKROOT'
    SOURCE_ROOT = u'SOURCE_ROOT'


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
    _SPECIAL_FOLDERS = [
        u'.bundle',
        u'.framework',
        u'.xcodeproj',
        u'.xcassets',
        u'.xcdatamodeld'
    ]

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_file(self, path, parent=None, tree=TreeType.SOURCE_ROOT, create_build_files=True, weak=False,
                 ignore_unknown_type=False, target_name=None, embed_framework=True):
        """
        Adds a file to the project, taking care of the type of the file and creating additional structures depending on
        the file type. For instance, frameworks will be linked, embedded and search paths will be adjusted automatically.
        Header file will be added to the headers sections, but not compiled, whereas the source files will be added to
        the compilation phase.
        :param path: Path to the file to be added
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param create_build_files: Creates any necessary PBXBuildFile section when adding the file
        :param weak: When adding a framework set it as a weak reference
        :param ignore_unknown_type: Stop insertion if the file type is unknown (Default is false)
        :param target_name: Target name where the file should be added (none for every target)
        :param embed_framework: When adding a framework sets the embed section
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """

        # decide the proper tree and path to add
        abs_path, path, tree = ProjectFiles._get_path_and_tree(self._source_root, path, tree)
        if path is None or tree is None:
            return []

        # create a PBXFileReference for the new file
        file_ref = PBXFileReference.create(path, tree)

        # determine the type of the new file:
        file_type, expected_build_phase = ProjectFiles._determine_file_type(file_ref,
                                                                            unknown_type_allowed=ignore_unknown_type)

        # set the file type on the file ref add the files
        file_ref.set_last_known_file_type(file_type)
        self.objects[file_ref.get_id()] = file_ref

        # determine the parent and add it to it
        self._get_parent_group(parent).add_child(file_ref.get_id())

        # no need to create the build_files, done
        if not create_build_files:
            return []

        attributes = [u'Weak'] if weak else None

        # get target to match the given name or all
        results = []
        for target in self.objects.get_targets(target_name):
            # determine if there is a suitable build phase created
            build_phases = target.get_or_create_build_phase(expected_build_phase)

            # if it's a framework and it needs to be embedded
            if embed_framework and expected_build_phase == u'PBXFrameworksBuildPhase' and file_ref.lastKnownFileType == u'wrapper.framework':
                embed_phase = target.get_or_create_build_phase(u'PBXCopyFilesBuildPhase',
                                                               (PBXCopyFilesBuildPhase._EMBEDDED_FRAMEWORKS,))
                build_phases.extend(embed_phase)

            # create the build file and add it to the phase
            for target_build_phase in build_phases:
                build_file = PBXBuildFile.create(file_ref, attributes)
                self.objects[build_file.get_id()] = build_file
                target_build_phase.add_build_file(build_file)

                results.append(build_file)

        # special case for the frameworks and libraries to update the search paths
        if tree != TreeType.SOURCE_ROOT or abs_path is None:
            return results

        # the path is absolute and it's outside the scope of the project for linking purposes
        library_path = os.path.join(u'$(SRCROOT)', os.path.split(file_ref.path)[0])
        if os.path.isfile(abs_path):
            self.add_library_search_paths([library_path], recursive=False)
        else:
            self.add_framework_search_paths([library_path, u'$(inherited)'], recursive=False)

        return results

    def add_file_if_doesnt_exist(self, path, parent=None, tree=TreeType.SOURCE_ROOT, create_build_files=True,
                                 weak=False, ignore_unknown_type=False, target_name=None, embed_framework=True):
        """
        :param path: Path to the file to be added
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param create_build_files: Creates any necessary PBXBuildFile section when adding the file
        :param weak: When adding a framework set it as a weak reference
        :param ignore_unknown_type: Stop insertion if the file type is unknown (Default is false)
        :param target_name: Target name where the file should be added (none for every target)
        :param embed_framework: When adding a framework sets the embed section
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """
        for section in self.objects._get_keys():
            for obj in self.objects.get_objects_in_section(section):
                if u'path' in obj and ProjectFiles._path_leaf(path) == ProjectFiles._path_leaf(obj.path):
                    return []

        return self.add_file(path, parent, tree, create_build_files, weak, ignore_unknown_type, target_name,
                             embed_framework)

    def get_file_by_id(self, id):
        """
        Gets the PBXFileReference to the given id
        :param id: Identifier of the PBXFileReference to be retrieved.
        :return: A PBXFileReference if the id is found, None otherwise.
        """
        file_ref = self.objects[id]
        if not isinstance(file_ref, PBXFileReference):
            return None
        return file_ref

    def get_files_by_name(self, name, parent=None):
        """
        Gets all the files references that have the given name, under the especified parent PBXGroup object or
        PBXGroup id.
        :param name: name of the file to be retrieved
        :param parent: PBXGroup that should be used to narrow the search or None to retrieve files from all project
        :return: List of all PBXFileReference that match the name and parent criteria.
        """
        if parent is not None:
            parent = self._get_parent_group(parent)

        files = []
        for file in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file.name == name and (parent is None or parent.has_child(file.get_id())):
                files.append(file)

        return files

    def get_files_by_path(self, path, tree=TreeType.SOURCE_ROOT):
        """
        Gets the files under the given tree type that match the given path.
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :return: List of all PBXFileReference that match the path and tree criteria.
        """
        files = []
        for file in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file.path == path and file.sourceTree == tree:
                files.append(file)

        return files

    def remove_file_by_id(self, id, target_name=None):
        """
        Removes the file id from given target name. If no target name is given, the file is removed
        from all targets
        :param id: identifier of the file to be removed
        :param target_name: The target name to remove the file from, if None, it's removed from all targets.
        :return: True if the file id was removed. False if the file was not removed.
        """

        file_ref = self.get_file_by_id(id)
        if file_ref is None:
            return False

        for target in self.objects.get_targets(target_name):
            build_phases = list(target.buildPhases)
            for build_phase_id in build_phases:
                build_phase = self.objects[build_phase_id]

                build_files = list(build_phase.files)
                for build_file_id in build_files:
                    build_file = self.objects[build_file_id]

                    if build_file.fileRef == file_ref.get_id():
                        # remove the build file from the phase
                        build_phase.remove_build_file(build_file)

                # if the build_phase is empty remove it too
                if build_phase.files.__len__() == 0:
                    # remove the build phase from the target
                    target.remove_build_phase(build_phase)

        # remove it iff it's removed from all targets or no build file reference it
        for build_file in self.objects.get_objects_in_section(u'PBXBuildFile'):
            if build_file.fileRef == file_ref.get_id():
                return True

        # the file is not referenced in any build file, remove it
        del self.objects[file_ref.get_id()]
        return True

    def remove_files_by_path(self, path, tree=TreeType.SOURCE_ROOT):
        """
        Removes all files for the given path under the same tree
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :return: True if all the files were removed without problems. False if at least one file failed.
        """
        result = True
        for file_ref in self.get_files_by_path(path, tree):
            result &= self.remove_file_by_id(file_ref.get_id())

        return result

    # miscellaneous functions, candidates to be extracted and decouple implementation
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
            raise ValueError(
                u'Unknown file extension: {0}. Please add the extension and Xcode type to ProjectFiles._FILE_TYPES' \
                    .format(os.path.splitext(file_ref.name)[1]))

        return file_type, build_phase

    @classmethod
    def _path_leaf(cls, path):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)

    @classmethod
    def _get_path_and_tree(cls, source_root, path, tree):
        # returns the absolute path, the relative path and the tree
        abs_path = None
        if os.path.isabs(path):
            abs_path = path

            if not os.path.exists(path):
                return None, None, None

            if tree == TreeType.SOURCE_ROOT:
                path = os.path.relpath(path, source_root)
            else:
                tree = TreeType.ABSOLUTE

        return abs_path, path, tree
