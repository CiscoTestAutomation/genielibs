--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified test_configure_replace_pass_rollback_complete
        * Added command show version | include operating mode to check for controller mode devices.
    * Modified InstallRemoveSmu clean stage
        * Re-applied connection initialization commands after SMU reload to
    * Modified image_handler
        * Use the copy_to_linux destination when copy_to_device receives an overridden image.
    * Modified InstallImage clean stage
        * Added save running-config after unconfiguring system ignore startup
        * Read debug config from active ROMMON variables.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added ConfigureNetconfYang stage
        * Configure NETCONF-YANG options and verify process readiness.
    * Added VerifyNetconfProcesses stage
        * Validate NETCONF process state and datastore synchronization.

* iosxe/nxos/iosxr
    * Added roomon boot for the power cycle stage
        * Use the golden image to boot device after power cycle


