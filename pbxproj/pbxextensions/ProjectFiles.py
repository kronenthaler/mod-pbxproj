from pbxproj.pbxsections import *


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
    _SPECIAL_FOLDERS = ['.bundle', '.framework', '.xcodeproj', '.xcassets', '.xcdatamodeld']

    def add_file(self, path, parent=None, tree='SOURCE_ROOT', create_build_files=True, weak=False,
                 ignore_unknown_type=False, target=None):
        # returns a list of elements that were added to the project successfully as PBXBuildFile objects
        results = []

        # decide the proper tree and path to add
        if os.path.isabs(path):
            abs_path = path

            if not os.path.exists(path):
                return results

            if tree == 'SOURCE_ROOT':
                path = os.path.relpath(path, self._source_root)
            else:
                tree = '<absolute>'

        # determine the parent
        parent = self._get_parent_group(parent)

        # create a PBXFileReference for the new file
        file_ref = PBXFileReference.create(path, tree)

        # determine the type of the new file:
        file_type, build_phase = self._determine_file_type(file_ref)

        if not ignore_unknown_type and file_type is None:
            print 'Unknown file extension: %s' % os.path.splitext(file_ref.name)[1]
            print 'Please add extension and Xcode type to PBXFileReference._FILE_TYPES'
            return []

        # set the file type on the file ref add the files
        file_ref.set_last_known_file_type(file_type)
        parent.add_child(file_ref.get_id())
        self.objects[file_ref.get_id()] = file_ref

        # get target to match the given name or all
        # for each target:
        #   for each buildPhase in target.buildPhases
        #       if type matches build_phase:
        #           create a pbxbuildfile
        #           add it the other phase.add_build_file
        #           add to the objects
        # -> decide if it's needed extra actions depending on the type
        # -> frameworks and libraries need flags and extra build phases

        return results

    def _determine_file_type(self, file_ref):
        ext = os.path.splitext(file_ref.name)[1]
        if os.path.isdir(file_ref.path) and ext not in ProjectFiles._SPECIAL_FOLDERS:
            f_type = 'folder'
            build_phase = None
            ext = ''
        else:
            file_type, build_phase = ProjectFiles._FILE_TYPES.get(ext, (None, 'PBXResourcesBuildPhase'))

        return file_type, build_phase