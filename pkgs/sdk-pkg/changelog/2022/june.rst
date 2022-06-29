--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_call_admission API
        * configure call admission
    * Added unconfigure_call_admission API
        * unconfigure call admission
    * Added configure_broadband_aaa API
        * configure broadband aaa
    * Added unconfigure_broadband_aaa API
        * unconfigure broadband aaa
    * Added configure_bgp_router_id_peergroup_neighbor
        * API for configure bgp router id with peergroup neighbor name details
    * Added configure_bgp_router_id_neighbor_ip_peergroup_neighbor
        * API for configure bgp router id neighbor ip assigned to peer group neighborname
    * Added clear_ip_reflexive_list API
        * API to clear_ip_reflexive_list
    * Added clear_dmvpn_statistics API
        * API for clearing dmvpn crypto commands.
    * Added API to configure device credentials
        * configure_masked_unmasked_credentials
    * Added API to configure enable password
        * configure_masked_unmasked_enable_secret_password
    * Added API to unconfigure enable password
        * unconfigure_enable_password
    * Added API to verify device login
        * verify_login_credentials_enable_password
    * Enhanced existing API verify_enable_password to support privilege level
        * verify_enable_password
    * Added API to configure aaa password restriction
        * enable_aaa_password_restriction
    * Added API to unconfigure aaa password restriction
        * disable_aaa_password_restriction
    * Added API to configure login password-reuse-interval <interval>
        * enable_login_password_reuse_interval
    * Added API to unconfigure login password-reuse-interval
        * disable_login_password_reuse_interval
    * Added API to configure aaa authentication login default local tacacs+
        * enable_aaa_authentication_login
    * Added API to unconfigure aaa authentication login default local tacacs+
        * disable_aaa_authentication_login
    * Added API to configure automate-tester username <name> probe-on vrf <vrf>
        * enable_radius_automate_tester_probe_on
    * Added API 'rdware_qfp_active_ipsec_data_drop_clear'
    * Added configure_nat64_interface API
        * API for configuring nat64 enable on interface
    * Added  unconfigure_nat64_interface API
        * API for unconfiguring nat64 enable on interface
    * Added configure_nat64_prefix_stateful API
        * API for configuring nat64 prefix stateful
    * Added unconfigure_nat64_prefix_stateful API
        * API for unconfiguring nat64 prefix stateful
    * Added configure_nat64_translation_timeout API
        * API for configuring nat64 translation timeout
    * Added unconfigure_nat64_translation_timeout API
        * API for unconfiguring nat64 translation timeout
    * Added configure_nat64_v4_list_pool API
        * API for configuring nat64 v4 list pool
    * Added  unconfigure_nat64_v4_list_pool API
        * API for unconfiguring nat64 v4 list pool
    * Added configure_nat64_v4_list_pool_overload API
        * API for configuring nat64 list pool overload
    * Added unconfigure_nat64_v4_list_pool_overload API
        * API for unconfiguring nat64 list pool overload
    * Added configure_nat64_v4_pool API
        * API for configuring nat64 v4 pool
    * Added unconfigure_nat64_v4_pool API
        * API for unconfiguring nat64 v4 pool
    * Added configure_nat64_v6v4_static API
        * API for configuring nat64 v6v4 static
    * Added unconfigure_nat64_v6v4_static API
        * API for un configuring nat64 nat64 v6v4 static
    * Added configure_nat64_v6v4_static_protocol_port API
        * API for configuring nat64 v6v4 static protocol port
    * Added unconfigure_nat64_v6v4_static_protocol_port API
        * API for un configuring nat64 nat64 v6v4 static protocol port
    * Added configure_nat_ipv6_acl API
        * API for configuring nat ipv6 acl
    * Added clear_dmvpn_statistics API
        * API for clearing dmvpn crypto commands.
    * Added API 'hardware_qfp_active_statistics_drop_clear'
    * Added API 'verify_interface_status'
    * Added API 'configure_SVI_Unnumbered'
    * Added API 'configure_SVI_Autostate'
    * Added API 'configure_VRF_RD_Value'
    * Added configure_hsrp_interface  API
        * API for configuring hsrp on interface
    * Added configure_ipv6_mtu  API
        * API for configuring ipv6 mtu on interface
    * Added unconfigure_ipv6_mtu  API
        * API for unconfiguring ipv6 mtu on interface
    * modified configure_ip_on_tunnel_interface API
        * change tunnel mode {mode} ipv4 to tunnel mode {mode} ip
    * Added configure_ip_dhcp_snooping_information_option_allow_untrusted API
        * API for ip dhcp snooping information option allow-untrusted
    * Added unconfigure_ip_dhcp_snooping_information_option_allow_untrusted API
        * API for no ip dhcp snooping information option allow-untrusted
    * Added configure_mdns_on_interface_vlan API
        * API to configure_mdns_on_interface_vlan
    * Added unconfigure_mdns_on_interface_vlan API
        * API to unconfigure_mdns_on_interface_vlan
    * Added configure_port_channel_standalone_disable API
        * API to configure_port_channel_standalone_disable
    * Added unconfigure_port_channel_standalone_disable API
        * API to unconfigure_port_channel_standalone_disable
    * Added API for configure extended acl with reflect
        * 'config_extended_acl_with_reflect'
    * Added API for unconfigure extended acl with reflect
        * 'unconfig_extended_acl_with_reflect'
    * Added API for configure extended acl with evaluate
        * 'config_extended_acl_with_evaluate'
    * Added API for unconfigure extended acl with evaluate
        * 'unconfig_extended_acl_with_evaluate'
    * Added configure_vfi API
        * API for configuring vfi into vlan interface.
    * Added unconfigure_vfi API
        * API for unconfiguring vfi into vlan interface.
    * Modified configure_l2vpn_vfi_context_vpls API
        * API has been modified to configure autodiscovery bgp signalling ldp under vfi
    * Added execute_clear_nat64_statistics API
        * API to clear nat64 statistics.
    * Added execute_clear_nat64_statistics_failure API
        * API to clear nat64 statistics failure.
    * Added execute_clear_nat64_statistics_global API
        * API to clear nat64 statistics global.
    * Added execute_clear_nat64_statistics_interface API
        * API to clear nat64 statistics interface {interface_name}.
    * Added execute_clear_nat64_statistics_pool API
        * API to clear nat64 statistics pool {pool_name}.
    * Added execute_clear_nat64_statistics_prefix_stateful API
        * API to clear nat64 statistics prefix stateful {ipv6_address}/{prefix_length}.
    * Added execute_clear_nat64_translations_all API
        * API to clear nat64 translations all.
    * Added execute_clear_nat64_translations_protocol API
        * API to clear nat64 translations protocol {protocol_name}.
    * Added configure_platform_qos_port_channel_aggregate API
        * API for configuring platform qos port-channel-aggregate.
    * Added unconfigure_platform_qos_port_channel_aggregate API
        * API for unconfiguring platform qos port-channel-aggregate.
    * Added configure_pppoe_enable_interface API
        * Configure pppoe on the router interface
    * Added unconfigure_pppoe_enable_interface API
        * Unconfigure pppoe on the router interface.
    * Fixed iosxe vrf folder and file name
    * Added get_installation_mode
        * Added new api to get installation mode for the controller
    * Added get_ap_model
        * Added new api to get ap model of the access point
    * Added get_tx_power
        * Added new api to get tx power of the access point
    * Added get_unused_channel
        * Added new api to get un used channels of the controller
    * Added get_assignment_mode
        * Added new api to get assignment mode of the controller
    * Added verify_tx_power
        * Added new api to verify tx power of the access point
    * Added verify_unused_channel
        * Added new api to verify un used channels of the controller
    * Added verify_assignment_mode
        * Added new api to verify assignment mode of the controller
    * Added ConfigureApTxPower
        * Added new class to configure access point Tx power
    * Added VerifyInstallationMode
        * Added new class to verify installation mode
    * Added ConfigureRrmDcaChannel
        * Added new class to configure rrm dca channel

* iosxr
    * Added configure_bandwidth_remaining_policy_map API
        * API for configure bandwidth remaining policy map on device
    * Added unconfigure_bandwidth_remaining_policy_map API
        * API for unconfigure bandwidth remainging policy map on device


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Updated configure_bgp_neighbor API
        * Fixed address-family being mandatory issue
    * Fixed get_software_version API
        * Changed the output of the API, added enclosing square bracket
        * NOT BACKWARDS COMPATIBLE
    * Modified api 'verify_file_exists'
        * Api checks exact directory and returns False if folder does not exist

* nxos
    * Modified
        * filetransferutils.fileutils.FileUtils.get_server()
        * sdk.apis.utils.copy_from_device()
        * sdk.apis.nxos.platform.get.get_platform_core()


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Added configure_tacacs_server API
        * Added the configure.py(configure_tacacs_server api) to cat9k folder


