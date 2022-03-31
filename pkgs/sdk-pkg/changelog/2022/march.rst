--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_static_nat_rule API
        * API for configuring static nat rule with udp port
    * Modified unconfigure_static_nat_rule API
        * API for unconfiguring static nat rule with udp port
    * Fix SISF API get_ip_theft_syslogs
        * Update regex to consider another variation
    * Modified verify_mpls_mroute_groupip api
        * Added next_hop argument to get the mapped lspvif interface
    * Modified verify_mpls_forwarding_table_vrf_mdt api
        * added a condition on failure, if 'prefix_no' is not 0 and traffic is not flowing, returned False. As by default traffic wont be runningi on prefix mdt 0
    * Modified verify_mpls_forwarding_table_gid_counter api
        * Added a expected_prefix_exempted condition on failure, as there will be default prefixes learnet which will not learn any traffic
    * Updated `verify_ping` API to use minimum success rate of 1 percent
    * Updated 'Install_Image' Clean Stage API
        * Updated install_add_one_shot_dialog to accept success if same image is already loaded.
    * Updated health_memory API
        * Fix a bug when passing command argument
    * Updated configure_ospf_routing API
        * configure_ospf_routing api to accept the nsf options, nsr and nsr options configuration.

* blitz
    * Prefixes not handeled correctly when origin is openconfig.

* apis
    * Modified creating the remote path so the files with more than one suffixes

* ios
    * Updated `verify_ping` API to use minimum success rate of 1 percent

* iosxr
    * Updated `verify_ping` API to use minimum success rate of 1 percent

* all
    * Modified setup.py and Makefile
        * pin grpcio version to be less than or equal to 1.36.1 to be in line with yang.connector

* sdk
    * triggers
        * update exclude platform for ha reload.
    * Updated the key value regex to handle unquoted integer key values in the xpath.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added 'configure_auto_qos' API
        * configure auto qos policy under interface
    * Added 'unconfigure_auto_qos' API
        * unconfigure auto qos policy under interface
    * Added verify_macsec_session API
        * API for verifying MKA MACsec session
    * Added verify_mka_session API
        * API for verifying MKA session
    * Added clear_ip_bgp API
        * API for clear ip bgp *
    * Added clear_mac_address_table_dynamic API
        * API for clear mac address-table dynamic
    * Added configure_cdp_interface API
        * API to configure cdp on interface.
    * Added unconfigure_cdp_interface API
        * API to unconfigure cdp on interface.
    * Added configure_disable_sci_dot1q_clear API
        * API to configure disable-sci and dot1q-in-clear on interface.
    * Added unconfigure_disable_sci_dot1q_clear API
        * API to unconfigure disable-sci and dot1q-in-clear on interface.
    * Added configure_scp_local_auth API
        * API to configure scp parameter with local authentication.
    * Added unconfigure_scp_local_auth API
        * API to configure scp parameter with local authentication.
    * Added execute_clear_platform_software_fed_active_cpu_interface API
        * API for executing clear cpu interface.
    * Added clear_mka_session API
        * API for clearing mka session.
    * Added execute_switch_card_OIR API
        * API for executing switch card OIR.
    * Added fp_switchover API
        * API to perform FP Switchover.
    * Added configure_ikev2_dpd API
        * API for configure ikev2 dpd.
    * Added configure_ikev2_fragmentation API
        * API for configure ikev2 fragmentation.
    * Added configure_ikev2_cac API
        * API for configure ikev2 CAC.
    * Added unconfigure_ikev2_proposal API
        * API for unconfigure ikev2 proposal.
    * Added unconfigure_ikev2_policy API
        * API for unconfigure ikev2 policy.
    * Added unconfigure_ikev2_dpd API
        * API for unconfigure ikev2 dpd.
    * Added unconfigure_ikev2_fragmentation API
        * API for unconfigure ikev2 fragmentation.
    * Added unconfigure_ikev2_cac API
        * API for unconfigure ikev2 CAC.
    * Added unconfigure_ikev2_authorization_policy API
        * API for unconfigure ikev2 authorization policy CAC.
    * Added configure_ipsec_fragmentation API
        * API for configure ipsec fragmentation.
    * Added configure_ipsec_df_bit API
        * API for configure ipsec donot fragment bit.
    * Added configure_ipsec_sa_global API
        * API for configure ipsec security association parameters.
    * Added unconfigure_ipsec_fragmentation API
        * API for unconfigure ipsec fragmentation.
    * Added unconfigure_ipsec_df_bit API
        * API for unconfigure ipsec donot fragment bit.
    * Added unconfigure_ipsec_sa_global API
        * API for unconfigure ipsec security association parameters.
    * Added get_component_details API
        * API for getting components' details (name, description, part number, serial number, hardware version)
    * Added get_component_description API
        * API for getting components' description
    * Added get_hardware_version API
        * API for getting components' hardware version
    * Added configure_mka_macsec API
        * API for configure mka macsec on interface.
    * Added unconfigure_mka_macsec API
        * API to unconfigure mka macsec on interface.
    * Added remove_ntp_master API
        * API to remove ntp master on interface.
    * Added configure_mdns_service_record_ttl API
        * API for configuring mDNS(Multicast Domain Name System) service record TTL value.
    * Added configure_mdns_service_receiver_purge_timer API
        * API for configuring mDNS(Multicast Domain Name System) service receiver Timer value.
    * Added configure_mdns_query_response_mode API
        * API for configuring mDNS(Multicast Domain Name System) query response mode.
    * Added configure_nat_route_map API
        * API for configuring a route-map in NAT feature.
    * Added unconfigure_nat_route_map API
        * API for unconfiguring a route-map in NAT feature.
    * Added configure_nat_extended_acl API
        * API for configuring a extended acl in NAT feature.
    * Added verify_ipv6_pim_neighbor API
        * verifies ipv6 pim neighbor on device
    * Added verify_acl_info_summary API
        * verifies acl summary on device
    * Added verify_ipv6_dhcp_pool
        * verifies ipv6 dhcp pool
    * Added verify_ipv6_ospf_neighbor_address_in_state
        * verifies ipv6 ospf neighbor
    * Added verify_ipv6_ospf_neighbor_addresses_are_not_listed
        * verifies ipv6 ospf neighbor not listed
    * Added get_ipv6_ospf_neighbor_address_in_state
        * get ipv6 ospfneighbor address
    * Added configure_bfd_neighbor_on_interface
        * configures bfd neighbor on interface
    * Added unconfigure_bfd_neighbor_on_interface
        * unconfigures bfd neighbor on interface
    * Added verify_acl_log
        * verifies acl log
    * Added verify_object_manager_error_objects_statistics
        * verifies error object stats
    * Added get_slice_id_of_interface
        * get slice id of interface
    * Added verify_ipv6_acl_tcam_utilization
        * verifies tcm uitilization of acl
    * Added 'execute_card_OIR_remove' API
        * execute card OIR remove API to remove the card
    * Added 'execute_card_OIR_insert' API
        * execute card OIR insert API to insert the card
    * Add disable debug API
    * Add clear matm table dynamic API
    * Added interface_counter_check api
        * Verifies packet flow on interface
    * Add EVPN API change_nve_source_interface
        * Added new API to change NVE source-interface IP
    * Added clear device-tracking database trigger
        * clear device-tracking database trigger added
    * Added 'verify_nve_evni_peer_ip_state' API
        * check whether evni for a given peer_ip is UP/DOWN
    * Added 'configure_crypto_ikev2_NAT_keepalive' API
        * configure crypto ikev2 nat keepalive <keepalive time>
    * Added 'unconfigure_crypto_ikev2_NAT_keepalive' API
        * unconfigure crypto ikev2 nat keepalive <keepalive time>
    * Added configure_boot_manual API
        * configure boot manual on device
    * Added configure_crypto_pki_server
        * Added new api to configure crypto pki server
    * Added configure_trustpoint
        * Added new api to configure crypto pki trustpoint
    * Added unconfigure_crypto_pki_server
        * Added new api to unconfigure crypto pki server
    * Added 'configure_crypto_ikev2_policy' API
        * configure crypto ikev2 policy <poicy_name>
    * Added 'unconfigure_crypto_ikev2_policy' API
        * unconfigure crypto ikev2 policy <policy_name>
    * Added 'configure_crypto_ikev2_proposal' API
        * configure crypto ikev2 proposal <proposal_name>
    * Added 'unconfigure_crypto_ikev2_proposal' API
        * unconfigure crypto ikev2 proposal <proposal_name>
    * Updated 'execute_card_OIR' API
        * execute card OIR updated to accept switch number for HA/SVL systems
    * Added configure_interface_switchport_pvlan_and_native_vlan API
        * Configuring switchport pvlan mode on Interface
    * Added configure_interface_switchport_pvlan_association API
        * Configuring switchport pvlan association on Interface
    * Added configure_interface_switchport_pvlan_mapping API
        * Configuring switchport pvlan mapping on Interface
    * Added configure_interface_pvlan_mode_with_submode API
        * Configuring switchport pvlan mode with submode on Interface
    * Added get_software_version API
        * API for getting a device software version info
    * Added get_firmware_version API
        * API for getting components' firmware version in CAT 9600 and 9400 series
    * Added removeMissingComp API
        * API for removing components that are in CLI but are not present in GNMI query
    * Added new configure_shape_map API
        * configure queuing shape-map on device
    * Added configure_vlan_shutdown API
        * Added new api to shutdown the data vlan
    * Added unconfigure_vlan_configuration API
        * Added new api to unconfigure the vlan configuration
    * Added unconfigure_mdns_location_filter API
        * Added new api to unconfigure the mdns location filter
    * Added configure_ospf_redistributed_static API
        * Added new api to configure the ospf params redistribute static
    * Added configure_bgp_update_delay API
        * Added new api to configu bgp params update delay
    * Added 'configure_crypto_ipsec_nat_transparency' API
        * configure/unconfigure crypto ipsec nat-transparency udp-encapsulation

* cheetah
    * Added verify_operation_state
        * Added new api to verify operation state of AP
    * Added verify_controller_name
        * Added new api to verify controller name to which AP has joined
    * Added verify_controller_ip
        * Added new api to verify controller IP/IPv6 address to which AP has joined
    * Added get_ap_mode
        * Added new api to get AP Mode
    * Added get_operation_state
        * Added new api to get AP Operation state
    * Added get_controller_name
        * Added new api to get controller name to which AP has joined
    * Added get_ip_address
        * Added new api to get controller IP/IPv6 address to which AP has joined
    * Added get_ip_prefer_mode
        * Added new api to get AP IP preferred mode.
    * Added execute_prime_ap
        * Added new file called execute.py where all execute commands can be written
        * Added api to execute command that primes AP to the controller
    * Added execute_erase_ap
        * Added api to execute command that erases the configurations of AP

* nxos
    * Added the following process restart test triggers
        * TriggerProcessKillRestartMonitor
        * TriggerProcessCrashRestartMonitor
        * TriggerProcessKillRestartIntersight
        * TriggerProcessCrashRestartIntersight
        * TriggerProcessKillRestartNXOSDC
        * TriggerProcessCrashRestartNXOSDC

* <iosxe>
    * Added API for execute_test_idprom_fake_insert
        * test idprom interface {interface} fake-insert
    * Added API for execute_test_idprom_fake_remove
        * test idprom interface {interface} fake-remove
    * Added API for configure_stackwise_virtual_dual_active_interfaces
        * interface {interface}; stackwise-virtual dual-active-detection
    * Added API for unconfigure_stackwise_virtual_dual_active_interfaces
        * interface {interface}; no stackwise-virtual dual-active-detection
    * Added API for configure_global_dual_active_recovery_reload_disable
        * stackwise-virtual; dual-active recovery-reload-disable
    * Added API for unconfigure_global_dual_active_recovery_reload_disable
        * stackwise-virtual; no dual-active recovery-reload-disable
    * Added API for configure_stackwise_virtual_dual_active_pagp
        * stackwise-virtual; dual-active detection pagp; dual-active detection pagp trust channel-group {port_channel}
    * Added API for unconfigure_stackwise_virtual_dual_active_pagp
        * stackwise-virtual; no dual-active detection pagp trust channel-group {port_channel}

* blitz
    * Added Negative Test banner
        * Negative Test banner will show if it is Negative Test
    * Yang action
        * Added support for include/exclude
        * Added sequence key to support return values and return sequence verified


