This module can read, modify, and write a .pbxproj file from an Xcode 4, 5 & 6 projects.  The file is usually called `project.pbxproj` and can be found inside the .xcodeproj bundle.

Basic Usage:

    from mod_pbxproj import XcodeProject
    project = XcodeProject.Load('/path/to/.pbxproj')

You now have a project object that has a bunch of methods for manipulating it.  By default files added to the project are also added to the appropriate build phase, as long as the file's type can be determined.

This will add a file in the root of a project.
**NOTE**: everything goes better if you supply absolute paths.

    project.add_file('/path/to/file.name')

This will return a group object that you can add files/folders under

    new_group = project.get_or_create_group('new group')

This will add other.file to the project as a child of 'new group'

    project.add_file('/path/to/other.file', parent=new_group)

If you want to add a framework or library that is found in the SDK,
supply a relative path and set the tree argument to 'SDKROOT'

    project.add_file('System/Libray/UIKit.framework', tree='SDKROOT')
    project.add_file('usr/lib/libz.dylib', tree='SDKROOT')

This will recursively create groups and add the directory's contents
to the project.  You can optionally turn off the recursion.

    project.add_folder('/path/to/folder')

You can supply an array of regular expressions for files you want to skip. This won't add any pdfs or mdown files found as it recurses.

    project.add_folder('/path/to/folder', excludes=["^.*\.mdown$", "^.*\.pdf$"])

If a modification you are trying to apply have already been applied to the project then it will be skipped.  This means that before saving the project you should check the modified flag to make sure changes have occured.

    if project.modified:
        project.backup()
        project.save() # will save by default using the new xcode 3.2 format
        project.save(old_format=True) # will force to save the project in plist XML format (NOT RECOMMENDED)

The backup method saves a copy of the project file in its current state on disk.  This can be very useful if a modification leaves the project file unreadable.

p.s. **NO WARRANTIES**
