--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* updated api unit tests
    * IOSXE
        * Updated the following API unit tests with the latest unit testing methodology
            * configure_aaa_accounting_connection_default_start_stop_group_tacacs_group
            * configure_aaa_accounting_identity_default_start_stop_group
            * configure_aaa_accounting_system_default_start_stop_group_tacacs_group
            * configure_aaa_authentication_enable_default_group_enable
            * configure_aaa_authentication_login_default_group_local
    * IOSXE
        * Updated unittests to new testing method
            * configure_mac_acl
            * configure_scale_ipv6_accesslist_config
            * configure_standard_acl
            * configure_type_access_list_action
            * delete_configure_ip_acl
            * delete_configure_ipv6_acl
            * delete_mac_acl
            * remove_acl_from_interface
            * unconfig_extended_acl_with_evaluate
            * unconfig_extended_acl_with_reflect
            * unconfig_ip_tcp_mss
            * unconfig_refacl_global_timeout
        * Removed the mock yaml under 'unconfigure_access_list_deny' as we do not have any API for it.
    * IOSXE
        * Updated the following API unit tests with the latest unit testing methodology
            * configure_SVI_Autostate
            * configure_SVI_Unnumbered
            * unconfigure_static_ip_route_all
            * configure_aaa_accounting_connection_default_start_stop_group_tacacs_group
            * configure_boot_manual
    * IOSXE
        * Updated the following API unit tests with the latest unit testing methodology
            * configure_radius_attribute_policy_name_globally
            * configure_radius_attribute_policy_name_under_server
            * configure_radius_interface
            * unconfigure_aaa_accounting_dot1x_default_start_stop_group
        * unconfigure_aaa_accounting_network_default_start_stop_group
    * IOSXE
        * Updated the following API unit tests with the latest unit testing methodology
            * configure_aaa_accounting_connection_default_start_stop_group_tacacs_group
            * configure_aaa_authorization_config_commands
            * configure_aaa_authorization_exec_default_group_if_authenticated
            * configure_aaa_authorization_network_default_group
            * configure_mab_eap_on_switchport_mode_access_interface
    * IOSXE
        * Updated unittests to new testing method
            * configure_as_path_acl
            * configure_extended_acl
            * configure_filter_vlan_list
            * configure_interface_ipv6_acl
        * Removed the mock yaml under 'configure_extended_acl_deny' as we do not have any API for it.

* cleaning api ut's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
            * configure_ipv6_subnet_to_sgt_mapping
            * configure_ipv6_to_sgt_mapping
            * configure_sap_pmk_on_cts
            * disable_cts_enforcement_vlan_list
            * enable_cts_enforcement_vlan_list
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
            * remove_default_ipv6_sgacl
            * unconfigure_cts_aaa_methods
            * unconfigure_cts_enforcement_interface
            * unconfigure_cts_enforcement_logging
            * unconfigure_cts_manual
            * unconfigure_cts_role_based_monitor
            * unconfigure_cts_role_based_permission
            * unconfigure_cts_role_based_permission_default
            * unconfigure_host_ip_to_sgt_mapping
            * unconfigure_interface_cts_role_based_sgt_map
            * unconfigure_ip_role_based_acl
            * unconfigure_ip_role_based_acl
            * unconfigure_ip_subnet_to_sgt_mapping_vrf
            * unconfigure_ip_to_sgt_mapping_vrf
            * unconfigure_ipv6_subnet_to_sgt_mapping
    * Iosxe
        * ACL
            * Updated with latest UT mathod to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's

* iosxe/rommon
    * Utils
        * update the send break boot to handle login creds

* updated unittests
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * configure_router_bgp_synchronization
            * unconfigure_bgp_auto_summary
            * unconfigure_bgp_log_neighbor_changes
            * unconfigure_bgp_redistribute_internal
            * unconfigure_bgp_redistribute_static
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * unconfigure_redestribute_ospf_metric_in_bgp
            * unconfigure_router_bgp_maximum_paths
            * unconfigure_router_bgp_network_mask
            * unconfigure_router_bgp_synchronization
            * configure_datalink_flow_monitor
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * unconfigure_datalink_flow_monitor
            * unconfigure_mac_address_table_notification_change
            * enable_http_server
            * set_clock_calendar
            * configure_call_home_alert_group

* iosxe
    * Modified verify_pattern_in_show_logging
        * Modified the API to search pattern from entire show logging output.
    * Added Support for Destination username pattern for copy_file_with_scp
    * Modified configure_route_map_permit to add vrf argument
        * Added Vrf for set vrf clause
    * Modified API unconfigure_ipv6_pim_bsr_candidate_rp
        * Added support for priority in the unconfiguration command.
        * Included CLI commands
    * Modified API `unconfigure_ipv6_pim_bsr_candidate_bsr`
        * Added support for `priority` in the unconfiguration command.
        * Included CLI commands
            * `no ipv6 pim bsr candidate bsr 20002 priority 254`
            * `no ipv6 pim bsr candidate bsr 20001`
            * `no ipv6 pim bsr candidate bsr 30001`
    * Modified configure_tacacs_server
        * Modified the API to use hostname instead of IP address as host for tacacs server configuration
        * Added support for TLS (Transport Layer Security) configuration options
            * TLS port number
            * TLS idle timeout
            * TLS connection timeout
            * TLS retries
            * TLS client and server trustpoints
            * IPv4 and IPv6 source interfaces for TLS
            * IPv4 and IPv6 VRF forwarding for TLS
            * TLS server identity matching for DNS-ID, IP address, and SRV-ID

* sdk-pkg
    * rommon/util
        * Added prompt recovery to support the state transition.

* linux
    * Modified scp API in linux
        * Handled first-time SSH connection prompt
        * Added support for 'Are you sure you want to continue connecting' dialog

* wsim
    * sdk-pkg
        * Removed execute and added sendline/expect because vsta_app would


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added unconfigure_flow_exporter_from_monitor
        * API for unconfigure_flow_exporter_from_monitor
    * Added configure_spanning_tree_extend_system_id
        * API to configure spanning-tree extend system id
    * Added API execute_diagnostic_start_module_port
        * Added API to execute_diagnostic_start_module_port
    * Added configure_app_hosting_docker_with_run_opts
        * API to configure app hosting docker with run opts
    * Added verify_backplane_optical_port_interface_config_media_type
        * API to verify backplane/optical port on 10G interface.
    * Added configure_app_hosting_docker
        * API to configure app hosting docker
    * Added API default_policy_map to deafult a policy-map on the device
    * ie3k
        * Added new api execute_copy_verify
    * Added configure_logging_host_ipv6
        * API to configure logging host ipv6
        * API to unconfigure logging host ipv6
    * Added configure_rep_preempt_and_block
        * API to configure rep preempt and block
    * Added API configure_file_verify_auto
        * API to configure file verify auto
    * Added API unconfigure_file_verify_auto
        * API to unconfigure file verify auto
    * Added ip pim send-rp-announce Loopback0 scope 10
    * Added configure_app_hosting_custom_profile
        * API to configure app hosting custom profile
    * Added API configure_sd
        * API to configure sdflash
    * Added API unconfigure_sd
        * API to unconfigure sdflash
    * Added API get_logging_message_time
        * Added API to get_logging_message_time
    * Added configure_app_hosting_vlan
        * API to configure app hosting vlan
    * Added configure_app_hosting
        * API to configure app hosting
    * Added enable_app_hosting_verification
        * API to enable app hosting verification
    * Added API default_attribute_service_map
        * API to default parameter-map type on the device
    * Added  API configure_ipv6_logging_with_discriminator
        * API to Configure IPv6 logging with discriminator on the device.
    * Added API configure_ipv6_pim_on_interface

* api
    * NXOS
        * Added breakout_interface_names

* iosxe/c9200cx
    * Added configure_management_ip
        * New API to configure management IP

* nxos
    * Added
        * verify_ping API that validates Ping at given device to given address


* * iosxe
    * cat9k
        * c9500
            * C9500-24Y4C
                * Inherited API's to configure and unconfigure the ignore startup config

* iosxe
    * ie3k
        * configure
            * Added 'configure and unconfigure ignore startup config' API under ie3k platform
        * Verify
            * Added 'verify_current_image' and 'verify_ignore_startup_config' Api's

