--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Added Api for get show output begin
    * Fixed api configure_trustpool_import_terminal
        * Fixed an issue that was causing failure in passing certificates to the configure_trustpool_import_terminal API
    * Modified API get_config_register
        * Added support for getting config register value in ROMMON state
    * Modified API configure_ignore_startup_config
        * Updated the logic to determine the new config register value based on the current value
    * Modified API unconfigure_ignore_startup_config
        * Updated the logic to determine the new config register value based on the current value
    * Modified API verify_ignore_startup_config
        * Updated the logic to only check the startup config bit in config register
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_source_template
        * test_api_unconfigure_crypto_key
        * test_api_configure_eigrp_named_networks
        * test_api_configure_eigrp_named_networks_with_af_interface
        * test_api_configure_eigrp_networks
        * test_api_configure_eigrp_networks_redistribute_ospf
        * test_api_configure_eigrp_passive_interface
        * test_api_configure_eigrp_passive_interface_v6
        * test_api_configure_eigrp_redistribute_bgp
        * test_api_configure_eigrp_redistributed_connected
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_eigrp_router_configs
        * test_api_configure_interface_eigrp_v6
        * test_api_configure_vrf_ipv6_eigrp_named_networks
        * test_api_enable_ipv6_eigrp_router
        * test_api_shutdown_ipv6_eigrp_instance
        * test_api_unconfigure_eigrp_named_router
        * test_api_unconfigure_eigrp_passive_interface
        * test_api_unconfigure_eigrp_passive_interface_v6
        * test_api_unconfigure_eigrp_router
        * test_api_unconfigure_eigrp_router_configs
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_interface_eigrp_v6
        * test_api_unconfigure_ipv6_eigrp_router
        * test_api_unshutdown_ipv6_eigrp_instance
        * test_api_change_nve_source_interface
        * test_api_clear_bgp_l2vpn_evpn
        * test_api_configure_evpn_default_gateway_advertise_global
        * test_api_configure_evpn_ethernet_segment
        * test_api_configure_evpn_evi_replication_type
        * test_api_configure_evpn_instance
        * test_api_configure_evpn_instance_encapsulation_type
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_evpn_instance_evi
        * test_api_configure_evpn_l2_instance_bd_association
        * test_api_configure_evpn_l2_instance_vlan_association
        * test_api_configure_evpn_l2_profile_bd_association
        * test_api_configure_evpn_l3_instance_bd_association
        * test_api_configure_evpn_l3_instance_vlan_association
        * test_api_configure_evpn_profile
        * test_api_configure_evpn_replication_type
        * test_api_configure_interface_evpn_ethernet_segment
        * test_api_configure_l2vpn_evpn
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_evpn_default_gateway_advertise_global
        * test_api_unconfigure_evpn_evi_replication_type
        * test_api_unconfigure_evpn_instance
        * test_api_unconfigure_evpn_instance_encapsulation_type
        * test_api_unconfigure_evpn_instance_evi
        * test_api_unconfigure_evpn_l2_instance_bd_association
        * test_api_unconfigure_evpn_l2_instance_vlan_association
        * test_api_unconfigure_evpn_l2_profile_bd_association
        * test_api_unconfigure_evpn_l3_instance_vlan_association
        * test_api_unconfigure_evpn_profile
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_l2vpn_evpn_advertise_sync
        * test_api_configure_l2vpn_evpn_flooding_suppression
        * test_api_configure_l2vpn_evpn_router_id
        * test_api_configure_nve_interface
        * test_api_configure_nve_interface_group_based_policy
        * test_api_configure_pvlan_loadbalancing_ethernetsegment_l2vpn_evpn
        * test_api_configure_replication_type_on_evi
        * test_api_configure_vfi_context_evpn
        * test_api_configure_vlan_service_instance_bd_association
        * test_api_enable_multicast_advertise_on_evi
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_evpn_replication_type
        * test_api_unconfigure_interface_evpn_ethernet_segment
        * test_api_unconfigure_l2vpn_evpn
        * test_api_unconfigure_l2vpn_evpn_flooding_suppression
        * test_api_unconfigure_l2vpn_evpn_router_id
        * test_api_unconfigure_mdt_config_on_vrf
        * test_api_unconfigure_nve_interface
        * test_api_unconfigure_nve_interface_group_based_policy
        * test_api_unconfigure_vfi_context_evpn
        * test_api_unconfigure_vlan_service_instance_bd_association
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_clear_monitor_capture
        * test_api_configure_active_timer_under_et_analytics
        * test_api_configure_datalink_flow_monitor
        * test_api_configure_et_analytics
        * test_api_configure_flow_exporter
        * test_api_configure_flow_monitor
        * test_api_configure_flow_monitor_cache_entry
        * test_api_configure_flow_monitor_on_vlan_configuration
        * test_api_configure_flow_record_collect_counter
        * test_api_configure_flow_record_collect_timestamp
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_configure_flow_record_match_collect_interface
        * test_configure_flow_record_match_datalink
        * test_configure_flow_record_match_ip
        * test_configure_fnf_exporter
        * test_configure_fnf_flow_record
        * test_configure_fnf_flow_record_match_flow
        * test_configure_fnf_monitor_datalink_interface
        * test_configure_fnf_monitor_sampler_interface
        * test_configure_fnf_record
        * test_configure_ipv6_flow_monitor
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_monitor_capture_buffer_size
        * test_api_configure_monitor_capture_export_location
        * test_api_configure_monitor_capture_export_status
        * test_api_configure_monitor_capture_limit_packet_len
        * test_api_configure_monitor_capture_match
        * test_api_configure_monitor_capture_without_match
        * test_api_configure_sampler
        * test_api_delete_monitor_capture
        * test_api_disable_et_analytics
        * test_api_enable_et_analytics
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_start_monitor_capture
        * test_stop_monitor_capture
        * test_unconfigure_active_timer_under_et_analytics
        * test_unconfigure_flow_exporter
        * test_unconfigure_flow_monitor
        * test_unconfigure_flow_monitor_on_vlan_configuration
        * test_unconfigure_flow_record
        * test_unconfigure_fnf_monitor_datalink_interface
        * test_unconfigure_fnf_monitor_on_interface
        * test_unconfigure_interface_datalink_flow_monitor
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * IE3K
        * Fixed the issue where factory reset API was not resetting the configuration when the 'config' parameter was set to True.
    * Modified API configure_management_ssh default timeout from 120 to 240 seconds.
    * Modified API copy_to_device to display more information in logs on error scenario.
    * Fix get_rp_status_info to handle cases where the output may not contain all expected fields, preventing potential exceptions and ensuring more robust parsing of RP status information.

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * configure_nat64_prefix_stateful
            * configure_nat64_translation_timeout
            * configure_nat64_v4_list_pool
            * configure_nat64_v4_list_pool_overload
            * configure_nat64_v4_pool
            * configure_nat64_v6v4_static
            * configure_nat64_v6v4_static_protocol_port
            * configure_nat_extended_acl
            * configure_nat_ipv6_acl
            * configure_nat_overload_rule
    * IOSXE
        * Updated unittests to new testing method
            * configure_static_nat_rule
            * configure_static_nat_source_list_rule
            * force_unconfigure_static_nat_route_map_rule
            * unconfigure_crypto_ikev2_NAT_keepalive
            * unconfigure_dynamic_nat_interface_overload_route_map_rule
            * unconfigure_dynamic_nat_outside_rule
            * unconfigure_dynamic_nat_pool_overload_route_map_rule
            * unconfigure_dynamic_nat_route_map_rule
            * unconfigure_dynamic_nat_rule
            * unconfigure_ip_access_group_in_out
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_nat64_interface
            * unconfigure_nat64_nd_ra_prefix
            * unconfigure_nat64_prefix_stateful
            * unconfigure_nat64_translation_timeout
            * unconfigure_nat64_v4_list_pool
            * unconfigure_nat64_v4_list_pool_overload
            * unconfigure_nat64_v4_pool
            * unconfigure_nat64_v6v4_static
            * unconfigure_nat64_v6v4_static_protocol_port
            * unconfigure_nat_pool
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_nat_pool_address
            * unconfigure_nat_pool_overload_rule
            * unconfigure_nat_port_route_map_rule
            * unconfigure_nat_route_map
            * unconfigure_nat_translation_max_entries
            * unconfigure_nat_translation_timeout
            * unconfigure_outside_static_nat_rule
            * unconfigure_standard_access_list
            * unconfigure_static_nat_network_rule
            * unconfigure_static_nat_outside_rule
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_static_nat_route_map_no_alias_rule
            * unconfigure_static_nat_route_map_rule
            * unconfigure_static_nat_rule
            * unconfigure_static_nat_source_list_rule
            * configure_interface_network_policy
            * configure_network_policy_profile_voice_vlan
            * unconfigure_global_network_policy
            * unconfigure_interface_network_policy
            * unconfigure_network_policy_profile_number
            * unconfigure_network_policy_profile_voice_vlan
    * IOSXE
        * Updated unittests to new testing method
            * remove_ntp_master
            * unconfigure_ntp_server
            * unconfig_nve_src_intf
            * unconfig_nve_vni_members
            * configure_switch_provision
            * unconfigure_switch_provision
            * configure_ipv4_object_group_network
            * configure_ipv4_object_group_service
            * configure_ipv4_ogacl_ip
            * configure_ipv4_ogacl_on_interface
    * IOSXE
        * Updated unittests to new testing method
            * configure_ipv4_ogacl_service
            * configure_ipv4_ogacl_src_dst_nw
            * configure_ipv6_acl_on_interface
            * configure_ipv6_object_group_network
            * configure_ipv6_object_group_service
            * configure_ipv6_ogacl
            * configure_object_group
            * unconfigure_ipv4_object_group
            * unconfigure_ipv4_object_group_service
            * unconfigure_ipv4_ogacl
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_ipv4_ogacl_on_interface
            * unconfigure_ipv6_acl
            * unconfigure_ipv6_acl_on_interface
            * unconfigure_ipv6_object_group_network
            * unconfigure_ipv6_object_group_network_entry
            * unconfigure_ipv6_object_group_service
            * unconfigure_ipv6_object_group_service_entry
            * unconfigure_ipv6_ogacl_ace
            * clear_ospfv3_process_all
            * configure_distribute_prefix_list_under_ospf
    * IOSXE
        * Updated unittests to new testing method
            * configure_distribute_prefix_list_under_ospf
            * configure_interface_ospfv3_ipsec_ah
            * configure_interface_ospfv3_ipsec_esp
            * configure_ip_ospf_mtu_ignore
            * configure_ip_prefix_list
            * configure_ipv6_ospf_mtu_ignore
            * configure_ipv6_ospf_router_id
            * configure_ipv6_ospf_routing_on_interface
            * configure_maximum_path_under_ospf
            * configure_neighbor_under_ospf
    * IOSXE
        * Updated unittests to new testing method
            * configure_ospf_area_type
            * configure_ospf_max_lsa_limit
            * configure_ospf_network_broadcast
            * configure_ospf_network_non_broadcast
            * configure_ospf_networks
            * configure_ospf_nsf_ietf
            * configure_ospf_priority
            * configure_ospf_redistributed_eigrp_metric
            * configure_ospf_redistributed_static
            * configure_ospf_routing
    * IOSXE
        * Updated unittests to new testing method
            * configure_ospfv3
            * configure_ospfv3_address_family
            * configure_ospfv3_interface
            * configure_ospfv3_ipsec_ah
            * configure_ospfv3_ipsec_esp
            * configure_ospfv3_max_lsa_limit
            * configure_ospfv3_network_point
            * configure_ospfv3_network_type
            * configure_ospfv3_on_interface
            * configure_ospfv3_redistributed_connected
    * IOSXE
        * Updated unittests to new testing method
            * configure_ospf_vrf_lite
            * configure_route_map
            * configure_router_ospf_redistribute_internal_external
            * configure_snmp_if_index_on_ospfv3_process_id
            * redistribute_bgp_metric_route_map_under_ospf
            * redistribute_bgp_on_ospfv3
            * redistribute_eigrp_under_ospf
            * redistribute_route_metric_vrf_green
            * unconfigure_distribute_prefix_list_under_ospf
            * unconfigure_interface_ospfv3_ipsec_ah

* utils
    * Fixed API get_file_size_from_server
        * Allow for proxy filesize retrieval via socat relay

* api/utils
    * copy_to_device
        * Fix copy_to_device to use filetransfer utils including pre and post config settings
    * copy_from_device
        * Fix copy_from_device to use filetransfer utils including pre and post config settings

* iosxe/ie3k
    * Modified API execute_set_config_register
        * Added support for setting config register value
    * Modified API configure_ignore_startup_config
        * Updated the logic to determine the new config register value based on the current value
    * Modified API unconfigure_ignore_startup_config
        * Updated the logic to determine the new config register value based on the current value
    * Modified API verify_ignore_startup_config
        * Updated the logic to only check the startup config bit in config register

* triggers/blitz/rpc_reply
    * Added fallback regex in add_key_nodes() to handle unquoted key values when RE_FIND_QUOTED_VALUE does not match.

* iosxe/cat9k/c9200/rommon
    * Fixed get_recovery_details KeyError when drec0 is empty by adding SchemaEmptyParserError handling and tftp_boot fallback support

* iosxe/rommon
    * Modified device_rommon_boot _rommon_switch_boot handler to to avoid infinite ROMMON boot attempts

* iosxe/ir1k/ir1100
    * Moved API's for model ir1100 & to ir1101

* generic
    * Modified get_interface_from_yaml to support segments


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added clear_bgp_ipv6_neighbor_soft
    * Added clear_ip_ssh_pubkey_server
        * API to clear ip ssh pubkey server configuration
    * Added configure_bgp_ipv6_neighbor_list
    * Added configure_bgp_confederation_identifier
    * Added configure_bgp_confederation_peers
    * Added configure_flow_record_parameters
        * API to configure flow record parameters
    * Added configure_bgp_route_reflector_client_address_family
        * API to configure BGP route reflector client address family
    * Added configure_interface_hsr_ring
        * API to configure interface hsr ring
    * Added unconfigure_interface_hsr_ring
        * API to unconfigure interface hsr ring
    * API to configure ip dns view group under interface
        * genie.libs.sdk.apis.iosxe.dns.configure.configure_interface_ip_dns_view_group
        * genie.libs.sdk.apis.iosxe.dns.configure.unconfigure_interface_ip_dns_view_group
    * Added new API configure_license_boot_mode_universal to convert mode to universal licensing (OS-Advantage, OS-essentials)
        * config command| license boot mode universal
    * Added new API unconfigure_license_boot_mode_universal to convert mode back to legacy (network-adv, network-essentials)
        * unconfig command|no license boot mode universal
    * Added configure_rep_no_neighbour
    * Added new API for ie9k platform to get boot variables.

* iosxe/ie3k
    * Added API get_config_register
        * Added support for getting config register value

* powercycler
    * Added EnlogicSnmpPDU and EnlogicSnmpv3PDU powercycler classes


