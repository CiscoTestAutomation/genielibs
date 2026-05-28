--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * configure_stack_power_mode_redundant
            * configure_stackpower_stack
            * configure_stackpower_stack_switch_standalone
            * configure_stack_power_switch
            * configure_stack_power_switch_no_standalone
            * configure_stack_power_switch_power_priority
            * configure_stack_power_switch_standalone
            * configure_switch_provision_model
            * configure_system_disable_password_recovery_switch_all
            * configure_system_ignore_startupconfig_switch_all
    * IOSXE
        * Updated unittests to new testing method
            * configure_snmp_mib_bulkstat_transfer
            * configure_snmp_server_contact
            * configure_snmp_server_location
            * configure_snmp_server_manager
            * configure_software_auto_upgrade
            * configure_source_template
            * configure_stack_power_auto_off
            * configure_stack_power_default_mode
            * configure_stack_power_ecomode
            * configure_stack_power_mode_power_shared
    * IOSXE
        * Updated unittests to new testing method
            * stack_ports_enable_disable
            * unconfig_cns_agent_password
            * unconfigure_absolute_time_range
            * unconfigure_archive_logging
            * unconfigure_archive_maximum
            * unconfigure_archive_path
            * unconfigure_archive_rollback
            * unconfigure_archive_time_period
            * unconfigure_archive_write_memory
            * unconfigure_bba_group
    * IOSXE
        * Updated unittests to new testing method
            * configure_line_vty
            * configure_logging_buffered_persistent_url
            * configure_macro_auto_global_processing
            * configure_macro_auto_global_processing_on_interface
            * configure_macro_auto_processing_on_interface
            * configure_macro_auto_sticky
            * configure_macro_global_apply
            * configure_macro_name
            * configure_mdix_auto
            * configure_no_boot_system_switch_all
    * IOSXE
        * Updated unittests to new testing method
            * configure_ip_http_authentication_local
            * configure_ip_http_client_secure_trustpoint
            * configure_ip_http_client_source_interface
            * configure_ip_http_client_source_interface_vlan_domain_lookup
            * configure_ip_http_client_source_interface_vlan_domain_lookup_name_server_vrf_mgmt_vrf
            * configure_ip_local_pool
            * configure_ip_name_server_vrf
            * configure_ip_scp_password
            * configure_ip_scp_server_enable
            * configure_ip_scp_username
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_enable_secret_level
            * unconfigure_enable_secret_password
            * unconfigure_event_manager_applet
            * unconfigure_global_source_template
            * unconfigure_hw_module_logging_onboard
            * unconfigure_hw_module_slot_breakout
            * unconfigure_hw_module_slot_logging_onboard_environment
            * unconfigure_hw_module_slot_logging_onboard_temperature
            * unconfigure_hw_module_slot_logging_onboard_voltage
            * unconfigure_hw_module_slot_upoe_plus
    * IOSXE
        * Updated unittests to new testing method
            * configure_process_cpu_statistics_limit_entry_percentage_size
            * configure_process_cpu_threshold_type_rising_interval
            * configure_qfp_drop_threshold
            * configure_rep_admin_vlan
            * configure_service_compress_config
            * configure_service_performance
            * configure_service_template
            * configure_service_timestamps
            * configure_set_clock_calendar
            * configure_snmp_mib_bulkstat
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_boot_manual_switch
            * unconfigure_boot_system
            * unconfigure_boot_system_switch_switchnumber
            * unconfigure_bridge_domain
            * unconfigure_broadband_aaa
            * unconfigure_bulkstat_profile
            * unconfigure_call_admission
            * unconfigure_cdp_run
            * unconfigure_commands_from_template
            * unconfigure_device_classifier_command
    * IOSXE
        * Updated unittests to new testing method
            * configure_parser_view
            * configure_periodic_time_range
            * configure_platform_acl_egress_dscp_enable
            * configure_platform_mgmt_interface
            * configure_platform_qos_port_channel_aggregate
            * configure_platform_shell
            * configure_policy_map_control
            * configure_policy_map_control_service_template
            * configure_port_channel_persistent
            * configure_power_inline_auto_max
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_ip_scp_password
            * unconfigure_ip_scp_server_enable
            * unconfigure_ip_scp_username
            * unconfigure_ip_sftp_password
            * unconfigure_ip_sftp_username
            * unconfigure_ip_source_binding
            * unconfigure_ip_ssh_source_interface
            * unconfigure_ip_tftp_blocksize
            * unconfigure_issu_set_rollback_timer
            * unconfigure_key_config_key_password_encrypt
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_device_classifier_operator
            * unconfigure_device_classifier_profile
            * unconfigure_device_classifier_profile_command
            * unconfigure_diagnostic_monitor_interval_module
            * unconfigure_diagnostic_monitor_module
            * unconfigure_diagnostic_monitor_switch
            * unconfigure_diagnostic_monitor_syslog
            * unconfigure_diagnostic_schedule_module
            * unconfigure_diagnostic_schedule_switch
            * unconfigure_diagonistics_monitor_switch
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_hw_module_switch_number_auto_off_led
            * unconfigure_hw_module_switch_number_ecomode_led
            * unconfigure_hw_switch_logging_onboard
            * unconfigure_hw_switch_switch_logging_onboard_environment
            * unconfigure_hw_switch_switch_logging_onboard_temperature
            * unconfigure_hw_switch_switch_logging_onboard_voltage
            * unconfigure_interface_port_channel
            * unconfigure_interface_VirtualPortGroup
            * unconfigure_interface_vlan
            * unconfigure_ip_local_pool
    * IOSXE
        * Updated unittests to new testing method
            * execute_issu_set_rollback_timer
            * hw_module_beacon_RP_active_standby
            * hw_module_beacon_rp_active_standby_status
            * hw_module_beacon_rp_status
            * hw_module_beacon_rp_toggle
            * hw_module_beacon_slot_on_off
            * hw_module_beacon_slot_status
            * power_supply_on_off
            * request_platform_software_package_clean
            * restore_running_config_file
    * IOSXE
        * Updated unittests to new testing method
            * configure_udld_aggressive
            * configure_udld_message_time
            * configure_udld_port_aggressive
            * configure_virtual_service
            * configure_virtual_service_vnic_gateway_guest_ip_address
            * copy_file_with_sftp
            * copy_running_config_to_tftp
            * copy_startup_config_from_flash
            * copy_startup_config_to_flash_memory
            * copy_startup_config_to_tftp
    * IOSXE
        * Updated unittests to new testing method
            * configure_ip_sftp_password
            * configure_ip_sftp_username
            * configure_ip_source_binding
            * configure_ip_ssh_source_interface
            * configure_ip_tftp_blocksize
            * configure_ipxe_forever
            * configure_ipxe_timeout
            * configure_key_config_key_newpass_oldpass
            * configure_key_config_key_password_encrypt
            * configure_license_smart_transport_off

* iosxe/ie3k
    * Updated verify_ignore_startup_config
        * Added fallback to SWITCH_IGNORE_STARTUP_CFG when ConfigReg is not present in show romvar output

* blitz
    * Modified
        * Added unit test coverage for existing Blitz, Yang execution, NETCONF utility, Maple converter, and snapshot restore behavior.
        * Updated Maple converter YAML loading to use ruamel.yaml.YAML(typ='safe') for compatibility with newer ruamel.yaml releases.
    * Modified
        * Added official execute scope support for parserless block, regex, and line-based output filtering before include/exclude validation.
        * Added unit test coverage for execute scope matching, optional fallback, save_as, retry, and invalid scope handling.

* iosxe
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_config_interface_prpchannel
        * test_api_config_ip_domain_lookup
        * test_api_config_ip_on_interface
        * test_api_config_link_local_ip_on_interface
        * test_api_config_load_interval_on_interface
        * test_api_config_port_security_on_interface
        * test_api_config_portchannel_range
        * test_api_configure_access_session_port_control
        * test_api_configure_console_default_privilege_level
        * test_api_configure_control_policies
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified configure_ikev2_profile
        * Added remote_ip support for IKEv2 profile configuration
    * Updated `get_show_output_section` API
        * Added optional `target` parameter to support executing on standby RP
    * Added unit test coverage for the updated API.
    * Modified
        * execute_set_config_register API consolidated and enhanced
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_ikev2_authorization_policy
        * test_api_unconfigure_ikev2_cac
        * test_api_unconfigure_ikev2_dpd
        * test_api_unconfigure_ikev2_fragmentation
        * test_api_unconfigure_ikev2_keyring
        * test_api_unconfigure_ikev2_policy
        * test_api_unconfigure_ikev2_profile
        * test_api_unconfigure_ikev2_proposal
        * test_api_unconfigure_isakmp_key
        * test_api_unconfigure_isakmp_policy
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_ppk_on_keyring
        * test_api_install_autoupgrade
        * test_api_install_remove_version
        * test_api_clear_interface_counters
        * test_api_confgiure_port_channel_min_link
        * test_api_config_enable_ip_routing
        * test_api_config_interface_ospfv3
        * test_api_config_interface_ospfv3_cost
        * test_api_config_interface_ospfv3_flood_reduction
        * test_api_config_interface_ospfv3_network_type
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * modified existing APIs to secure
        * unconfigure_aaa_login_method_none
        * unconfigure_radius_automate_tester
        * unconfigure_dscp_radius_server
        * unconfigure_dscp_radius_server_group
        * unconfigure_radius_attribute_policy_name_under_server
        * unconfigure_radius_attribute_policy_name_under_servergroup
        * source_configured_template
        * configure_monitor_capture_export_location
        * unconfigure_crypto_ikev2_keyring
        * configure_line_vty_needs_enhancement
        * configure_ntp_server
        * unconfigure_ntp_server
        * unconfigure_system_disable_password_recovery_switch_all
        * unconfigure_commands_from_template
        * configure_software_auto_upgrade
        * unconfigure_software_auto_upgrade
        * unconfigure_enable_secret_password
        * unconfigure_snmp_server_group
        * configure_snmp_server_trap
        * unconfigure_snmp_server_trap
        * unconfigure_snmp_server_user
        * configure_snmp_host_version
        * unconfigure_snmp_host_version
        * configure_snmp_server_enable_traps_power_ethernet_group
        * configure_snmp_server_host_trap
        * _build_snmp_server_host_command
        * configure_snmp_server_host
        * configure_commands_to_template
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_crypto_map_on_interface
        * test_api_configure_dialer_interface
        * test_api_configure_downlink_interface
        * test_api_configure_dual_port_interface_media_type
        * test_api_configure_eapol_eth_type_interface
        * test_api_configure_egress_interface
        * test_api_configure_eui_64_over_ipv6_enabled_interface
        * test_api_configure_glbp_details_on_interface
        * test_api_configure_hsrp_interface
        * test_api_configure_hsrp_version_on_interface
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified 'configure_pki_enroll' API.
        * Added Dialog statement support for EST request certificate query.
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_ip_verify_source
        * test_api_configure_interface_ip_verify_unicast_notification
        * test_api_configure_interface_ip_verify_unicast_reversepath
        * test_api_configure_interface_ip_verify_unicast_source
        * test_api_configure_interface_ip_wccp
        * test_api_configure_interface_keepalive
        * test_api_configure_interface_l2protocol_tunnel
        * test_api_configure_interface_lacp_fast_switchover
        * test_api_configure_interface_lacp_max_bundle
        * test_api_configure_interface_logging_event
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_dot1x_timeout_txp
        * test_api_configure_interface_duplex
        * test_api_configure_interface_flow_control
        * test_api_configure_interface_inherit_disable
        * test_api_configure_interface_interfaces_on_port_channel
        * test_api_configure_interface_ip_nbar
        * test_api_configure_interface_ip_tcp_adjust_mss
        * test_api_configure_interface_ipv6_tcp_adjust_mss
        * test_api_configure_interface_ipv6_verify_unicast_reversepath
        * test_api_configure_interface_ipv6_verify_unicast_source
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified configure_crypto_ikev2_keyring
        * Added ppk support

* nxos
    * SDK
        * libs/abstracted_libs/nxos/ha.py
        * apis/nxos/platform/get.py

* linux
    * remove internal Apis for decodeing core files and cdet creation.

* sdk-pkg
    * Modified utility APIs
        * ``convert_server_to_linux_device`` returns ``None`` when server metadata is missing.
        * ``get_proxy`` safely handles devices without ``via`` metadata during proxy lookup.

* sdk
    * Modified pkgs/sdk-pkg/src/genie/libs/sdk/powercycler/base.py
        * BaseVCenterPowerCycler.connect()
            * Use .get() for safe access to server credentials, address,
            * Raise exception on connection failure instead of silently
        * BaseVCenterPowerCycler.find_vm_by_instance_uuid()
            * Use keyword arguments for SearchIndex.FindByUuid() call for
            * On UUID lookup failure, call new _log_all_vm_uuids() helper to
        * Added new method BaseVCenterPowerCycler._log_all_vm_uuids()
            * Walks the entire vCenter inventory and logs each VM's name, BIOS
            * Used for debugging when an instance UUID lookup fails
    * Updated the `execute_config_register` api.

* management
    * configure
        * Added support for media-type configuration in configure_management API


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added IOSXE SDK API support for
        * `execute_show_subscriber_session_feature`
    * Added unit test coverage for the new API.
    * Added
        * configure_plim_qos_in_map_ip_dscp_based API
    * Added
        * unconfigure_subinterface_dot1q_encapsulation API
    * Added API get_object_manager_error_object
        * Added API to get_object_manager_error_object
    * Added configure_rip_version
    * Added unconfigure_rip_version
    * Added unconfigure_rip_auto_summary
    * Added configure_rip_auto_summary
    * Added configure_rip_redistribute_bgp
    * Added unconfigure_rip_redistribute_bgp
    * Added
        * configure_macsec_key_chain API
    * Added ``health_crashinfo`` API in ``apis/iosxe/health/health.py``
        * Baseline/differential approach first call (``copy_files=False, delete_files=False``) records existing files; subsequent calls only act on new files
        * Supports single RP, HA (dual RP), and stack topologies
        * Copies new crashinfo files to ``runtime.directory/crashinfo/`` subfolder
        * Optionally deletes files from device after successful copy (``delete_files=True``)
        * Returns ``health_data`` dict with ``num_of_crashfiles`` and ``crashfiles`` list when ``health=True``, or a flat list when ``health=False``
    * Added API ``configure_dhcp_relay_pool``
    * Added API ``unconfigure_dhcp_relay_pool``
    * Added API ``configure_ip_dhcp_class``
    * Added API ``unconfigure_ip_dhcp_class``
    * Added
        * configure_platform_filesystem_harddisk_offline API
    * Added
        * configure_platform_filesystem_harddisk_online API
    * Added IOSXE SDK API support for
        * `configure_class_map_type_traffic`
        * `unconfigure_class_map_type_traffic`
        * `configure_redirect_server_group`
        * `unconfigure_redirect_server_group`
    * Added unit test coverage for the new APIs.
    * Added configure_subinterface_qinq_encapsulation API
    * Added unconfigure_subinterface_qinq_encapsulation API
    * Added IOSXE SDK API support for
        * `unconfigure_interface_ip_subscriber_initiator`
    * Added unit test coverage for the new API.
    * Added test_api_execute_show_monitor_event_trace, test_api_execute_monitor_event_trace_crypto  to pki-execute.py
        * New API support for 'monitor event-trace crypto {options}' cli
        * New API support for 'show monitor event-trace {options}' cli
    * Added
        * configure_connect_subinterfaces API
        * unconfigure_connect_subinterfaces API
    * Added
        * configure_subinterface_dot1q_encapsulation API
    * Added configure_mac_access_list_extended
    * Added
        * configure_hw_module_slot_reload API
    * Added secure APIs
        * configure_snmpv3_user
        * unconfigure_snmpv3_user
        * get_snmpv3_snmpwalk
    * Added secure APIs
        * configure_aaa_login_method_local
        * configure_secure_file_transfer
        * unconfigure_secure_file_transfer
    * Added IOSXE SDK API support for
        * `configure_nve_interface`
        * `unconfigure_nve_interface`
    * Added unit test coverage for the new APIs.
    * Added
        * configure_interface_macsec_access_control API
    * Added
        * configure_hw_module_slot_start API
    * Added IOSXE SDK API support for ISG service policy-map
        * `configure_policy_map_type_service_isg`
    * Added unit test coverage for the new API.
    * Added
        * configure_system_mode_insecure API
    * Added configure_bgp_redist_static
    * Added configure_bgp_timers
    * Added configure_bgp_neighbor_weight
    * Added configure_bgp_neighbor_next_hop_self
    * Added configure_bgp_community_new_format
    * Added configure_bgp_update_source
    * Added unconfigure_bgp_community_new_format
    * Added
        * configure_interface_mka_pre_share_key API
        * unconfigure_interface_mka_pre_share_key API
    * Added API btdecode_grep
        * Added API btdecode_grep to search and filter btdecode command output.
    * Added iosxe flow monitor cache inactive timeout API support
        * New API support for 'configure_flow_monitor_cache_inactive_timeout' CLI command to configure flow monitor cache inactive timeout on IOSXE devices.
        * New API support for 'unconfigure_flow_monitor_cache_inactive_timeout' CLI command to unconfigure flow monitor cache inactive timeout on IOSXE devices.
    * Added SDK API support for
        * `vpdn logging dead-cache`
        * `vpdn session-limit <limit>`
        * `vpdn-group <group>; session-limit <limit>`
        * `vpdn-group <group>; local name <name>`
        * `vpdn-group <group>; l2tp tunnel busy timeout <timeout>`
        * `vpdn-group <group>; no l2tp tunnel busy timeout <timeout>`
        * `snmp-server host <ip> <community>`
        * `no snmp-server host <ip> <community>`
        * `logging buffered <size> [severity]`
        * `interface <parent>.<subif> [action]`
    * Added unit test coverage for the new and updated helper APIs.
    * Added show policy-firewall stats platform to platform-execute.py
        * New API support for 'show policy-firewall stats platform'
    * Added IOSXE SDK API support for
        * ``configure_ip_dhcp_use_vrf_remote``
        * ``unconfigure_ip_dhcp_use_vrf_remote``
        * ``configure_interface_multiservice``
        * ``unconfigure_interface_multiservice``
    * Added unit test coverage for the new APIs.
    * Added
        * configure_interface_ip_proxy_arp API

* ios
    * Added IOS SDK API support for
        * ``renew_dhcp``
            * Executes ``renew dhcp <interface>`` to renew the DHCP lease on
    * Added unit test coverage for the new API.
    * Added IOS SDK API support for
        * `get_show_output_include`
        * `get_show_output_exclude`
    * Added unit test coverage for the new APIs.
    * Added configure_radius_server_key API
        * Configures radius-server key on device
    * Added unconfigure_radius_server_key API
        * Unconfigures radius-server key on device
    * Added IOS SDK API support for
        * `configure_service_simulator_radius_server`
        * `unconfigure_service_simulator_radius_server`
        * `configure_ip_domain_lookup`
        * `unconfigure_ip_domain_lookup`
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * `configure_static_route` - Configure IPv4 static route
        * `unconfigure_static_route` - Unconfigure IPv4 static route
        * `configure_ipv6_static_route` - Configure IPv6 static route
        * `unconfigure_ipv6_static_route` - Unconfigure IPv6 static route
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * `config_enable_ipv6_routing`
        * `unconfig_disable_ipv6_routing`
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * `execute_clear`
        * `execute_simulator_radius_request_coa`
    * Added unit test coverage for the new APIs.
    * Added IOS SDK API support for
        * `configure_ipv6_dhcp_client_pd_on_interface`
        * `unconfigure_ipv6_dhcp_client_pd_on_interface`
    * Added unit test coverage for the new APIs.

* linux
    * Added secure APIs
        * get_snmpv3_snmpwalk
        * get_snmpv3_snmpget
        * set_snmpv3_snmpset

* sdk-pkg
    * Added server route lookup APIs
        * `find_server_ip_for_device_ip` - given a device IP and testbed, returns the best-matching server interface IP by longest-prefix match against server management routes.
        * Added unit test coverage for the new APIs.


--------------------------------------------------------------------------------
                                    Enhanced                                    
--------------------------------------------------------------------------------

* iosxe
    * Updated API ``configure_dhcp_pool``


--------------------------------------------------------------------------------
                                    Clarity                                     
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Extended ``configure_dhcp_pool`` with an optional ``class_name`` argument


