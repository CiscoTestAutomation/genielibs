--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added telnet break option to device recovery using `console_breakboot_telnet_break` boolean

* clean
    * iosxr/ncs540
        * Added new stage install_image.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * IOSXR
        * Modified execute_copy_run_to_start api to support xr7 platform.(ncs540 device)
    * IOSXE
        * Moved the common reload clean stage to iosxe stage as it is specific for iosxe.
    * common
        * Removed rommon logic from reload stage.

* iosxe/sdwan
    * tftp_boot
        * Fixed issue with the regex.
    * expand_image
        * Added the timeout feature


