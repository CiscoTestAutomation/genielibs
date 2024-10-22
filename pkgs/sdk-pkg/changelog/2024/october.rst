--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_ppp_multilink
        * added api to configure ppp multilink
    * Added unconfigure_ppp_multilink
        * added api to unconfigure ppp multilink
    * Added configure_spanning_tree_portfast under c9500
        * New API to configures spanning-tree portfast under c9500
    * Added unconfigure_spanning_tree_portfast under c9500
        * New API to unconfigures spanning-tree portfast under c9500
    * Added unconfigure_spanning_tree_portfast under c9610
        * New API to unconfigures spanning-tree portfast under c9610
    * Added configure_key_config_key_newpass_oldpass
        * API to change the master key password
    * Added unconfigure_port_channel
        * API to clear port-channel configuration
    * Added new API to get interface traffic counters
        * get_interface_traffic_counters
    * Added API's to configure cli commands for QoS feature.
        * API to configure_ip_access_list_with_dscp_on_device
        * API to configure_class_map_access_group_on_device
        * API to configure_service_policy_type_queueing_on_interface
        * API to configure_traffic_class_for_class_map
    * Added configure_aaa_authorization_config_commands
        * API for configure aaa authorization config-commands
    * Added configure_aaa_accounting_connection_default_start_stop_group_tacacs_group
        * API for configure aaa accounting connection default start-stop group tacacs+ group {server_group_name}
    * Added configure_aaa_accounting_system_default_start_stop_group_tacacs_group
        * API for configure aaa accounting system default start-stop group tacacs+ group {server_group_name}
    * Added clear_ip_dhcp_snooping_track_server
        * API for clear ip dhcp snooping track server
    * Added execute_monitor_capture_limit_duration
        * Execute monitor_capture_limit_duration
    * Added execute_monitor_capture_access_list
        * Execute monitor_capture_access_list
    * Added execute_monitor_capture_vlan_in_match_any
        * Execute monitor_capture_vlan_in_match_any
    * Added configure_bgp_l2vpn_route_reflector_client
    * Added configure_bgp_l2vpn_route_map
    * Added configure_vlan_service_instance_bd_association
    * Added unconfigure_vlan_service_instance_bd_association
    * Added configure_evpn_profile,unconfigure_evpn_profile
    * Added configure_evpn_l2_profile_bd_association
    * Added unconfigure_evpn_l2_profile_bd_association
    * Added configure_evpn_l3_instance_bd_association
    * Added configure_ospf_network_broadcast
    * Added configure_ospf_priority
    * Added clear_monitor_capture
        * API for "monitor capture {capture_name} clear" command
    * Added configure_interface_rep_stcn_segment
        * rep stcn segment 1
    * Added unconfigure_interface_rep_stcn_segment
        * no rep stcn segment 1
    * Added configure_interface_rep_stcn_stp
        * rep stcn stp
    * Added unconfigure_interface_rep_stcn_stp
        * no rep stcn stp
    * Added configure_rep_segment_edge_preferred
        * rep segment 1 edge preferred
    * Added unconfigure_rep_segment_edge_preferred
        * no rep segment 1 edge preferred
    * Added configure_rep_segment_edge_primary
        * rep segment 1 edge primary
    * Added unconfigure_interface_rep_segment_edge_primary
        * no rep segment 1 edge primary
    * Added configure_rep_ztp
        * rep ztp
    * Added unconfigure_rep_ztp
        * no rep ztp
    * Added API test_platform_software_fed_switch_phy_options
        * Added API to test platform software fed switch active phy options
    * Added configure_parser_view under c8000v
        * New API to configure a parser view under c8000v
    * Added unconfigure_parser_view under c8000v
        * New API to unconfigure a parser view under c8000v
    * Added API execute_test_fru_fake_insert
        * Added execute_test_fru_fake_insert
    * Added configure_snmp_server_host under c8000v
        * New API to configure snmp-server host  under c8000v
    * Added unconfigure_snmp_server_host under c8000v
        * New API to unconfigures snmp_server host under c8000v


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified `check_memory_leaks` processor
        * changed to processor.passed/failed
    * added `execute_reload`  processor
        * new processor to reload the device
    * _condition_validator in Blitz
        * Fixed debug message
    * Modified configure_redistribute_connected to add route_map
    * Modified configure_bgp_router_id_peergroup_neighbor to add listen_range and peer_group
    * Fixed configure_evpn_instance_evi , default-gateway has to be appended with enable
    * Added eth_tag to configure_evpn_l2_instance_bd_association
    * Modified configure_route_map_permit to add match_interface
    * Updated default argument trunk as True
        * added trunk default argument in configure_rep_segment

* nxos
    * Added MPLS SR Support in conf model of interface,ospf & bgp
    * Added BGP PIC Support in conf of BGP


