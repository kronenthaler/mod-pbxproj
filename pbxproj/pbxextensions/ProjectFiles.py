from pbxproj.pbxsections import *


class TreeType:
    ABSOLUTE = u'<absolute>'
    GROUP = u'<group>'
    BUILT_PRODUCT_DIR = u'BUILT_PRODUCTS_DIR'
    DEVELOPER_DIR = u'DEVELOPER_DIR'
    SDKROOT = u'SDKROOT'
    SOURCE_ROOT = u'SOURCE_ROOT'

    @classmethod
    def options(cls):
        return [TreeType.SOURCE_ROOT, TreeType.SDKROOT, TreeType.GROUP, TreeType.ABSOLUTE,
                TreeType.DEVELOPER_DIR, TreeType.BUILT_PRODUCT_DIR]


class FileOptions:
    """
    Wrapper class for all file parameters required at the moment of adding a file to the project.
    """
    def __init__(self, create_build_files=True, weak=False, ignore_unknown_type=False, embed_framework=True,
                 code_sign_on_copy=True):
        """
        Creates an object specifying options to be consided during the file creation into the project.

        :param create_build_files: Creates any necessary PBXBuildFile section when adding the file
        :param weak: When adding a framework set it as a weak reference
        :param ignore_unknown_type: Stop insertion if the file type is unknown (Default is false)
        :param embed_framework: When adding a framework sets the embed section
        :param code_sign_on_copy: When embedding a framework, sets the code sign attribute
        """
        self.create_build_files = create_build_files
        self.weak = weak
        self.ignore_unknown_type = ignore_unknown_type
        self.embed_framework = embed_framework
        self.code_sign_on_copy = code_sign_on_copy

    def get_attributes(self):
        attributes = [u'Weak'] if self.weak else None
        if self.code_sign_on_copy:
            if attributes is None:
                attributes = []
            attributes += [u'CodeSignOnCopy', u'RemoveHeadersOnCopy']
        return attributes


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
        u'.xcdatamodeld',
        u'.storyboardc'
    ]

    def __init__(self):
        raise EnvironmentError('This class cannot be instantiated directly, use XcodeProject instead')

    def add_file(self, path, parent=None, tree=TreeType.SOURCE_ROOT, target_name=None, force=True, file_options=FileOptions()):
        """
        Adds a file to the project, taking care of the type of the file and creating additional structures depending on
        the file type. For instance, frameworks will be linked, embedded and search paths will be adjusted automatically.
        Header file will be added to the headers sections, but not compiled, whereas the source files will be added to
        the compilation phase.
        :param path: Path to the file to be added
        :param parent: Parent group to be added under
        :param tree: Tree where the path is relative to
        :param target_name: Target name where the file should be added (none for every target)
        :param force: Add the file without checking if the file already exists
        :param file_options: FileOptions object to be used during the addition of the file to the project.
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """
        results = []
        # if it's not forced to add the file stop if the file already exists.
        if not force:
            for section in self.objects.get_sections():
                for obj in self.objects.get_objects_in_section(section):
                    if u'path' in obj and ProjectFiles._path_leaf(path) == ProjectFiles._path_leaf(obj.path):
                        return results

        # decide the proper tree and path to add
        abs_path, path, tree = ProjectFiles._get_path_and_tree(self._source_root, path, tree)
        if path is None or tree is None:
            return None

        # create a PBXFileReference for the new file
        file_ref = PBXFileReference.create(path, tree)

        # determine the type of the new file:
        file_type, expected_build_phase = ProjectFiles._determine_file_type(file_ref, file_options.ignore_unknown_type)

        # set the file type on the file ref add the files
        file_ref.set_last_known_file_type(file_type)
        self.objects[file_ref.get_id()] = file_ref

        # determine the parent and add it to it
        self._get_parent_group(parent).add_child(file_ref)

        # no need to create the build_files, done
        if not file_options.create_build_files:
            return results

        # additional attributes in for libraries/embed frameworks
        attributes = file_options.get_attributes()

        # get target to match the given name or all
        for target in self.objects.get_targets(target_name):
            # determine if there is a suitable build phase created
            build_phases = target.get_or_create_build_phase(expected_build_phase)

            # if it's a framework and it needs to be embedded
            if file_options.embed_framework and expected_build_phase == u'PBXFrameworksBuildPhase' and \
                    file_ref.lastKnownFileType == u'wrapper.framework':
                embed_phase = target.get_or_create_build_phase(u'PBXCopyFilesBuildPhase',
                                                               (PBXCopyFilesBuildPhaseNames.EMBEDDED_FRAMEWORKS,))
                # add runpath search flag
                self.add_flags(XCBuildConfigurationFlags.LD_RUNPATH_SEARCH_PATHS,
                               u'$(inherited) @executable_path/Frameworks', target_name)
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

    def get_file_by_id(self, file_id):
        """
        Gets the PBXFileReference to the given id
        :param file_id: Identifier of the PBXFileReference to be retrieved.
        :return: A PBXFileReference if the id is found, None otherwise.
        """
        file_ref = self.objects[file_id]
        if not isinstance(file_ref, PBXFileReference):
            return None
        return file_ref

    def get_files_by_name(self, name, parent=None):
        """
        Gets all the files references that have the given name, under the specified parent PBXGroup object or
        PBXGroup id.
        :param name: name of the file to be retrieved
        :param parent: PBXGroup that should be used to narrow the search or None to retrieve files from all project
        :return: List of all PBXFileReference that match the name and parent criteria.
        """
        if parent is not None:
            parent = self._get_parent_group(parent)

        files = []
        for file_ref in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file_ref.name == name and (parent is None or parent.has_child(file_ref.get_id())):
                files.append(file_ref)

        return files

    def get_files_by_path(self, path, tree=TreeType.SOURCE_ROOT):
        """
        Gets the files under the given tree type that match the given path.
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :return: List of all PBXFileReference that match the path and tree criteria.
        """
        files = []
        for file_ref in self.objects.get_objects_in_section(u'PBXFileReference'):
            if file_ref.path == path and file_ref.sourceTree == tree:
                files.append(file_ref)

        return files

    def remove_file_by_id(self, file_id, target_name=None):
        """
        Removes the file id from given target name. If no target name is given, the file is removed
        from all targets
        :param file_id: identifier of the file to be removed
        :param target_name: The target name to remove the file from, if None, it's removed from all targets.
        :return: True if the file id was removed. False if the file was not removed.
        """

        file_ref = self.get_file_by_id(file_id)
        if file_ref is None:
            return False

        for target in self.objects.get_targets(target_name):
            for build_phase_id in target.buildPhases:
                build_phase = self.objects[build_phase_id]

                for build_file_id in build_phase.files:
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

        # remove the file from any groups if there is no reference from any target
        for group in self.objects.get_objects_in_section(u'PBXGroup'):
            if file_ref.get_id() in group.children:
                group.remove_child(file_ref)

        # the file is not referenced in any build file, remove it
        del self.objects[file_ref.get_id()]
        return True

    def remove_files_by_path(self, path, tree=TreeType.SOURCE_ROOT, target_name=None):
        """
        Removes all files for the given path under the same tree
        :param path: Path to the file relative to the tree root
        :param tree: Tree type to look for the path. By default the SOURCE_ROOT
        :param target_name: Target name where the file should be added (none for every target)
        :return: True if all the files were removed without problems. False if at least one file failed.
        """
        files = self.get_files_by_path(path, tree)
        result = 0
        total = files.__len__()
        for file_ref in files:
            if self.remove_file_by_id(file_ref.get_id(), target_name=target_name):
                result += 1

        return result != 0 and result == total

    def add_folder(self, path, parent=None, excludes=None, recursive=True, create_groups=True, target_name=None,
                   file_options=FileOptions()):
        """
        Given a directory, it will create the equivalent group structure and add all files in the process.
        If groups matching the logical path already exist, it will use them instead of creating a new one. Same
        apply for file within a group, if the file name already exists it will be ignored.

        :param path: OS path to the directory to be added.
        :param parent: Parent group to be added under
        :param excludes: list of regexs to ignore
        :param recursive: add folders recursively or stop in the first level
        :param create_groups: add folders recursively as groups or references
        :param target_name: Target name where the file should be added (none for every target)
        :param file_options: FileOptions object to be used during the addition of the file to the project.
        :return: a list of elements that were added to the project successfully as PBXBuildFile objects
        """
        if not os.path.isdir(path):
            return None

        if not excludes:
            excludes = []

        results = []

        # add the top folder as a group, make it the new parent
        path = os.path.abspath(path)
        if not create_groups and os.path.splitext(path)[1] not in ProjectFiles._SPECIAL_FOLDERS:
            return self.add_file(path, parent, target_name=target_name, force=False, file_options=file_options)

        parent = self.get_or_create_group(os.path.split(path)[1], os.path.split(path)[1], parent)

        # iterate over the objects in the directory
        for child in os.listdir(path):
            # exclude dirs or files matching any of the expressions
            if [pattern for pattern in excludes if re.match(pattern, child)]:
                continue

            full_path = os.path.join(path, child)
            children = []
            if os.path.isfile(full_path) or os.path.splitext(child)[1] in ProjectFiles._SPECIAL_FOLDERS or \
                    not create_groups:
                # check if the file exists already, if not add it
                children = self.add_file(full_path, parent, target_name=target_name, force=False,
                                         file_options=file_options)
            else:
                # if recursive is true, go deeper, otherwise create the group here.
                if recursive:
                    children = self.add_folder(full_path, parent, excludes, recursive, target_name=target_name,
                                               file_options=file_options)
                else:
                    subgroup = self.get_or_create_group(child, child, parent)

            results.extend(children)

        return results

    # miscellaneous functions, candidates to be extracted and decouple implementation
    @classmethod
    def _determine_file_type(cls, file_ref, unknown_type_allowed):
        ext = os.path.splitext(file_ref.name)[1]
        if os.path.isdir(os.path.abspath(file_ref.path)) and ext not in ProjectFiles._SPECIAL_FOLDERS:
            file_type = 'folder'
            build_phase = u'PBXResourcesBuildPhase'
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
