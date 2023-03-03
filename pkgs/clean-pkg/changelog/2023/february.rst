--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* linux
    * Added
        * New clean stages were added for wsim under linux.
    * Added configure_controller_details
        * API Configures the controller details on wsim
    * Added configure_ap_details
        * API Configures the ap details on wsim
    * Added configure_client_details
        * API Configures the client details on wsim
    * Added run_wsim_config
        * API that runs the configs on wsim
    * Added configure_ap_client_count
        * API Configures the ap client count details on wsim
    * Added simulate_ap_container
        * API simulates the containers on wsim
    * Added verify_ap_associate
        * API verify ap join status on wsim

* iosxe
    * Added configure_switch_provision_model
        * API unset switch provision
    * Added configure_snmp_server_manager
        * API set snmp server manager
    * Added unconfigure_event_manager_applet
        * API to unset event manager applet
    * Added configure_event_manager_applet
        * API to set event manager applet
    * Added configure_power_inline_auto_max
        * API to power inline auto max


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* common
    * Updated 'apply_configuration' clean stage
        * added dialog to handle prompt by `license accept end user agreement`


