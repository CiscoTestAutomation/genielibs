--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified InstallImage
        * Updated the logic for the device to reload if it does not do auto reload after installing the image


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean-pkg
    * iosxe
        * Modified CopyToDevice
            * Added check not to skip copy_to_device when smu image is provided

* iosxe
    * Modified InstallImage
        * In the show version parsed output, we don't have a 'mode' key. Instead, we have an 'installation_mode' key, from which we retrieve the 'installation_mode' value.

* clean
    * Add quad support
    * Reverted the changes to reload with service wrapper
    * Changed breakout interface behaviour in ConfigureInterfaces stage


