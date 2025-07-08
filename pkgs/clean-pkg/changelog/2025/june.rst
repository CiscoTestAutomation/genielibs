--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * modified reset configuration clean stage
        * Keep aaa new-model config, default enable auth to none
    * modified apply_configuration stage
        * Added show running-config / show startup-config
    * remove_smu_image
    * Updated clean stages to use syslog statement to ensure syslog messages are captured during execution.
    * connect
        * Boot device from ROMMON has been modified to reflect a 'failed' status instead of 'passx' when an exception occurs

* clean-pkg
    * iosxe
        * Updated the check_reload_dialog pattern list for install image stage

* clean/iosxe/stages
    * Modified the Rommon Boot stage
    * Modified the Rommon Boot stage

* os/iosxe
    * Modified rommon boot stage
        * deprecated the tftp argument
    * Modified reset configuration
        * add no platform console virtual to KEEP dictionary
    * Modified InstallImage stage
        * Updated the image matching logic to match the build label first and then xe_version.
        * Added new steps for Verify the ignore startup configs.


