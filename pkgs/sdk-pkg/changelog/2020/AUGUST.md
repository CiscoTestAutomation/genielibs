
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.8         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* IOSXE
    * Removed 'execute_reload' apis for cat9k and cat9500
        * Not needed since the default IOSXE level works
    * Added get_platform_cpu_load_detail
    * Added get_platform_memory_usage_detail

* Junos
    * Added get_chassis_memory_util
    * Added get_chassis_cpu_util
    * Added get_pfe_count
    * Added verify_interfaces_queue_packets
    * Added verify_pcap_dscp_bits
    * Added verify_bgp_best_path
    * Added verify_bgp_error_message
    * Added verify_bgp_last_error
    * Added verify_bgp_peer_state
    * Added verify_bgp_holdtime
    * Added verify_bgp_active_holdtime
    * Added verify_ldp_overview
    * Added get_interface_queue_counters_queued_packets
    * Added get_class_of_service_classifiers
    * Added verify_ospf_advertising_router_metric_in_database
    * Added is_push_present_in_route
    * Added verify_lsp_neighbor
    * Added get_rsvp_hello_sent
    * Added verify_class_of_service_interface
    * Added verify_pcap_packet_type
    * Added verify_pcap_packet_protocol
    * Added verify_pcap_packet_source_port
    * Added verify_pcap_packet_destination_port
    * Added get_configuration_mpls_label_switched_path_name
    * Added get_configuration_mpls_paths
    * Added verify_mpls_experimental_bits
    * Added verify_route_forwarding_type
    * Added get_route_table_switched_path_destination_address
    * Added verify_rsvp_session_state
    * Added verify_bfd_session
    * Added get_log_message_time
    * Added get_system_uptime
    * Added get_system_current_time
    * Added verify_interfaces_input_output_policer_found
    * Added verify_interfaces_queue_packets
    * Added verify_source_of_best_path
    * Added verify_cluster_list_length_of_path
    * Added verify_route_has_no_output
    * Added verify_next_hop_in_route
    * Added verify_protocol_next_hop_in_route
    * Added verify_bgp_not_peer_state
    * Added is_bgp_running
    * Added is_bgp_neighbor_authentication_key_configured
    * Added get_bgp_neighbor_prefixes_count
    * Added verify_no_ospfv3_interface_in_database:
        * show ospf3 database extensive
    * Added verify_no_ospf_interface_in_database:
        * show ospf database extensive
    * Added verify_ldp_session_status
        * show ldp session {address} detail
    * Added verify_ldp_restart_state
        * show ldp overview
    * Added verify_communities_in_route
        * show route {route} extensive
    * Added verify_route_table_label
        * show route table mpls.0 label {label}
    * Added verify_learned_protocol
        * show route {address} extensive
    * Added verify_push_present_in_show_route
        * show route {address} extensive
    * Added verify_route_flag
    * Added verify_route_best_path_metric
    * Added verify_route_non_best_path_metric
    * Added get_peer_bgp_address
        * get peer address via show bpg neighbor command
    * Added verify_bgp_all_neighbor_status
    * Added verify_bgp_updown_time
    * Added verify_route_as_length
    * Added verify_best_path_is_towards_to_interface
    * Added verify_metric_of_route
    * Added compare_metric_of_route
    * Added verify_rt_destination
    * Added verify_pcap_packet
    * Added get_interface_queue_counters_transmitted_byte_rate
    * Added verify_pcap_mpls_packet
        * Verifies pcap file values for mpls and ip packets
    * Added verify_route_table_output_interface
    * Added verify_route_forwarding_table
    * Added get_route_table_output_interface
    * Added get_route_table_output_label
    * Added get_ldp_database_session_label
    * Added verify_route_table_mpls_label
    * Added verify_route_advertised_protocol_community
    * Added get_route_advertising_label
    * Updated verify_route_has_no_output
        * Added command show route {protocol_type}-protocol {protocol} {address}
    * Updated verify_rt_destination
        * Added command show route {protocol_type}-protocol {protocol} {address}
        * Added command show route {route} extensive

* NXOS 
    * Added analyze_core_by_bingopy
    * Added start_perf
    * Added stop_perf_and_generate_svg
    * Added get_platform_cpu_load
    * Added get_platform_cpu_load_detail
    * Added get_platform_memory_usage
    * Added get_platform_memory_usage_detail

* LINUX
    * Added get_platform_logging
    * Added get_mpls_out_label
    * Added analyze_core_by_ucd

* Utils
    * Added verify_no_mpls_header
    * Added save_dict_to_json_file
    * Added load_dict_from_json_file

* BLITZ
    * Added looping ability to BLITZ
    * Added action compare 
    * Added ability to save values through regex
    * Added append and append to list for saving values more dynamically in the exisiting values
    * Added condition statement to BLITZ
    * Added action compare to BLITZ
    * Added section_continue
    * Added a converter to convert maple scripts into BLITZ testscripts
    * Added supportin maple converter features e.g maple action, maple_search action

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* COM
    * Modified configure_replace subsection:
      * To allow usage of device alias alongside device name

* Junos
    * Modified verify_log_exists to allow inversion
    * Enhanced verify_ping
    * Updated verify_route_best_path:
        * Added an argument: expected_to, and enhanced the API. 
    * Modified verify_route_best_path:
        * Added arguments "interface" and "extensive" to make the API support 
            show command "show route protocol bgp {interface} extensive"
    * Updated verify_next_hop_in_route
        * Added active_tag argument to verify next hop in best path
    * Modified verify_route_best_path:
        * Added one argument 'expected_med'
    * Modified verify_pcap_dscp_bits:
        * Changed to allow checking for ospf packets
        * Fixed gross logic and code
    * Modified get_pfe_count
        * Added variable formatting
    * Modified verify_routing_interface_preference
        * Added support for ip_address
    * Update verify_routing_route
        * added isNegativeCriteria as argument
        * Added expected_active_tag as an optional argument
        * Added expected_community as an optional argument
        * Verifies route community list 
    * Update verify_route_advertised_protocol_community
        * added isNegativeCriteria as argument
    * Update verify_ping
        * added mpls_rsvp as argument
    * Modified verify_interfaces_queue_packets:
        * Changed it to use get_values properly
    * Modified verify_pcap_dscp_bits
        * Added expected_src_port_number parameter
        * Added port_and_or parameter
        * Added check for turning protocol number to string
        * Added TCP check
        * Added RSVP check
    * Updated if condition in verify_route_flag

* NXOS
    * Modified nxapi_method_restconf and nxapi_method_nxapi_rest apis:
      * To follow what the nxapi GUI does

* Blitz
    * Modified:
        * aetest.setup and aetest.cleanup section discovery.
        If a section name starts with 'setup_' then it will be decorated with @aetest.setup. Same for cleanup.

* Utils
    * Fixed diff action in Blitz to judge difference properly
    * Updated get_interfaces to search based on link name instead of alias