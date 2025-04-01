--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified ChangeBootVariable
        * Removed duplicate code from verify_boot_variable step

* clean-pkg
    * iosxe
        * set the step as passx if ignore stratup config fail.
    * Fix syntax warning


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean-pkg
    * iosxe
        * Remove the unused key `reload_timeout` from `install_smu`
    * iosxe
        * Added hot smu support for `install_remove_smu` and `install_smu` stage
    * iosxe
        * Added multiple smu support for `install_remove_smu` and `install_smu` stage

* iosxe
    * Added
        * ChangeBootVariable for IE3K


