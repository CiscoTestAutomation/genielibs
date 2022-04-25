--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added execute_switch_renumber API
        * API for switch renumbering
    * Added 'configure_private_vlan_on_vlan' API
        * configure private vlan on device
    * Added 'disable_ip_dhcp_auto_broadcast' API
        * disable ip dhcp auto broadcast on device
    * Added 'enable_ip_dhcp_auto_broadcast' API
        * enable ip dhcp auto broadcast on device
    * Added 'enable_dhcp_smart_relay' API
        * enable dhcp smart relay on device
    * Added 'disable_dhcp_smart_relay' API
        * disable dhcp smart relay on device
    * Added 'unconfigure_ip_dhcp_snooping_verify' API
        * unconfigure ip dhcp snooping verify on device
    * Added 'configure_ip_dhcp_client' API
        * configure ip dhcp client on device
    * Added 'configure_uplink_interface' API
        * configure uplink interface setup on interface
    * Added 'configure_downlink_interface' API
        * configure downlink interface setup on interface
    * Added 'configure_switchport_trunk_native_vlan' API
        * configure switchport trunk native vlan on interface
    * Added 'configure_switchport_mode_trunk_snooping_trust' API
        * configure switchport mode trunk snooping trust on interface
    * Added 'configure_egress_interface' API
        * configure egress interface on interface
    * Added unconfigure_interfaces_on_port_channel API
        * API for unconfigure interfaces on port channel
    * Added execute_redundancy_reload API
        * API for redundancy reload peer
    * Added configure_interface_tunnel_hub API
        * Added new API for configuring Interface Tunnel Hub
    * Added configure_interface_tunnel_spoke API
        * Added new API for configuring Interface Tunnel Spoke
    * Added configure_interface_virtual_template API
        * Added new API for configuring Interface Virtual Template
    * Added API 'unconfigure_ikev2_keyring'
    * Added API 'unconfigure_ikev2_profile'
    * Added API 'clear_crypto_session'
    * Added clear_device_tracking_messages API
        * API for clearing device-tracking messages
    * Added DHCPv4 APIs
        * Added get_dhcpv4_server_stats API
        * Added get_dhcpv4_server_bindings API
        * Added get_dhcpv4_binding_address_list API
        * Added clear_dhcpv4_server_stats API
        * Added verify_dhcpv4_packet_received API
        * Added verify_dhcpv4_binding_address API
    * Added DHCPv6 APIs
        * Added get_dhcpv6_server_stats API
        * Added get_dhcpv6_server_bindings API
        * Added get_dhcpv6_binding_address_list API
        * Added verify_dhcpv6_packet_received API
        * Added verify_dhcpv6_binding_address API
    * Added get_static_routing_routes API
        * API for getting static routes, in a similar way to get_routing_routes
    * Added configure_ip_local_pool API
        * configure ip local pool on router
    * Added configure_mdns_service_list API
        * API for configuring mDNS(Multicast Domain Name System) service list
    * Added unconfigure_match_service_type_mdns_service_list API
        * API for unconfiguring mDNS(Multicast Domain Name System) matche services in service list
    * Added unconfigure_service_type_mdns_service_definition API
        * API for unconfiguring mDNS(Multicast Domain Name System) service_definition
    * Added configure_mdns_controller_service_list API
        * API for configuring mDNS(Multicast Domain Name System) controller service list
    * Added unconfigure_match_service_type_mdns_controller_service_list API
        * API for unconfiguring mDNS(Multicast Domain Name System) controller service list
    * Added configure_controller_policy API
        * API for configuring mDNS(Multicast Domain Name System) controller policy
    * Added unconfigure_controller_policy_service_export API
        * API for unconfiguring mDNS(Multicast Domain Name System) controller policy
    * Added configure_mdns_service_peer_group API
        * API for configuring mDNS(Multicast Domain Name System) service peer group
    * Added configure_dynamic_nat_outside_rule API
        * API for configuring a dynamic NAT outside rule.
    * Added unconfigure_dynamic_nat_outside_rule API
        * API for unconfiguring a dynamic NAT outside rule.
    * Added configure_disable_nat_scale API
        * API for configuring disable NAT scale.
    * Added configure_nat_translation_timeout API
        * API for configuring ip nat translation timeout.
    * Added unconfigure_nat_translation_timeout API
        * API for unconfiguring ip nat translation timeout.
    * Added configure_interface_service_policy API
        * API for configuring service policy on interface
    * Added verify_routing_route_attrs and verify_static_routing_route_attrs APIs
        * APIs to verify existence of an IPv4/IPv6 route or static route, and
    * Added get_static_routing_ipv6_routes
        * Get `show ipv6 static detail` parser output containing IPv6 static
    * Added configure_bba_group API
        * bba-group pppoe {name}
        * virtual-template {vt_number}
    * Added unconfigure_bba_group API
        * no bba-group pppoe {name}
    * Added configure_tftp_source_interface API
        * ip tftp source-interface {interface}
    * Added unconfigure_tftp_source_interface API
        * no ip tftp source-interface {interface}
    * Added configure_virtual_template API
        * Configure virtual template on the router
    * Added unconfigure_configure_virtual_template API
        * Unconfigure virtual template on the router
    * Added configure_flow_monitor_cache_entry API
        * Added new API to configure flow monitor with cache entries
    * Added unconfigure_flow_monitor API
        * Added new API to unconfigure flow monitor
    * Added configure_fnf_record API
        * Added new API to configure flow record with extra parameters
    * Added unconfigure_flow_record API
        * Added new API to unconfigure flow record
    * Added configure_sampler API
        * Added new API to configure sampler
    * Added unconfigure_sampler API
        * Added new API to unconfigure sampler
    * Added configure_fnf_monitor_sampler_interface API
        * Added new API to configure flow monitor with sampler on interface
    * Added configure_fnf_monitor_datalink_interface API
        * Added new API to configure flow monitor with datalink on interface
    * Added unconfigure_fnf_monitor_datalink_interface API
        * Added new API to unconfigure flow monitor with datalink on interface
    * Added get_total_asics_cores  API
        * Added new API to get the total number of ASICs and COREs
    * Added unconfigure_routing_ip_route_vrf API
        * unconfigure_routing_ip_route_vrf to remove the config done by configure_routing_ip_route_vrf
    * Added configure_routing_ipv6_route API
        * configure_routing_ipv6_route to configure IPv6 route
    * Added unconfigure_routing_ipv6_route API
        * unconfigure_routing_ipv6_route to unconfigure IPv6 route
    * Added configure_routing_ipv6_route_vrf API
        * configure_routing_ipv6_route_vrf to configure IPv6 route with VRF
    * Added unconfigure_routing_ipv6_route_vrf API
        * unconfigure_routing_ipv6_route_vrf to unconfigure IPv6 route with VRF
    * Added configure_ipv6_enable API
        * configure_ipv6_enable under given interface
    * Added unconfigure_ipv6_enable API
        * unconfigure_ipv6_enable under given interface
    * Added configure_eigrp_named_networks API
        * configure_eigrp_named_networks to configure named EIGRP
    * Added unconfigure_eigrp_named_router API
        * unconfigure_eigrp_named_router to unconfigured named EIGRP
    * Added copy_running_config_to_flash_memory API
        * Restore config from local file using copy function on Device
    * Added unconfig_qos_rewrite_dscp API
        * Unconfigures qos rewrite ip dscp on Device
    * Added config_qos_rewrite_dscp API
        * Configures qos rewrite ip dscp on Device
    * Added config_replace_to_flash_memory API
        * Configures replace to flash memory
    * Added get_run_configuration API
        * Search config in show running-config output
    * Added get_startup_configuration API
        * search config in show startup-config output
    * Added get_status_for_rollback_replacing_in_flash API
        * search the status for rollback replacing in flash memory
    * Added configure_fips_authorization_key API
        * API to configure fips authorization key
    * Added unconfigure_fips_authorization_key API
        * API to unconfigure fips authorization key

* blitz
    * Test that should remove a value yet the value is not removed has wrong message.
        * Check if node still remains and provide correct log message.
    * Enhanced yangexec to compare the RPC error in case of negative testing
    * Added variable section.parameters
        * section.parameters can be accessed via %VARIABLES{section.parameters.<>} in Blitz yaml


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Added bdi option to clear_device_tracking_messages
    * Fixed 'verify_ping' API
        * Modified logic of the API to allow use of all options
    * Modified get_ip_theft_syslogs API
        * Updated the parsing to return common interface names
    * Modified execute_issu_install_package API
        * API for installing  issu package
    * Modify get_ipv6_interface_ip_address API
        * Add `as_list` keyword argument (default `False`) to return multiple
    * Modify get_routing_routes and get_routing_ipv6_routes APIs
        * Allow the `vrf` argument to be passed as `None` and execute the
    * Modified configure_flow_monitor API
        * Made few arguments as optional, added new arguments
    * Modified configure_flow_record API
        * Made the default arguments to have proper values
    * Updated configure_ospf_routing API
        * configure_ospf_routing to configure OSPF with VRF and without router-id
    * Updated unconfigure_ospf_on_device API
        * unconfigure_ospf_on_device to take VRF for unconfiguring ospf
    * Updated configure_ikev2_profile_pre_share API
        * configure_ikev2_profile_pre_share to take fvrf
    * Updated configure_ipsec_tunnel API
        * configure_ipsec_tunnel to take ivrf (overlay) and fvrf (underlay)
    * Updated configure_bgp_neighbor API
        * configure_bgp_neighbor to take address family and VRF
    * Updated config_interface_ospfv3 API
        * config_interface_ospfv3 to take af ipv4 or ipv6
    * Updated unconfig_interface_ospfv3 API
        * unconfig_interface_ospfv3 to take af ipv4 or ipv6
    * Added unconfigure_vlan_vpls
        * API was incorrectly removed in user-submitted PR from a few months ago

* all
    * Modified setup.py and Makefile
        * pin grpcio version to be less than or equal to 1.36.1 to be in line with yang.connector

* nxos
    * Modified triggers.processrestart.libs.nxos.processrestart.ProcessRestartLib
        * Exclude nxoc_dc service from core check upon crash test
        * Avoid script crash when service 'sap' is not available in show command output

* genie.libs.sdk
    * Added `yang.connector` as dependency

* blitz
    * run_netconf
        * fixed the sequence flag issue
    * Modified yang action to fix a NoneType object is not iterable bug


--------------------------------------------------------------------------------
                                      Vrf.                                      
--------------------------------------------------------------------------------


