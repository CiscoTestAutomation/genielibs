--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Add API configure_breakout_cli
        * Added the timeout for the Proc
    * Add API unconfigure_breakout_cli
        * Added the timeout for the Proc
    * Add API configure_mode_change
        * Added the timeout for the Proc
    * Added API config_qinq_encapsulation_on_interface
        * This API configures dot1q encapsulation on an interface with double tagging (Q-in-Q).
        * Takes device, interface, VLAN, and second VLAN as arguments.
        * Applies the encapsulation configuration to the specified interface.
        * Raises SubCommandFailure in case of errors during the configuration.
    * Added configure_sub_interface_range
        * API for configure the sub interface range
    * Added configure_interface_range_switchport_mode
        * API for configure the interface range switchport mode
    * Added shutdown_sub_interface_range
        * API for shutdown the subinterface range
    * Added shutdown_interface_range
        * API for shutdown the interface range
    * Added no_shut_interface_range
        * API for un shut the interface range
    * Added no_shut_sub_interface_range
        * API for un shut the subinterface range
    * Added configure_sub_interface_encapsulation_dot1q
        * API for configure_sub_interface_encapsulation_dot1q
    * Added configure_ip_ssh_client_algorithm_mac
    * Added configure_ip_ssh_client_algorithm_kex
    * Added configure_ip_ssh_client_algorithm_encryption
    * c8000v
        * Added configure_autoboot API
    * Added configure_datalink_flow_monitor
        * New API to configure datalink flow monitor
    * Added unconfigure_datalink_flow_monitor
        * New API to unconfigure datalink flow monitor
    * Added configure_ipv6_nd_cache_expire
        * New API to configure ipv6 nd cache expire {timeout}
    * Added unconfigure_ipv6_nd_cache_expire
        * New API to unconfigure ipv6 nd cache expire
    * Added configure_policy_map_class
        * API to configure policy map class
    * Added configure_interface_span_portfast
        * API to configure interface portfast
    * Added execute_issu_set_rollback_timer API
        * Added API for execute_issu_set_rollback_timer
    * Added unconfigure_issu_set_rollback_timer API
        * Added API for unconfigure_issu_set_rollback_timer
    * Added API test_platform_software_usb_fake_insert_remove
        * Added API to test_platform_software_usb_fake_insert_remove
    * Added API configure_aaa_authentication_enable_default_group_enable
        * Added API to configure_aaa_authentication_enable_default_group_enable
    * Added API configure_aaa_authentication_login_default_group_local
        * Added API to configure_aaa_authentication_login_default_group_local
    * Added API configure_aaa_authorization_exec_default_group_if_authenticated
        * Added API to configure_aaa_authorization_exec_default_group_if_authenticated
    * Added API configure_aaa_authorization_network_default_group
        * Added API to configure_aaa_authorization_network_default_group
    * aaa
        * configure
            * configure_aaa_accounting_network_default_start_stop_group
                * Args
            * unconfigure_aaa_accounting_network_default_start_stop_group
                * Args
            * configure_aaa_accounting_identity_default_start_stop_group
                * Args
            * unconfigure_mab_on_switchport_mode_access_interface
                * Args
            * configure_mab_eap_on_switchport_mode_access_interface
                * Args
    * Added monitor_event_trace_dmvpn_nhrp_enable
        * API for monitor event trace dmvpn nhrp enable
    * Added monitor_event_trace_dmvpn_nhrp_clear
        * API for monitor event trace dmvpn nhrp clear
    * Added configure_phymode_ignore_linkup_fault
    * Added unconfigure_phymode_ignore_linkup_fault
    * Added configure_system_debounce_link_up_timer
    * Added configure_system_debounce_link_down_timer
    * Added unconfigure_system_debounce_link_up_timer
    * Added unconfigure_system_debounce_link_down_timer
    * Added configure_default_spanning_tree_vlan
        * API to configure default spanning tree vlan.
    * Added configure_ip_ssh_server_algorithm_mac
    * Added configure_ip_ssh_server_algorithm_kex
    * Added configure_ip_ssh_server_algorithm_encryption
    * Added configure_ip_ssh_server_algorithm_hostkey
    * Added new API get_boot_variables for IE3K devices
        * get_boot_variables - Get boot variables for IE3K devices

* util
    * Added configure_peripheral_terminal_server
        * API for configure speed for line of terminal server in the testbed
    * Added configure_terminal_lines_speed
        * API for configure speed of a line

* utils
    * Added configure_management_console api
        * New api for configuring speed on console

* apis
    * iosxe/asr1k
        * Added new api configure_boot_manual.
    * iosxe
        * cat9k
            * utils
                * Added new api password_recovery.
            * configure
                * Added new api configure_ignore_startup_config.
                * Added new api unconfigure_ignore_startup_config.
            * verify
                * Added new api verify_ignore_startup_config.
        * rommon/utils
            * Added new api send_break_boot.

* sdk-pkg
    * update `pysnmp-lextudio==6.1.2` to avoid deprecation issues


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Updated API get_boot_variables
        * Handled a scenario were current/next boot variable not found in parser output
    * Fixed enable_usb_ssd_verify_exists
        * command provided is incorrect. Fixed the show command to display the correct output.
    * Fixed install_wcs_enable_guestshell
        * API call is incorrect. Fixed the API call to enable the guestshell.
    * Fixed save_device_information
        * Added try except block to handle the exception since the configureation is no more applicable to latest iosxe

* nxos
    * Added virtual peer link attributes in vPC Domain
        * virtual_peer_link_dst_ip = '2.2.2.2'
        * virtual_peer_link_src_ip = '2.2.2.1'
        * virtual_peer_link_dscp = 56

* sdk
    * verifcation
        * Updated verifcation file to address moved parsers

* apis
    * Modified `verify_is_syncing_done` API
        * Renamed API to verify_yang_is_syncing_done, deprecate `verify_is_syncing_done`
        * Added namespace


