--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean/stages/deletefiles
    * Added timeout parameter to delete_files method to specify timeout for delete operation.

* iosxe
    * RommonBoot Stage
        * Added retry functionality for TFTP boot with configurable tftp_boot_max_attempts and tftp_boot_sleep_interval parameters
        * Default 3 attempts with 30 second intervals between retries
        * Applies to iosxe, cat9k, and ie3k platforms

* iosxe/cat9k/stackwise_virtual
    * New stage for StackWise Virtual configuration

* clean-pkg
    * Added image handler for RommonBoot stage to set image in rommon_boot section
    * iosxe/cat9k
        * updated the schema to make image as Optional parameter in RommonBoot stage


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean-pkg
    * Added support for new flag overwrite_if_size_different to allow conditional overwriting only when the existing file’s size differs.

* iosxe
    * RommonBoot Stage
        * Improved ROMMON TFTP logging to report each ROMMON variable as it is set, making ROMMON boot failures easier to debug.

* clean/iosxe/test_connect_device_rommon
    * Removed the extra comma in the FIND_BOOT_IMAGE setting to fix the UT.

* installimage stage
    * N9k
        * Added check_reload logic to detect if device auto reloads after image install and wait for device to reload.

* clean
    * IOSXE - ResetConfiguration
        * Re-initialize init commands after rollback in case they were removed

* clean/recovery/recovery
    * Added a check to verify the boot manual recovery process.


