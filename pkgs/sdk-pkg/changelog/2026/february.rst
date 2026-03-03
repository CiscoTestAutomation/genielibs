--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * unconfig_standard_acl_for_ip_pim
            * unconfigure_igmp_version
            * unconfigure_ip_forward_protocol_nd
            * unconfigure_ip_igmp_join_group
            * unconfigure_ip_igmp_join_group_source
            * unconfigure_ip_igmp_snooping_last_member_query_interval
            * unconfigure_ip_igmp_snooping_tcn_flood
            * unconfigure_ip_igmp_snooping_vlan_mrouter_interface
            * unconfigure_ip_igmp_ssm_map
            * unconfigure_ip_igmp_ssm_map_query_dns
    * IOSXE
        * Updated unittests to new testing method
            * configure_crypto_ikev2_NAT_keepalive
            * configure_disable_nat_scale
            * configure_dynamic_nat_outside_rule
            * configure_dynamic_nat_pool_overload_route_map_rule
            * configure_dynamic_nat_route_map_rule
            * configure_dynamic_nat_rule
            * configure_enable_nat_scale
            * configure_ip_access_group_in_out
            * configure_nat64_interface
            * configure_nat64_nd_ra_prefix
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_ip_igmp_ssmmap_static
            * unconfigure_ip_msdp_vrf_peer
            * unconfigure_ip_multicast_routing_distributed
            * unconfigure_ip_pim
            * unconfigure_ip_pim_enable_bidir_enable
            * unconfigure_ip_pim_rp_address
            * unconfigure_ip_pim_ssm
            * unconfigure_ip_pim_vrf_ssm_default
            * unconfigure_ipv6_mld_access_group
            * unconfigure_ipv6_mld_join_group
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_ipv6_mld_snooping_enhance
            * unconfigure_ipv6_mld_snooping_vlan_mrouter_interface
            * unconfigure_ipv6_mld_snooping_vlan_static_interface
            * unconfigure_ipv6_mld_vlan
            * unconfigure_ipv6_mld_vlan_immediate_leave
            * unconfigure_ipv6_multicast_routing
            * unconfigure_ipv6_pim_rp_address
            * unconfigure_pim_register_source
            * unconfigure_static_ip_pim_rp_address
            * unconfigure_static_ipv6_pim_rp_address
    * IOSXE
        * Updated unittests to new testing method
            * C9500_24Y4C unconfigure_ignore_startup_config
            * C9500_48Y4C configure_ignore_startup_config
    * IOSXE
        * Updated unittests to new testing method
            * C9500_48Y4C/configure unconfigure_ignore_startup_config
            * spanning_tree/configure configure_spanning_tree_portfast
            * spanning_tree/configure unconfigure_spanning_tree_portfast
            * c9610/spanning_tree/configure configure_spanning_tree_portfast
            * c9610/spanning_tree/configure unconfigure_spanning_tree_portfast
            * C9800/configure configure_ignore_startup_config
            * C9800/configure unconfigure_ignore_startup_config
            * configure configure_tacacs_server
    * IOSXE
        * Updated unittests to new testing method
            * configure configure_ignore_startup_config
            * configure unconfigure_ignore_startup_config
            * cdp configure_cdp
            * cdp configure_cdp_holdtime
            * cdp configure_cdp_interface
            * cdp configure_cdp_neighbors
            * cdp configure_cdp_timer
    * IOSXE
        * Updated unittests to new testing method
            * configure_nat_pool
            * configure_nat_pool_overload_rule
            * configure_nat_port_route_map_rule
            * configure_nat_route_map
            * configure_nat_translation_max_entries
            * configure_nat_translation_timeout
            * configure_static_nat_network_rule
            * configure_static_nat_outside_rule
            * configure_static_nat_route_map_no_alias_rule
            * configure_static_nat_route_map_rule
    * Removed mock_data file for configure_standard_access_list and the above file as it is no longer needed for the new testing method

* iosxe
    * Modified configure_ip_host API
        * configure ip host to support multiple IP addresses.
    * Modified unconfigure_ip_host API
        * unconfigure ip host to support multiple IP addresses.
    * Added 3 new interface unconfigure APIs
        * unconfigure_interface_ip_redirect
            * Unconfigure ip redirect on interface
        * unconfigure_interface_ip_proxy_arp
            * Unconfigure ip proxy-arp on interface
        * unconfigure_interface_ip_unreachables
            * Unconfigure ip unreachables on interface
    * Modified API configure_ip_acl
        * Added support for source='any' parameter
    * Fixed the get_power_supply_status API to accept an optional command parameter.
    * Modified unconfigure_mac_acl
        * Added source and destination any condition handling while unconfiguring mac acl
    * Modified configure_ospfv3_network_range
        * Added bfd all-interfaces command under ospfv3 network range configuration
    * Modified configure_mac_acl
        * Added source and destination any condition handling while configuring mac acl
    * Modified configure_ipv6_ospf_bfd
        * Added disable parameter to configure bfd disable on interface
    * Modified unconfigure_ipv6_ospf_bfd
        * Added disable parameter to unconfigure bfd disable on interface
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_disable_dhcp_relay_information_option
        * test_api_disable_dhcp_smart_relay
        * test_api_disable_dhcp_snooping_glean
        * test_api_disable_ip_dhcp_auto_broadcast
        * test_api_enable_dhcp_compatibility_suboption
        * test_api_enable_dhcp_relay_information_option
        * test_api_enable_dhcp_smart_relay
        * test_api_enable_dhcp_snooping
        * test_api_enable_ip_dhcp_auto_broadcast
        * test_api_exclude_ip_dhcp
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_cts_role_based_sgt_map_vlan_list
        * test_api_unconfigure_dhcp_channel_group_mode
        * test_api_unconfigure_dhcp_pool
        * test_api_unconfigure_dhcp_relay_short_lease
        * test_api_unconfigure_dhcp_snooping_track_server_dhcp_acks
        * test_api_unconfigure_dhcp_snooping_verify_no_relay_agent_address
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_radius_attribute_policy_name_under_servergroup
        * test_api_configure_call_home_profile_destination_message_size_limit
        * test_api_configure_call_home_profile_destination_preferred_msg_format
        * test_api_configure_call_home_profile_destination_transport_method
        * test_api_configure_policy_map
        * test_api_configure_ignore_startup_config (c9300)
        * test_api_unconfigure_ignore_startup_config (c9300)
        * test_api_configure_ignore_startup_config (c9400)
        * test_api_unconfigure_ignore_startup_config (c9400)
        * test_api_configure_ignore_startup_config (C9500_24Y4C)
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_vlan_dot1q_tag_native (dot1q)
        * test_api_unconfigure_vlan_dot1q_tag_native (dot1q)
        * test_api_clear_access_session (dot1x)
        * test_api_clear_access_session_mac (dot1x)
        * test_api_config_identity_ibns (dot1x)
        * test_api_configure_access_session_acl_default_passthrough (dot1x)
        * test_api_configure_access_session_limit (dot1x)
        * test_api_configure_access_session_mac_move (dot1x)
        * test_api_configure_access_session_macmove_deny (dot1x)
        * test_api_configure_access_session_macmove_deny_uncontrolled (dot1x)
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_authentication_control_direction
        * test_api_configure_authentication_event_server
        * test_api_configure_authentication_open
        * test_api_configure_class_map_subscriber
        * test_api_configure_class_map_type_match_any
        * test_api_configure_class_map_type_match_none
        * test_api_configure_default_spanning_tree
        * test_api_configure_dot1x_cred_profile
        * test_api_configure_dot1x_supplicant
        * test_api_configure_enable_cisp
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_parameter_map
        * test_api_configure_parameter_map_subscriber
        * test_api_configure_radius_server_accounting_system
        * test_api_configure_service_policy
        * test_api_configure_service_template_with_absolute_timer
        * test_api_configure_service_template_with_access_group
        * test_api_configure_service_template_with_command_line
        * test_api_configure_service_template_with_description
        * test_api_configure_service_template_with_inactivity_timer
        * test_api_configure_service_template_with_redirect_url
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_service_template_with_sgt
        * test_api_configure_service_template_with_tag
        * test_api_configure_service_template_with_vlan
        * test_api_configure_template_methods_for_dot1x
        * test_api_configure_template_methods_using_max_reauth
        * test_api_unconfigure_access_session_acl_default_passthrough
        * test_api_unconfigure_access_session_limit
        * test_api_unconfigure_access_session_mac_move
        * test_api_unconfigure_access_session_macmove_deny
        * test_api_unconfigure_access_session_macmove_deny_uncontrolled
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_authentication_control_direction
        * test_api_unconfigure_authentication_event_server
        * test_api_unconfigure_authentication_open
        * test_api_unconfigure_autoconf
        * test_api_unconfigure_class_map_subscriber
        * test_api_unconfigure_dot1x_template
        * test_api_unconfigure_enable_cisp
        * test_api_unconfigure_parameter_map
        * test_api_unconfigure_parameter_map_subscriber
        * test_api_unconfigure_service_policy
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Updated the logic on all reference to verify_ignore_startup_config.
    * c9500
        * Removed the api to use the default iosxe api to unconfigure ignore startup config

* sdk-pkg
    * iosxe/rommon
        * Modified the device_rommon_boot api to handle switch number conflict during booting from rommon.

* nxos
    * Updated APIs to support standby devices
        * verify_file_exists
        * free_up_disk_space

* blitz
    * Updated parallel message return
        * Allows for custom messages or descriptions to be used in place of standard messages.

* iosxe/rommon
    * Updated the rommon_boot api to accept new params, timeout and grub_activity_pattern

* iosxe/cat9k/c9400
    * Modified execute_install_one_shot
        * Updated install one shot API dialog handling during reload

* iosxe/cat9k
    * Moved the `execute_set_config_register` api under cat9k/platform `execute.py`


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added api for configure_role_based_access_list
        * Added new api configure_role_based_access_list .
    * Added api for configure_cts_role_based_sgt_map_vrf
        * Added new api configure_cts_role_based_sgt_map_vrf .
    * Added api for unconfigure_cts_role_based_sgt_map_vrf
        * Added new api unconfigure_cts_role_based_sgt_map_vrf .
    * Added api for unconfigure_cts_sxp_export_import_group_option
        * Added new api unconfigure_cts_sxp_export_import_group_option .
    * Added api for unconfigure_cts_sxp_connection_peer
        * Added new api unconfigure_cts_sxp_connection_peer .
    * Added api for configure_cts_sxp_node_id
        * Added new api configure_cts_sxp_node_id .
    * Added api for unconfigure_cts_sxp_node_id
        * Added new api unconfigure_cts_sxp_node_id .
    * cat9k
        * Added configure_radius_server_accounting_system_host_config
        * Added unconfigure_radius_server_accounting_system_host_config
    * Added 4 new BFD template and interval management APIs
        * configure_bfd_template
            * Configure BFD single-hop template with interval parameters
        * configure_bfd_template_on_interface
            * Apply BFD template to a specific interface
        * unconfigure_bfd_template
            * Remove BFD single-hop template configuration
        * unconfigure_bfd_interval
            * Remove BFD interval configuration from interface
    * Added API for clear_sxp_filter_counters
        * Added a new API to clear sxp filter counters.
    * Added API clear_fqdn_database_fqdn
        * Added support for 'clear fqdn database fqdn' command in IOSXE devices.
    * Modified API clear_authentication_session
        * Updated to include support for 'clear authentication session interface' command.
    * Added API configure_ip_fqdn_acl
        * Added support for configuring IP FQDN ACLs in IOSXE devices.
    * clear_platform_software_fed_matm_stats
        * Added support for 'clear platform software fed matm stats' command in IOSXE devices.
    * Added API's to configure fqdn ttl-timeout-factor.
        * API to configure_fqdn_ttl_timeout_factor
        * API to unconfigure_fqdn_ttl_timeout_factor
    * Added configure_fpga_profile
        * API to configure fpga profile
    * Added configure_hsr_hsr_mode
        * API to configure hsr hsr mode
    * Added unconfigure_hsr_hsr_mode
        * API to unconfigure hsr hsr mode
    * Added configure_hsr_multicast_filter
        * API to configure hsr multicast filter
    * Added unconfigure_hsr_multicast_filter
        * API to unconfigure hsr multicast filter
    * Added configure_ip_dns_view_list
        * Added support for 'ip dns view-list' configuration commands.
    * Added unconfigure_ip_dns_view_list
        * Added support for 'ip dns view-list' unconfiguration commands.
    * Added configure_ip_dns_view
        * Added support for 'ip dns view' configuration commands.
    * Added unconfigure_ip_dns_view
        * Added support for 'ip dns view' unconfiguration commands.
    * Added configure_ip_host_vrf_view API
        * Added new api to configure ip host vrf view
    * Added unconfigure_ip_host_vrf_view API
        * Added new api to unconfigure ip host vrf view
    * Added unconfigure_fqdn_acl API
        * Added new api to unconfigure fqdn acl
    * Add configure_isis_passive_interface API
        * New API to configure 'passive_interface' on device.
    * Added iosxe sweep ping API support for the CLI command
        * New API support for 'sweep_ping' CLI command to support sweep ping on IOSXE devices.
        * New API support for 'config_interface_default_mtu' CLI command to config interface default mtu on IOSXE devices.
    * Added iosxe verigy interface state API support for the CLI command
        * New API support for 'verify_interface_state' CLI command to verify interface state on IOSXE devices.
    * Added clear_ptp_corrections API
        * API to clear ptp corrections
    * Added iosxe ip host view API support
        * New API support for 'configure_ip_host_view' CLI command to configure ip host view on IOSXE devices.
        * New API support for 'unconfigure_ip_host_view' CLI command to unconfigure ip
    * Added API clear_stealthwatch_cloud_data to clear swc data
    * Added 'configure_monitor' and 'unconfigure_monitor' to IOSXE monitor-configure.py
        * New API support for configure and unconfigure of 'monitor {option}' cli
    * Modified iosxe API for the CLI command
        * Modified API for 'unconfigure_cdp_interface' CLI command to unconfigure cdp interface on IOSXE devices.
        * Modified API for 'hw_module_sub_slot_stop' CLI command to hw module sub slot stop on IOSXE devices.
        * Modified API for 'hw_module_sub_slot_start' CLI command to hw module sub slot start on IOSXE devices.
        * Modified API for 'hw_module_sub_slot_oir_power_cycle' CLI command to hw module sub slot oir power cycle on IOSXE devices.

* api utils
    * Added API support in api utils
        * New API support for 'get_slot_num_by_interface' to get slot num by interface.

* powercycler module
    * Added
        * Support for power cycling of virtual machines in Proxmox environment.


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* blitz/yangexec
    * run_netconf
        * Add support for rpc operation in yangexec trigger.

* iosxe/rommon/utils
    * device_rommon_boot
        * Verify that all connections have left rommon state before  declaring the boot successful to avoid false success.


