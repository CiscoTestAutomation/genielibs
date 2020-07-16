* Please follow the template we introduced in NOVEMBER.md file.
* Every Trigger/verification need to be added under the corresponding feature.

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |               |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* UTILS
    * Added send_email

* JUNOS
    * Added verify_file_size
    * Added verify_ldp_session
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

* LINUX
    * Added get_platform_logging

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

* JUNOS
    * Added get_platform_default_dir
    * Added get_class_of_service_shaping_rate
    * Added get_interface_output_error_drops
    * Added get_interface_statistics_output_error_drops
    * Added get_interface_queue_counters_dropped
    * Modified get_file_size

*Blitz
    * By default save device name and make it reusable in the script

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* Junos
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
* NXOS
    * Fixed nxapi_method_nxapi_rest for get methods not returning data

* JUNOS
    * Fixed verify_ospf3_neighbor_state to support command with extensive
