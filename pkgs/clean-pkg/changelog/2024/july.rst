--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified
        * Added prompt-level none to image install command


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Recovery
        * Refactored Recovery logic to use send_break_boot api.
    * Reload
        * Updated logic todo Reload when the boot variable is not set.
    * Modified InstallRemoveInactive
        * Added new parameter force_remove to remove inactive package forcefully
    * Added dialog
    * api
        * Added condition for golden image


