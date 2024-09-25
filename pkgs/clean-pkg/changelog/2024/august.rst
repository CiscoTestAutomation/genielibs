--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * connect stage
        * add password recovery for connect stage.

* clean-pkg
    * updated the default keep configuration


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * set controller mode stage
        * the stage is now working properly fix the issue with stage and reload stage
    * Modified install_image
        * Added new flag skip_save_running_config to skip the step to save the the running configuration to the startup config.

* generic
    * Modified configure_management
        * Added `alias_as_hostname` argument
        * Allows user to use the alias as the device hostname
