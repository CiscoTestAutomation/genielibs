--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * Modified iosxe.stage.Connect.connect
        * Set learn hostname to False after hostname learned
    * Modified tftp_device_recovery
        * If username and password are not provided, use default username and password

* utils
    * Modified validate_clean to not raise any exceptions on passing image_management to clean yaml file


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified
        * Allowing a config_register option in RommonBoot stage, with a default of 0x0
    * Added
        * Added support for quad sup devices in clean to connect the active and standby
    * Modified Clean Connect
        * Added check for console speed being incorrect as well as a fix
