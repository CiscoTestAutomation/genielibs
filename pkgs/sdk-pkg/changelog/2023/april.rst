--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_ip_arp_inspection_on_interface
        * New API to configure ip arp inspection on interface
    * Added unconfigure_ip_arp_inspection_on_interface
        * New API to unconfigure ip arp inspection on interface
    * Added configure_interface_split_horizon_eigrp API
        * API to configure interface split horizon eigrp for ip and ipv6
    * Added unconfigure_interface_split_horizon_eigrp API
        * API to unconfigure interface split horizon eigrp for ip and ipv6
    * Added configure_ospfv3_network_range
        * API for configure the ospfv3 network range
    * Added configure_ospfv3_on_interface
        * API for configure the ospfv3 area and pid on interface
    * Modified configure_ptp_modes
        * Modified/Added ptp  destination-mac non-forwardable on device
    * Added unconfigure_ptp_aes67_rates
        * API for unconfigure ptp aes67 rates
    * Added configure_ptp_vlan
        * API for configure ptp vlan on device
    * Added unconfigure_ptp_vlan
        * API for unconfigure ptp vlan on device
    * Added configure_ptp_source
        * API configure ptp source on device
    * Added unconfig_diagnostic_monitor_threshold
        * New API to Unconfgure diagnostics monitor threshold on switch
    * Added unconfig_banner
        * New API to Unconfig day banner
    * Added config_load_interval_on_interface
        * New API to configure load interval on interface
    * Added configure_logging_facility
        * New API to configure logging facility
    * Added configure_login_log
        * New API to configure login log on switch
    * Added configure_logging_host_transport_tcp_port
        * New API to configure logging host transport tcp port
    * Added configure_logging_snmp_trap {type}
        * API configure_logging_snmp_trap alerts,critical,debugging,emergencies,errors etc
    * Added unconfigure_logging_snmp_trap {type}
        * API unconfigure_logging_snmp_trap alerts,critical,debugging,emergencies,errors etc
    * Added  unconfigure_netconf_yang_polling
        * API for unconfigure_netconf_yang_polling
    * Added configure_disable_config_key_encryption
        * API configure_disable_config_key_encryption
    * Added configure_spanningtree_sso_block_tcn
        * New API to configure spanning-tree sso block-tcn
    * Added configure_spanningtree_cost_on_interface
        * New API to configure spanning-tree cost
    * Added unconfigure_spanningtree_cost_on_interface
        * New API to unconfigure spanning-tree cost
    * Added unconfigure_spanningtree_sso_block_tcn
        * New API to unconfigure spanning-tree sso block-tcn
    * Added configure_mac_address_table_control_packet_learn
        * New API to configure mac address-table control-packet-learn
    * Added unconfigure_mac_address_table_control_packet_learn
        * New API to unconfigure mac address-table control-packet-learn
    * Added configure_evpn_instance
        * API to configure l2vpn evpn instance
    * Added unconfigure_evpn_instance
        * API to unconfigure l2vpn evpn instance
    * Added configure_evpn_l2_instance_bd_association
        * API to configure VLAN association to EVPN instance
    * Added unconfigure_evpn_l2_instance_bd_association
        * API to unconfigure VLAN association to EVPN instance
    * Added configure_evpn_floodsuppress_dhcprelay_disable_globally
        * API to config l2vpn evpn flooding suppression dhcp-relay disable globally
    * Added unconfigure_evpn_floodsuppress_dhcprelay_disable_globally
        * API to unconfig l2vpn evpn flooding suppression dhcp-relay disable globally
    * Added configure_license_smart_url
        * added api to Configures license smart url smart {url}
    * Added configure_call_home
        * added api to configure to Enter into call-home configuration mode
    * Added configure_exec_prompt_timestamp
        * added api to configure to Exec Prompt Print timestamps for show commands
    * Added configure_flow_record_match_ip
        * API to configure flow record match ip parameters
    * Added configure_flow_record_match_collect_interface
        * API to configure flow record match or collect interface parameters
    * Added configure_flow_record_match_datalink
        * API to configure flow record match datalink parameters
    * Added configure_flow_record_collect_timestamp
        * API to configure flow record match or collect timestamp parameters
    * Added configure_flow_record_collect_counter
        * API to configure flow record collect counter parameters
    * Added execute_request_platform_software_package_install_switch_rollback_auto_copy
        * API to execute request platform software package install switch rollback on-reboot auto-copy
    * Added unconfigure_enable_secret_level API
        * API for unconfigure enable secret level
    * Added configure_ip_arp_inspection_vlan_logging
        * API to configure ip arp inspection vlan logging
    * Added unconfigure_ip_arp_inspection_vlan_logging
        * API to unconfigure ip arp inspection vlan logging
    * Added config_erspan_monitor_session_shut_unshut
        * New API to Configure erspan monitor session shutdown
    * Added unconfig_erspan_monitor_session_no_source
        * New API to Configure no source on erspan monitor session
    * Added unconfig_erspan_monitor_session_no_filter
        * New API to Configure no filter on erspan monitor session
    * Added config_erspan_monitor_session_filter
        * New API to Configure filter on erspan monitor session
    * Added configure_crypto_isakmp_policy
        * added api to configure crypto isakmp policy
    * Added configure_crypto_map_entry
        * updated api to configure crypto map entry
    * Added unconfigure_ip_pim
        * API for unconfigure the ip pim on interface
    * Added configure_mdix_auto
        * New API to configure mdix auto on interface
    * Added unconfigure_mdix_auto
        * New API to unconfigure mdix auto on interface
    * Added configure_switchport_vlan_mapping
        * API to switchport vlan mapping {vlan} on device interface
    * Added unconfigure_switchport_vlan_mapping
        * API to no switchport vlan mapping {vlan} on device interface
    * Added configure_interface_ipv6_isis_router_name
        * API configure ipv6 router under interface
    * Added unconfigure_isis_vrf
        * API to unconfigure vrf under isis
    * Modified configure_isis_with_router_name_network_entity
        * To additionally include vrf under isis
    * Added configure_bgp_isis_redistribution
        * API to configure isis under BGP redistribution
    * Added configure_mpls_te_nsr
        * API to configure NSR for mpls te
    * Added configure_rsvp_gracefull_restart
        * API to configure gracefull restart for rsvp
    * Added configure_ip_source_binding
        * API for to configure ip source binding
    * Added unconfigure_ip_source_binding
        * API for to unconfigure ip source binding
    * Added configure_boot_manual_switch
        * API for to configure boot manual switch
    * Added unconfigure_boot_manual_switch
        * API for to unconfigure boot manual switch
    * Added unconfigure_radius_server
        * New API to unconfigure radius server
    * Added configure_license_smart_transport_callhome
        * added api to configure license smart transport callhome
    * Added execute_license_smart_trust_idtoken
        * added api to execute license smart trust idtoken
    * Added copy_startup_config_from_flash
        * API to copy startup config from the flash memory
    * Added clear_ip_arp_inspection
        * added api to clear_ip_arp_inspection stats and log
    * Added unconfigure_logging_buffered
        * New API to unconfigure logging buffered
    * Added unconfigure_power_efficient_ethernet_auto
        * New API to unconfigure power efficient ethernet auto on interface
    * Added an api clear_ip_ospf_rib to clear rib information from routers configured with ospf
    * Added configure_vlan_group_list and unconfigure_vlan_group_list
        * added api to configure and unconfigure vlan group
    * Added configure_ipv6_dhcp_pool_preifx_delegation_pool
        * added api to configure ipv6 dhcp pool prefix delegation pool
    * Added configure_ipv6_local
        * added api to configure ipv6 local pool or policy
    * Added configure_ipv6_prefix_name_on_interface
        * added api to configure ipv6 address with prefix name on interface
    * Added configure_ipv6_dhcp_client_pd_on_interface
        * added api to configure ipv6 dhcp client pd on interface
    * Updated enable_ipv6_dhcp_server
        * updated api with variable rapid_commit
    * Added configure_logging_buffered_persistent_url
        * New API to configure logging buffered, logging persistent url
    * Added execute_clear_redundancy_history
        * API to execute clear redundancy history
    * Added configure_diagnostic_bootup_level_minimal
        * API to configure diagnostic bootup level minimal
    * Added configure_cos
        * API to configure_cos
    * Modified `get_interface_packet_output_rate` API
        * Removed dependency with timestamp output
    * Modified `configure_ipsec_tunnel` API
        * Added arguments to support IPv6 based tunnel
    * Modified `config_interface_isis` API
        * Added `process` and `metric` arguments
    * Added `configure_isis_interface_metric` API
        * New API to configure ISIS metric under interface
    * Added `unconfigure_isis_interface_metric` API
        * New API to unconfigure ISIS metric under interface
    * Added `get_isis_interface_metric` API
        * New API to get ISIS interface metric on interface
    * Modified `execute_write_erase` API
        * Support multiple devices with Pcall
    * Modified `get_routes` API
        * Added `route` and `vrf` arguments
    * Modified `get_next_hops` API
        * Added `vrf` argument
    * Added `get_next_hops_with_vrf` API
        * New API to get next hop from routing table info
    * Added `get_outgoing_interface_with_vrf` API
        * New API to get outgoing interface from routing table info
    * Modified `restore_running_config` API
        * Added `delete_after`, `max_time` and `check_interval` arguments
    * Modified `get_vrf_route_distinguisher` API
        * Added `vrf` argument
    * Modified `get_devices` API
        * Changed `testbed` argument as optional
    * Added `get_devices_simple` API
        * New API to get devices based on runtime.testbeds
    * Added `check_memory_leaks` processor
        * New processor to check memory leak
    * Modified `Restore` class in abstracted_libs
        * Added `timeout` argument to restore config
    * Added configure_interface_ip_verify_source
        * API to configure ip verify source on interface
    * Added unconfigure_interface_ip_verify_source
        * API to unconfigure ip verify source on interface
    * Modified configure_ip_arp_inspection_validateip
        * added variable address_type to handle multiple inputs
    * Modified unconfigure_ip_arp_inspection_validateip
        * added variable address_type to handle multiple inputs
    * Added configure_ip_arp_inspection_log_buffer
        * API to configure ip arp inspection log-buffer
    * Added unconfigure_ip_arp_inspection_log_buffer
        * API to unconfigure ip arp inspection log-buffer
    * Added configure_ospf_redistributed_eigrp_metric
        * New API to configure ospf with redistributed eigrp metric-type
    * Added configure_eigrp_networks_redistribute_ospf
        * New API to configure eigrp with redistributed ospf metric-type
    * Added config_interface_ospfv3_cost API
        * API to configure interface OSPFv3 cost dynamic
    * Added unconfig_interface_ospfv3_cost API
        * API to unconfigure interface OSPFv3 cost dynamic
    * Added configure_l2vpn_evpn_flooding_suppression and unconfigure_l2vpn_evpn_flooding_suppression
        * API to Configure and Unconfigure the flooding suppression address resolution disable
    * Added clear_ip_arp_inspection_stats
        * API to Clear ip arp inspection statistics
    * Added the following NVE APIs
        * unconfig_nve_src_intf
        * unconfig_nve_vni_members
        * get_nve_vnis
        * get_nve_interface_tunnel
        * verify_nve_vni_no_entry
        * verify_nve_vni_members_cfg
    * Added execute_clear_platform_software_product_analytics_report
        * added API for execute "clear platform software product analytics report"
    * Added execute_test_platform_software_product_analytics_tdl_periodic
        * added API for execute "test platform software product analytics tdl periodic"
    * Added execute_test_platform_software_product_analytics_data_proc_sql_periodic
        * added API for execute "test platform software product analytics data proc sql periodic"
    * Added get_telemetry_report_all_kpis
        * added API for getting telemetry report all kpis
    * Added verify_license_smart_transport_support_telemetry
        * added API for verifying license smart transport support telemetry
    * Added configure_ipv6_local_pool
        * New API to Configure ipv6 local pool
    * Added uninstall_appliance_package
        * New API to uninstall appliance package
    * Added configure_crypto_map
        * New API to configure crypto map
    * Added delete_mac_acl
        * New API to delete mac ACL
    * Modified configure_mac_acl
        * Modified API to configure mac acl
    * Added unconfigure_mac_acl
        * New API to Un configuring MAC ACL
    * Added configure_switchport_port_security_aging_time
    * Added configure_switchport_port_security_aging_type
    * Added configure_switchport_port_security_maximum
    * Added clear_ipv6_ospf_process API
        * API for clear ipv6 ospf process
    * Added get_traceroute_ipv6_parsed_output
        * API to get parsed output of traceroute ipv6 command
    * Added unconfigure_stack_power_switch
        * API for un configures stack-power switch
    * Added config_policy_map_on_interface
        * New API to configure policy map on interface
    * Added unconfigure_policy_map_on_interface
        * New API to unconfigure policy map on interface
    * Added configure_device_sensor_filter_list
        * added api to configure device-sensor filter-list {protocol} list {list_name} commands
    * Added request_platform_software_process_core
        * added api to configure request platform software process core {process_type}
    * Added request_system_shell
        * added api to login to device system shell
    * Added unconfigure_device_sensor_filter_list
        * added api to unconfigure device-sensor filter-list {protocol} list {list_name} commands

* linux
    * Added get_snmp_snmpget API
        * API for snmp get request
    * Added get_snmp_snmpgetnext API
        * API for snmp get next request
    * Added get_snmp_snmpwalk_v3 API
        * API for snmpwalk version 3
    * Added set_snmp_snmpset API
        * API to configure via snmpset

* added unconfigure_stack_mac_persistent_timer
    * New API to unconfigure stack-mac persistent timer

* common
    * Added `verify_ping` processor
        * Verify ping result in parallel
    * Modified `execute_reload` API
        * Added `reload_command`, `error_pattern`, `devices` and `exclude_devices` arguments

* blitz
    * Added functionality, that will use timestamps in gnmi Subscribtions to measure transaction_time

* sdk
    * triggers
        * blitz
            * Added a logic to convert response object to a json to fix the Attribute error


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified config_port_security_on_interface
    * Modified configure_archive_logging
        * Added hidekeys, notify syslog fields to API
    * Modified configure_ospf_routing API
        * Modification done to include log_adjacency optional variable
    * Modified clear_flow_exporter_statistics API
        * Modification done to include exporter_name as optional variable
    * Fixed removeMissingComp API
        * Replaced older GNMI get operation with recent one
    * Added enable_system_integrity api
        * API to configure system integrity
    * Modify clear_flow_monitor_statistics API
        * Modified the API by adding monitor_name as argument and switch as optional
    * Modified remove_routing_ip_route
        * Modified the remove ip route API
    * Modified configure_bgp_neighbor_filter_description
        * Fixed the API if condition and description
    * Modified execute_vtp_primary
        * Modified api name in execute vtp primary
    * Modified perform_ssh
        * Added algorithm as an optional argument
    * Modified configure_aaa_authentication_login
        * Added group name argument to the API
    * Modified configure_aaa_authorization_exec_default
        * Added group name argument to the API
    * Modified configure_username
        * Added privilige argument to the API
    * Modified `verify_ping` API
        * Added AttributeError handling
    * Modified `learn_routing` processor
        * Fixed initializing default argument value
    * Modified configure_vrf_ipv6_eigrp_named_networks
        * Modified api configure vrf ipv6 eigrp named networks
    * Modified configure_switchport_port_security_mac_address
        * Added optional variable vlan_type to cater vlan parameter
    * Modified configure_switchport_port_security_maximum
        * Added optional variable vlan_type to cater vlan parameter
    * Updated configure_policy_map
        * updated api to configure policy_map
    * Added unconfigure_policy_map_type_service
        * updated api to configure policy_map typ service
    * Modified config_ip_on_interface
        * Added prefix_name options to API

* common
    * Updated `restore_running_configuration` processor
        * Enhanced to run in parallel for speed
    * Updated `save_running_configuration` processor
        * Enhanced to run in parallel for speed

* added disable_system_integrity api
    * API to unconfigure system integrity

* blitz
    * Fix to auto validate the keys in response with multiple list entry.


