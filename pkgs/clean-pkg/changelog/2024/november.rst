--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean-pkg
    * iosxe
        * Added default `LOAD_IMAGE` template
    * iosxe
        * image_handler
            * check if smu image is passed instead of base image in the image list
        * Skip `install_image` if smu only image passed.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages/iosxe
    * install image
        * Ensure startup config is verified if install image is skipped.
    * install image
        * Updated _check_for_member_config to handle install image stage.

* iosxe
    * Modified clean stages
        * Fixed the usage of steps in the clean stages to ensure correct result rollup
    * Modified copy_to_device
        * Skip verifying free space on the device if skip_deletion is set to True

* apic
    * Modified copy_to_device
        * Skip verifying free space on the device if skip_deletion is set to True

* generic
    * Modified copy_to_device
        * Skip verifying free space on the device if skip_deletion is set to True

* recovery
    * Modified recovery_processor
        * Removed unused params from docstring


