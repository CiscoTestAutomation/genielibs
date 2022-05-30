--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_interface_switchport API
        * API for configure interfaces on switchport
    * Added configure_ip_unnumbered_loopback API
        * API for configure ip unnumbered loopback
    * Added configure_span_monitor_session API
        * API for configure span monitor session
    * Added unconfigure_span_monitor_session API
        * API for unconfigure span monitor session
    * Added configure_stack_mac_persistent_timer API
        * API for stack_mac-persistent timer {mac_timer}
    * Added configure_stack_mac_persistent_timer API
        * API for stack_mac-persistent timer {mac_timer}
    * Added execute_diagnostic_start_switch_module_test API
        * API for diagnostic start switch {switch_num} module {mod_num} test {include}
    * Added verify_Software_Fed_Active_Ipv6_Mld_Snooping_Vlan
        * Added new api to verify value parallel to provided key in dict from the mentioned command in API
    * Added verify_Software_Fed_Igmp_Snooping
        * Added new api to verify value parallel to provided key in dict from the mentioned command in API
    * Added verify_Software_Fed_Ipv6_Mld_Snooping_Groups
        * Added new api to verify value parallel to provided key in dict from the mentioned command in API
    * Added verify_software_fed_ip_igmp_snooping_groups
        * Added new api to verify value parallel to provided key in dict from the mentioned command in API
    * Modified configure_ipsec_tunnel to add vrf option
    * Modified configure_ikev2_profile_pre_share to add vrf option
    * Added configure_mdns_active_response_timer API
        * API for configuring mDNS(Multicast Domain Name System) active response timer
    * Added unconfigure_mdns_active_response_timer API
        * API for unconfiguring mDNS(Multicast Domain Name System) active response timer
    * Added configure_mdns_service_query_timer_periodicity API
        * API for unconfiguring mDNS(Multicast Domain Name System) service query timer periodicity
    * Added clear_mdns_controller_statistics API
        * API for configuring mDNS(Multicast Domain Name System) controller statistics
    * Added configure_mdns_service_policy API
        * API for unconfiguring mDNS(Multicast Domain Name System) service policy
    * Added configure_default_mdns_controller API
        * API for configuring mDNS(Multicast Domain Name System) default mdns controller
    * Added configure_controller_policy API
        * API for configuring mDNS(Multicast Domain Name System) controller policy
    * Added unconfigure_controller_policy_service_export API
        * API for unconfiguring mDNS(Multicast Domain Name System) controller policy service export
    * Added unconfigure_mdns_service_policy API
        * API for unconfiguring mDNS(Multicast Domain Name System) service policy
    * Added unconfigure_mdns_service_policy_vlan API
        * API for unconfiguring mDNS(Multicast Domain Name System) service policy vlan
    * Added unconfigure_mdns_gateway_globally API
        * API for unconfiguring mDNS(Multicast Domain Name System) gateway globally
    * Added unconfigure_mdns_trust API
        * API for unconfiguring mDNS(Multicast Domain Name System) trust
    * Added force_unconfigure_static_nat_route_map_rule API
        * API for force unconfiguring static nat route-map rule
    * Added configure_dhcp_relay_short_lease API
        * configure configure dhcp relay short lease on router
    * Added unconfigure_dhcp_relay_short_lease API
        * unconfigure dhcp relay short lease on router
    * Added configure_ethernet_vlan_unlimited API
        * configure ethernet vlan unlimited on subslot
    * Added unconfigure_ethernet_vlan_unlimited API
        * unconfigure ethernet vlan unlimited on subslot
    * Added configure_ip_vrf_forwarding_interface API
        * configure ip vrf forwarding on interface
    * Added unconfigure_ip_vrf_forwarding_interface API
        * unconfigure ip vrf forwarding on interface
    * Added create_ip_vrf API
        * create ip vrf on router
    * Added delete_ip_vrf API
        * delete ip vrf on router
    * Added enable_dhcp_relay_information_option API
        * configure dhcp relay information option on router
    * Added disable_dhcp_relay_information_option API
        * unconfigure dhcp relay information option on router
    * Added API 'execute_diagnostic_start_module_test'
    * Added configure_hw_module_breakout API
        * configuring hw_module breakout
    * Added unconfigure_hw_module_breakout API
        * unconfiguring hw_module breakout
    * Added configure_vpdn_group API
    * Added unconfigure_vpdn_group API
    * Added configure_ip_ospf_mtu_ignore
        * Added new API for configuring ip ospf mtu-ignore
    * Added unconfigure_ip_ospf_mtu_ignore
        * Added new API for unconfiguring ip ospf mtu-ignore
    * Added Verify_ospf_icmp_ping
        * Verifying "ping <ip> df size <size>"
    * Added configure_dope_wrsp API
        * Added new API to configure WRSP parameters in dope shell
    * Added get_show_derived_interface_dict API
        * get_show_derived_interface_dict to get the IPv4 and IPv6 ACLs
    * Added clear_ip_traffic API
        * clear_ip_traffic to clear ip traffic counters
    * modified API 'configure_nve_interface'
        * Added l3vni option for nve interface
    * Added configure_switchport_trunk_vlan API
        * Configure switchport trunk vlan on Device
    * Added configure_switchport_trunk_vlan_with_speed_and_duplex API
        * Configure switchport trunk vlan on interface with speed and duplex type on Device
    * Added get_switch_qos_queue_config_on_interface API
        * Get platform hardware fed on switch and qos queue config on Interface
    * Added config_policy_map_on_device API
        * Configure policy-map type on Device
    * Added perform_telnet API
        * API to perform telnet
    * Updated execute_card_OIR API
        * API for Card OIR powercycle
    * Updated execute_card_OIR_remove API
        * API for Card OIR remove
    * Updated execute_card_OIR_insert API
        * API for Card OIR insert
    * Added verify_matm_mactable API
    * Added API for configure ipv6 static route
        * 'configure_ipv6_static_route'
    * Added API for un-configure ipv6 static route
        * 'unconfigure_ipv6_static_route'


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API configure_local_span_source
        * added api to configure local span for source interface
    * Added API configure_local_span_destination
        * added api to configure local span to specficy destination interface
    * Added API remove_all_span
        * added api to unconfigure all span session
    * Added `verify_ptp_profile` API to verify the configured ptp profile using "show run | include ptp" command
    * Modified api 'transceiver_info'
        * changed the comments according to the function args
    * Modified `execute_write_memory` API, added dialog to handle confirm prompt
    * Modified configure_enable_nat_scale API
        * Added dialog to configure_enable_nat_scale
    * Modified configure_fnf_exporter API
        * Made few arguments as optional
    * Modified configure_fnf_record API
        * Made collect interface as Optional
    * Modified api 'verify_file_exists'
        * Api returns False if folder and/or file does not exist
    * Modified API for configure/unconfigure ipsec tunnel
        * 'configure_ipsec_tunnel'
        * 'unconfigure_ipsec_tunnel'
    * Modified API for configure ikev2 profile pre share
        * 'configure_ikev2_profile_pre_share'

* generic
    * Fix copy_to_device API filename path
    * Add support for sshtunnel host as proxy for copy_to_device and copy_from_device APIs

* all
    * Modified
        * Ignore unconnected devices in learn_system_defaults setup subsection

* ios
    * Modified `execute_write_memory` API, added dialog to handle confirm prompt
    * Modified api 'verify_file_exists'
        * Api returns False if folder and/or file does not exist

* blitz
    * gNMI subscibe ONCE and POLL not working
        * Fix thread handling for action, add poll message, fix verification.
    * Fix for gNMI subscibe and get returns validation not working for Boolean "False" and 0 values
        * Fix for xpath appending an extra '/' at the start, causing error in validation.
    * loop action
        * fixed the markup issue with range


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified clear_crypto_session API
        * clear_crypto_session to clear crypto sessions
    * Modified perform_ssh API
        * API to perform ssh


