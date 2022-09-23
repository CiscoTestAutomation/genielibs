--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* generic
    * Added ``delete_files`` clean stage
    * Added ``execute_command`` clean stage

* genie.libs.clean.templates
    * nxos
        * add DEFAULT clean template

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified reload clean stage
        * Fixed issue with reconnect_via argument
* iosxe
    * Modified install_image clean stage
      * Added `reload_service_args`
      * Change check for packages.conf to use tclsh
      * Updated regex pattern for same image file
    * Modified power_cycle clean stage
      * Added `sleep_before_connect` option
      * Added `connect_arguments` option
      * Added `connect_retry_wait` option
* iosxe/template
    * Modified:
        * Added placeholders for iosxe clean template
* genie.libs.clean.templates
    * iosxe:
        * Fix typos in DEFAULT clean templates

* genie.libs.clean.stages
    * modified:
        * allow PowerCycle clean function to be referred to by 'power_cycle' and 'powercycle'
    * Modified
        * Fixed issue with reconnect_via argument in reload clean stage


