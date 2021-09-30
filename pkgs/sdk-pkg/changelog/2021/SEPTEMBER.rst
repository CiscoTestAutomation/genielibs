--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API 'source_configured_template'
    * Added API 'configure_dot1x_cred_profile'
    * Added API 'configure_eap_profile_md5'
    * Added API 'configure_dot1x_supplicant'
    * Added API 'configure_mode_to_eEdge'
    * Added API 'enable_autoconf'
    * Added API 'configure_access_session_monitor'
    * Added API 'configure_access_session_sticky'
    * Added API 'enable_dot1x_sysauthcontrol'
    * Added API 'clear_access_session'
    * Added API 'config_identity_ibns'
    * Added attach_dhcpv6_guard_policy_to_vlan API
        * Attaches DHCPv6 guard policy to a vlan
    * Added detach_dhcpv6_guard_policy_vlan API
        * Detaches DHCPv6 guard policy from a vlan
    * Added attach_device_tracking_policy_to_interface API
        * Attaches device tracking policy to an interface
    * Added configure_authentication_parameters_interface
        * Configures authentication parameters on interface
    * Added authentication_convert_to_new_style API
        * Configures new style authentication
    * Added API `configure_ptp_modes'
    * Added API `configure_ptp_transport_ipv4'
    * Added API `configure_ptp_domain'
    * Added API `configure_ptp_priority'
    * Added API `configure_switchport_trunk'
    * Added API `configure_svi'
    * Added API `configure_ptp_dscp_message'
    * Added API `unconfigure_ptp_dscp_message'
    * Added API `unconfigure_svi'
    * Added API 'unconfigure_ptp_modes'
    * Added API 'configure_ptp_aes67_rates'
    * Added API 'unconfigure_ptp_transport_ipv4'
    * Added API 'unconfigure_ptp_domain'
    * Added API 'verify_ptp_states'
    * Added API 'verify_ptp_platform_fed_results'
    * Added API 'verify_ptp_clock'
    * Added API 'verify_ptp_counters'
    * Added API 'verify_ptp_parent'
    * Added API 'verify_ptp_calibration_states'
    * Added API 'unconfig_vlan'
    * Added TriggerClearIpv4BGPSoft
        * Trigger to soft clear for IPv4 BGP session using ```clear ip bgp * soft``` command
    * Added TriggerClearIpv4BGPHard
        * Trigger to hard clear for IPv4 BGP session using ```clear ip bgp *``` command
    * Added TriggerUnconfigConfigPortChannelInterface
        * Trigger to unconfigure and reconfigure Port-channel interfaces on IOSXE devices
    * Added TriggerUnconfigConfigBridgeDomainInterface
        * Trigger to unconfigure and reconfigure Port-channel interfaces on IOSXE devices
    * Added API configure_radius_attribute_6(device)
    * Added API unconfigure_radius_attribute_6(device)
    * Added API configure_any_radius_server(device, server_name, addr_type, address, authport, acctport, secret)
    * Added API unconfigure_any_radius_server(device, server_name)
    * Added API configure_radius_server_group(device, servergrp, rad_server)
    * Added API unconfigure_radius_server_group(device, servergrp)
    * Added API configure_aaa_new_model(device)
    * Added API configure_aaa_default_dot1x_methods(device,server_grp,group_type='group',group_type2='',server_grp2='')
    * Added API unconfigure_aaa_default_dot1x_methods(device)
    * Added API configure_aaa_login_method_none(device,servergrp)
    * Added API unconfigure_aaa_login_method_none(device,servergrp)
    * Added API configure_wired_radius_attribute_44(device)
    * Added API unconfigure_wired_radius_attribute_44(device)
    * Added API configure_radius_interface(device, interface)
    * Added API unconfigure_radius_interface(device, interface)
    * Added API get_running_config_section_attr44(device, option)
    * Added API verify_test_aaa_cmd(device, servergrp, username, password, path)
    * Added API configure_interface_switchport_voice_vlan(device, interface, vlan)
    * Added API unconfigure_dot1x_supplicant(device, profile_name, intf, eap_profile='')
    * Added API unconfigure_dot1x_system_auth_control(device)
    * Added API configure_authentication_host_mode(device,mode,intf,style='legacy')
    * Added API unconfigure_authentication_host_mode(device,mode,intf,style='legacy')
    * Added API configure_authentication_order(device,order,intf)
    * Added API unconfigure_authentication_order(device,order,intf)
    * Added API configure_authentication_priority(device,priority,intf)
    * Added API unconfigure_authentication_priority(device,priority,intf)
    * Added API configure_authentication_port_control(device,control,intf,style='legacy')
    * Added API unconfigure_authentication_port_control(device,control,intf,style='legacy')
    * Added API configure_authentication_periodic(device,intf)
    * Added API unconfigure_authentication_periodic(device,intf)
    * Added API configure_authentication_timer_reauth(device,value,intf)
    * Added API unconfigure_authentication_timer_reauth(device,value,intf)
    * Added API configure_auth_method(device,value,intf)
    * Added API unconfigure_auth_method(device,value,intf)
    * Added API 'configure_ip_on_tunnel_interface'
        * conigure ip address on tunnel interface
    * Added API 'unconfigure_tunnel_interface'
        * unconfigure tunnel interface
    * Added API 'configure_route_map_under_interface'
        * configure route-map under interface
    * Added API 'unconfigure_route_map_under_interface'
        * unconfigure route-map under interface
    * Added API 'configure_route_map'
        * configure route-map
    * Added API 'unconfigure_route_map'
        * unconfigure route-map
    * Added API 'unconfigure_acl'
        * unconfigure acl
    * Added API 'unconfigure_ace'
        * unconfigure ace
    * Added API 'verify_acl_usage'
        * verify acl usage
    * Added API 'verify_route_map'
        * verify route-map
    * Added API 'verify_tunnel_status'
        * verify tunnel status
    * Added API 'verify_tunnel_stats'
        * verify tunnel statistics
    * Added API clear_aaa_cache(device, server_grp, profile='all')
    * Added API configure_username(device, username, pwd, encryption=0)
    * Added API unconfigure_username(device, username)
    * Added API configure_radius_automate_tester(device, server_name, username, idle_time=None)
    * Added API unconfigure_radius_automate_tester(device, server_name, username)
    * Added API configure_eap_profile(device, profile_name,method='md5')
    * Added API unconfigure_eap_profile(device, profile_name)
    * added `configure_device_tracking_binding` API
    * added `configure_ipv6_destination_guard_attach_policy` API
    * added `configure_ipv6_destination_guard_detach_policy` API
    * added `configure_ipv6_destination_guard_policy` API
    * added `unconfigure_ipv6_destination_guard_policy` API
    * added `configure_device_tracking_tracking` API
    * Added API `configure_cts_authorization_list'
    * Added API `enable_cts_enforcement'
    * Added API `enable_cts_enforcement_vlan'
    * Added API `configure_device_sgt'
    * Added API `configure_vlan_to_sgt_mapping'
    * Added API `configure_ipv4_to_sgt_mapping'
    * Added API `configure_ipv4_subnet_to_sgt_mapping'
    * Added API `assign_static_ipv4_sgacl'
    * Added API `assign_default_ipv4_sgacl'
    * Added API 'configure_cts_credentials'
    * Added API 'configure_pac_key'
    * Added API 'configure_port_sgt'
    * Added new trigger 'TriggerUnconfigConfigBgpVpnRd'
    * Added configure_global_stackwise_virtual API
        * Configures global SVL and domain
    * Added unconfigure_global_stackwise_virtual API
        * Removes global SVL
    * Added configure_stackwise_virtual_interfaces API
        * Attaches interfaces to SVL
    * Added unconfigure_stackwise_virtual_interfaces
        * Removes interfaces from SVL
    * Added API 'disable_dhcp_snooping'
    * Added API 'unconfigure_cts_authorization_list'
    * Added API 'disable_cts_enforcement'
    * Added API 'disable_cts_enforcement_vlan'
    * Added API 'unconfigure_ipv4_to_sgt_mapping'
    * Added API 'remove_static_ipv4_sgacl'
    * Added API 'remove_default_ipv4_sgacl'
    * Added API 'clear_cts_credentials'
    * Added API 'clear_cts_counters'
    * Added API 'unconfigure_ipv4_subnet_to_sgt_mapping'
    * Added configure_errdisable API
        * Configures error disable
    * Added unconfigure_errdisable API
        * Removes error disable
    * Added configure_template API
        * Configures template
    * Added unconfigure_template
        * Removes template
    * Added configure_spanning_tree API
        * Configures spanning tree
    * Added unconfigure_spanning_tree API
        * Removes spanning tree
    * Added configure_interface_template API
        * Attaches template to an interface
    * Added unconfigure_interface_template
        * Removes templates from an interface
    * Added execute_clear_logging
        * Executes clear logging

* nxos/aci
    * Added `verify_file_exists` and `delete_files` APIs

* api utils
    * Added API Unit Test Generator
        * Added module that is capable of connecting to a device and automatically


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified TriggerReload
        * Changed TriggerReload from NotImplemented to complete implementation of node reload.
    * Modified `get_show_tech` API, improved exception handling
    * Modified configure_radius_group API
    * Modified API configure_dot1x_supplicant(device, interface, cred_profile_name, eap_profile='')
    * Modified RouteOutput
        * Updated template for routeOpsOutput_vrf1 and routeOpsOutput for ipv6 routes since the parser logic was incorrect.
    * Modified config_extended_acl
        * new condition is added to configure acl with using only host keyword.
    * Modified config_identity_ibns
        * Added port_control as an arg, and made 'auto' the default
    * Modified configure_authentication_host_mode
        * Added spaces between args for readability
    * Modified API execute_card_OIR(device, card_number, timeout=60)

* iosxr
    * Modified `get_show_tech` API, improved exception handling

* nxos
    * Modified `get_show_tech` API, improved exception handling
    * Modified
        * Issu trigger can now handle invalid boot mode command on unsupported platforms/images.

* aci
    * Modified `get_show_tech` API, improved exception handling

* mapping
    * Added logging to show Ops structure when Mapping errors out


--------------------------------------------------------------------------------
                                     Update                                     
--------------------------------------------------------------------------------

* iosxe
    * Added configure_fnf_exporter API
        * Configures Flow exporter
    * Added unconfigure_flow_exporter_monitor_record API
        * Unconfigures the Flow exporter, monitor and record
    * Added configure_fnf_monitor_on_interface API
        * Configures the interface with the flow monitor
    * Added configure_flow_record API
        * Configures Flow record
    * Added configure_flow_monitor API
        * Configures Flow monitor
    * Added unconfigure_fnf_monitor_on_interface API
        * Unconfigures flow monitor from interface
    * Added set_filter_packet_capture_inject API
        * Sets filter for packet capture inject
    * Added start_packet_capture_inject API
        * Starts packet capture inject
    * Added stop_packet_capture_inject API
        * Stops packet capture inject API

* added unconfigure_vlan_interface api
    * Unconfigures vlan interface


