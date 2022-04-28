--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified
        * Fixed device recovery issue after power cycling and booting golden image
    * Modified
        * Fixed device recovery issue on vwlc where wrong image is booted
    * cat9k
        * Added enable_boot_manual execution step for tftp boot stage
        * Updated the unittest for tftp boot
    * Install_image
        * add dialog and error pattern for install failing.
    * Modify image hander, upload reload service arguments with image_to_boot

* clean/tests
    * updated the symlink for platforms which were not added

* iosxr
    * Added new api execute clear platform_hardware fed active qos statistics interface
        * to clear qos statistics on interface

* utils
    * Modify validate_clean API
        * Fixed a bug when clean_data[section] is None and clean_data[section].pop is called
        * Changed clean class string to be snake case during clean-file validation to properly compare clean stages and their classes

* generic
    * Modify recovery processor, only recover device if it has been connected


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_policy_map API
        * configuring policy map
    * CAT9K
        * Added rommon_boot stage


