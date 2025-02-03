--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_nat64_mapt_domain
        * API to configure nat64 mapt domain
    * Added unconfigure_nat64_mapt_domain
        * API to unconfigure nat64 mapt domain
    * Added configure_nat64_route
        * API to configure nat64 route
    * Added configure_nat64_mapt_ce
        * API to configure nat64 mapt ce
    * Added configure_nat_service_all_algs
        * API to configure nat service all algs
    * Added configure_nat_setting_gatekeeper_size
        * API to configure nat setting gatekeeper size
    * Added API request_platform_software_trace_archive
        * Added API to request_platform_software_trace_archive
    * Added configure_eem_applet_watchdog_time
    * Added configure_eem_action_cli_command
    * Added configure_eem_action_syslog_msg
    * Added configure_eem_action_wait
    * Added configure_eem_action_info_type_routername
    * Added configure_bgp_route_reflector_client
    * Added configure_fall_over_bfd_on_bgp_neighbor
    * Added unconfigure_interface_evpn_ethernet_segment
    * Added configure_l2vpn_evpn_ethernet_segment_all_active
    * Added api for clear_platform_software_fed_switch_active_access_security_table_counters
        * Added new api clear platform software fed switch active access-security table counters.
    * Added api for clear_platform_software_fed_switch_active_access_security_auth_acl_counters
        * Added new api clear platform software fed switch active access-security auth-acl counters .
    * Added configure_macro_auto_execute
        * API to configure macro auto template
    * Added unconfigure_macro_auto_execute
        * API to unconfigure macro auto template
    * Added configure_shell_trigger
        * API to configure shell trigger
    * Added unconfigure_shell_trigger
        * API to unconfigure shell trigger
    * Added configure_macro_auto_trigger
        * API to configure macro auto trigger
    * Added unconfigure_macro_auto_trigger
        * API to unconfigure macro auto trigger
    * Added configure_macro_auto_fallback
        * API to configure macro auto global processing {fallback} {parameters}
    * Added unconfigure_macro_auto_fallback
        * API to unconfigure macro auto global processing {fallback} {parameters}
    * Added Async specific APIs for line
        * configure_line for applying  configurations on line.
        * configure_line_raw_socket_tcp_client for raw socket client on line.
        * configure_line_raw_socket_tcp_server for raw socket server on line.
        * unconfigure_line for removing raw line configurations.
        * unconfigure_line_raw_socket_tcp_client for removing raw socket client on line.
        * unconfigure_line_raw_socket_tcp_server for removing raw socket server on line.
    * Added configure_radius_group_load_balance_method
    * Added configure_aaa_authorization_exec
    * Added unconfigure_aaa_authorization_exec
    * Added configure_aaa_authorization_console
    * Added unconfigure_aaa_authorization_console
    * Added configure_aaa_accounting_exec_default_start_stop
    * Added unconfigure_aaa_accounting_exec_default_start_stop
    * Added enable_ssh_on_vty
    * Added disable_ssh_on_vty
    * Added configure_login_authentication_on_vty
    * Added configure_authorization_exec_on_vty
    * Added unconfigure_login_authentication_on_vty
    * Added unconfigure_authorization_exec_on_vty
    * Added configure_aaa_authentication_enable_none
    * Added configure_ipv6_flow_monitor_sampler
        * added api to configure ipv6 flow monitor <monitor_name> sampler <sampler_name> input
    * Added configure_macro_auto_device_parameters
        * API to configure macro auto device {device_name} {parameters}
    * Added unconfigure_macro_auto_device_parameters
        * API to unconfigure macro auto device {device_name} {parameters}
    * Added configure_dhcp_option
        * API to configure ip dhcp pool with option
    * Added configure_ip_ddns_update_method
        * API to configure_ip_ddns_update_method
    * Added unconfigure_ip_ddns_update_method
        * API to unconfigure_ip_ddns_update_method
    * Added new API to configure rep ztp on the interface
        * rep ztp-enable
    * Added new API to unconfigure rep ztp on the interface
        * no rep ztp-enable
    * Added API's to configure cli commands for acl.
        * API to configure_protocol_acl_any_any
        * API to unconfigure_protocol_acl_any_any
    * Added locate_switch
        * API to locate switch
    * Added configure_interface_macro_description
        * API to configure macro description on interface
    * Added unconfigure_interface_macro_description
        * API to unconfigure macro description on interface
    * Added configure_macro_auto_mac_address_group
        * API to configure macro auto mac address group
    * Added unconfigure_macro_auto_mac_address_group
        * API to unconfigure macro auto mac address group
    * Added API set_platform_software_ilpower_mcu
        * Added API to set_platform_software_ilpower_mcu
    * Added config_pseudowire_class_interworking
    * cat9k
        * c9300
            * Added API's to configure and unconfigure the ignore startup config
        * c9400
            * Added API's to configure and unconfigure the ignore startup config
        * c9800
            * Added API's to configure and unconfigure the ignore startup config
        * c9500
            * Added API's to configure and unconfigure the ignore startup config
        * c9500
            * C9500-40X
                * Added API's to configure and unconfigure the ignore startup config
    * Added configure_mac_acl_etherType
    * Added configure_routing_ip_route_track
    * Added unconfigure_routing_ip_route_track
    * Added unconfigure_interface_speed_auto
        * API to unconfigure interface speed auto on interface
    * Added configure_ip_dhcp_relay_information_option_insert
        * API to configure_ip_dhcp_relay_information_option_insert
    * Added unconfigure_ip_dhcp_relay_information_option_insert
        * API to unconfigure_ip_dhcp_relay_information_option_insert
    * Added API show_platform_software_mcu_snapshot_detail_request
        * Added API to show_platform_software_mcu_snapshot_detail_request
    * Added Async specific apis for serial interface
        * API configure_interface_serial_physical_layer for configuring physical layer.
        * API unconfigure_interface_serial_physical_layer for unconfiguring physical layer.
        * API configure_interface_serial_encapsulation for configuring encapsulation.
        * API unconfigure_interface_serial_encapsulation for unconfiguring encapsulation.
        * API configure_interface_raw_socket_client for raw socket configuration.
        * API unconfigure_interface_raw_socket_client for raw socket unconfiguration.
    * Added
        * API for ip host <hostname> <ip_addr> (configure and unconfigure)
        * API for ip dns server (configure and unconfigure)


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_macro_auto_trigger
        * Modified api to configure trigger based on parameter passed
    * Modified configure_policy_map priority percent
    * Modified
        * Updated configure_monitor_capture API with additional arguments
    * Removed default argument trunk as True
    * Removed the configure_interface_rep_segment_edge_primary api from interface/configure.py and modified configure_rep_segment, configure_fast_rep_segment
    * Removed the unconfigure_interface_rep_segment_edge_primary api from interface/configure.py and modified unconfigure_rep_segment, unconfigure_fast_rep_segment
    * Modified configure_tacacs_server
        * Modified the api to configure tacacs server and use hostname instead of ip address as host
    * Updated configure_replace API, add hostname learning to detect hostname changes
    * Modified configure_interface_speed_auto
    * health/cpu
        * add handeling for InvalidCommandError

* genielibs
    * Removed `TriggerUnconfigureConfigureOspf` trigger from yaml file

* junos
    * Modified verify_ospf_interface_in_database
        * For newer version of `netaddr`, passing INET_ATON argument IPAddress to allow all kinds of weird-looking addresses to be parsed

* utils
    * Modified netmask_to_bits
        * For newer version of `netaddr`, passing INET_ATON argument IPAddress to allow all kinds of weird-looking addresses to be parsed
    * copy to device
        * Fixed the logic for proxy dev to check for proxy in servers
    * copy_to_device
        * add support for dual rp devices for http copy using proxy
    * copy to device
        * fix the logic for proxy dev to check for proxy in servers
    * copy to device
        * update the unittest for copy to device using proxy

* sdk/blitz
    * Change pyATS Health check logging to debug level

* health
    * Change pyATS Health check logging to debug level

* sdk
    * Made code 3.13 compliant

* sdk-pkg
    * Fix syntax warning


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* sdk-pkg
    * Add support for stack device password recovery


