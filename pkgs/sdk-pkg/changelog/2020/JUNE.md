
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.6         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* JUNOS
    * Added verify_default_route_protocol
    * Added verify_ospf_interface_type
    * Added verify_ospf_neighbor_state
    * Added verify_no_ospf_neigbor_output
    * Added verify_neighbor_state_went_down
    * Added verify_ospf3_interface_type
    * Added verify_ospf3_neighbor_state
    * Added verify_no_ospf3_neigbor_output
    * Added verify_ospf_interface
    * Added verify_ospf_neighbor_number
    * Added verify_ospf3_neighbor_number
    * Added verify_ospf3_interface
    * Added get_route_destination_address
    * Added verify_ospf_spf_delay
    * Added verify_ospfv3_spf_delay
    * Added is_logging_ospf_spf_logged
    * Added verify_diff_time_between_logs
    * Added get_interface_speed
    * Added verify_ospf_metric
    * Added verify_ospf3_metric
    * Added get_ospf_metric
    * Added verify_ospf3_neighbors_found
    * Added verify_ospf3_overview
    * Added verify_ospf_neighbors_found
    * Added verify_ospf_overview
    * Added verify_show_ospf_database_lsa_types
    * Added verify_show_ospf3_database_lsa_types
    * Added verify_ospf_interface_in_database
    * Added verify_ospf3_interface_in_database
    * Added verify_ospf3_database_prefix
    * Added verify_ospf_neighbors_not_found
    * Added verify_ospfv3_neighbors_not_found
    * Added verify_routing_routes

* Processors:
    * Enhanced pre_execute_command and post_execute_command processors. Now both have an option to save show command outputs as file.

* Common API:
    * Added slugify to convert special characters such as backslash, dot and etc to underscore
    * Added verify_pcap_has_imcp_destination_unreachable and verify_pcap_has_imcpv6_destination_unreachable for verifying pcap files
    * Added repeat_command_save_output to Execute the command on the device and store the output to file

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

* Blitz:
    * Fixed the polling issue in blitz
    * Fixed run_genie_sdk action
