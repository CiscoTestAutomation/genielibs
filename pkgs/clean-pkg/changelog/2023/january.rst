--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

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
    * Added
        * New clean stage Verify HA state under c9800


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* common
    * Added `mgt_itf`` in NOT_A_STAGE
    * Updated 'apply_configuration' clean stage
        * added `error_pattern` argument to pass it to device.configure()

* cheetah
    * Modified
        * Increase sleep timeout in EraseApConfiguration since certain AP MODELS take extra time to reload.

* iosxe
    * Modified
        * Changed trustpoint name to device.hostname since sometimes hostname differs from name.


