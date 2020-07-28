
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.7         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* UTILS
    * Added send_email

* JUNOS
    * Added verify_file_size
    * Added verify_ldp_session
    * Added verify_ldp_database_session
    * Added verify_ospfv3_interface_in_database
    * Added verify_show_ospf_route_network_extensive
    * Added verify_ospf_interface_in_database
    * Added verify_ospf3_interface_in_database
    * Added verify_ospf3_database_prefix
    * Added verify_ospf_neighbors_not_found
    * Added verify_ospfv3_neighbors_not_found
    * Added verify_routing_routes
    * Added verify_ospfv3_router_id
    * Added verify_ospfv3_no_router_id
    * Added verify_ospf_router_id
    * Added verify_ospf_no_router_id
    * Added verify_routing_no_ospf_metric_match
    * Added verify_routing_ospf_metric_match_or_greater
    * Added request_chassis_routing_engine_master_switch
    * Added request_routing_engine_login_other_routing_engine
    * Added get_ospf_router_id
    * Added verify_log_exists
    * Added get_configuration_mpls_label_switched_path_name
    * Added get_configuration_mpls_paths
    * Added get_mpls_record_routes
    * Added get_ospf_database_checksum
    * Added verify_rsvp_neighbor
    * Added verify_rsvp_session_state
    * Added verify_bfd_session
    * Added get_log_message_time
    * Added get_system_uptime
    * Added get_system_current_time
    * Added verify_interfaces_input_output_policer_found
    * Added verify_ted_interface
    * Added verify_metric_in_route
    * Added get_interface_queue_counters_trans_packets
    * Added verify_igp_metric_in_ldp
    * Added delete_file_on_device
    * Added verify_hello_interval_holdtime
    * Added verify_ldp_interface
    * Added verify_traceroute_number_of_hops
    * Added verify_ping_loss_rate

* LINUX
    * Added get_platform_logging

* IOSXE
    * Added execute_reload under CAT9K platform

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOS
    * Added get_platform_default_dir
    * Added get_platform_core

* IOSXE
    * Added get_platform_default_dir
    * Added get_platform_core
    * Added get_platform_logging
    * Added get_platform_memory_usage
    * Added get_platform_cpu_load

* IOSXR
    * Added get_platform_default_dir
    * Added get_platform_core

* NXOS
    * Added get_platform_default_dir
    * Added get_platform_core
    * Fixed nxapi_method_nxapi_rest for get methods not returning data
    * updated nxapi_method_nxapi_rest to support passing expected return code
    * updated nxapi_method_nxapi_cli to support passing expected return code
    * updated nxapi_method_restconf to support passing expected return code

* JUNOS
    * Added get_platform_default_dir
    * Added get_class_of_service_shaping_rate
    * Added get_interface_output_error_drops
    * Added get_interface_statistics_output_error_drops
    * Added get_interface_queue_counters_dropped
    * Modified get_file_size
    * Modified 'verify_routing_ip_exist' to handle more variations
    * Modifid 'verify_routing_ip_exist' to handle more variations
    * Modifid 'verify_ospfv3_interface_in_database' to handle more variations
    * Modifid 'verify_ospf_interface_in_database' to handle more variations
    * Modified 'verify_ospf_interface' to look for hello-interface
    * Modified 'verify_ospf3_interface' to look for hello-interface
    * Modified 'verify_ospf_neighbors_found' for look only at a specific interface
    * Modified 'verify_ospf3_neighbors_found' for look only at a specific interface
    * Modified 'verify_ospf_neighbors_found' to look for an instance
    * Modified 'verify_ospf3_neighbors_found' to look for an instance
    * Modified 'verify_routing_route' to look for tag and table name
    * Modified 'verify_ospf3_neighbor_number' to support command "show ospf3 neighbor extensive"
    * Modified 'verify_ospf3_database_prefix' to support command "show ospf3 database link advertising-router {ipaddress} detail"
    * Modified 'verify_ospf_overview' to get overload time
    * Modified 'verify_ospf3_overview' to get overload time
    * Modified 'verify_ospf_database_lsa_id' to check link ID
    * Fixed verify_ospf3_neighbor_state to support command with extensive

*Blitz
    * By default save device name and make it reusable in the script
