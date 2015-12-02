# mod-pbxproj

This module can read, modify, and write a .pbxproj file from an Xcode 4, 5 & 6 projects. The file is usually called project.pbxproj and can be found inside the .xcodeproj bundle.

## Table of Contents
* [Table of Contents](#table-of-contents)
* [Installation](#installation)
  * [Using pip](#using-pip)
  * [Using setup.py](#using-setuppy)
* [Using as CLI](#using-as-cli)
  * [CLI options](#cli-options)
* [Basic usage](#basic-usage)
  * [Import the module](#import-the-module)
  * [Load &amp; Write](#load--write)
    * [Load a project file](#load-a-project-file)
    * [Create a backup](#create-a-backup)
    * [Save the project](#save-the-project)
  * [Groups](#groups)
    * [Create or get a group](#create-or-get-a-group)
    * [Create groups recursively](#create-groups-recursively)
    * [Remove group by ID](#remove-group-by-id)
    * [Remove group by name](#remove-group-by-name)
  * [Files](#files)
    * [Add files](#add-files)
    * [Add a library/framework](#add-a-libraryframework)
    * [Remove files by ID](#remove-files-by-id)
    * [Remove files by path](#remove-files-by-path)
  * [Flags](#flags)
    * [Add a flag](#add-a-flag)
      * [Compiler flags](#compiler-flags)
      * [Linker flags](#linker-flags)
      * [Any other flags](#any-other-flags)
    * [Remove flags](#remove-flags)


## Installation
### Using pip
You can install this project directly without cloning it by executing:

```
sudo pip install mod_pbxproj
```

### Using setup.py
You need to clone this repository, open a terminal and go to the folder and execute:

```
sudo python setup.py install
```

## Using as CLI
This repository allows you to use the project as a CLI tool or as python module inside your script.
If you clone the repository you can execute the CLI, you need to navigate to the repository folder first. Once there, you can execute the CLI version with:

```
python -m mod_pbxproj <args>
```

_Note: If you installed it using pip, you can use the command above from any directory._

### CLI options
Currently the CLI only allows to add and remove flags on the project. It's a handy way to modify compilation or linking flags without the need of writing a full python script.

```
usage: Modify an xcode project file using a single command at a time.
       [-h] [-af AF] [-rf RF] [-b] project {Debug,Release,All}

positional arguments:
  project              Project path
  {Debug,Release,All}  Modify the flags of the given configuration

optional arguments:
  -h, --help           show this help message and exit
  -af AF               Add a flag value, in the format key=value
  -rf RF               Remove a flag value, in the format key=value
  -b, --backup         Create a temporary backup before modify
  -pp, --pure-python   Use the pure python parser
```

For instance, it you want to add the `-ObjC` flag to a project, remove `-all_load` from the same project, on all configurations, making a backup for security, execute:

```
python -m mod_pbxproj -b -af OTHER_LDFLAGS=-ObjC -rf OTHER_LDFLAGS=-all_load MyApp.xcodeproj/project.pbxproj All
```

## Basic usage
### Import the module
First thing you need to do, no matter if you copied the mod_pbxproj.py file to your project or you installed it using pip, you need to import the module in your script with:

```
from mod_pbxproj import XcodeProject
```
### Load & Write
#### Load a project file
Second thing to do, is open the file to start the modifications.

```
project = XcodeProject.Load('myapp.xcodeproj/project.pbxproj')
```

Here there is an optional parameter:

* pure_python: Boolean, that allows you use this project on non-mac machines. Because this feature is in experimental phase, use it under your own risk.

#### Create a backup
In case something goes wrong during the parsing or writing, is a good idea to make a backup before starting to do any modifications to the file.

```
project.backup()
```

The function receives 2 optional parameters:

* file_name: String, the path and name where the project should be backed up. Default is the same path that the project file.
* backup_name: String, the name of the backup file. Default is None, and will generate a timestamped version of the project file name.

#### Save the project
To save the changes in your project you need to call the save method:

```
project.save()
```

Here there is an optional parameters:

* file_name: String, a new path to save the project to.
* old_format: Boolean, forces to use the old XML format. This format is deprecated by Apple.
* sort: Boolean, forces to sort all entries in the project. Eases the source code control tasks, but changes the order of the files in the project tree.

### Groups
#### Create or get a group
Groups are logical folders inside the Xcode's project, you can search or create them if they don't exists with a single method call:

```
group = project.get_or_create_group('my folder')
```

The function receives 2 optional parameters:

* path: String, represents the relative physical path to the parent group. For instance, if your files are in Classes/Module/, and you want to add the Module group, path has to be 'Module'
* parent: String or PBXGroup object, represents the group that will act as the parent. if you want to add a group under another, you have to retrieve the parent first and pass it to this method as the parent.

#### Create groups recursively
This will recursively create groups and add the directory's contents to the project. You can optionally turn off the recursion.

```
project.add_folder('/path/to/folder')
```

You can supply an array of regular expressions for files you want to skip. This won't add any pdfs or mdown files found as it recurses.

```
project.add_folder('/path/to/folder', excludes=["^.*\.mdown$", "^.*\.pdf$"])
```

#### Remove group by ID
You need to have the ID of the group. The ID is a string of hexadecimal of 24 characters

```
project.remove_group('AF62C671190997D50075DD39')
```

Optionally, you can remove everything recursively

* recursive: Boolean, remove all children groups and files from the project. Default true.

#### Remove group by name
You can remove the group by it's human-readable name. 

```
project.remove_group_by_name('Classes')
```

Optionally, you can remove everything recursively

* recursive: Boolean, remove all children groups and files from the project. Default true.

_Caution: If many groups match the same name all will be removed as well._


### Files
#### Add files
To add new files to your project execute:

```
project.add_file_if_doesnt_exist('my folder/file.m')
```

This method contains the following optional paramters:

* parent: PBXGroup object, the group reference under the file will be listed in the project. None means Project Root.
* tree: String, indicating what filesystem should be used as a root. By default SOURCE_ROOT is used, meaning this project folder.
* create_build_files: Boolean, add this files to the build phase. By default, all files are added to the build phase.
* weak: Boolean, link the file as a required or weak reference. Only applies to frameworks and libraries.
* ignore_unknown_type: Boolean, when adding files that are unknown to the project an error is reported. That check can be overruled with this flag. Using this flag may lead to unexpected behaviors.

#### Add a library/framework
Libraries and Frameworks are the second most common assets added to a project. They are special files, they might have special requirements (minimum version to work, other system frameworks, etc). Also they have 2 types, system frameworks and 3rd party frameworks.

To add a system framework:

```
project.add_file_if_doesnt_exist('System/Library/Frameworks/AdSupport.framework', parent=frameworks, weak=True, tree='SDKROOT')
```

_parent_ can be either a group previously created/retrieved or an ID indicating the name of the group. In the example: `frameworks = project.get_or_create_group('Frameworks')`.
Most system frameworks are under the tree `SDKROOT` and the relative path is `System/Library/Frameworks/`.
System libraries reside under the `SDKROOT` as well but in a different path `usr/lib/`. For instance: `usr/lib/libsqlite3.0.dylib`

To add a 3rd party framework:

```
project.add_file_if_doesnt_exist('Libraries/MyFramework.framework', parent=frameworks, weak=True)
```

_parent_ can be either a group previously created/retrieved or an ID indicating the name of the group. In the example: `frameworks = project.get_or_create_group('Frameworks')`.
This will look up for the framework under the tree `SOURCE_ROOT` a.k.a. the project folder.

#### Remove files by ID
You need to have the ID of the file. The ID is a string of hexadecimal of 24 characters

```
project.remove_file('AF62C671190997D50075DD39')
```

#### Remove files by path
You can remove files by their physical path relative to the group. For instance, imagine 'Classes/Module/Header.h', if all groups are created properly to match the physical structure, you have to delete the file using: "Header.h". Au contraire, if the groups don't match the physical structure, you have to use the real relative path: 'Module/Header.h' or 'Classes/Module/Header.h' depending on the parent group.

```
project.remove_file_by_path('Header.h')
```

### Flags
#### Lists of flags
Another common task is to add compilation flags to the project. There are 2 convenient methods to add specific kinds of flags easily, "Other Compiler flags" and "Other Linker flags".

##### Compiler flags
Compiler flags are passed as they are defined down to the C compiler. If you want to enable/disable or define something you have to format your flag as the compiler expects it.

```
project.add_other_cflags('-DDEBUG=1')
```

or 

```
project.add_other_cflags(['-DDEBUG=1', '-DLOG=OFF'])
```

##### Linker flags
Linker flags are passed as they are defined to the linker. If you want to enable/disable or define something you have to format your flag as the compiler expects it.

```
project.add_other_ldflags('-ObjC')
```

or

```
project.add_other_ldflags(['-ObjC', '-all_load', '-fobjc-arc'])
```

##### Any other flags
The above methods are simple aliases of this method using the specific key to add the flags to.
To add any other flags, just specify the name of the flag and the values to be add to it.

```
project.add_flags('OTHER_LDFLAGS', ['-ObjC', '-all_load', '-fobjc-arc'])
```

##### Remove flags from a list of flags
Removing flags works exactly the same way as adding flags.

```
project.remove_flags('OTHER_LDFLAGS', ['-ObjC', '-all_load', '-fobjc-arc'])
```

#### Single-valued flags
The above methods will add/remove flags to a list of flags in your project file. If you would instead like to add/modify/remove a flag like `ENABLE_BITCODE` or `CLANG_ENABLE_MODULES`, which take a single value instead of a list of values, you can use these methods instead.

```
project.add_single_valued_flag('ENABLE_BITCODE', 'YES')
project.remove_single_valued_flag('CLANG_ENABLE_MODULES')
```

#### Only modifying some build configurations
All four generic `add`/`remove` methods also take an optional `configuration` parameter that can limit what build configuration to modify by name. By default, the methods modify all build configurations in the project.
