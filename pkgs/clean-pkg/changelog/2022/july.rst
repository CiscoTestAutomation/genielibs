--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* genie.libs.clean.stages
    * CopyToLinux stage
        * Added optional key to protocol to resolve ValueError Clean schema check failed in clean yaml file

* clean
    * Modified Reload stage
        * Pass expected arguments to device.initiate()

* recovery
    * _disconnect_reconnect
        * Added condition to check if the device is in rommon

* apis/verify
    * verify_connectivity
        * Added condition to check if the device is in rommon

* iosxe
    * Modified image handler to allow image override by stage
    * Fixed image management for reload stage
    * Modified InstallImage in Clean Stages
        * Removed line where show clock was being appended to packages.conf

* genie.libs.clean
    * Updated reload stage
        * fix the issue for replay object for returning mock object when accessing


