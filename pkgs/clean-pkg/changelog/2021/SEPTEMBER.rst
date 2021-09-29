--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* all
    * Modified copy_to_device
        * copy_to_device stage now supports arguments unique_file_name, unique_number, and rename_images

* iosxr
    * Updated `install_image_and_packages` clean stage to install packages with local file path
    * Added `source_directory` option for `install_image_and_packages` clean stage

* utils clean
    * Modified remove_string_from_image
        * Added condition to check unwanted removal of string from image path.

* iosxe
    * Modified install_image stage
        * changed the error_pattern['Failed'] to append_error_pattern['Failed']

* modified imageloader & imagehandler
    * added support for arbitrary extra files under the extra attribute


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* nxos
    * Added execute_delete_boot_variable
        * added the execute_delete_boot_variable api for nxos n3k

* viptela(sd-wan controllers)
    * Added pyATS Clean support for SD-WAN Controllers (vManage/vBond/vSmart)

* all
    * Modified CleanTestcase - Cisco Internal Change
        * Added telemetry data collection within __iter__()

* iosxe/sdwan (cedge devices)
    * Added pyATS Clean support for IOSXE/SDWAN cEdge devices

* iosxe
    * Added tftp_boot stage for cat9k

* major infrastructure overhaul
    * Clean stages have been converted from a function into a class which provides the following benefits
        * **Class inheritance** - Prevents duplicated code, duplicated work, and duplicated bugs due to copy and pasting existing code to make a small modification.
        * **Tests** - With class based stages, each step in the stage is it's own method. This provides the ability to mock up and test small steps of a stage to get complete code coverage. In turn better unittest means less bugs.
        * **Execute clean stages within scripts** - Due to the redesign it is possible to execute clean stages within your scripts (Highly asked for)! In the near future we will release an easy-to-use method for calling these stages (similar to device.api).
        * **100% backwards compatible** - From a user point of view, the clean yaml file and usage is still the exact same. Nothing changes from a user point of view as we do not want to break anyone.
    * Soon to come
        * Method to easily execute clean stages within a script
        * New developer documentation


