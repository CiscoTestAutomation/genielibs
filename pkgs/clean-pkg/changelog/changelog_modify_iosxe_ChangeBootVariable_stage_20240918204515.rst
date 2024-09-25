--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOSXE
    * Modified ChangeBootVariable:
        * Modified verify_boot_variable to verify next reload boot variables using running image if current_running_image is True
