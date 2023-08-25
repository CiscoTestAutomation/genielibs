--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_ipv6_acl
        * added time range parameter
    * Modified configure_management_vty_lines API to only set authentication if username and password provided
    * Modified configure_dhcp_pool_ipv6_domain_name
        * API to configure dhcp-pool ipv6 domain-name
    * Modify configure_bgp_address_advertisement
        * Updated API to support vrf
    * Modified configure_snmp_server_enable_traps_power_ethernet_group
        * added correct mode of execution
        * variable name modified as mentioned in def arguments
    * Modified API's to unconfigure skip-client cli.
        * API to unconfigure_sks_client
    * Modified configure_interface_service_policy
        * added return statement to return the output
    * Modified configure_archive_logging
        * added optional variables hidekeys, notify_syslog. Default set to True
    * Modified request_platform_software_package_clean
        * added optional variables timeout default to 60
    * Modified generate_crypto_key
        * added mapping timeout which is missing
    * Modified delete_local_file
        * added dialog
    * Modified clear_logging
        * added timeout optional variable default to 60
    * Modified delete_local_file
        * added the dialog statement
    * Modified configure_interface_ip_verify_unicast_reversepath
        * added no_switchport optional input variable
    * Modified configure_interface_ip_verify_unicast_notification
        * added no_switchport optional input variable
    * Modified configure_interface_ip_verify_unicast_source
        * added no_switchport optional input variable
    * Modified configure_interface_ipv6_verify_unicast_reversepath
        * added no_switchport optional input variable
    * Modified hw_module_switch_usbflash_security_password
        * added return statement
    * Modified request_system_shell
        * added command optional variable
    * Modify configure_switchport_vlan_mapping
        * API for configure switchport vlan mapping
    * Modify unconfigure_switchport_vlan_mapping
        * API for unconfigure switchport vlan mapping
    * Modified config_ip_on_vlan
        * API for config_ip_on_vlan
    * Modified unconfig_ip_on_vlan
        * API for unconfig_ip_on_vlan
    * Modified configure_dhcp_pool
        * added parameter vrf and dns_server
    * Modified unconfigure_dhcp_pool
        * added parameter vrf and dns_server

* blitz
    * Converted sanity test to end-to-end tests.
    * Added
        * Added support of datastore to the Blitz action, 'yang_snapshot_restore'. Also it will send edit-config after multiple locking tries.

* genie.libs.sdk
    * Modified blitz RPC verification code to support XPATH with and without key prefix
    * Modified blitz RPC verification code to support XPATH with leading and trailing WHITESPACE in Key content
    * Modified trim_response method to return the list of all responses from the index of parent_key


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* iosxe
    * Added api delete_directory
        * API to delete directory from the filesystem
    * Added API's to configure cli commands to collect smd logs and store it in a flash feature.
        * API to show_logging_smd_output_to_file
    * Added unconfigure_ipv6_redirects
        * API to unconfigure ipv6 redirects
    * Added configure_ipv6_nd_suppress_ra
        * API to configure ipv6 nd suppress-ra
    * Added unconfigure_ipv6_nd_suppress_ra
        * API to unconfigure ipv6 nd suppress-ra
    * Added unconfigure_ipv6_address_test
        * API to unconfigure ipv6 address test
    * Added configure_ipv6_address_config
        * API to configure ipv6 address config
    * Added unconfigure_ipv6_address_config
        * API to unconfigure ipv6 address config
    * Added unconfigure_ipv6_address_autoconfig
        * API to unconfigure ipv6 address autoconfig
    * Added API's to configure cli commands for aaa filter-spec protocol config feature.
        * API to configure_access_session_attr_filter_list
        * API to unconfigure_access_session_attr_filter_list
        * API to unconfigure_access_session_attr_filter_list_protocol
    * Added configure_bba_group_session_auto_cleanup
        * added api to configure_bba_group_session_auto_cleanup
    * Added configure_avb
        * API to configure avb
    * Added unconfigure_avb
        * API to unconfigure avb
    * Added enable_keepalive_on_interface
        * API to configure enable_keepalive_on_interface
    * Added configure_ptp_enable_on_interface
        * New API to configure ptp enable on interface
    * Added configure_no_ptp_enable_on_interface
        * New API to unconfigure no ptp enable on interface
    * Modified cts manual cli
        * API to configure policy with or without trust and also to disable propagation
    * Add new API verify_bgp_neighbor_state_vrf
        * Verify state/pfxrcd entry in show bgp {vpnv4/vpnv4} {unicast} vrf {vrfid} summary
    * Add logging pre-check in health check
    * Added configure_monitor_capture_export_location
        * New API to Configure Monitor capture export location file
    * Added configure_monitor_capture_export_status
        * New API to Configure Monitor capture export status
    * Added enable_debug_pdm
        * API to execute debug pdm {parameter} {enable}
    * Added disable_debug_pdm
        * API to configure no debug pdm {parameter} {enable}
    * Added unconfigure_switchport_trunk_allowed_vlan
        * API to unconfigure switchport trunk allowed vlan
    * Added unconfigure_switchport_trunk_native_vlan
        * API to unconfigure switchport trunk native vlan
    * Added disable_switchport_trunk_on_interface
        * API to disable switchport trunk
    * Added configure_switchport_pvlan_trunk_allowed_vlan
        * API for configure pvlan trunk allowed vlan
    * Added unconfigure_switchport_pvlan_trunk_allowed_vlan
        * API for unconfigure pvlan trunk allowed vlan
    * Added configure_switchport_pvlan_trunk_native_vlan
        * API for configure pvlan trunk native vlan
    * Added unconfigure_switchport_pvlan_trunk_native_vlan
        * API for unconfigure pvlan trunk native vlan
    * Added configure_interface_pvlan_mapping
        * API for configure interface pvlan mapping
    * Added unconfigure_interface_pvlan_mapping
        * API for unconfigure interface pvlan mapping
    * Added unconfigure_interface_switchport_pvlan_mapping
        * API for unconfigure interface switchport pvlan mapping
    * Added unconfigure_interface_switchport_pvlan_association
        * API for unconfigure interface switchport pvlan association
    * Added unconfigure_interface_pvlan_host_assoc
        * API for unconfigure interface pvlan host association
    * Added clear_interface_range
        * API for clear the interface range
    * Added API's to configure cli commands for QoS feature.
        * API to configure_table_map_on_device
        * API to configure_policy_map_class_precedence
        * API to unconfigure_interface_service_policy
    * Added API's to configure cli commands for aaa filter-spec accounting feature.
        * API to config_access_session_accnt_attr_filter_spec_include_list
        * API to unconfig_access_session_accnt_attr_filter_spec_include_list
    * New unconfigure_management_netconf
        * Added api unconfigure_management_netconf
    * Added configure_ipv4_object_group_network
        * API for configure ipv4 object group network
    * Added unconfigure_ipv4_object_group
        * API for unconfigure ipv4 object group
    * Added configure_ipv4_object_group_service
        * API for configure ipv4 object group service
    * Added unconfigure_ipv4_object_group_service
        * API for unconfigure object group service
    * Added configure_ipv4_ogacl_src_dst_nw
        * API for configure ipv4 ogacl src dst nw
    * Added configure_ipv4_ogacl_service
        * API for configure ipv4 ogacl service
    * Added configure_ipv4_ogacl_ip
        * API for configure ipv4 ogacl ip
    * Added unconfigure_ipv4_ogacl
        * API for unconfigure ipv4 ogacl
    * Added configure_ipv4_ogacl_on_interface
        * API for configure ipv4 ogacl on interface
    * Added unconfigure_ipv4_ogacl_on_interface
        * API for unconfigure ipv4 ogacl on interface
    * Added configure_glbp_details_on_interface
        * API for configure glbp details on interface
    * Added API's to configure cli commands for aaa authentication filter-spec feature.
        * API to config_access_session_auth_attr_filter_spec_include_list
        * API to unconfig_access_session_auth_attr_filter_spec_include_list
    * Added execute_switch_card_OIR_power_force
        * New API to executr switch card oir power force
    * Added configure_evpn_instance_evi
        * New API to configure evpn instance evi
    * Added unconfigure_evpn_instance_evi
        * New API to unconfigure evpn instance evi
    * Added configure_vfi_context_evpn
        * New API to  configure vfi context evpn
    * Added unconfigure_vfi_context_evpn
        * New API to unconfigure vfi context evpn
    * Added upgrade_hw_programmable
        * API to execute upgrade hw-programmable all
    * Added configure_udld_recovery
        * API to configure udld recovery
    * Added configure_l2vpn_evpn_ethernet_segment
        * API for configure_l2vpn_evpn_ethernet_segment
    * Added unconfigure_snmp_server_enable_traps_power_ethernet_group
        * API to unconfigure snmp server enable traps power ethernet group
    * Added configure_rommon_tftp
        * API to configure tftp rommon variables
    * Added clear_cts_counters_ipv4
        * API for clear cts role-based counters ipv4
    * Added unshut_port_channel
        * API for unshut_port_channel
    * Added get_lisp_instance_id_running_config
        * API for get_lisp_instance_id_running_config
    * Added clear_controllers_ethernet_controller
        * API to clear_controllers_ethernet_controller

* com
    * Added device_boot_recovery
        * API to boot the device from rommon using golden image or tftp boot.

* blitz
    * Added support for veryfing deletion of nodes while using GNMI
    * Added possibility to create custom verifiers and decoders when using Netconf.
    * Changed custom verifiers architecture from monolitic to modular (separate class per protocol).

* sdk
    * Version pinned pysnmp and pyasn1 to fix the type error in execute_power_cycle_device api


