--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added get_interface_capabilities_multiple_media_types
        * API for "get_interface_capabilities_multiple_media_types to know type of connection i.e fiber, copper and dual-port"
    * Added request platform_software_package_expand
        * API to expand package from filesystem
        * API to expand package from sub directory filesystem
    * Added configure_snmp_server_host_trap
        * API to configure snmp server host trap
    * Added configure_ipv6_dhcp_relay_trust
        * API to configure ipv6 dhcp relay trust
    * Added unconfigure_ipv6_dhcp_relay_trust
        * API to unconfigure ipv6 dhcp relay trust
    * Added configure_ipv6_dhcp_relay_option_vpn
        * API to configure ipv6 dhcp relay option vpn
    * Added unconfigure_ipv6_dhcp_relay_option_vpn
        * API to unconfigure ipv6 dhcp relay option vpn
    * Added configure_ipv6_dhcp_relay_source_interface_intf_id
        * API to configure ipv6 dhcp relay source-interface interfaceid
    * Added unconfigure_ipv6_dhcp_relay_source_interface_intf_id
        * API to unconfigure ipv6 dhcp relay source-interface interfaceid
    * Added configure_ipv6_dhcp_relay_destination_ipv6address
        * API to configure ipv6 dhcp relay destination ipv6address
    * Added unconfigure_ipv6_dhcp_relay_destination_ipv6address
        * API to unconfigure ipv6 dhcp relay destination ipv6address
    * Added configure_aaa_accounting_update_periodic_interval
        * API to configure aaa accounting update periodic {interval}
    * Added configure_ip_dhcp_snooping_information_option_allow_untrusted_global
        * API to configure ip dhcp snooping information option allow-untrusted global
    * Added unconfigure_ip_dhcp_snooping_information_option_allow_untrusted_global
        * API to unconfigure ip dhcp snooping information option allow-untrusted global
    * Added configure_management_gnmi api
        * New API to configure gnmi
    * Updated configure_management_protocol api
        * updated the logic to support the new schema
    * Added disable_cts_enforcement_vlan_list
        * API to disable CTS enforcement on vlan-list
    * Added execute_clear_ipv6_mld_group
        * New API to execute clear ipv6 mld group
    * Added execute_clear_ip_igmp_group
        * New API to execute clear ip igmp group
    * Added configure_object_list_schema_transfer_for_bulkstat
        * API to configure object list schema transfer for bulkstat
    * Added configure_bridge_domain
        * added api to configure bridge-domain
    * Added unconfigure_bridge_domain
        * added api to unconfigure bridge-domain
    * Added configure_interface_vlan
        * New API to configure interface vlan 10
    * Added configure_interface_range_no_switchport
        * New API to configure interface range no switchport
    * Added execute_clear_aaa_counters_server
    * Added configure_aaa_accounting_update
        * API to configure aaa accounting update
    * Added unconfigure_aaa_accounting_update
        * API to unconfigure aaa accounting update
    * Added unconfigure_aaa_accounting_identity_default_start_stop
        * API to unconfigure aaa accounting identity default start stop
    * Added configure_service_instance
        * added api to configure service instance
    * Added unconfigure_service_instance
        * added api to unconfigure service instance
    * Added configure_interface_ip_nbar
        * added api to configure interface ip nbar
    * Added unconfigure_interface_ip_nbar
        * added api to unconfigure interface ip nbar
    * Added execute_archive_tar
        * API to execute archive tar
    * Added api configure_breakout_cli
        * API to configure breakout
    * Added api unconfigure_breakout_cli
        * API to unconfigure breakout
    * Added configure_ip_multicast_routing_distributed
        * New API to configure ipv6 multicast routing
    * Added unconfigure_ip_multicast_routing_distributed
        * New API to unconfigure ipv6 multicast routing
    * Added clear_crypto_call_admission_stats
        * New API to clear ikev1 statistics
    * Added disable_crypto_engine_compliance
        * New API to disable crypto engine compliance shield
    * Added get_interface_media_types
        * API for "get interface media_types"
    * Added config_ip_pim_vrf_mode
        * added api to configure ip pim vrf mode
    * Added unconfig_ip_pim_vrf_mode
        * added api to unconfigure ip pim vrf mode
    * Added config_ip_multicast_routing_vrf_distributed
        * added api to configure ip multicast-routing vrf distributed
    * Added unconfig_ip_multicast_routing_vrf_distributed
        * added api to unconfigure ip multicast-routing vrf distributed
    * Added api erase startup-config
        * API to erase startup-config
    * Added  install_wcs_enable_guestshell
        * New API to  install wcs enable guestshell
    * Added execute_apphosting_cli
        * New API to execute apphosting cli
    * Added enable_usb_ssd_verify_exists
        * New API to  enable usb ssd verify exists
    * Added configure_app_management_networking
        * New API to configure app management networking
    * Added clear_ip_mfib_counters
        * New API to execute clear ip mfib counters
    * Added configure_controller_shutdown API
        * API to configure controller shutdown/no shutdown
    * Added api configure_mode_change
        * API to configure mode change

* sdk-pkg
    * Modified pysnmp to pysnmp-lextudio

* linux
    * Added generate_rsa_ssl_key
        * New API to generate an RSA key on a linux server via OpenSSL
    * Added generate_ecc_ssl_key
        * New API to generate an Elliptic Curve key with a user selected algorithm via OpenSSL
    * Added generate_ca_certificate
        * New API to generate a CA Certificate via OpenSSL
    * Added generate_ssl_certificate
        * New API to generate an SSL Certificate via OpenSSL
    * Added get_supported_elliptic_curves
        * New API to fetch supported curves on a Linux server via OpenSSL and return a list
    * Added get_file_contents
        * New API that cats out the contents of a file to a return


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* utils
    * Modified
        * Fix trigger discovery from relative Task object

* iosxe
    * Modified configure_evpn_l2_instance_vlan_association
        * added protected optional input variable
    * Modified configure_ospf_redistributed_connected
        * added vrf optional input variable
    * Modified configure_ospfv3
        * added redistribute {route_method} command
    * Modified configure_static_nat_route_map_rule
        * Added no_alias to configure static nat route-map rule with no-alias
    * Modified unconfigure_static_nat_route_map_rule
        * Added no_alias to unconfigure static nat route-map rule with no-alias
    * Modified config_extended_acl
        * added parameter port type
    * Modified
        * Modified copy_to_device to update the image path if verify_running_image is True
    * Modify configure_cdp and unconfigure_cdp
        * Added timeout for show interfaces
    * Modified configure_snmp_server_user
        * Added elif to configure snmp server user
    * Updated get_interface_interfaces_under_vrf
        * No change to API. Adjusted UT for related parser change
    * Modified configure_gdoi_group
        * added additional attributes gikev2_profile, rekey_address_acl, gikev2_client and pfs

* jinja2
    * Modified change_configuration_using_jinja_templates
        * Passing kwargs to device.configure

* general
    * Fix loading APIs under threaded environment

* genie.libs.sdk
    * Updated yang.connector and rest.connector dependencies to use correct versions.


--------------------------------------------------------------------------------
                                     Update                                     
--------------------------------------------------------------------------------

* sdk-pkg
    * Modified health logging


