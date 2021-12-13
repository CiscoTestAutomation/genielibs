--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_common_criteria_policy API
        * API for configuring common criteria policy for enable password.
    * Added unconfigure_common_criteria_policy API
        * API for unconfiguring a common criteria policy.
    * Added configure_enable_policy_password API
        * API for configuring enable password with a common criteria policy
    * Added unconfigure_enable_policy_password API
        * API for unconfiguring enable password.
    * Added configure_service_password_encryption API
        * API for configuring service password with encryption.
    * Added unconfigure_service_password_encryption API
        * API for unconfiguring service password encryption
    * Added verify_enable_password API
        * API for verifying enable password
    * Added AAA Secret Key Hash API
        * Added API to retrive values from CLI commands to compare with YANG model data for Secret key Hash AAA leaf
    * Added API 'configure_evpn_default_gateway_advertise_global'
    * Added API 'configure_evpn_evi_replication_type'
    * Added API 'configure_evpn_instance_encapsulation_type'
    * Added API 'configure_evpn_l2_instance_vlan_association'
    * Added API 'configure_evpn_l3_instance_vlan_association'
    * Added API 'configure_evpn_replication_type'
    * Added API 'configure_l2vpn_evpn'
    * Added API 'configure_l2vpn_evpn_router_id'
    * Added API 'unconfigure_evpn_default_gateway_advertise_global'
    * Added API 'unconfigure_evpn_evi_replication_type'
    * Added API 'unconfigure_evpn_instance_encapsulation_type'
    * Added API 'unconfigure_evpn_l2_instance_vlan_association'
    * Added API 'unconfigure_evpn_l3_instance_vlan_association'
    * Added API 'unconfigure_evpn_replication_type'
    * Added API 'unconfigure_l2vpn_evpn'
    * Added API 'unconfigure_l2vpn_evpn_router_id'
    * Added configure_logging_buffered_errors api
        * Confgiure logging buffered errors
    * Added unconfigure_logging_buffered_errors api
        * Unconfgiure logging buffered errors
    * Added configure_logging_console_errors api
        * Confgiure logging console errors
    * Added unconfigure_logging_console_errors api
        * Unconfgiure logging console errors
    * Added get_authentication_config_mode api
        * Get current authentication config mode on device
    * Added 'clear_access_session_intf' API
        * clearing access-session interface
    * Added 'clear_ipv6_mld_group' API
        * clearing ipv6 mld group
    * Added 'configure_no_boot_manual' API
        * configuring boot manual
    * Added 'clear_ip_mroute_vrf' API
        * clearing ip mroute on perticular vrf
    * Added 'clear_errdisable_intf_vlan' API
        * clearing errdisable interface with vlan
    * Added configure_class_map API
        * API for configuring class map for policy.
    * Added unconfigure_class_map API
        * API for unconfiguring class map from policy.
    * Added configure_policy_map API
        * API for configuring policy map for service-policy.
    * Added unconfigure_policy_map API
        * API for unconfigure_policy_map policy map.
    * Added configure_table_map API
        * API for configuring table map.
    * Added unconfigure_table_map API
        * API for unconfiguring table map.
    * Added get_trunk_interfaces_encapsulation api
        * get a dictionary with interface as key and encapsulation as the value
    * Added get_show_output_section api
        * Display the lines which are match from section
    * Added execute_clear_platform_software_fed_switch_acl_counters_hardware api
        * clear platform software fed switch acl counters hardware
    * Modified start_packet_capture api
        * Added direction to capture the packets
    * Added configure_terminal_length api
        * Configure terminal length
    * Added configure_terminal_width api
        * Configure terminal width
    * Added configure_logging_buffer_size api
        * Configure logging buffer
    * Added configure_terminal_exec_prompt_timestamp api
        * Configure terminal exec prompt timestamp
    * Modified execute_delete_boot_variable api
        * boot variable arg can now be a list
    * Added configure_logging_console API
        * Enable logging console
    * Added unconfigure_logging_console API
        * disble logging console
    * Added configure_logging_monitor API
        * Enable logging monitor
    * Added unconfigure_logging_monitor API
        * disble logging monitor
    * added `get_ip_theft_syslogs` API
    * Added 'configure_mdns' API
        * Configures mDNS(Multicasr Domain name services)
    * Added 'unconfigure_mdns_config' API
        * Unconfigures mDNS(Multicasr Domain name services)
    * Added 'configure_vlan_agent' API
        * Configures vlan agent
    * Added 'unconfigure_mdns_vlan' API
        * Unconfigures mDNS vlan
    * Added 'configure_vlan_sp' API
        * Configures vlan sp(Service Peer)
    * Added 'configure_mdns_location_filter' API
        * Configures mDNS location filter
    * Added 'configure_mdns_location_group' API
        * Configures mDNS location group
    * Added 'configure_mdns_sd_agent' API
        * Configures mdns sd agent
    * Added 'configure_mdns_sd_service_peer' API
        * Configures mdns sd service peer
    * Added 'configure_mdns_trust' API
        * Configures mdns trust
    * Added 'configure_mdns_service_definition' API
        * Configures mdns service definition
    * Added unconfigure_device_tracking_binding API
    * Added verify_empty_device_tracking_policies API
    * Added verify_empty_device_tracking_database API
    * Added
        * configure_interface_mac_address
        * unconfigure_interface_mac_address
    * Added
        * configure_interface_pvlan_host_assoc
        * configure_interface_switchport_pvlan_mode
        * configure_interface_span_portfas
        * verify_port_channel_member_state
        * configure_vtp_mode
        * configure_pvlan_svi_mapping
        * configure_pvlan_primary
        * configure_pvlan_type
        * configure_vrf_definition_family
    * Added configure_eapol_eth_type_interface API
        * Configures EAPOL Ethernet Type on interface
    * Added unconfigure_eapol_eth_type_interface API
        * Unconfigures EAPOL Ethernet Type on interface
    * Added config_mka_policy_delay_protection API
        * Configures MKA Policy with delay protection on device/interface
    * Added unconfig_mka_policy_delay_protection API
        * Unconfigures MKA Policy with delay protection on device/interface
    * Added configure_mka_policy API
        * Configures MKA policy on device/interface
    * Added unconfigure_mka_policy API
        * Unconfigures MKA policy on device/interface
    * Added unconfigure_mka_keychain_on_interface API
        * Unconfigures MKA keychain on interface
    * Added enable_ipv6_multicast_routing API
        * enables ipv6 multicast routing on device
    * Added disable_ipv6_multicast_routing API
        * disables ipv6 multicast routing on device
    * Added configure_ospfv3_network_point API
        * Configures ospfv3 network type point-to-point on interface
    * Added unconfigure_ospfv3_network API
        * Unconfigures ospfv3 network type on interface
    * Added configure_ipv6_ospf_bfd API
        * Configures ipv6 ospf bfd on interface
    * Added unconfigure_ipv6_ospf_bfd API
        * Unconfigures ipv6 ospf bfd on interface
    * Added unconfigure_bfd_on_interface API
        * Unconfigures bfd on interface
    * Added configure_ipv6_object_group_network API
        * configures ipv6 network object group  on device
    * Added configure_ipv6_object_group_service API
        * configures ipv6 service object group  on device
    * Added configure_ipv6_ogacl API
        * configures IPv6 OG ACL on device
    * Added configure_ipv6_acl_on_interface API
        * configures IPv6 og acl on interface
    * Added unconfigure_ipv6_ogacl_ace API
        * Unconfigures IPv6 OGACL ACE on device
    * Added unconfigure_ipv6_object_group_service_entry api
        * Unconfigures ipv6 service object group entry on device
    * Added unconfigure_ipv6_object_group_network_entry api
        * Unconfigures ipv6 network object group entry on device
    * Added unconfigure_ipv6_object_group_service api
        * Unconfigures ipv6 service object group  on device
    * Added unconfigure_ipv6_object_group_network api
        * Unconfigures ipv6 network object group  on device
    * Added unconfigure_ipv6_acl API
        * unconfigures ipv6 acl on device
    * Added unconfigure_ipv6_acl_on_interface api
        * Removes ipv6 acl from interface
    * Added config_ip_pim under multicast.py
    * Added config_rp_address under multicast.py
    * Added config_multicast_routing_mvpn_vrf under multicast.py
    * Added configure_igmp_version under multicast.py
    * Added unconfigure_igmp_version under multicast.py
    * Added configure_ip_pim_vrf_ssm_default under multicast.py
    * Added unconfigure_ip_pim_vrf_ssm_default under multicast.py
    * Added config_standard_acl_for_ip_pim under multicast.py
    * Added unconfig_standard_acl_for_ip_pim under multicast.py
    * Added verify_ip_pim_vrf_neighbor under verify.py multicast folder
    * Added verify_mpls_mldp_neighbor under verify.py multicast folder
    * Added verify_mpls_mldp_root under verify.py multicast folder
    * Added verify_mfib_vrf_hardware_rate under verify.py multicast folder
    * Added verify_mfib_vrf_summary under verify.py multicast folder
    * Added verify_mpls_route_groupip under verify.py multicast folder
    * Added verify_bidir_groupip under verify.py multicast folder
    * Added unconfigure_mdt_auto_discovery_mldp API
    * Added configure_mdt_overlay_use_bgp API
    * Added configure_mdt_auto_discovery_mldp API
    * Added unconfigure_mdt_overlay_use_bgp API
    * Added verify_mpls_forwarding_table_gid_counter API
    * Added verify_mpls_forwarding_table_vrf_mdt API
    * Added clear_arp_cache API
        * Clears device arp cache
    * Added config_ip_on_vlan API
        * Configures IPv4/IPv6 address on a vlan
    * Added unconfigure_interface_switchport_access_vlan API
        * Unconfigures switchport access on interface vlan
    * Added authentication convert-to new-style single-policyinterface {interface}
    * Added access-session single-policy interface {interface}
    * Added access-session single-policy policy-name {policy_name}
    * Added authentication convert-to new-style
    * Added
        * Added verify_pattern_in_show_logging api to verify the pattern list in show logging output
    * Added remove_acl_from_interface API
        * API for removing an ACL from an interface

* utils
    * Added get_interface_type_from_yaml
        * get 'type' of interface for a device from topology in testbed object

* api utils
    * Modified api_unittest_generator
        * Added support to positional arguments and keyword arguments in API calls
    * Added test_api_unittest_generator
        * Added unit tests to cover api_unittest_generator code

* common
    * Added 'execute_and_parse_json' API
        * Executes a CLI command that outputs JSON and parses the output of the command as

* iosxr
    * Added clear_logging API
        * To clear logging message

* nxos
    * Added clear_logging API
        * To clear logging message

* aireos
    * Added
        * verify_ping
        * get_boot_variables


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Fix remove_device_tracking_policy
        * changed string format variable name
    * Fix clear_device_tracking_database
        * changed to parse passed in args properly
    * Fixed `get_ip_theft_syslogs` to support syslogs without a timezone
    * Modified
        * configure_dot1x_supplicant
    * Modified
        * configure_interface_switchport_access_vlan
    * Modified get_bgp_route_ext_community
        * Fixed a hole in the logic if neither vrf nor rd arguments were passed
    * Modified unconfigure_acl
        * Added option to unconfigure standard no ip access-list as well as extended
    * updated 'pkgs/sdk-pkg/src/genie/libs/sdk/apis/iosxe/mdns/configure.py'
        * Added 'configure_mdns_controller' API
        * Added 'unconfigure_mdns_controller' API
        * Added 'configure_mdns_svi' API
        * Added 'unconfigure_mdns_svi' API
        * Added 'clear_mdns_query_db' API
        * Added 'clear_mdns_statistics' API
        * Added 'unconfig_mdns_sd_service_peer' API
        * Added 'unconfigure_mdns_service_definition' API
    * Modified TriggerUnconfigConfigVrf
        * handle SchemaEmptyParserError on empty 'show vrf detail' output
    * APIs configure_interfaces_shutdown and configure_interfaces_unshutdown
        * Now raises a SubCommandFailure instead of logging an error
    * BGP API name change from 'get_routing_routes' to 'get_bgp_routes' due to conflict API name
        * WARNING API name is changed. if using this API, script/testcase needs to be Updated
    * BGP verify_bgp_routes_from_neighbors API
        * Updated to adjust API name change of from 'get_routing_routes' to 'get_bgp_routes'
    * PBR API name change from 'configure_route_map' to 'configure_pbr_route_map' due to conflict API name
        * WARNING API name is changed. if using this API, script/testcase needs to be Updated
    * PBR API name change from 'unconfigure_route_map' to 'unconfigure_pbr_route_map' due to conflict API name
        * WARNING API name is changed. if using this API, script/testcase needs to be Updated
    * Updated health_logging API
        * Added 'clear_log' argument to clear logging message

* api utils
    * Modified API Unit Test Generator
        * Fixed `--module-path` parsing
    * Modified api_uniitest_generator.py
        * Fixed Value Error when no arguments were provided
    * Modified API Unit test Generator
        * Added exception for unsupported connections
        * Added init_config_command and init_exec_command to connection settings
        * Updated test template to include connection settings
    * Modified api_unittest_generator
        * Fixed bug with --module-path
        * Removed unused arguments on _create_testbed

* modified is_next_reload_boot_variable_as_expected api
    * Added better error handling by rising an exception.

* common
    * Modified verify.py
        * Changed verify_current_image comparison method to split directories and images on delimiter characters
    * Updated load_jinja_template API
        * Added StrictUndefined jinja2.Environment to error out in case definition in template is not passed

* ios and iosxe
    * Using regex search in get_md5_hash_of_file API

* apic
    * Updated apic_rest_get API
        * Added target_subtree_class argument support
    * Updated apic_rest_post API
        * Added xml_payload argument support

* common api
    * Updated get_devices API
        * Show more accurate message depending on condition
        * check if testbed object is same with runtime.testbed and give warning if different

* iosxr
    * Updated health_logging API
        * Added 'clear_log' argument to clear logging message

* nxos
    * Updated health_logging API
        * Added 'clear_log' argument to clear logging message

* nxos/n9k
    * Moved health API for nxos n9k
        * To fix API pickup via abstraction

* linux
    * Updated scp API
        * Updated prompt pattern and docstring


