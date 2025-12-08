--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean-pkg
    * Added support to block copy operations if the target file size does not match.

* rommonboot stage
    * iosxe
        * Removed duplicate task function.
    * cat9k
        * Removed device.destroy() call and added device.sendline() in the rommon boot stage so that the device reaches the rommon prompt.

* clean-pkg/stages
    * Added the reset of the rollup flag when recovery is enabled
    * Updated the api configure_management to able to skip for missing attribute instead of failing complete stages.

* iosxe
    * clean-pkg/utils
        * Fixed issue with updating protected file for image


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean/recover
    * Added power cycle retry mechanism to enhance reliability during device recovery.
    * Updated the console speed configuration in case of failiure connection to device


