--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added 'configure access vlan' API
        * creating access vlan and adding interface
    * Added 'show mac address table| i count' API
        * api to display final mac count without displaying all mac address enties
    * Added 'udld port alert' API
        * configuring udld alert only mode on interface
    * Added 'trigger udld tx drop' API
        * configuring udld transmiddion drop on interface
    * Added API 'configure_ip_igmp_snooping_querier'
    * Added API 'unconfigure_ip_igmp_snooping_querier'
    * Added API 'configure_ip_igmp_snooping_vlan_querier'
    * Added API 'unconfigure_ip_igmp_snooping_vlan_querier'
    * Added API 'configure_ip_igmp_snooping_vlan_query_version'
    * Added API 'unconfigure_ip_igmp_snooping_vlan_query_version'
    * Added API 'configure_ipv6_mld_snooping'
    * Added API 'unconfigure_ipv6_mld_snooping'
    * Added API 'configure_ipv6_mld_snooping_querier_version'
    * Added API 'unconfigure_ipv6_mld_snooping_querier_version'
    * Added API 'configure_ipv6_mld_snooping_querier_address'
    * Added API 'unconfigure_ipv6_mld_snooping_querier_address'
    * Added API 'configure_ipv6_mld_snooping_vlan_querier_version'
    * Added API 'unconfigure_ipv6_mld_snooping_vlan_querier_version'
    * Added API 'configure_vrf_definition_stitching'
    * Added API 'unconfigure_vrf_definition_stitching'
    * Added API 'configure_static_ip_pim_rp_address'
    * Added API 'configure_static_ipv6_pim_rp_address'
    * Added API 'unconfigure_static_ip_pim_rp_address'
    * Added API 'unconfigure_static_ipv6_pim_rp_address'
    * Added API 'unconfig_disable_ipv6_routing'
    * Added API 'configure_ip_multicast_routing'
    * Added API 'unconfigure_ip_multicast_routing'
    * Added API 'configure_ip_multicast_vrf_routing'
    * Added API 'unconfigure_ip_multicast_vrf_routing'
    * Added API 'configure_interface_storm_control_level'
        * configure storm-control level under interface
    * Added API 'unconfigure_interface_storm_control_level'
        * unconfigure storm-control level under interface
    * Added API 'configure_interface_storm_control_action'
        * configure storm-control action under interface
    * Added API 'unconfigure_interface_storm_control_action'
        * unconfigure storm-control action under interface
    * Added API 'configure_platform_sudi_cmca3'
    * Added API 'unconfigure_platform_sudi_cmca3'
    * Added API 'configure_service_private_config_encryption'
    * Added API 'unconfigure_service_private_config_encryption'
    * Added API 'verify_Parser_Encrypt_decrypt_File_Status'
    * Added API 'verify_cmca3_certificates'
    * Added API 'verify_crypto_entropy_status'
    * Added API 'verify_crypto_pki_certificate'
    * Added API 'verify_hardware_slot'
    * Added API 'verify_hw_auth_status'
    * Added API 'verify_sudi_cert'
    * Added API 'verify_sudi_pki'
    * Added configure_hqos_policer_map API
        * API for configuring hqos policy map for service-policy.
    * Added API 'configure_nve_interface' in evpn
    * Added API 'unconfigure_nve_interface' in evpn
    * Added API 'configure_interface_pim' in mcast
    * Added API 'unconfigure_interface_pim' in mcast
    * Added config_mka_policy API
        * API for configuring MKA Policy globally and also interface level
    * Added unconfig_macsec_should_secure API
        * API for Removal of Should secure on interface level
    * Added config_macsec_should_secure API
        * API for Configuring Should secure on interface level
    * Added unconfig_mka_policy API
        * API for unconfiguring MKA Policy globally and also interface level
    * Added configure_default_mpls_mldp api
    * Added configure_mdt_data_mpls_mldp api
    * Added configure_mdt_data_threshold api
    * Added configure_mdt_partitioned_mldp_p2mp api
    * Added configure_mdt_preference_under_vrf api
    * Added configure_mdt_strict_rpf_interface_vrf api
    * Added configure_multicast_routing_mvpn_vrf api
    * Added configure_vpn_id_in_vrf api
    * Added unconfigure_mdt_data_threshold api
    * Added 'clear_mdns_cache' API
        * clears mDNS cache
    * Added 'clear_mdns_statistics_all' API
        * clears mDNS statistics
    * Added 'clear_mdns_statistics_sp_sdg' API
        * clears mDNS statistics sp(Service Peer)_sdg(Agent)
    * Added 'clear_mdns_statistics_servicepeer' API
        * clears mDNS statistics sp(Service Peer)
    * Added 'configure_mdns_boot_level_license' API
        * Configures mDNS boot level license
    * Added config_vlan_range API
        * To configure vlan for a range
    * Added unconfig_vlan_range API
        * To unconfigure vlan for a range
    * Added config_portchannel_range API
        * To configure portchannel for a range
    * Added 'unconfigure_ipv6_mld_snooping_querier_version' API
        * Added doc string to unconfigure.
    * Added 'configure_ipv6_mld_snooping_querier_address' API
        * Changed Args headline for ipv6_address and updated ipv6 MLD querier source IPv6 address
    * Added execute_issu_install_package API
        * To execute issu install packages on device
    * Added verify_wireless_management_trustpoint_name
        * Added new api to verify wireless management trustpoint
    * Added verify_pki_trustpoint_state
        * Added new api to verify crypto pki trustpoint
    * Added get_wireless_management_trustpoint_name
        * Added new api to get wireless management trustpoint certificate name
    * Added get_pki_trustpoint_state
        * Added new api to get crypto pki trustpoint key state
    * Added execute_self_signed_certificate_command
        * Added new file called execute.py where all execute commands can be written
        * Added api to execute command that installs self-signed certificate
    * Added enable_http_server
        * Added new file called configure.py where all configure commands can be written
        * Added api to configure  ip http server on controller
    * Added set_clock_calendar
        * Added api to configure valid clock calendar
    * Added configure_pki_trustpoint API
        * Configures Trustpoint on device
    * Added unconfigure_pki_trustpoint API
        * Unconfigures Trustpoint on device
    * Added configure_pki_export_pem API
        * Generates a certificate in device
    * Added configure_pki_authenticate_certificate API
        * Pastes the pagent certificate in the device
    * Added unconfigure_crypto_pki_server API
        * Unconfigures Crypto PKI server on device
    * Added configure_crypto_pki_server API
        * Configures Crypto PKI server on device
    * Added configure_pki_enroll_certificate API
        * Enrolls certificate on device
    * Added ignore modules argument for verify_module_status api
    * Added
        * Added new API config_port_security_on_interface, configuring port security on interface.
    * Added disable_ipv6_dhcp_server API
        * unconfigures ipv6 dhcp server  on interface
    * Added configure_dhcp_pool_ipv6_domain_name API
        * configures domain name under dhcp pool on device
    * Added enable_ipv6_address_dhcp API
        * enables ipv6 address dhcp on interface
    * Added disable_ipv6_address_dhcp API
        * disables ipv6 address dhcp on interface
    * Added configure_ipv6_ospf_mtu_ignore API
        * Configures ipv6 ospf mtu-ignore on interface
    * Added unconfigure_ipv6_ospf_mtu_ignore API
        * Unconfigures ipv6 ospf mtu-ignore on interface
    * Added configure_ipv6_ospf_routing_on_interface API
        * Configures ipv6 ospf routing instance on interface
    * Added unconfigure_ipv6_ospf_routing_on_interface API
        * Unconfigures ipv6 ospf routing instance on interface
    * Added unconfig_interface_ospfv3 API
        * unconfigures ospfv3 on interface

* utils
    * Added get_interface_attr_from_yaml
        * get attribute value of a interface from topology in testbed object

* clean/reload
    * Added an argument to ignore modules during check modules step.

* iosxr
    * Added ignore modules argument for verify_module_status api

* nxos
    * Added ignore modules argument for verify_module_status api

* added new api configure_control_policies, configuring policy-map.

* added new api clear_port_security, clearing port security stats, clear port-security all.

* added new api unconfig_vlan_tag_native, unconfig vlan dot1q tag native.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Fix config_mka_keychain_on_interface API
        * API for Configuring Primary MKA Key chain and fallback MKA Key chain on interface level
    * Updated 'configure_mdns' API
        * Added if condition for creating only one service list with direction and definition name
    * Modified `verify_ip_mac_binding_in_network`
        * Added verify_reachable option to require entries to be reachable
    * Fixed `get_ip_theft_syslogs`
        * Corrected to support new syslog output
    * Modified `verify_module_status` API to ignore empty slots
    * Updated `get_md5_hash_of_file` API to use 180s default timeout
    * Updated health_cpu API
        * Added 'timeout' argument
    * Updated health_memory API
        * Added 'timeout' argument

* generic
    * Updated `copy_from_device` and `copy_to_device` APIs to support dynamic HTTP fileserver

* api utils
    * Modified api_unittest_generator
        * Proxy connection raises proper error message

* iosxr
    * Added c8000 platform for get_mgmt APIs
    * Updated health_cpu API
        * Added 'timeout' argument
    * Updated health_memory API
        * Added 'timeout' argument

* blitz
    * actions_helper
        * Fixed the issue with configure_dual
    * Added gnmi_util module for message constuction
        * Fixed OpenConfig module gNMI message building for complex RPCs.
        * Fixed "empty" error when gNMI return message does not validate zero value.
        * Negative range not validating return message values.
    * Added protobuf and cisco-gnmi dependency for genie.libs.sdk package
    * Updated rest_handler
        * Fixed 'save' handling in 'rest' action

* apic
    * Updated apic_rest_get API
        * Added order_by argument support

* nxos
    * Updated health_cpu API
        * Added 'timeout' argument
    * Updated health_memory API
        * Added 'timeout' argument
    * Updated nxapi_method_nxapi_rest API
        * Fixed wrong avariable name to show proper error message


