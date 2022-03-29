--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* utils
    * Modified load_clean_json function
        * Now it only loads the first time called and save the data in a global variable. Any consecutive calls will just return that data instantly.

* iosxr
    * Modified VerifyRunningImage
        * Fixed a bug in the version comparison

* iosxe
    * Modified device recovery grub menu logic
        * To support more device types


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cheetah
    * Added new clean stage erase_ap_configuration
        * Erases the configurations on AP
    * Added new clean stage prime_ap
        * Primes the AP to controller and validates it joined the right controller.


