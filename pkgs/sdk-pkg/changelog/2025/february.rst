--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_interface_ip_subscriber
        * API to configure_interface_ip_subscriber
    * Added unconfigure_interface_ip_subscriber
        * API to unconfigure_interface_ip_subscriber
    * Added configure_ip_cef
        * API to configure_ip_cef
    * Added unconfigure_ip_cef
        * API to unconfigure_ip_cef
    * Added configure_ip_dhcp_client
        * API to configure_ip_dhcp_client
    * Added unconfigure_ip_dhcp_client
        * API to unconfigure_ip_dhcp_client
    * Added configure_ip_dhcp_server
        * API to configure_ip_dhcp_server
    * Added unconfigure_ip_dhcp_server
        * API to unconfigure_ip_dhcp_server
    * Added configure_tftp_server
        * API to configure_tftp_server
    * Added unconfigure_tftp_server
        * API to unconfigure_tftp_server
    * Added configure_interface_ipv6_rip
        * API to configure_interface_ipv6_rip
    * Added unconfigure_interface_ipv6_rip
        * API to configure_interface_ipv6_rip
    * Added configure_interface_ipv6_dhcp_server_allow_hint
        * API to configure_interface_ipv6_dhcp_server_allow_hint
    * Added unconfigure_interface_ipv6_dhcp_server_allow_hint
        * API to unconfigure_interface_ipv6_dhcp_server_allow_hint
    * Added configure_ipv6_dhcp_server
        * API to configure_ipv6_dhcp_server
    * Added unconfigure_ipv6_dhcp_server
        * API to configure_ipv6_dhcp_server
    * Added configure_ipv6_dhcp_relay_option
        * API to configure_ipv6_dhcp_relay_option
    * Added unconfigure_ipv6_dhcp_relay_option
        * API to unconfigure_ipv6_dhcp_relay_option
    * Added new API to configure ip dhcp ping packets
        * ip dhcp ping packets {packets_no}
    * Added new API to unconfigure ip dhcp ping packets
        * no ip dhcp ping packets {packets_no}
    * Added new API to configure ip dhcp remember
        * ip dhcp remember
    * Added new API to unconfigure ip dhcp remember
        * no ip dhcp remember
    * Added new API to configure ipv6 nd managed-config-flag on the interface
        * ipv6 nd managed-config-flag
    * Added new API to unconfigure ipv6 nd managed-config-flag on the interface
        * no ipv6 nd managed-config-flag
    * Added new API to configure ipv6 dhcp-relay bulk-lease
        * ipv6 dhcp-relay bulk-lease {option} {value}
        * ipv6 dhcp-relay bulk-lease {option}
    * Added new API to unconfigure ipv6 dhcp-relay bulk-lease
        * no ipv6 dhcp-relay bulk-lease {option} {value}
        * no ipv6 dhcp-relay bulk-lease {option}
    * Added new API to configure ipv6 dhcp relay destination global
        * API to configure ipv6 dhcp relay destination global
    * Added new API to unconfigure ipv6 dhcp relay destination global
        * API to unconfigure ipv6 dhcp relay destination global
    * Added new API to configure ipv6 dhcp pool functions
        * API to configure ipv6 dhcp pool functions
    * Added new API to unconfigure ipv6 dhcp pool
        * API to unconfigure ipv6 dhcp pool
    * Added unconfigure_ipv6_dhcp_pool_prefix_delegation_pool
        * added api to unconfigure_ipv6_dhcp_pool_prefix_delegation_pool under ipv6/configure.py
    * Added unconfigure_ipv6_local_pool
        * added api to unconfigure_ipv6_local_pool under ipv6/configure.py
    * Added unconfigure_ipv6_dhcp_client_pd_on_interface
        * added api to unconfigure_ipv6_dhcp_client_pd_on_interface under interface/configure.py
    * Added API configure_bfd_ospf_timers
        * added api to configure bfd timers for ospf
    * Added API rp_bfd_all_interfaces
        * API to enable BFD on all interfaces on the device
    * Added configure_route_map_with_description
        * API to configure route-map with description
    * Added route_map_unconfigure_description
        * API to unconfigure route-map with description
    * Added unconfigure_route_map
        * API to unconfigure route-map
    * Added configure_rep
        * New API to configure rep segment
    * Added configure_fastrep
        * New API to configure fastrep segment
    * Added unconfigure_rep
        * New API to unconfigure rep segment
    * Added unconfigure_fastrep
        * New API to unconfigure fastrep segment
    * Added new API to configure ipv6 dhcp binding track ppp
        * ipv6 dhcp binding track ppp
    * Added new API to unconfigure ipv6 dhcp binding track ppp
        * no ipv6 dhcp binding track ppp
    * Added new API to configure ipv6 dhcp route-add
        * ipv6 dhcp {route_add}
    * Added new API to unconfigure ipv6 dhcp route-add
        * no ipv6 dhcp {route_add}
    * Added new API to configure ipv6 dhcp server join all-dhcp-server
        * ipv6 dhcp server join all-dhcp-server
    * Added new API to unconfigure ipv6 dhcp server join all-dhcp-server
        * no ipv6 dhcp server join all-dhcp-server
    * Added new API to configure ip dhcp binding cleanup interval
        * ip dhcp binding cleanup interval {interval_time}
    * Added new API to unconfigure ip dhcp binding cleanup interval
        * no ip dhcp binding cleanup interval {interval_time}
    * Added configure_ipv6_dhcp_relay_source
        * API to configure ipv6 dhcp-relay trust source-interface {interface}
    * Added unconfigure_ipv6_dhcp_relay_source
        * API to unconfigure ipv6 dhcp-relay trust source-interface {interface}
    * Added configure_source_destination_remote_vlan
        * API for configure source destination remote vlan
    * Added unconfigure_source_destination_remote_vlan
        * API for unconfigure source destination remote vlan
    * Added configure_data_mdt
        * API to configure data mdt
    * Added new API to verify ip address on interface
        * API to verify ip address on interface
    * Added configure_interface_ipv6_dhcp_client_request_vendor
        * API to configure_interface_ipv6_dhcp_client_request_vendor
    * Added unconfigure_interface_ipv6_dhcp_client_request_vendor
        * API to unconfigure_interface_ipv6_dhcp_client_request_vendor
    * Added configure_interface_ipv6_dhcp_client_information
        * API to configure_interface_ipv6_dhcp_client_information
    * Added unconfigure_interface_ipv6_dhcp_client_information
        * API to unconfigure_interface_ipv6_dhcp_client_information
    * Added configure_ipv6_dhcp_test_relay
        * API to configure_ipv6_dhcp_test_relay
    * Added unconfigure_ipv6_dhcp_test_relay
        * API to unconfigure_ipv6_dhcp_test_relay
    * Added configure_ipv6_dhcp_test_server
        * API to configure_ipv6_dhcp_test_server
    * Added unconfigure_ipv6_dhcp_test_server
        * API to unconfigure_ipv6_dhcp_test_server
    * Added unconfigure_ipv6_dhcp_client_pd_on_interface
        * API to unconfigure_ipv6_dhcp_client_pd_on_interface
    * Added unconfigure_ip_unnumbered_on_interface
        * API to unconfigure_ip_unnumbered_on_interface
    * Added enable_ospf_bfd_all_interfaces
        * API to configure enable_ospf_bfd_all_interfaces
    * Added def configure_device_sensor_dhcpv6_snooping
    * Added def unconfigure_device_sensor_dhcpv6_snooping
    * SPAN
        * Added configure_remote_span_on_vlan
            * API to configure remote span on vlan
    * Added API set_isis_timers
        * API to configure isis timers on the device
    * Added configure_device_tracking_policy_reachable
        * API to configure device tracking options
    * Added configure_device_tracking_binding_globally
        * API to configure device-tracking binding vlan globally
    * Added unconfigure_device_tracking_binding_globally
        * API to unconfigure device-tracking binding vlan globally
    * Added configure_ip_dhcp_database
        * API to configure_ip_dhcp_database
    * Added unconfigure_ip_dhcp_database
        * API to unconfigure_ip_dhcp_database
    * Added configure_logging_host
    * Added unconfigure_logging_host
    * Added configure_logging_source_interface
    * Added unconfigure_logging_source_interface
    * Added API enable_eigrp_bfd_all_interfaces
        * configure api for Enabling bfd on all interfaces for eigrp instance
    * Added API configure_ospf_interface_cost
        * API to configure ospf interface cost on the device
    * Added API configure_radius_server_dtls_trustpoint
    * API to Configure radius server dtls trustpoint
    * Added configure_ipv6_pim_rp_vrf
        * configure api for ipv6 pim rp vrf
    * Added ip pim send-rp-announce Loopback0 scope 10
    * Added configure_interface_ip_ddns_update
        * API to configure_interface_ip_ddns_update
    * Added unconfigure_interface_ip_ddns_update
        * API to unconfigure_interface_ip_ddns_update
    * Added configure_interface_ip_dhcp_client
        * API to configure_interface_ip_dhcp_client
    * Added unconfigure_interface_ip_dhcp_client
        * API to unconfigure_interface_ip_dhcp_client
    * Added API set_platform_software_selinux
        * Added API to set_platform_software_selinux
    * Added new API to configure access-session tls-version
        * access-session tls-version {tls-version}
    * Added new API to unconfigure access-session tls-version
        * no access-session tls-version
    * Updated configure_eap_profile
        * updated api to configure_eap_profile for ciphersuite
    * Added configure_tracking_object
    * Added unconfigure_tracking_object
    * Added configure_preemption_easycli
        * New API to configure preemption easycli
    * Added unconfigure_preemption_easycli
        * New API to unconfigure preemption easycli
    * sdk-pkg
        * clear_raw_socket_transport_statistics_all
    * Added new API to configure ip dhcp relay on the interface
        * API to configure ip dhcp relay on the interface
    * Added new API to unconfigure ip dhcp relay on the interface
        * API to unconfigure ip dhcp relay on the interface
    * Added new API to configure ipv6 dhcp ping packets
        * API to configure ipv6 dhcp ping packets
    * Added new API to configure ip dhcp drop inform
        * API to configure ip dhcp drop inform
    * Added new API to unconfigure ip dhcp drop inform
        * API to unconfigure ip dhcp drop inform
    * Added
        * configure_scada_dnp3_serial_channel
        * configure_scada_dnp3_serial_session
        * configure_scada_dnp3_ip_channel
        * configure_scada_dnp3_ip_session
        * configure_scada_enable
        * unconfigure_scada_enable
        * unconfigure_scada_dnp3_ip_session
        * unconfigure_scada_dnp3_ip_channel
        * unconfigure_scada_dnp3_serial_session
        * unconfigure_scada_dnp3_serial_channel
        * configure_scada_t101_serial_channel
        * configure_scada_t101_serial_session
        * configure_scada_t101_serial_sector
        * configure_scada_t104_ip_channel
        * configure_scada_t104_ip_session
        * configure_scada_t104_ip_sector
        * unconfigure_scada_t104_ip_sector
        * unconfigure_scada_t104_ip_session
        * unconfigure_scada_t104_ip_channel
        * unconfigure_scada_t101_serial_sector
        * unconfigure_scada_t101_serial_session
        * unconfigure_scada_t101_serial_channel
    * Added unconfig_svi_vlan_range
        * API to unconfig_svi_vlan_range

* sdk
    * ios
        * Added new API to clear_idle_vty_sessions
    * iosxe
        * Added new API to clear_idle_vty_sessions
        * Added execute_issu_set_rollback_timer API
        * Added API for execute_issu_set_rollback_timer
        * Updated regex for is_management_interface
    * utils
        * Added abstract argument to parser call
        * Added time_to_int
        * Added PID_BREAKOUT_MAP
    * IOSXR
        * Added breakout_interface_names API

* sdk-pkg
    * ixos
        * Added api to get bandwidth


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified
        * Updated configure_interface_monitor_session API with additional optional argument to specify the monitor session direction.
    * Updated api configure_ip_on_tunnel_interface
        * updated api with ip_mode to support both ip and ipv4
    * Modified configure dhcp pool API to support all the dhcp pool parameters
        * API to configure dhcp pool
    * Added configure_ipv6_dhcp_relay_destination_ipv6address
        * API to configure_ipv6_dhcp_relay_destination_ipv6address
    * Added uncconfigure_ipv6_dhcp_relay_destination_ipv6address
        * API to unconfigure_ipv6_dhcp_relay_destination_ipv6address
    * cat9k
        * c9500
            * Updated API's to configure and unconfigure the ignore startup config
        * c9500
            * C9500-48Y4C
                * Added API's to configure and unconfigure the ignore startup config
    * Updated configure_interface_switchport_access_vlan
        * updated api to configure_interface_switchport_access_vlan
    * Updated configure_dialer_interface
        * updated api to configure_dialer_interface
    * Updated configure_ppp_multilink
        * updated api to configure_ppp_multilink
    * Updated clear_platform_software_fed_switch_active_access_security_table_counters
        * updated api to clear_platform_software_fed_switch_active_access_security_table_counters
    * Updated clear_platform_software_fed_switch_active_access_security_auth_acl_counters
        * updated api to clear_platform_software_fed_switch_active_access_security_auth_acl_counters
    * Modified configure_subinterface to include vrf
    * Modified config_interface_carrier_delay made delay_type an optional argument
    * Modified
        * Updated configure_replace API to raise SubCommandFailure exception if error pattern matched

* sdk
    * Generic
        * Added `disconnect_termserver` argument to `execute_clear_line`

* sdk-pkg
    * iosxe
        * updated the clear_idle_vty_sessions api
    * utils
        * updated the time_to_int function

* tooling
    * Modified Makefile
        * Updated makefile to include make jsons for each feature

* abstracted_libs
    * processors
        * Enhanced message for initialize_traffic


