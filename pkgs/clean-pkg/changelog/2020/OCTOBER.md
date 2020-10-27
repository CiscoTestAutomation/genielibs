October 2020
============

October 27
----------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.10        |

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------
* IOSXE
    * Modified tftp_boot stage:
        * To properly wait for device to start reloading
        * Removed 'device_reload_sleep' argument
        * Removed stage skipping if device_recovery had already run
    * Modified install_image stage:
        * To fix script hanging due to regex mismatch
    * Modified install_packages stage:
        * To fix script hanging due to regex mismatch
    * Modified install_image_and_packages stage:
        * to use a modified timeout for 'install activate id' command
    * Modified device_recovery:
        * To handle edge case scenarios in rommon mode
        * To boot the correct image when using 'golden_image'
* IOSXR
    * Modified install_image_and_packages stage:
        * To fix script hanging due to different device output
    * Modified tftp_boot stage:
        * Removed stage skipping if device_recovery had already run
* COM
    * Modified recovery to handle prompt interactions with both kickstart and system image
    * Modified apply_configuration stage schema to support 'configure_replace'
    * Fixed clean failing after device_recovery recovers the device
    * Modified apply_configuration stage:
        * To support configure replace
        * To support hostname changes when configuring by file
    * Modified reload stage:
        * To use prompt-recovery when reconnecting
* STAGES
    * Modified connect stage:
        * Added max_timeout and interval parameters
        * Allows function to retry connection if it fails
* NXOS
    * Modified tftp_boot stage:
        * Removed stage skipping if device_recovery had already run


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------
* NXOS
    * Added support for N3K platform
* LINUX 
    * Added clean stage: revert_vm_snapshot
* COM
    * Moved all recovery code from clean/stages into clean/recovery
* IOSXE
    * IOSXE Grub Menu are now supported for pyATS Clean
    * Added install_remove_inactive stage
* PLEASE FOLLOW THE TEMPLATE.
* ADDED `PYATSDEVICECLEAN` MODULE FOR USE INSIDE `CLEANERS` SECTION OF THE CLEAN YAML. THIS ALLOWS USE OF BOTH PYATS CLEAN AND UNICLEAN SIMULTANEOUSLY.


