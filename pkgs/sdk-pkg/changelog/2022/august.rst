--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* nxos
    * Modified _perform_issu API
        * Added support for disruptive ISSU

* iosxe
    * Modified unconfigure_stackwise_virtual_interfaces API
        * API for Unconfiguring stackwise config on interface level to hendel prompt yes or no.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* blitz
    * Fix for gNMI Payload Build for Multiple List with "/" in Key Values.
    * Fix for GNMI Subscription ONCE and POLL mode reciever stops after 1st response for Subscription list containing multiple paths.
    * Validation Support for Subscription list containing multiple paths (All Modes).
    * rpcverify.py
        * Fix to handle different namespaces in the rpc reply.
* iosxe
    * Modified verify_bgp_rt7_mvpn_all_ip_mgroup
        * Removed colon check for rd and also corrected the ipv6 check
    * Modified verify_bgp_rt5_mvpn_all_ip_mgroup
        * Removed colon check for rd and also corrected the ipv6 check
    * Modified verify_bgp_l2vpn_evpn_rt2_ipprefix api
        * Removed colon check from ip address and will consider ipv6 address in prefix
    * Modified verify_bgp_l2vpn_evpn_rt5_ipprefix api
        * Removed colon check from ip address and will consider ipv6 address in prefix
    * Modified configure_routing_static_route API
        * Added more VRF config
    * Updated get_component_descr API
        * Splited regex <p1> into <p1> and <p2>; and made the code changes in the respective section
    * Modified configure_bgp_neighbor_activate api
        * Added vrf argument to support vrf
    * Updated config_extended_acl API:
        * Added log_option and changed how the existing commands are appended
* common
    * Updated execute_copy_run_to_start API
        * add a dialog for handling device output.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cat9k
    * Added get_fabric_ap_state
        * Added new api to get fabric ap state for the access point
    * Added get_lisp_session_state
        * Added new api to get lisp session state of the access point
    * Added get_ap_ip
        * Added new api to get ap ip of the access point
    * Added get_rloc_ip
        * Added new api to get rloc ip of the access point
    * Added get_matching_line_processes_platform
        * Added new api to get matching lines from  processes platform for a given process
    * Added get_matching_line_platform_software
        * Added new api to get matching lines from platform software for a given process
    * Added get_processes_platform_dict
        * Added new api to get processes platform for a given process
    * Added get_platform_software_dict
        * Added new api to get platform software for a given process
    * Added VerifyApFabricSummary
        * Added new clean stage VerifyApFabricSummary
    * Added VerifyLispSessionEstablished
        * Added new clean stage VerifyLispSessionEstablished
    * Added VerifyAccessTunnelSummary
        * Added new clean stage VerifyAccessTunnelSummary
    * Added VerifyWirelessProcess
        * Added new clean stage VerifyWirelessProcess

* iosxe
    * Added unconfigure_hw_module_slot_shutdown API
        * API to unshut hw-module slot.
    * Added configure_hw_module_slot_shutdown API
        * API to shutdown hw-module slot.
    * Added unconfigure_ripng
        * API for unconfigure the rip ipv6 configuation on device
    * Added configure_ripng
        * API for configure the rip ipv6 configuration on device
    * Added unconfigure_rip
        * API for unconfigure the rip ipv4 configuration on device
    * Added config_interface_ripng
        * API for configure the rip ipv6 configuration on interface
    * Added unconfig_interface_ripng
        * API for unconfigure the rip ipv6 configuration on interface
    * Added configure_rip
        * API for configure the rip ipv4 configuration on device
    * Added tunnel_range_shut_unshut
        * API for doing shutdown and unshutdown of tunnel interface range configuation on device
    * Added copy_config_from_tftp_to_media
        * API for copying configuration file from tftp location to device media
    * Added configure_snmp_server_user and unconfigure_snmp_server_user API
        * API for configure, unconfigure snmp server user cli
    * Added clear_ipv6_pim_topology api
        * Api for clear ipv6 pim topology
    * Added verify_bgp_l2vpn_evpn_rt2_nxthop api
        * Api for verifying rt2 next hop in show ip bgp l2vpn evpn all
    * Added verify_bgp_l2vpn_evpn_rt5_nxthop api
        * Api for verifying rt5 next hop in show ip bgp l2vpn evpn all
    * Added debug_platform_memory_fed_backtrace and debug_platform_memory_fed_callsite API
        * API for debug platform memory callsite and backtrace
    * Added get_neighbor_count
        * api for  show ip ospf neighbor count
    * Added configure_ipv4_dhcp_relay_helper_vrf API
        * API to configure IPv4 DHCP relay helper IP under interface
    * Added unconfigure_ipv4_dhcp_relay_helper_vrf API
        * API to unconfigure IPv4 DHCP relay helper IP under interface
    * Added configure_vrf_select_source API
        * API to configure VRF select source under interface
    * Added unconfigure_vrf_select_source API
        * API to unconfigure VRF select source under interface
    * Added configure_snmp_server_trap and unconfigure_snmp_server_trap API
        * API for configure, unconfigure snmp server traps and informs cli
    * Added get_total_cdp_entries_displayed API
        * Added new API to get the total cdp entries dispalyed
    * Added verify_total_cdp_entries_displayed_interfaces API
        * Added new API to verify total cdp entries i.e interfaces displayed
    * Added get_cpu_processes_details_include_with_specific_process
        * api for  show cpu processes details include with specific process
    * Added transceiver_power_intf,transceiver_interval_intf and transceiver_intf_components API's
        * API's for getting the values from "show interfaces transceiver detail" parser,related switch transceiver interfaces and return values respectively
    * Added configure_mpls_mtu API
        * API for configure mpls mtu on device interface
    * Added configure_ip_igmp_static_group api
        * Api for configuring ip igmp static-group
    * Added configure_ipv6_mld_static_group
        * Api for configuring ipv6 mld static-group addr addr
    * Added configure_ip_igmp_join_group
        * Api for configuring ip igmp join-group addr source addr
    * Added configure_bgp_neighbor_advertisement_interval api
        * Api for configuring advertisement interval in addressfamily of
        * router bgp that includes vrf also if given
    * Added configure_bgp_l2vpn_evpn_rewrite_evpn_rt_asn api
        * Api for configuring rewrite evpn rt asn in l2vpn evpn of router bgp
    * Added clear_ip_bgp_af_as api
        * Api for clearing clear ip bgp address_family as_numbers
    * install
        * Added install_auto_abort_timer_stop under configure.py
        * Added clear_install_state under configure.py
        * Added create_rollback_label under configure.py
        * Added clear_install_label under configure.py
        * Added create_rollback_description under configure.py
        * Added install_remove under configure.py
        * Added install_commit under configure.py
        * Added install_add under configure.py
        * Added install_activate under configure.py
        * Added install_one_shot under configure.py
        * Added install_abort under configure.py
        * Added install_deactivate under configure.py
        * Added install_rollback under configure.py
        * Added get_install_version under get.py
        * Added verify_rollback_label under verify.py
        * Added verify_active_standby under verify.py
        * Added verify_rollback_description under verify.py
        * Added verify_install_state under verify.py
        * Added verify_install_auto_abort_timer_state under verify.py
    * platform
        * Added execute_clear_parser_statistics under execute.py
    * Added cts_refresh_policy API
        * API to refresh CTS policy
    * Added cts_refresh_environment_data API
        * API to refresh CTS environment data
    * Added cts_refresh_pac API
        * API to refresh CTS pac
    * Added clear_ipv6_nhrp
        * API for clear ipv6 nhrp
    * Added configure_debug_snmp_packets API
        * Api for configure snmp debug packets
    * Added unconfigure_debug_snmp_packets API   
        * Api for un configure snmp debug packets
    * Added configure_snmp_host_version API
        * Api for snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}
    * Added unconfigure_snmp_host_version API   
        * Api for no snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}
    * Added get_number_of_interfaces API
        * API to get number of interfaces/type in device
    * Added get_platform_model_number API
        * API to get platform model number or chassis type of device
    * Added verify_interface_config_speed API
        * API to verify interface configured speed
    * Added verify_interface_config_duplex API
        * API to verify interface configured duplex
    * Added verify_ip_mroute_group_and_sourceip:
        * Api for verifying mroute parameters in show ip mroute mgroup supports ipv6 too
    * Added verify_ip_mroute_mgroup_rpf_state:
        * Api for verifying mroute rpf state in show ip mroute supports ipv6 and vrf too
    * Added verify_ip_mfib_hw_pkt_per_sec api:
        * Api for verifying hw pkt count per sec
    * Added verify_ip_pim_neighbor:
        * Api for verifying neighbor in show ip pim neighbor
    * Added get_ip_mfib_hw_pkts_per_sec:
        * Api for getting hw counters from show ip mfib supports ipv6 and vrf too
* blitz
    * Added GNMI ASCII encoding support
        * Specify ASCII encoding in format for GNMI request.
        * To verify the GNMI response, in returns section, set datatype to ascii, and expected value. An acceptable operator is '=='.

* Common
    * Added new power_off_device and power_on_device APIs
        * Add device APIs to toggle device power on or off