--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe/copy_to_device
    * Added md5 verification before copying the image to the device.

* stages
    * Install image reloads to Press Enter key add a statement to handle return key after the image reloads.

* iosxe
    * Modified clean connect to handle exhaused credentials error and trigger password recovery

* clean-pkg
    * Added delay after applying configuration to the device
    * iosxe
        * Updated the logic to work for ha/stack device in install image and install SMU stages
        * Increased the timeout to 3 minutes since by default the image take time to be applied.

* iosxe/connect
    * Removed duplicate configure rommon variable in connect stage.


