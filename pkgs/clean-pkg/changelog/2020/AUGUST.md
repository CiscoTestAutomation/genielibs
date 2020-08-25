August 2020
==========

August 25
--------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.8         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* COM
    * Updated copy_to_linux:
        * added 'rename_images' argument to rename images

* IOSXE
    * Added install_image stage:
      * installs an image using 'install mode'
    * Added install_packages stage:
      * installs provided packages/SMUs onto device
    * Added schema to image handler:
      * Will verify images schema before running

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* COM
    * Modified connect stage:
        * To use prompt_recovery
    * Fixed not being able to use a stage more than once
    * Fixed the exit code in case clean fails
    * Modified ImageHandlers:
      * to have better error messages if the structure of images is invalid
    * Modified reload stage:
      * removed 'reload_file' argument
      * to allow any unicon reload service variables
    * Modified copy_to_linux:
      * to dynamically trim server.path from image path
    * Modified copy_to_device:
      * to dynamically trim server.path from image path
    * Modified:
        * All unittest filenames
        * Fixed broken symlinks in unittests
        * Fixed broken unittests
    * Modified validate_schema:
        * Changed name to validate_clean
        * Removed raising exceptions now returns warnings and exceptions instead

* IOSXE
    * Modified:
      * change_boot_variable to save run to start after deleting existing variables

* UTILS
    * Modified remove_string_from_image:
      * Removed the default 'tftpboot/' from the 'string' argument