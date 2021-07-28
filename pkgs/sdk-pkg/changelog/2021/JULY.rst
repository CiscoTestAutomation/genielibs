--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* nxos
    * Added TriggerProcessCliRestartNgmvpn
        * added 'cli restart of ngmvpn'
    * Added TriggerProcessCrashRestartNgmvpn
        * added 'crash process of ngmvpn'
    * Added TriggerProcessKillRestartNgmvpn
        * added 'kill process of ngmvpn'

* iosxe
    * Added the following APIs
        * unconfigure_interface_monitor_session
        * remove_channel_group_from_interface
        * remove_port_channel_interface
        * config_edge_trunk_on_interface
        * config_wan_macsec_on_interface
        * config_macsec_replay_protection_window_size
        * config_macsec_keychain_on_device
        * config_mka_keychain_on_interface
        * config_macsec_network_link_on_interface
        * unconfig_macsec_network_link_on_interface
        * config_mka_policy_xpn
        * clear_macsec_counters
        * config_mpls_ldp_on_device
        * remove_mpls_ldp_from_device
        * config_mpls_lable_protocol
        * remove_mpls_lable_protocol_from_device
        * config_mpls_ldp_router_id_on_device
        * remove_mpls_ldp_router_id_from_device
        * config_mpls_ldp_explicit_on_device
        * remove_mpls_ldp_explicit_from_device
        * config_speed_nonego_on_interface
        * config_encapsulation_on_interface
        * config_xconnect_on_interface
        * configure_service_internal
        * configure_ospf_routing
        * configure_ospf_routing_on_interface
        * unconfigure_ospf_on_device
        * configure_ospf_message_digest_key
        * configure_ospf_network_point
        * configure_ospf_bfd
        * configure_ospfv3
        * unconfigure_ospfv3
        * enable_ip_routing
        * enable_ipv6_unicast_routing
        * disable_ip_routing
        * set_system_mtu
        * disable_keepalive_on_interface
        * config_vlan
        * configure_mpls_ldp_nsr
        * configure_mpls_ldp_graceful_restart
        * configure_pseudowire_encapsulation_mpls
        * configure_mpls_pseudowire_xconnect_on_interface
        * unconfigure_mpls_ldp_nsr
        * unconfigure_mpls_ldp_graceful_restart
        * unconfigure_pseudowire_encapsulation_mpls
        * unconfig_macsec_keychain_on_device
        * unconfig_mka_policy_xpn
        * verify_device_tracking_policy_configuration
        * verify_missing_device_tracking_policy_configuration
        * verify_ipv6_nd_raguard_policy
        * verify_ipv6_nd_raguard_configuration
        * verify_missing_ipv6_nd_raguard_configuration
        * verify_ipv6_source_guard_policy
        * verify_ipv6_source_guard_configuration
        * verify_missing_ipv6_source_guard_configuration
        * verify_device_tracking_counters_vlan_dropped
        * verify_device_tracking_counters_vlan_faults
        * get_device_tracking_policy_name_configurations
        * get_device_tracking_database_details_binding_table_configurations
        * get_device_tracking_database_details_binding_table_count
        * get_ipv6_nd_raguard_policy_configurations
        * get_ipv6_source_guard_policy_configurations
        * get_device_tracking_counters_vlan_message_type
        * get_device_tracking_counters_vlan_faults
        * config_device_tracking_policy
        * unconfig_device_tracking_policy
        * config_ipv6_nd_raguard_policy
        * unconfig_ipv6_nd_raguard_policy
        * config_ipv6_source_guard_policy
        * unconfig_ipv6_source_guard_policy
        * device_tracking_attach_policy
        * device_tracking_detach_policy
        * ipv6_nd_raguard_attach_policy
        * ipv6_nd_raguard_detach_policy
        * ipv6_source_guard_attach_policy
        * ipv6_source_guard_detach_policy
        * enable_service_internal
        * disable_service_internal
        * device_tracking_unit_test
        * configure_ipv6_dhcp_guard_policy
        * unconfigure_ipv6_dhcp_guard_policy
        * configure_ipv6_nd_suppress_policy
        * unconfigure_ipv6_nd_suppress_policy
        * configure_ip_dhcp_snooping
        * unconfigure_ip_dhcp_snooping
        * configure_device_tracking_upgrade_cli
        * attach_ipv6_dhcp_guard_policy
        * detach_ipv6_dhcp_guard_policy
        * attach_ipv6_nd_suppress_policy
        * detach_ipv6_nd_suppress_policy

* subsection
    * Added  include_os, exclude_os, include_devices, exclude_devices and all for configure_replace.

--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* blitz
    * Updated 'include'/'exclude' with Dq reason message
    * Updated decorator for pyATS Health Check
        * Support '--health-notify-webex' argument
    * gNMI empty datatype value not verifying correctly.
    * Added several tests for all gNMI reponse verification.
    * Updated 'check_opfield' API.
        * Avoided adding double quotes if value is already enclosed with quotes.

* sdk
    * updated copy_from_device and copy_to_device APIs to use http authentication

* utils
    * Updated 'get_testcase_name' API
        * Added `escape_regex_chars` argument to return escaped regex chars in testcase name
    * Updated 'copy_from_device' API
        * changed return value for API to str/None from boolean
    * Updated 'copy_to_device' API
        * changed return value for API to str/None from boolean

* iosxe
    * Modified the following APIs
        * configure_interface_monitor_session - Added description,source_vlan,mtu and vrf to config.
        * config_mpls_ldp_on_interface - Added named arguments to log and config.
        * remove_mpls_ldp_from_interface - Added named arguments to log and config.
    * Updated 'health_core' API
        * To support HTTP transfer via proxy support
    * updated 'pkgs/sdk-pkg/src/genie/libs/sdk/apis/iosxe/dhcp/configure.py'
        * changed 'def disable_dhcp_snooping_Option_82(device)' to lowercase
    * updated 'pkgs/sdk-pkg/src/genie/libs/sdk/apis/iosxe/interface/configure.py'
        * changed 'def config_helper_ip_on_interface' name
    * Modified 'health_cpu' API
        * Added 'add_total' argument to add total of CPU load
    * Modified 'health_memory' API
        * Added 'add_total' argument to add total of Memory usage

* iosxr
    * Modified get_available_space and get_total_space
        * Update get_available_space and get_total_space to return an int like other platforms do
    * Updated 'health_core' API
        * To support HTTP transfer via proxy support
    * Modified 'health_cpu' API
        * Added 'add_total' argument to add total of CPU load
    * Modified 'health_memory' API
        * Added 'add_total' argument to add total of Memory usage

* nxos
    * Updated 'health_core' API
        * To support HTTP transfer via proxy support
    * Modified 'health_cpu' API
        * Added 'add_total' argument to add total of CPU load
    * Modified 'health_memory' API
        * Added 'add_total' argument to add total of Memory usage

* iosxe/iosxr/nxos/aci
    * Delete file after get_show_tech API copied the file successfully
