--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * recovery
        * update the recovery process to use state machine for bringing device to enable state
    * iosxe/connect
        * Password Recovery did not kick in if the fallback credential did not work.
    * recovery/iosxe
        * update the recovery process to update grub_boot_image if there is grub activity pattern
    * iosxe/stages
        * Handled the variable total_size when the size of the filedata returns
    * recovery
        * update the recovery process to use multi threading and handling grub menu for device recovery

* iosxe
    * Added new dialog to handle reload patterns


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* iosxe
    * Added exception handler for enable authentication failure to trigger recovery.


