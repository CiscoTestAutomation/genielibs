--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* generic
    * Modified 'reload' clean stage, fixed check_modules logic

* iosxe/sdwan
    * Fixed 'image' handling in 'tftp_boot' stage
    * Updated ERROR_PATTERN in 'connect' stage
    * Changed clean stage name from 'controller_mode' to 'set_controller_mode'

* all
    * Modified CleanTestcase - Cisco Internal Change
        * Telemetry data collection now uses stage order instead of all defined stages
    * Modified CleanTestcase - Cisco Internal Change
        * Telemetry data is no longer collected in genie.libs.clean

* com
    * Modified copy_to_device stage
        * To reply to the overwrite prompt if the file exists when copying
    * Modified Device Recovery
        * Fixed a bug where break_count would default to None when it should be an integer.
    * Modified PingServer
        * To fix a bug where the server name would not be resolved into an IP address


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe/sdwan
    * added 'delete_inactive_versions' option to 'controller_mode' stage
        * delete inactive versions after changing software


