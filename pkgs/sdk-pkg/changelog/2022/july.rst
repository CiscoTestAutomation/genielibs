--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_isis_network_entity
        * API for configure the isis network entity on device
    * Added remove_isis_configuration
        * API for remove the isis configuration on device
    * Added config_interface_isis
        * API for isis configuration on interface
    * Added unconfig_interface_isis
        * API for remove the isis configuration on interface
    * Added verify_bgp_l2vpn_evpn_rt2_ipprefix api
        * APi for verifying rt2 ipprefix in show ip bgp l2vpn evpn all
    * Added verify_bgp_l2vpn_evpn_rt5_ipprefix
        * Api for verifying rt5 ipprefix in show ip bgp l2vpn evpn all
    * Added verify_bgp_rt5_mvpn_all_ip_mgroup
        * Api for verifying rt5 ipprefix,group in
        * show ip bgp ipv4 mvpn all
    * Added verify_bgp_rt7_mvpn_all_ip_mgroup
        * Api for verifying rt7 ipprefix,group in
        * show ip bgp ipv4 mvpn all
    * Modified configure_ikev2_keyring api
        * Added the option to configure manual or dynamic ppk while making pre share key optional
    * Added configure_snmp_server_view and unconfigure_snmp_server_view API
        * API for configure, unconfigure snmp server view
    * Added configure_sdm_prefer_custom_template API
        * API for sdm prefer custom template
    * Added configure_sap_pmk_on_cts API
        * Added new API to configure sap pmk under cts
    * Added unconfigure_cts_manual API
        * Added new API to unconfigure cts manual
    * Added install_remove_version API
        * API to remove installed packages for particular version
    * Added configure_flow_monitor_vlan_configuration API
        * API to configure flow monitor under vlan configuration
    * Added unconfigure_flow_monitor_vlan_configuration API
        * API to unconfigure flow monitor under vlan configuration
    * Added enable_dhcp_relay_information API
        * API to enable DHCP Relay Information
    * Added disable_dhcp_relay_information API
        * API to disable DHCP Relay Information
    * Added configure_snmp_server_group and unconfigure_snmp_server_group API
        * API for configure, unconfigure snmp server group cli
    * Modified configure_common_criteria_policy api
        * Added the options char_rep and restrict, and set default values to existing options.
    * Modification of existing API for configure_lldp,unconfigure_lldp,configure_lldp_interface,unconfigure_lldp_interface API
        * API to configure lldp neighbors on interface level
    * Modification of existing API for configure_cdp_neighbors,configure_cdp_neighbors,API
        * API to configure and unconfigure cdp neighbors on globally
    * Added configure_port_channel_lacp_max_bundle,unconfigure_port_channel_lacp_max_bundle API
        * API to configure configure_port_channel_lacp_max_bundle and unconfigure_port_channel_lacp_max_bundle on port-channel interface level
    * Added configure_ospf_nsf_ietf API
        * API for configure nsf ietf under ospf
    * Added enable_multicast_advertise_on_evi API
        * API for Enable multicast advertise on evi
    * Added configure_replication_type_on_evi API
        * API for configure replication-type on evi
    * Added enable_switchport_trunk_on_interface API
        * API for enable switchport trunk on interface
    * Added disable_autostate_on_interface API
        * API for disable autostate on interface
    * Added configure_ip_unnumbered_on_interface API
        * API for configure ip unnumbered loopback on interface
    * Added configure_switchport_trunk_allowed_vlan API
        * API for configure switchport trunk allowed vlan on interface
    * Added configure_ip_pim_bsr_candidate API
        * API for configure ip pim bsr-candidate on interface
    * Added configure_ip_pim_rp_candidate_priority API
        * API for configure ip pim rp candidate priority on device
    * Added configure_bgp_router_id_interface API
        * API for configure bgp router-id interface on interface
    * Added configure_bgp_redistribute_static API
        * API for configure bgp redistribute static
    * Added configure_bgp_advertise_l2vpn_evpn API
        * API for configure bgp advertise l2vpn evpn
    * Added configure_nat_pool_overload_rule API
        * API to configure nat pool overload rule.
    * Added unconfigure_nat_pool_overload_rule API
        * API to unconfigure nat pool overload rule.
    * Added configure_static_nat_network_rule API
        * API to configure nat static network rule.
    * Added unconfigure_static_nat_network_rule API
        * API to unconfigure static nat network rule.
    * Added 'Reflexive ACL global timeout' API
    * Added 'tcp mss global and interface config' API
    * Added 'platform_software_fed_fnf_sw_stats_clear' API
    * Added configure_sks_client API:
      * Configure sks-client.
    * Added unconfigure_sks_client API:
      * Unconfigure sks-client with the given config block name.

* API utils
    * Modified api_unittest_generator
        * Added __init__.py file generation to support pytest
        * Added dynamic mock_data path to allow test runs from other folders

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* blitz
    * Fix for gNMI SET for List with Multiple Key Values in same testcase.
    * rpcverify.py
        * Fixed issue with remove/delete operation under verify_rpc_data_reply method
    * test_rpc.py
        * Updated existing test case and added new test case to test failed remove/delete operation.

* iosxe
    * Modified unconfigure_fnf_monitor_datalink_interface API
        * Changed the command, updated the parameters(added sampler_name and direction)
    * Fixed configure_ikev2_profile_advanced API
        * Fixed API for trustpoint configuration.


