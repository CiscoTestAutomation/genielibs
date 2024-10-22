--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean-pkg
    * iosxe
        * image_handler
            * Update clean schema to handle smu images
        * Added new clean stages `install_smu`, `install_remove_smu`


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * Modified recovery_worker
        * Changed to use `device_rommon_boot` for TFTP booting
    * Modified device_rommon_boot
        * Changed it to try and use TFTP_BOOT environment variable if TFTP path is too long


