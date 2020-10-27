
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.10        |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* IOSXE
    * Added get_valid_config_from_running_config api

* IOS
    * Added get_valid_config_from_running_config api
    * Added get_platform_logging api
    * Added get_platform_cpu_load api
    * Added get_platform_cpu_load_detail api

* Junos
    * Added verify_route_exists
    * Added verify_bgp_peer_option
    * Added verify_route_push_label
    * Added verify_route_table_label_output
    * Added verify_bgp_peer_as
    * Added get_route_as_path
    * Added verify_route_has_as_path_length
    * Added verify_as_path_of_route
    * Added get_file_timestamp
    * Added get_interface_traffic_input_pps
    * Added verify_firewall_filter
    * Added verify_firewall_packets
    * Added verify_preference_show_route
        * show route protocol bgp extensive {address}
    * Added verify_bgp_peer_prefixes_match
    * Added verify_bgp_peer_import_value
    * Added verify_route_has_as_path
    * Added verify_route_as_path_count
    * Added verify_route_all_as_length
    * Added verify_route_same_as_peer_local
    * Added get_bgp_peer_prefixes
    * Added get_routing_best_routes
    * Added get_interface_traffic_output_pps
    * Added verify_route_best_path_counter
    * Added verify_cluster_exists_in_route
    * Added get_peer_restart_flags_received
    * Added get_routing_metric
    * Added get_routing_best_path_peer_id
    * Added get_routing_nonbest_path_peer_id
    * Added verify_firewall_counter

* NXOS 
    * Added enable_backtrace api
    * Added get_valid_config_from_running_config api

* IOSXR
    * Added get_platform_cpu_load api
    * Added get_platform_cpu_load_detail api
    * Added get_valid_config_from_running_config api
    * Added get_platform_memory_usage api
    * Added get_platform_memory_usage_detail api

* ASA
    * Added get_running_config_dict api

* Processors:
    * Added configure_replace
    * Added delete_configuration

* Blitz
    * Added 'feature' in 'diff' action to get exclude list from Ops
    * Added 'mode' in 'diff' action to get specific mode such as 'add', 'remove', 'modified'
    * Added include/exclude to bash_console
    * Added support for all the keyword arguments that unicon supports for configure and execute action.
    * Added access to job related values in trigger datafile (e.g. runtime.job.name, section.uid, task.id etc.).
    * Added custom starting step message.
    * Added expected_failure feature for all actions.

* Utils
    * Added verify_login_with_credentials
    * Added get_connection
    * Added get_system_users
    * Added get_system_connections_sessions
    * Added unit_convert api


--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOS
    * Datafiles
        * Fixed to load ios default datafiles

* IOSXE
    * Modified execute_install_package api:
        * To allow for dynamic reconnect timeout
        * To log connection issues during connect polling
    * Modified get_platform_memory_usage_detail to remove unnecessary code

* Junos
    * Updated verify_route_has_as_path
        * Added parameter 'non_extensive' to let it support 'show route protocol bgp'
    * Modified verify_route_has_no_output:
        * Added arguments 'peer_address' and 'target_address'
    * Modified verify_route_is_advertised_or_received:
        * Added arguments 'protocol', 'extensive' and 'invert'
    * Modified verify_route_has_as_path:
        * Added arguments 'protocol_type' and 'peer_address'
    * Modified verify_route_is_advertised_or_received:
       * Added one argument 'target_address', now it supports command 'show route {protocol_type}-protocol {protocol} {address} {target_address}'
    * Update verify_ping to support source as argument
    * Updated verify_route_non_best_path_metric to pass protocol as argument
    * Modified verify_routing_route:
        * Added one argument 'single_community'
    * Modified verify_file_details_exists
        * Added invert parameter
    * Updated verify_routing_ip_exist:
        * Added arguments: protocol_type, command address, and enhanced the API.
    * Modified verify_route_has_no_output
        * Allows it to be inverted
    * Modified get_log_message_time
        * Allows it to select a file to check. Defaults to messages
        * Allows it to check for microseconds
    * Modified verify_best_path_is_towards_to_interface
        * Supports different arguments check
    * Modified verify_learned_protocol
        * Added cluster_value parameter
    * Modified get_chassis_cpu_util
        * Added parameter so you can verify cpu utilization section
    * Modified verify_bgp_updown_time
        * Modified code so only one regex pattern gets matched
        * Added parameter 'flip' to verify if up/down time is either less than 'given_time'
    * Modified verify_route_all_as_length
        * Strips 'AS Path' from as-path
    * Modified verify_route_as_path_count
        * Strips 'AS Path' from as-path
        * Added 'as_path = list()' to beginning to resolve undeclared variable error

* Utils
    * Updated verify_login_with_credentials
        * Added hostname as argument
    * Updated get_system_users
        * Returns list of users instead of dictionary

* Processor
    * Updated delete_configuration to handle all devices

* NXOS Triggers
    * class ProcessRestartLib:
        * Fixed Urib process skip switchover

* Blitz
    * Fixed the issue with parse on resend command
