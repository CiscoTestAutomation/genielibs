--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added SDK API support for
        * `subscriber service session-accounting`
        * `no subscriber service session-accounting`
        * `subscriber service target-atm-vc`
        * `no subscriber service target-atm-vc`
    * Added unit test coverage for the new helper APIs.
    * Added hw_module_session to iosxe-utils.py
        * New API support for 'hw_module_session {subslot}' cli
    * Added get_lldp_info
        * added api to get parsed output of 'show lldp'
    * Added get_lldp_interface_info
        * added api to get parsed output of 'show lldp interface'
    * Added get_lldp_interface_list
        * added api to get the list of interfaces with lldp enabled
    * Added get_lldp_neighbors_brief_info
        * added api to get parsed output of 'show lldp neighbors'
    * Added get_lldp_neighbors_interface_info
        * added api to get parsed output of
    * Added get_lldp_entry_info
        * added api to get parsed output of 'show lldp entry'
    * Added get_total_lldp_entries_displayed
        * added api to get total lldp entries displayed
    * Added get_lldp_traffic_info
        * added api to get parsed output of 'show lldp traffic'
    * Added get_lldp_error_info
        * added api to get parsed output of 'show lldp errors'
    * Added
        * configure_interface_macsec_dot1q API
    * Added
        * execute_change_directory API
    * cat9kv
        * Added send_break_boot API
    * Added
        * unconfigure_interface_macsec API
    * Added get_span_session_info
        * added api to get parsed output of 'show monitor session <session_id>'
    * Added get_span_session_running_config
        * added api to extract span session info from device running-config
    * Added collect_install_log API to collect install failure logs for c9800 device
    * Added SDK API support for
        * `clear vpdn history failure`
    * Added unit test coverage for the new helper API.
    * Added unconfigure_lldp_interface_only
        * added api to unconfigure lldp transmit/receive on a specific interface
    * Added configure_l2tp_class
        * added api to configure l2tp-class
    * Added unconfigure_l2tp_class
        * added api to unconfigure l2tp-class
    * Added remove_l2tp_class
        * added api to remove l2tp-class
    * Added SDK API support for
        * `simulator radius request 1 coa <profile_num>`
        * `simulator radius request 1 coa <profile_num> client <client_ip> host <host_ip>`
    * Added unit test coverage for the new simulator radius CoA request API.
    * Added
        * configure_plim_qos_in_map_ipv_tc_queue_strict_priority API
    * Added configure_aaa_authentication_ppp_default_type
        * added api to configure aaa authentication ppp default type
    * Added secure APIs
        * configure_username_secure
        * configure_enable_policy_password_secure
        * unconfigure_enable_policy_password_secure
        * configure_dot1x_cred_profile_secure
        * configure_credentials
        * configure_crypto
        * copy_startup_config_to_scp
        * copy_running_config_to_scp
        * configure_radius_server_secure
    * Added configure_local_span_source_and_get_output
        * added api to configure local span source interface and
    * Added configure_local_span_destination_and_get_output
        * added api to configure local span destination interface and
    * Added
        * configure_hw_module_slot_stop API
    * Added IOSXE SDK API support for
        * `clear_subscriber_session_all`
    * Added unit test coverage for the new API.
    * Added
        * execute_print_working_directory API
    * Added configure_virtual_ppp
        * added api to configure Virtual-PPP
    * Added unconfigure_virtual_ppp
        * added api to unconfigure Virtual-PPP
    * Added
        * clear_crypto_cryptotype API
    * Added generic IOSXE AAA SDK APIs
        * `configure_aaa_authentication`
        * `unconfigure_aaa_authentication`
        * `configure_aaa_authorization`
        * `unconfigure_aaa_authorization`
        * `configure_aaa_accounting`
        * `unconfigure_aaa_accounting`
    * Added unit test coverage for all new APIs.
    * Added
        * configure_clear_macsec_interface_statistics API
    * Added SDK APIs for L2 QoS configuration
        * configure_wrr_queue_bandwidth
        * unconfigure_wrr_queue_bandwidth
        * configure_wrr_queue_cos_map
        * unconfigure_wrr_queue_cos_map
        * configure_interface_switchport_priority_default
        * unconfigure_interface_switchport_priority_default
        * configure_interface_switchport_priority_override
        * unconfigure_interface_switchport_priority_override
        * configure_interface_switchport_priority_extend_cos
        * unconfigure_interface_switchport_priority_extend_cos
        * configure_interface_switchport_priority_extend_trust
        * unconfigure_interface_switchport_priority_extend_trust
    * Added unit test coverage for the new L2 QoS APIs.
    * Added
        * configure_interface_macsec API
    * cat9kv
        * Added configure_ignore_startup_config API.
    * Added IOSXE SDK API support for ISG control policy-map
        * `configure_policy_map_type_control_isg`
        * `unconfigure_policy_map_type_control_isg`
    * Added unit test coverage for the new APIs.
    * Added API execute_test_platform_software_command
    * Added API configure_power_redundancy
    * Added API unconfigure_power_redundancy
    * Added API configure_service_unsupported_transceiver
    * Added API unconfigure_service_unsupported_transceiver
    * Added
        * execute_fsck API
    * Added verify_show_lldp
        * added api to verify 'show lldp' output against expected values
    * Added verify_show_lldp_interface
        * added api to verify 'show lldp interface' output against
    * Added verify_show_lldp_traffic
        * added api to verify 'show lldp traffic' counters within min/max range
    * Added verify_show_lldp_error
        * added api to verify 'show lldp error' output safety
    * Added verify_lldp_entry
        * added helper api to verify a single lldp neighbor entry
    * Added verify_show_lldp_neighbors_detail
        * added api to verify 'show lldp neighbors detail' output
    * Added verify_show_lldp_entry
        * added api to verify 'show lldp entry' output against expected values
    * Added configure_interface_service_policy_type_control
        * New API for ``service-policy type control <policy_name>`` under an interface.
    * Added unconfigure_interface_service_policy_type_control
        * New API for ``no service-policy type control [policy_name]`` under an interface. ``policy_name`` is optional.
    * Added unconfigure_interface_ip_subscriber_initiator_type
        * New API for ``no initiator <type>`` under ``ip subscriber`` on an interface (e.g. ``dhcp``, ``radius-proxy``).
    * Enhanced configure_interface_ip_subscriber
        * Added support for ``initiator`` keyword to emit ``initiator <type>`` / ``initiator unclassified ...`` sub-commands under ``ip subscriber``.
    * Added configure_pseudowire_class
        * added api to configure pseudowire class
    * Added unconfigure_pseudowire_class
        * added api to unconfigure pseudowire class
    * Added IOSXE SDK API support for
        * `configure_policy_map_type_service_isg`
        * `unconfigure_policy_map_type_service_isg`
        * `configure_policy_map_type_control`
        * `unconfigure_policy_map_type_control`
    * Added unit test coverage for the new APIs.
    * Added
        * configure_mpls_ldp_advertise
        * unconfigure_mpls_ldp_advertise
        * configure_vpdn_multihop
        * unconfigure_vpdn_multihop

* ios
    * Added IOS SDK API support for
        * `configure_logging`
        * `unconfigure_logging`
        * `clear_logging`
    * Supports optional timestamp, queue-limit, rate-limit, buffer level
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * `execute_ping`
    * Added unit test coverage for the new API.
    * Added IOS SDK API support for
        * ``configure_interface_ip_dhcp_client``
            * Emits ``ip dhcp client <option> <type> [tag]`` under an interface (mirrors the iosxe API signature; supports e.g. ``ip dhcp client broadcast-flag clear``).
        * ``unconfigure_interface_ip_dhcp_client``
            * Emits ``no ip dhcp client <option> <type> [tag]`` under an interface (mirrors the iosxe API signature; supports e.g. ``no ip dhcp client broadcast-flag clear``).
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * ``configure_static_arp``
            * Emits ``arp <ip_address> <mac_address> ARPA`` globally.
        * ``unconfigure_static_arp``
            * Emits ``no arp <ip_address> <mac_address> ARPA`` globally.
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * ``create_dhcp_pool`` - creates ``ip dhcp pool`` with the
        * ``modify_dhcp_pool`` - adds or removes optional sub-commands
        * ``remove_dhcp_pool`` - removes the DHCP pool.
    * Added unit test coverage for the new APIs.

* added get powercycler config api to return the powercycler configuration for a given target.

* blitz
    * Added
        * Added execute extract support for parserless regex extraction with typed scalar and list values, optional defaults, count bounds, deduplication, sorting, and Blitz variable saving.
        * Added unit test coverage for execute extract success, failure, scope integration, include/exclude ordering, retry, and backward-compatible save handling.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * configure_policy_map_with_no_set_dscp
            * configure_policy_map_with_percent
            * configure_policy_map_with_police_cir_percentage
            * configure_policy_map_with_pps
            * configure_service_policy_with_queueing_name
            * configure_shape_map
            * configure_table_map_on_device
            * configure_table_map_values
            * unconfigure_bandwidth_remaining_policy_map
            * unconfigure_policy_map
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_prp_sup_vlan_aware
            * unconfigure_prp_sup_vlan_aware_allowed_vlan_list
            * unconfigure_prp_sup_vlan_aware_reject_untagged
            * unconfigure_prp_sup_vlan_id
            * unconfigure_prp_sup_vlan_tagged
            * configure_no_ptp_enable_on_interface
            * configure_ptp_8275_holdover_spec_duration
            * configure_ptp_announce_transmit
            * configure_ptp_enable_on_interface
            * configure_ptp_modes
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_policy_map_class
            * unconfigure_policy_map_class_parameters
            * unconfigure_policy_map_set_cos_cos_table
            * unconfigure_policy_map_shape_on_device
            * unconfigure_policy_map_type_service
            * unconfigure_policy_map_with_pps
            * unconfigure_policy_map_with_type_queue
            * unconfigure_service_policy_with_queueing_name
            * unconfigure_table_map_values
            * configure_ip_prefix_list_deny_permit
    * IOSXE
        * Updated unittests to new testing method
            * configure_policy_map
            * configure_policy_map_class
            * configure_policy_map_class_parameters
            * configure_policy_map_class_precedence
            * configure_policy_map_on_device
            * configure_policy_map_parameters
            * configure_policy_map_set_cos_cos_table
            * configure_policy_map_type_service
            * configure_policy_map_with_dscp_police
            * configure_policy_map_with_dscp_table
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_platform_mgmt_interface
            * unconfigure_platform_qos_port_channel_aggregate
            * unconfigure_policy_map_control_service_temp
            * unconfigure_process_cpu_statistics_limit_entry_percentage_size
            * unconfigure_process_cpu_threshold_type_rising_interval
            * unconfigure_qfp_drop_threshold
            * unconfigure_rep_admin_vlan
            * unconfigure_router_bgp
            * unconfigure_router_ospf
            * unconfigure_service_compress_config
    * IOSXE
        * Updated unittests to new testing method
            * configure_license_smart_proxy
            * configure_license_smart_transport_callhome
            * configure_license_smart_transport_cslu
            * configure_license_smart_url
            * configure_license_smart_url_cslu
            * configure_license_smart_usage_interval
            * configure_line_console
            * configure_platform
            * configure_smart_transport_url
            * unconfigure_call_home
    * IOSXE
        * Updated unittests to new testing method
            * config_policy_map_on_interface
            * config_qos_rewrite_dscp
            * config_replace_to_flash_memory
            * config_replace_to_flash_memory_force
            * configure_auto_qos
            * configure_auto_qos_global
            * configure_ip_access_list_with_dscp_on_device
            * configure_queue_sub_interface
            * copy_running_config_to_flash_memory
            * unconfig_qos_rewrite_dscp
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_auto_qos
            * unconfigure_auto_qos_global
            * unconfigure_policy_map_on_interface
            * config_standby_console_enable
            * configure_redundancy
            * unconfigure_redundancy
            * configure_fast_rep_segment
            * configure_rep_segment
            * unconfigure_fast_rep_segment
            * unconfigure_rep_segment
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_license_smart_url_cslu
            * unconfigure_license_smart_usage_interval
            * unconfigure_smart_transport_url
            * configure_class_map
            * configure_class_map_access_group_on_device
            * configure_traffic_class_for_class_map
            * unconfigure_class_map
            * config_policy_map_on_device
            * configure_bandwidth_remaining_policy_map
            * configure_hqos_policer_map
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_http_client_secure_trustpoint
            * unconfigure_http_client_source_interface
            * unconfigure_http_secure_trustpoint
            * unconfigure_ip_domain_name
            * unconfigure_ip_domain_timeout
            * unconfigure_ip_http_authentication_local
            * unconfigure_ip_http_secure_server
            * unconfigure_ip_http_server
            * unconfigure_license_smart_proxy
            * unconfigure_license_smart_transport
    * IOSXE
        * Updated unittests to new testing method
            * configure_ip_prefix_list_description
            * configure_ip_prefix_list_seq
            * configure_prp_static_vdan_entry
            * configure_prp_static_vdan_entry_with_vlan
            * configure_prp_sup_vlan_aware
            * configure_prp_sup_vlan_aware_allowed_vlan_list
            * configure_prp_sup_vlan_aware_reject_untagged
            * configure_prp_sup_vlan_id
            * configure_prp_sup_vlan_tagged
            * unconfigure_prp_static_vdan_entry
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_virtual_service
            * unconfigure_virtual_service_activate
            * configure_call_home
            * configure_exec_prompt_timestamp
            * configure_http_client_secure_trustpoint
            * configure_http_secure_trustpoint
            * configure_ip_domain_timeout
            * configure_ip_http_authentication_local
            * configure_ip_http_secure_server
            * configure_license_smart
    * IOSXE
        * Updated unittests to new testing method
            * configure_ptp_neighbor_propagation_delay_threshold
            * configure_ptp_priority
            * configure_ptp_role_primary
            * configure_ptp_source
            * configure_ptp_vlan
            * unconfigure_ptp_8275_holdover_spec_duration
            * unconfigure_ptp_announce_transmit
            * unconfigure_ptp_modes
            * unconfigure_ptp_neighbor_propagation_delay_threshold
            * unconfigure_ptp_vlan
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_license_smart_reservation
            * unconfigure_line_vty
            * unconfigure_macro_auto_global_processing
            * unconfigure_macro_auto_global_processing_on_interface
            * unconfigure_macro_auto_processing_on_interface
            * unconfigure_macro_auto_sticky
            * unconfigure_mdix_auto
            * unconfigure_parser_view
            * unconfigure_periodic_time_range
            * unconfigure_platform_acl_egress_dscp_enable

* iosxe
    * Modified verify_ignore_startup_config
        * Read ignore-startup-config from the active ROMMON variables.
    * Modified configure_vpdn_group
        * modified api configure_vpdn_group
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_configure_port_channel_lacp_max_bundle
        * test_api_configure_port_channel_standalone_disable
        * test_api_configure_power_efficient_ethernet_auto
        * test_api_configure_power_inline
        * test_api_configure_ppp_multilink
        * test_api_configure_pppoe_enable_interface
        * test_api_configure_print_timestamp_for_show_command
        * test_api_configure_scale_subintfs_via_tftp
        * test_api_configure_service_instance
        * test_api_configure_service_policy_type_queueing_on_interface
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Updated configure_management_master_key
        * Added logic to check if master key is already configured and skip configuration if any warning message return by device.
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_configure_ipv6_mtu
        * test_api_configure_ipv6_nd_dad_processing
        * test_api_configure_ipv6_nd_suppress_ra
        * test_api_configure_ipv6_prefix_name_on_interface
        * test_api_configure_mdns_on_interface_vlan
        * test_api_configure_medium_p2p_interface
        * test_api_configure_monitor_erspan_source_interface
        * test_api_configure_phymode_ignore_linkup_fault
        * test_api_configure_physical_interface_vmi
        * test_api_configure_portchannel_dpi_algorithm
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_unconfig_interface_ospfv3
        * test_api_unconfig_interface_ospfv3_cost
        * test_api_unconfig_interface_ospfv3_flood_reduction
        * test_api_unconfig_interface_ospfv3_network_type
        * test_api_unconfig_interface_prpchannel
        * test_api_unconfig_ip_domain_lookup
        * test_api_unconfigure_control_policies
        * test_api_unconfigure_crypto_map_on_interface
        * test_api_unconfigure_eapol_eth_type_interface
        * test_api_unconfigure_eui_64_over_ipv6_enabled_interface
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_configure_span_monitor_session
        * test_api_configure_sub_interface_encapsulation_dot1q
        * test_api_configure_sub_interface_range
        * test_api_configure_subinterface
        * test_api_configure_subinterface_second_dot1q
        * test_api_configure_switchport_mode_trunk_snooping_trust
        * test_api_configure_switchport_nonegotiate
        * test_api_configure_switchport_protected
        * test_api_configure_switchport_pvlan_trunk_allowed_vlan
        * test_api_configure_switchport_pvlan_trunk_native_vlan
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_vlan
        * test_api_configure_ip_dlep
        * test_api_configure_ip_on_atm_interface
        * test_api_configure_ip_on_tunnel_interface
        * test_api_configure_ip_unnumbered_on_interface
        * test_api_configure_ipv4_dhcp_relay_helper_vrf
        * test_api_configure_ipv6_address_config
        * test_api_configure_ipv6_address_on_hsrp_interface
        * test_api_configure_ipv6_enable
        * test_api_configure_ipv6_mld_static_group
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * modified existing APIs to secure
        * configure_masked_unmasked_enable_secret_password
        * unconfigure_system_disable_password_recovery_switch_all
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_switchport_access_vlan
        * test_api_configure_interface_switchport_block_address
        * test_api_configure_interface_switchport_dot1q_ethertype
        * test_api_configure_interface_switchport_port_security_violation
        * test_api_configure_interface_switchport_pvlan_and_native_vlan
        * test_api_configure_interface_switchport_pvlan_association
        * test_api_configure_interface_switchport_pvlan_mapping
        * test_api_configure_interface_switchport_pvlan_mode
        * test_api_configure_interface_switchport_trunk
        * test_api_configure_interface_template_sticky
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * management
        * Updated configure_ip_ssh_version API to support integer SSH version input.
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_snmp_trap_mac_notification_change
        * test_api_configure_interface_span_cost
        * test_api_configure_interface_span_portfast
        * test_api_configure_interface_span_vlan_priority
        * test_api_configure_interface_speed
        * test_api_configure_interface_speed_auto
        * test_api_configure_interface_split_horizon_eigrp
        * test_api_configure_interface_storm_control_action
        * test_api_configure_interface_storm_control_level
        * test_api_configure_interface_switchport
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified configure_replace
        * Added support for controller mode devices where 'configure replace' is not supported.
    * Modified configure_virtual_template
        * modified api configure_virtual_template
    * Modify iosxe port-settings API
        * API support error_pattern.
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_unconfigure_interface_access_session
        * test_api_unconfigure_interface_auth_vlan
        * test_api_unconfigure_interface_auth_vlan_no_resp
        * test_api_unconfigure_interface_authentication_violation
        * test_api_unconfigure_interface_bandwidth
        * test_api_unconfigure_interface_channel_group_auto_lacp
        * test_api_unconfigure_interface_dot1x_eap_profile
        * test_api_unconfigure_interface_dot1x_max_reauth_req
        * test_api_unconfigure_interface_dot1x_max_req
        * test_api_unconfigure_interface_dot1x_timeout_txp
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_configure_vrf_select_source
        * test_api_configure_vrrp_on_interface
        * test_api_configure_vrrp_version_on_device
        * test_api_disable_autostate_on_interface
        * test_api_disable_ipv6_address_dhcp
        * test_api_disable_ipv6_dhcp_server
        * test_api_disable_switchport_trunk_on_interface
        * test_api_enable_ipv6_address_dhcp
        * test_api_enable_ipv6_dhcp_server
        * test_api_enable_switchport_protected_on_interface
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Added APIs for EVPN Route Leaking with allow-evpn keyword
        * configure_vrf_export_ipv4_unicast_map_allow_evpn
        * configure_vrf_import_ipv4_unicast_map_allow_evpn
        * configure_vrf_export_ipv6_unicast_map_allow_evpn
        * configure_vrf_import_ipv6_unicast_map_allow_evpn
        * unconfigure_vrf_ipv4_unicast_map_allow_evpn
        * unconfigure_vrf_ipv6_unicast_map_allow_evpn
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_unconfigure_interface_duplex_mode
        * test_api_unconfigure_interface_flow_control
        * test_api_unconfigure_interface_inherit_disable
        * test_api_unconfigure_interface_ip_nbar
        * test_api_unconfigure_interface_ip_tcp_adjust_mss
        * test_api_unconfigure_interface_ip_verify_source
        * test_api_unconfigure_interface_ip_verify_unicast
        * test_api_unconfigure_interface_ipv6_tcp_adjust_mss
        * test_api_unconfigure_interface_ipv6_verify_unicast
        * test_api_unconfigure_interface_l2protocol_tunnel
    * Removed mock_data.yaml files for the above tests as they are no longer
    * BLITZ
        * Modified gnmi_util script
            * modified prefix handling when building GNMI Json
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_unconfigure_interface_rep_segment_edge_preferred
        * test_api_unconfigure_interface_rep_stcn_segment
        * test_api_unconfigure_interface_rep_stcn_stp
        * test_api_unconfigure_interface_service_policy
        * test_api_unconfigure_interface_snmp_trap_mac_notification_change
        * test_api_unconfigure_interface_span_cost
        * test_api_unconfigure_interface_span_vlan_priority
        * test_api_unconfigure_interface_speed
        * test_api_unconfigure_interface_storm_control_action
        * test_api_unconfigure_interfaces_on_port_channel
    * Removed mock_data.yaml files for the above tests as they are no longer
    * Fixed snmp / ssh configuration APIs
        * test_api_snmp_trap_type_regression
        * configure_snmp_server_trap
        * unconfigure_snmp_server_trap
        * unconfigure_snmp_server_group
        * unconfigure_snmp_server_user
        * configure_ip_ssh_version
    * Modified the following unit tests to use unittest.mock.Mock instead of
        * test_api_configure_switchport_trunk_allowed_vlan
        * test_api_configure_switchport_trunk_native_vlan
        * test_api_configure_switchport_trunk_native_vlan_tag
        * test_api_configure_switchport_trunk_vlan
        * test_api_configure_switchport_trunk_vlan_with_speed_and_duplex
        * test_api_configure_system_debounce_link_down_timer
        * test_api_configure_system_debounce_link_up_timer
        * test_api_configure_tunnel_with_ipsec
        * test_api_configure_uplink_interface
        * test_api_configure_vfi
    * Removed mock_data.yaml files for the above tests as they are no longer

* abstracted_libs
    * Modified processors
        * Added error_pattern support to pre_execute_command and post_execute_command.
        * Suppressed device-level execute error patterns when error_pattern is an empty list.
        * Preserved the original execute failure when reconnect recovery cannot be performed.

* blitz
    * Modified actions and markup
        * Hardened debug logging so unsafe output stringification does not fail actions.

* modified execute powercycler apis
    * Parallelized independent power_cycler entries for power on and power off operations.
    * Preserved existing single powercycler behavior.

* modified get powercycler apis
    * Uses get powercycler config API to return the powercycler object for a given device.

* powercycler
    * Modified SNMPv3 powercycler authentication handling to use credentials
    * Added unit test coverage for powercycler-scoped SNMPv3 credentials,

* iosxr
    * update the md5 check to use bash for calculating the hash.


--------------------------------------------------------------------------------
                                Mock_Device_Cli                                 
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                                     Needed                                     
--------------------------------------------------------------------------------


