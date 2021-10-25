--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* api utils
    * Modified api_unittest_generator
        * Fixed module and module-path arguments to remove OS dependency.

* iosxe
    * Modified configure_ospf_routing API
        * Updated the doc string
    * Modified configure_ospfv3 API
        * Updated the doc string
    * Modified clear_interface_interfaces API
        * Updated the doc string
    * Modifed config_mka_policy_xpn API
        * Added sak_rekey_int, key_server_priority arguments
    * Modified config_macsec_keychain_on_device API
        * Added lifetime argument
    * Modified enable_ipv6_unicast_routing API
        * Updated device type in doc string
    * Modified config_wan_macsec_on_interface API
        * Added new argument dot1q_clear
    * Modified config_macsec_keychain_on_device API
        * Updated new arguments
    * Modified trigger_datafile_iosxe.yaml
        * Removed frames_tolerance as a parameter from the compare_traffic_profile postprocessor as it was causing an unexpected keyword argument error
    * Modified
        * Modified copy_file_to_running_config API
            * Modified the API to pass timeout value as an argument
    * Modified API verify_acl_usage
        * Updated API to accomodate the enhancement of ShowPlatformSoftwareFedActiveAclUsage Parser.
    * Add timeout.sleep() calls to polling loops that are missing them
    * Fix verify_ip_mac_binding_in_network to use device.parse() over device.parser()
    * Modify configure functions that directly access optional keys in dictionaries to use .get() to be more safe

* nxos
    * Modified API 'health_core'
        * Added remote_path support for http protocol
    * Modified _is_boot_variable_as_expected
        * To fix a bug where no boot variables were parsed but the parser was not empty.

* ios
    * Modified trigger_datafile_ios.yaml
        * Removed frames_tolerance as a parameter from the compare_traffic_profile postprocessor as it was causing an unexpected keyword argument error

* modified load_jinja_template api
    * Added error message in case template is not found


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_l2vpn_vfi_context_vpls API
        * Configures l2vpn vfi context vpls on device
    * Added unconfigure_l2vpn_vfi_context_vpls API
        * Unconfigures l2vpn vfi context vpls on device
    * Added configure_encapsulation_mpls_ldp API
        * Configures encapsulation mpls ldp on interface
    * Added configure_vlan_vpls API
        * Configures vpls on vlan
    * Added unconfigure_vlan_vpls API
        * Unconfigures vpls on vlan
    * Updated API 'verify_ptp_states' due to small parser changes
    * Updated API 'verify_ptp_platform_fed_results' due to small parser changes
    * Updated API 'verify_ptp_clock' due to small parser changes
    * Updated API 'verify_ptp_counters' due to small parser changes
    * Updated API 'verify_ptp_parent' due to small parser changes
    * Added 'clear_ip_nat_translation_all' API
        * clear ip nat translation *
    * Added 'clear_flow_monitor' API
        * clear flow monitor with name and options
    * Added 'clear_ipv6_mfib_vrf_counters' API
        * clear all ipv6 mfib vrf counter or for perticular
    * Added 'clear_access_list_counters' API
        * clear all access-list counters or with perticular options
    * Added 'clear_ip_mroute_all' API
        * clear ip mroute all
    * Added configure_default_gateway API
        * Configures default gateway
    * Added config_vlan_tag_native API
        * Configures vlan dot1q tag native on device
    * Added config_vlan_tag_native API
        * Unconfigures vlan dot1q tag native on device
    * Added config_license API
        * Configures license on device
    * Added API verify_template_bind
    * Added configure_tacacs_server
    * Added export_packet_capture
    * added `remove_ipv6_dhcp_guard_policy` API
    * added `remove_ipv6_nd_suppress_policy` API
    * added `remove_single_device_tracking_policy` API
    * added `remove_ipv6_source_guard_policy` API
    * added `clear_device_tracking_database` API
    * added `clear_device_tracking_counters` API
    * Added get_auth_session API
        * API for getting the dot1x/mab authentication session
    * Added get_radius_packets API
        * API for getting the radius packets from pcap file
    * Added get_packet_attributes_scapy API
        * API for getting the attribute value pairs from a packet
    * Added get_packet_info_field API
        * API for getting the packet info(code field) from a packet
    * Added get_ip_packet_scapy API
        * API for getting the IP layer from a packet
    * Added get_packet_ip_tos_field API
        * API for getting the types of services field from a packet
    * Added configure_enable_aes_encryption API
        * API for enabling aes password encryption
    * Added configure_disable_aes_encryption API
        * API for disabling aes password encryption
    * Added API `get_snmp_snmpwalk`
    * Added API `configure_snmp`
    * Added API `unconfigure_snmp`
    * Added get_bgp_rt2_community_label API
        * Gets external-community, label info from route-type 2 that
        * matches with specific ip and mac
    * Added get_bgp_rt5_community_paths_label API
        * Gets external-community, label, path from route-type 5 that
        * matches with specific ip address
    * Added verify_bgp_rt2_route_target API
        * Checks for specific Route Target from route-type 2 output
    * Added verify_bgp_rt5_reoriginated_from API
        * Checks for re-origination path from route-type 5 output
    * Added verify_bgp_rt5_route_target API
        * Verifies Route Target from route-type 5 output
    * Added verify_bgp_rt5_label API
        * Verifies for specific label from route-type 5 output
    * Added verify_bgp_rt2_label API
        * Verifies for specifi label from route-type 2 output
    * Added get_arp_interface_mac_from_ip API
        * Gets a list of mac and outgoing interface of specific route
    * Added verify_arp_vrf_interface_mac_entry API
        * Verifies for specific mac and outgoing interface in arp table
    * Added unconfigure_vlan_config API
        * Unconfigs vlan in config level
    * Added get_routing_vrf_entries API
        * Gets route entris from specific vrf route
    * Added verify_routing_subnet_entry API
        * Verifies for specific route entry
    * Added configure_evpn_instance_vlan_based_with_reoriginate_rt5 API
        * Configures evpn vlan instance with re-originate RT5 in it
    * Added unconfigure_evpn_instance_vlan_based API
        * Unconfigs evpn vlan instance with re-originate RT5 in it
    * Added 'clear_platform_software_fed_active_acl_counters_hardware' API
        * to clear acl hardware counters on device
    * Added API `configure_interface_switchport_trunk_vlan`
    * Added 'configure_ip_mtu' API
        * configure mtu value under interface
    * Added 'unconfigure_ip_mtu' API
        * unconfigure mtu value under interface
    * Added configure_radius_interface_vrf API
        * Configures RADIUS source interface via VRF
    * Added unconfigure_radius_interface_vrf API
        * Unconfigures RADIUS source interface via VRF
    * Added configure_eapol_dest_address_interface API
        * Configures EAPOL Destination address on interface
    * Added unconfigure_eapol_dest_address_interface API
        * Unconfigures EAPOL Destination address from interface
    * Added API verify_device_tracking_counters_interface
    * Added API verify_device_tracking_counters_vlan
    * Added API configure_device_tracking_binding_options
    * Added API unconfigure_device_tracking_binding_options
    * Added decrypt_tacacs_pcap
    * Added parse_tacacs_packet
    * Added verify_tacacs_packet
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
    * Added perform_ssh
    * Added concurrent_ssh_sessions

* linux
    * Added `scp` API for linux os

* blitz
    * actions
        * Added dialog action to handle dialog interactions
    * actions_helper
        * Added dialog_handler to process dialog interactions

* sdk
    * Added RestconfRequestBuilder class, run_restconf, dict to XML conversion, and map to determine function to run based on protocol


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified export_packet_capture


