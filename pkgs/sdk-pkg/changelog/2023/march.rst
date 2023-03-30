--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_evpn_instance_vlan_based_flood_suppression
        * API for to configure evpn instance vlan based flood suppression
    * Added unconfigure_evpn_instance_vlan_based_flood_suppression
        * API to unconfigure evpn instance vlan based flood suppression
    * Added configure_authentication_control_direction
        * added api to configure authentication control-direction
    * Added unconfigure_authentication_control_direction
        * added api to unconfigure authentication control-direction
    * Added configure_authentication_open
        * added api to configure authentication open
    * Added unconfigure_authentication_open
        * added api to unconfigure authentication open
    * Add a get API to retrieve the whole MPLS forwarding-table.
    * Added configure_interface_switchport
        * API for to configure switchport on interface
    * Added configure_ptp_vlan
        * API for to configure ptp vlan on interface
    * Added unconfigure_ptp_vlan
        * API for to unconfigure ptp vlan on interface
    * modified API  unconfigure_source_template_global
        * modified api unconfigure_source_template_global to address duplicate names
    * Added configure_ipv6_traffic_filter_acl
        * API to configure ipv6 traffic-filter {acl} {direction} on vlan interface range
    * Added unconfigure_ipv6_traffic_filter_acl
        * API to unconfigure ipv6 traffic-filter {acl} {direction} on vlan interface range
    * Added configure_ip_dhcp_restrict_next_hop
        * added api to configure ip dhcp restrict-next-hop on interface
    * Added unconfigure_ip_dhcp_restrict_next_hop
        * added api to unconfigure ip dhcp restrict-next-hop on interface
    * Added configure_aaa_accounting_exec_default_start_stop_group
        * API to configure aaa accounting exec default start-stop group
    * Added unconfigure_aaa_accounting_exec_default_start_stop_group
        * API to unconfigure aaa accounting exec default start-stop group
    * Added configure_local_span_filter
        * New API to configure local span filter
    * Added unconfigure_local_span_filter
        * New API to unconfigure local span filter
    * Added configure_policy_map_with_dscp_table
        * New API to configure policy map with dscp table
    * Added configure_policy_map_with_percent
        * New API to configure policy map with percentage value
    * Added configure_policy_map_with_no_set_dscp
        * New API to configure policy map with no set dscp value
    * Added configure_service_policy_with_queueing_name
        * API to configure service policy map with queueing type
    * Added unconfigure_policy_map_with_type_queue
        * API to unconfigure policy map with queue type
    * Added configure_policy_map_with_dscp_police
        * API to configure policy map with dscp
    * Added configure_table_map
        * API to configure table map from value to to value
    * Added unconfigure_table_map
        * API to unconfigure table map from value to to value
    * Added configure_interface_monitor_session_shutdown
        * API to configure monitor session on interface by shuttingdown
    * Added configure_ip_dhcp_snooping_limit
        * New API to configure ip dhcp snooping limit rate on interface
    * Added clear_ip_bgp_ipv6_unicast
        * API for clear ip bgp ipv6 unicast {route}
    * Added configure_ip_dlep
        * added api to configure ip dlep
    * Added unconfigure_ip_dlep
        * updated api to unconfigure ip dlep
    * Added configure_physical_interface_vmi
        * added api to configure vmi interface pppoe-rar mode
    * Added config_interface_ospfv3
        * updated api to configure network, hello_interval
    * Added configure_virtual_template
        * updated api to configure authentication, load_delay, mss, mtu
    * Added execute_switch_clear_stack_mode API
        * API to execute clear stack-mode for a switch
    * Added execute_switch_role API
        * API to switch role mode for a switch
    * Added unconfigure_ipv6_pim_bsr_candidate_bsr
        * added api to unconfigure ipv6 pim bsr candidate bsr
    * Added unconfigure_ipv6_pim_bsr_candidate_rp
        * added api to unconfigure ipv6 pim bsr candidate rp
    * Added configure config_pim_acl
        * added api to configure ipv6 pim accept-register lis acl_name
    * Added unconfigure unconfig_pim_acl
        * added api to unconfigure ipv6 pim accept-register lis acl_name
    * Added configure_ipv6_mld_join_group_acl
        * added api to configure ipv6 mld join-group saddress source-lis acl_name
    * Added unconfigure_interface_datalink_flow_monitor
        * API for unconfigure datalink flow monitor
    * Added execute_clear_ip_nat_translation
        * API for clearing ip nat translation
    * Fixed configure_bgp_neighbor_filter_description
        * Fix a conditional statement
    * Added unconfigure_static_ip_route_all API
        * API to unconfigure static ip route
    * Added configure_diagnostic_monitor_syslog
        * API to enable configure diagnostic monitor syslog
    * Added unconfigure_diagnostic_monitor_syslog
        * API to disable configure diagnostic monitor syslog
    * Added unconfigure_device_classifier_command
        * API to unconfigure device classifier command
    * Added unconfigure_device_classifier_profile_command
        * API to unconfigure device classifier profile command
    * Added configure_device_classifier_command
        * API to configure device classifier command
    * Added unconfigure_device_classifier_profile
        * API to unconfigure device classifier profile
    * Added unconfigure_device_classifier_operator
        * API to unconfigure device classifier operator
    * Added configure_dscp_global
        * API to configure global dscp values
    * Added unconfigure_dscp_global
        * API to remove configuration of global dscp values
    * Added configure_flow_monitor_on_vlan_configuration API
        * API to Configure Flow Monitor on vlan configuration
    * Added unconfigure_flow_monitor_on_vlan_configuration API
        * API to Unconfigure Flow Monitor on vlan configuration
    * Added execute_license_smart_save_usage_all_file
        * API to excute license smart save usage all file
    * Added execute_more_file_count
        * API to execute more file <filepath> | count <regex>
    * Added execute_license_smart_save_usage_unreported_file
        * API to execute license smart save usage unreported file
    * Added unconfigure_dscp_radius_server
        * New API to unconfigure dscp authentication and accounting values in radius server configuration
    * Added unconfigure_dscp_radius_server_group
        * New API to unconfigure dscp authentication and accounting values in radius server group configuration
    * Added configure_mdt_auto_discovery_vxlan
        * New API to configure mdt auto discovery vxlan under vrf definition
    * Added configure_ip_dhcp_exclude_vrf
        * New API to configure ip dhcp exclude vrf on device
    * Added configure_ipv6_mld_access_group
        * New API to configure ipv6 mld access group
    * Added unconfigure_ipv6_mld_access_group
        * New API to unconfigure ipv6 mld access group
    * Added configure_ptp_announce_transmit
        * API for to configure ptp announce transmit on interface
    * Added unconfigure_ptp_announce_transmit
        * API for to unconfigure ptp announce transmit on interface
    * Added configure_ipv6_route_nexthop_vrf API
        * API to configure ipv6 route nexthop vrf
    * Added unconfigure_ipv6_route_nexthop_vrf API
        * API to unconfigure ipv6 route nexthop vrf
    * Added unconfigure_system_mtu API
        * API to unconfigure system mtu
    * Added clear_ip_eigrp_neighbor
        * API to clear ip eigrp neighbor
    * Added configure_eigrp_passive_interface API
        * API to configure passive interface in eigrp ipv4
    * Added unconfigure_eigrp_passive_interface API
        * API to unconfigure passive interface in eigrp ipv4
    * Added configure_eigrp_passive_interface_v6 API
        * API to configure passive interface in eigrp ipv6
    * Added unconfigure_eigrp_passive_interface_v6 API
        * API to unconfigure passive interface in eigrp ipv6
    * modified  configure_hsrp_interface API
        * Modification done including the HSRP ipv6 configuration under the interface
    * Added get_policy_map_interface_queue_output
        * API to get policy map queuing interfaces
    * Added
        * config_interface_ospfv3_network_type
        * unconfig_interface_ospfv3_network_type
        * config_interface_ospfv3_flood_reduction
        * unconfig_interface_ospfv3_flood_reduction
    * Added configure_ipv6_mld_snooping_enhance and uconfigure_ipv6_mld_snooping_enhance
        * API to configure mld snooping, unconfig
    * Added configure_ip_pim_ssm and unconfigure_ip_pim_ssm
        * API to configure ip pim ssm , unconfigure
    * Added unconfigure_ip_igmp_snooping_vlan_mrouter_interface
        * API to unconfigure ip igmp snooping vlan
    * Added configure_route_map_permit and unconfigure_route_map_permit
        * API to configure route map, unconfig
    * Added configure_ipv6_ospf_router_id
        * New API to configure ipv6 ospf router id
    * Added configure_macro_auto_processing_on_interface
        * New API to configure macro auto processing on device interface
    * Added unconfigure_macro_auto_processing_on_interface
        * New API to unconfigure macro auto processing on device interface
    * Added configure_switchport_trunk_pruning_vlan_except
        * New API to configure switchport trunk pruning vlan except vlan numbers
    * Added configure_vtp_trunk_interface
        * New API to configure vtp trunk interface
    * Added execute_config_confirm
        * New API to execute the config confirm
    * Added execute_device_dir_path
        * New API to execute the device dir flash for total bytes
    * Added execute_archive_config
        * New API to execute archive config on device
    * Added restore_running_config_file
        * Modified API restore running config file

* blitz
    * Made that gnmi tests are not aborted in case of an error, but are always executed until max_stream/polls_number is reached
    * Added decimal_64 type handling
    * Combined sample_interval and polls_number into single parameter named sample_poll
    * Added support for "any" operator for returned value verification.
        * If datatype is correct the test passes regardless of value.


--------------------------------------------------------------------------------
                                       ~                                        
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modify configure_nat64_prefix_stateful API
        * Modified the API by adding vrf_name parameter
    * Modify unconfigure_nat64_prefix_stateful API
        * Modified the API by adding vrf_name parameter
    * Modify configure_nat64_v6v4_static API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modify unconfigure_nat64_v6v4_static API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modify configure_nat64_v4_list_pool API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modify unconfigure_nat64_v4_list_pool API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modify configure_nat64_v4_list_pool_overload API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modiy uconfigure_nat64_v4_list_pool_overload API
        * Modified the API by adding vrf_name and match_in_vrf parameters
    * Modified configure_isis_with_router_name_network_entity
        * Modified api configure isis with router name network_entity, vrf and redistribute bgp
    * Modified unconfig_interface_ospfv3
        * Modified unconfig_interface_ospfv3 to add option for unconfiguring network
    * Modified configure_ip_igmp_join_group_source
        * Modified api name in configure ip igmp join group source
    * Modified unconfigure_ip_igmp_join_group_source
        * Modified api name in unconfigure ip igmp join group source
    * Modified perform_telnet
        * Fixed the API perform_telnet to handle the prompt 'Password' after sending the CLI 'enable' while performing telnet
    * Uplifted configure_radius_server
        * Uplifted the API to accommodate dscp authentication and accounting values in radius server configuration
    * Uplifted configure_radius_group
        * Uplifted the API to accommodate dscp authentication and accounting values in radius group configuration
    * Modified configure_vrf_ipv6_eigrp_named_networks
        * Modified vrf ipv6 eigrp
    * Modified perform_ssh API
        * Added hmac field in the API

* blitz
    * Fixed transaction_time for gnmi subscribe SAMPLE


