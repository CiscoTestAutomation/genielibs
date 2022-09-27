--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added confgiure_port_channel_min_link
        * API for configure port-channel min links
    * Added unconfgiure_port_channel_min_link
        * API for unconfigure port-channel min links
    * Added configure_vtp_domain
        * API for configure vtp domain on the device
    * Added configure_vtp_version
        * API for configure vtp domain on the device
    * Added unconfigure_vtp_version
        * API for unconfigure vtp version on the device
    * Added configure_interface_vtp
        * API for configure vtp on a interface
    * Added unconfigure_interface_vtp
        * API for unconfigure vtp on a interface
    * Added configure_mdt_data_vxlan api
        * Api for configuring mdt data vxlan ip inside of addressfamily of vrf
    * Added unconfigure_mdt_data_vxlan api
        * Api for unconfiguring mdt data vxlan ip inside of addressfamily of vrf
    * Created crypto_key_zeroize api
        * Created a new API to clear or zeroize crypto keys
    * Created generate_crypto_key api
        * Created a new API to generate crypto keys
    * Created crypto_key_export api
        * Created a new API to export crypto keys
    * Added configure_gdoi_group API
        * Added new API to configure getvpn gdoi group
    * Added unconfigure_gdoi_group API
        * Added new API to unconfigure getvpn gdoi group
    * Added clear_crypto_gkm API
        * Added new API to clear getvpn gkm group
    * Added configure_isakmp_policy api
        * Api to configure isakmp policy
    * Added unconfigure_isakmp_policy api
        * Api to unconfigure isakmp policy
    * Added configure_isakmp_key api
        * Api to configure isakmp key
    * Added unconfigure_isakmp_key api
        * Api to unconfigure isakmp key
    * Added configure_spanning_tree_mode
        * API for configure spanning tree mode
    * Added unconfigure_spanning_tree_mode
        * API for Unconfigure the spanning tree mode
    * Added configure_isis_with_router_name_network_entity
        * API for configure the isis with router name
    * Added unconfigure_isis_with_router_name
        * API for unconfigure the isis with router name
    * Added config_interface_with_isis_router_name
        * API for configure the interface with isis router name
    * Added unconfig_interface_isis_router_name
        * API for unconfigure the interface isis router name
    * Added configure_ospf_area_type
        * API for configure ospf area type
    * Added unconfigure_ospf_area_type
        * API for unconfigure ospf area type
    * Added redistribute_eigrp_under_ospf
        * API for configure redistribute eigrp under ospf
    * Added unconfigure_redistribute_eigrp_under_ospf
        * API for unconfigure redistribute eigrp under ospf
    * Added configure_ip_igmp_snooping
        * API for configure ip igmp snooping on switch
    * Added unconfigure_ip_igmp_snooping
        * API for unconfigure ip igmp snooping on switch
    * Added configure_lacp_ratefast
        * API for configure lacp rate fast on an interface
    * Added unconfigure_lacp_ratefast
        * API for unconfigure lacp rate fast on an interface
    * Added configure_lacp_port_priority
        * API for configure lacp port priority on an interface
    * Added unconfigure_lacp_port_priority
        * API for unconfigure lacp port priority on an interface
    * Added configure_ipv6_to_sgt_mapping API
        * Added new API to configure ipv6 to sgt mapping
    * Added unconfigure_ipv6_to_sgt_mapping API
        * Added new API to unconfigure ipv6 to sgt mapping
    * Added configure_ipv6_subnet_to_sgt_mapping API
        * Added new API to configure ipv6 subnet to sgt mapping
    * Added unconfigure_ipv6_subnet_to_sgt_mapping API
        * Added new API to unconfigure ipv6 subnet to sgt mapping
    * Added configure_host_ip_to_sgt_mapping API
        * Added new API to configure host ip to sgt_mapping
    * Added unconfigure_host_ip_to_sgt_mapping API
        * Added new API to unconfigure host ip to sgt_mapping
    * Added configure_vrf_ip_to_sgt_mapping API
        * Added new API to configure configure vrf ip to sgt_mapping
    * Added unconfigure_vrf_ip_to_sgt_mapping API
        * Added new API to unconfigure configure vrf ip to sgt_mapping
    * Added configure_vrf_ip_subnet_to_sgt_mapping API
        * Added new API to configure vrf subnet ip to sgt_mapping
    * Added unconfigure_vrf_ip_subnet_to_sgt_mapping API
        * Added new API to unconfigure vrf subnet ip to sgt_mapping
    * Added configure_cts_role_based_permission API
        * Added new API to configure cts role based permission
    * Added unconfigure_cts_role_based_permission API
        * Added new API to unconfigure cts role based permission
    * Added configure_cts_role_based_permission_default API
        * Added new API to configure cts role based permission default
    * Added unconfigure_cts_role_based_permission_default API
        * Added new API to unconfigure cts role based permission default
    * Added configure_cts_role_based_monitor API
        * Added new API to configure cts role based monitor
    * Added unconfigure_cts_role_based_monitor API
        * Added new API to unconfigure cts role based monitor
    * Added configure_cts_enforcement_interface API
        * Added new API to configure cts enforcement on interface
    * Added unconfigure_cts_enforcement_interface API
        * Added new API to unconfigure cts enforcement on interface
    * Added configure_ip_role_based_acl API
        * Added new API to configure cts ip role based acl
    * Added unconfigure_ip_role_based_acl API
        * Added new API to unconfigure cts ip role based acl
    * Added configure_ipxe_timeout and configure_ipxe_forever API
        * API for configuring boot ipxe timeout switch and boot ipxe forever switch cli
    * Added config_standby_console_enable API
        * API to enable standby console
    * Added configure_power_inline
        * API for configure power inline commands on interface
    * Added unconfigure_power_inline
        * API for unconfigure power inline commands on interface
    * Added enable_dhcp_snooping_glean
        * Added new api to configure - ip dhcp snooping glean
    * Added disable_dhcp_snooping_glean
        * Added new api to unconfigure - no ip dhcp snooping glean
    * Added clear_ip_dhcp_binding
        * Added new api to - clear ip dhcp binding *
    * Added clear_ip_dhcp_snooping_binding
        * Added new api to - clear ip dhcp snooping binding *
    * Added verify_dhcp_snooping_glean_enabled
        * Added new api which confirms dhcp snooping glean has been enabled
    * Added verify_dhcp_snooping_glean_disabled
        * Added new api which confirms dhcp snooping glean has been disabled
    * Added configure_access_session_port_control
        * Added new api to configure - access-session port-control auto - on an interface
    * Added configure_lacp_system_priority
        * API for configure lacp system priority
    * Added unconfigure_lacp_system_priority
        * API for unconfigure lacp system priority
    * Added configure_port_channel_mode
        * API for configure port channel mode
    * Added unconfigure_port_channel_mode
        * API for unconfigure port channel mode
    * Added configure_interface_channel_group_auto_lacp
        * API for configure auto Enable LACP auto on this interface
    * Added unconfigure_interface_channel_group_auto_lacp
        * API for unconfigure auto Enable LACP auto on this interface
    * Added configure_service_timestamps
        * API for configure service timestamps
    * Added unconfigure_service_timestamps
        * API for unconfigure service timestamps
    * Added copy_startup_config_to_tftp
        * API for copy startup configs to tftp
    * Added copy_startup_config_to_flash_memory
        * API for copy starup configs to flash memory
    * Added copy_running_config_to_tftp
        * API for copy running configs to tftp
    * Added clear_fqdn_database_all as API
        * Added "clear fqdn database all" command
    * Added clear_fqdn_packet_statistics as API
        * Added "clear fqdn packet statistics" command
    * Added configure_archive_logging API
        * Configure archive logging enable cli on device
    * Added unconfigure_archive_logging API
        * Unconfigure archive cli on device
    * Added configure_switch_provision API
        * Configure switch provision cli on device
    * Added unconfigure_switch_provision API
        * Unconfigure switch provision cli on device
    * Added configure_interface_macro API
        * configure interface macro cli on device
    * Added configure_lineconsole_exectimeout API
        * API for configure line console exec timeout
    * Added configure_crypto_map_for_gdoi  API
        * API for configuring crypto map for gdoi protocol
    * Added configure_crypto_map_on_interface  API
        * API for configuring crypto map on interface
    * Added unconfigure_gdoi_group_on_gm  API
        * API for unconfiguring gdoi group on group member device
    * Added unconfigure_crypto_map_on_interface API
        * API for unconfiguring crypto map on interface
    * Added unconfigure_crypto_map_for_gdoi  API
        * API for unconfiguring crypto map for gdoi protocol
    * Added hw_module_beacon_slot_on_off API
        * On/Off hw-module beacon on device
    * Added stack_ports_enable_disable API
        * Enable/Disable stack-port on device
    * Added configure_interface_tunnel_key API
        * Configure tunnel key on a tunnel interface on device
    * Added unconfigure_interface_tunnel_key API
        * Unconfigure tunnel key on a tunnel interface on device
    * Added clear_access_session_mac API
        * Added clear_access_session_mac API
    * Added configure_aaa_authentication_enable
        * API for "aaa authentication enable default {group} {group_name} {group_action="enable"}""
    * Added unconfigure_aaa_authentication_enable
        * API for unconfigure "aaa authentication enable default" configuration on device
    * Added configure_aaa_authorization_commands
        * API for configure "aaa authorization commands {level=15} {level_name="default"} {level_action="none"}" configuration on device
    * Added unconfigure_aaa_authorization_commands
        * API for unconfigure configure 'aaa authorization commands {level=15} {level_name="default"} {level_action="none"}'configuration on interface
    * Added configure_aaa_accounting_commands
        * API for configure 'aaa accounting commands {level=15} {level_name="default"} {level_action="none"}' configuration on interface
    * Added unconfigure_aaa_accounting_commands
        * API for onfigure 'aaa accounting commands {level=15} {level_name="default"} {level_action="none"}' configuration on device
    * Added unconfigure_tacacs_server
        * API for unconfigure unconfigure tacacs server configuration on interface
    * Added unconfigure_tacacs_group
        * API for unconfigure unconfigure aaa tacacs server group configuration on device
    * Added execute_format
        * Api for format the file_system

* iosxr/ncs540
    * Added new api get_software_version.
    * Added new api verify_current_image.

* added create_dir_file_system
    * Api for creating new dir in file system

* added rename_dir_file_system
    * Api for renaming the dir or file name in file system


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* common
    * Added support for raritan type powercycler with connection type telnet.
        * add a proc for raritan in base.py and powercyclers.py.

* blitz
    * Returns with non string datatype.
    * If values don't match
    * Fix for Rpc Verify for xpaths having no data

* iosxe
    * Modified config_ip_on_interface API
        * Modified config_ip_on_interface to allow for ip address dhcp hostname to be configured
    * Modified TriggerShutNoShutLoopbackInterface trigger
        * updated requirement to check for unnumbered IPv4
    * Modified verify_ip_mroute_group_and_sourceip api
        * Added code to handle list for outgoing interface
    * Modified unconfigure_fnf_monitor_on_interface API
        * Made sampler name optional
    * Modified configure_snmp_server_trap API
        * API modified to configure all traps and specific trap_type without hostname , username, interface and version.
    * Modified unconfigure_snmp_server_trap API
        * API modified to unconfigure all traps and specific trap_type without hostname , username, interface and version.

* yang
    * Fix for false passes on GNMI subscribe failures


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified execute_install_one_shot API
        * API for install one shot to handle negative test


