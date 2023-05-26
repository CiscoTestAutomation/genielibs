--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* generic
    * Added configure_management clean stage


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * Updated VerifyRunningImage clean stage to allow user to ignore flash directories
    * Added clean stage for cat9k to ignore flash directories by default

* iosxe
    * Modified the logic to pick the golden_image if the clean fails with a crash image.


