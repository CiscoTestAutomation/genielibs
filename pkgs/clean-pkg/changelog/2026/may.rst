--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages
    * Updated delete_files stage to handle SchemaEmptyParserError when directory does not exist or is empty on the device

* clean
    * Modified get_clean_function
        * Added abstract deprecation context to clean stage lookup results so

* iosxe
    * Connect stage
        * Added handling for UniconAuthenticationError and CredentialsExhaustedError during reconnect to trigger password recovery via device.api.password_recovery.

* nxos
    * n7k/platform
        * Updated ChangeBootVariable save handling to automatically use
    * n9k/platform
        * Updated ChangeBootVariable save handling to automatically use
    * clean/stages/nxos
        * Updated NX-OS boot variable delete APIs to save running-config to
    * n3k/platform
        * Updated NX-OS boot variable delete APIs to save running-config to
    * n5k/platform
        * Updated NX-OS boot variable delete APIs to save running-config to
    * mds/platform
        * Updated NX-OS boot variable delete APIs to save running-config to


