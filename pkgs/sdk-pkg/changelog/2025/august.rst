--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_pvlan_for_input_service_policy
        * API to Configures private VLAN settings on an input interface.
    * Added configure_pvlan_for_output_service_policy
        * API to Configures private VLAN settings on an output interface.
    * Added configure_extended_acl_with_dscp
    * Added configure_rep_segment_auto
        * API to configure_rep_segment_auto
    * Added configure_fastrep_segment_auto
        * API to configure_fastrep_segment_auto
    * Added unconfigure_call_home_profile_destination_transport_method
        * API to unconfigure_call_home_profile_destination_transport_method
    * Added config API configure_crypto_isakmp_profile
    * Added config API unconfigure_crypto_isakmp_profile
    * cat9kv
        * Added API get_boot_variables and get_config_register
    * ISA
        * API to clear crypto isakmp
    * Added configure_ipv6_prefix_list_with_permit_deny
        * API to Configures ipv6 prefix list on Device
    * Added unconfigure_ipv6_prefix_list_with_permit_deny
        * API to unconfigures ipv6 prefix list on Device
    * Added config API configure_crypto_pki_http_max_buffer_size
    * Added config API unconfigure_crypto_pki_http_max_buffer_size
    * Added configure_ip_nat_switchover_http and unconfigure_ip_nat_switchover_http
        * API to configure_ip_nat_switchover_http and unconfigure_ip_nat_switchover_http
    * Added config API configure_crypto_pki_crl_request
    * Added config API unconfigure_crypto_pki_crl_request
    * Added execute API clear_crypto_pki
    * Added new API to configure ipv4 access list on line vty
        * API to configure ipv4 access list on line vty
    * Added new API to unconfigure ipv4 access list on line vty
        * API to unconfigure ipv4 access list on line vty
    * Added new API to configure ipv6 access list on line vty
        * API to configure ipv6 access list on line vty
    * Added new API to unconfigure ipv6 access list on line vty
        * API to unconfigure ipv6 access list on line vty
    * Added API to configure facility alarm temperature primary
        * Added support for configuring the primary temperature threshold for facility alarms.
        * The API allows setting the temperature threshold to 'high' and specifying the value.
    * Added API to unconfigure facility alarm temperature primary
        * Added support for unconfiguring the primary temperature threshold for facility alarms.
        * The API allows removing the temperature threshold configuration.
        * Added support for configuring and unconfiguring notifications for primary temperature alarms.
        * Added support for configuring and unconfiguring relay settings for primary temperature alarms.
        * Added support for configuring and unconfiguring syslog settings for primary temperature alarms.
    * Added API to configure facility alarm temperature secondary
    * Added API to unconfigure facility alarm temperature secondary
        * Added support for unconfiguring the secondary temperature threshold for facility alarms.
        * The API allows removing the temperature threshold configuration.
        * Added support for configuring and unconfiguring notifications for secondary temperature alarms.
        * Added support for configuring and unconfiguring relay settings for secondary temperature alarms.
        * Added support for configuring and unconfiguring syslog settings for secondary temperature alarms.
    * Added API to configure logging alarm
    * Added API to unconfigure logging alarm

* api to configure extended access-list with dscp configure.

* iosxe/health/health_core
    * Update the api to collect core files for stack devices.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_route_map_permit to add few arguments
        * Added global_nhop for default recursive global next hop
        * Added default_recursive for default recursive next hop
        * Added default_nhop_ip for default recursive next hop address
    * Modified unconfigure_route_map_permit to add few arguments
        * Added vrf for default recursive vrf next hop
        * Added global_nhop for default recursive global next hop
        * Added default_recursive for default recursive next hop
        * Added default_nhop_ip for default recursive next hop address
    * Updated password_recovery API, added init_connection to initialize connection
    * Removed
        * unconfigure_crypto_pki_server

* iosxe/platform/get
    * Refactored get_platform_model_number to reliably return chassis PID as a string.
    * Added fallback logic to gather PIDs from inventory slots if chassis PID is missing.
    * Normalized show version parsing to ensure consistent comparison with inventory PIDs.

* iosxe/rommon/utils
    * Updated device_rommon_boot api to use correct tftp boot command.
    * Updated device_rommon_boot api
        * Reordered the execution of execute_rommon_reset, execute_set_config_register

* iosxe/platform
    * Updated logic to handle standby scenario.

* iosxe/asr1k
    * Updated logic to handle standby scenario.

* sdk/utils
    * Modified password_recovery api
        * Moved init_connection to step 5 to handle the syslogs.

* iosxe/sdk-pkg
    * Added an api get_recovery_details to get recovery details.
    * Updated the device_rommon_boot to use the api to get details.

* nxos
    * Modified
        * Added flag to handle 'minimally-disruptive' mode for ISSU trigger in NXOS


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* iosxe/routing/configure
    * Added configure_ip_route_cache_on_interface API

* iosxe/platform
    * added 'show platform hardware qfp active feature alg statistics sip clear' api.


--------------------------------------------------------------------------------
                                    Fix/Add                                     
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_flow_record_match_datalink
        * Added nested if statement to account for 'match datalink {field_type} vlan {direction}' command.
    * Modified configure_fnf_flow_record_match_flow
        * Added else clause to if statement block for 'match flow {flow_name}' command.
    * Added configure_flow_record_transport API
        * Added new API to configure flow record transport fields match/collect source-port/destination-port/tcp flags.


