--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added enable_cts_enforcement_vlan_list
        * API to configure enable cts role-based enforcement on given vlan range
    * Added configure_default_spanning_tree
        * API to configure default spanning-tree
    * Added configure_access_session_mac_move
        * API to configure access-session mac-move
    * Added unconfigure_access_session_mac_move
        * API to unconfigure access-session mac-move
    * Added hw_module_beacon_RP_active_standby
        * API to configure hw module beacon RP {supervisor} {operation}.
    * Added confirm_iox_enabled_requested_storage_media
        * API to configure iox enabled requested storage media
    * Added set_stack_mode
        * API to set-stack mode
    * Added clear_pdm_steering_policy
        * API for clear pdm steering policy
    * Added configure_interface_bandwidth
        * New API to configure bandwidth on interface
    * Added unconfigure_interface_bandwidth
        * New API to unconfigure bandwidth on interface
    * Added API's to configure cli commands under gkm group.
        * API to configure_gikev2_profile_under_gkm_group
        * API to configure_client_protocol_under_gkm_group
        * API to configure_gkm_group_identity_number
        * API to configure_rekey_under_gkm_group
        * API to configure_ipsec_under_gkm_group
        * API to configure_server_redundancy_under_gkm_group
        * API to configure_protocol_version_optimize_cli_under_gkm_group
        * API to configure_ip_for_server_local_under_gkm_group
        * API to configure_ipv4_server_under_gkm_group
        * API to configure_pfs_enable_or_disable_under_gkm_group
    * Added configure_interface_no_switchport_voice_vlan
        * API to configure interface no switchport voice vlan
    * Added configure_global_interface_template_sticky
        * API to configure global interface template sticky
    * Added configure_mdt_default
        * API to configure mdt default
    * Added configure_mdt_auto_discovery_inter_as_mdt_type
        * API to configure mdt auto discovery inter as mdt type
    * Added configure_template_pseudowire
        * API to configure template pseudowire
    * Added configure_mpls_ldp_sync_under_ospf
        * API to configure mpls ldp sync under ospf
    * Added configure_member_vfi_on_vlan_configuration
        * API to configure member vfi on vlan configuration
    * Added clear_ip_arp
        * API to clear ip arp
    * Added configure_graceful_reload
        * API to configure graceful reload
    * Added api execute_dir_file_system
        * API to show files present in the filesystem or the subdirectory of the filesystem
    * Added upgrade_hw_module_subslot_sfp cli
        * API to upgrade hw-module_subslot <slot number> sfp <sfp number> <Image path>
    * Added configure_fnf_flow_record
        * API for configure_fnf_flow_record
    * Added `unconfigure_route_map_route_map_to_bgp_neighbor` API
        * Added unconfigure API corresponding to `configure_route_map_route_map_to_bgp_neighbor`
    * Added `unconfigure_bgp_redistribute_static` API

* sdk
    * Version pinned pysnmp and pyasn1 to fix the type error in execute_power_cycle_device api


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified reset_interface
        * added return statement
    * Modified configure_flow_exporter
        * Added if condition to configure source {source_int} on flow exporter
    * Fix vrf syntax for `configure_management_routes` API
    * Modified configure_service_policy_with_queueing_name
        * added return statement to return the output
    * Modified unconfigure_table_map
        * renamed "unconfigure_table_map" api to "unconfigure_table_map_values" due to duplicate api name
    * Modified configure_table_map
        * renamed "configure_table_map" api to "configure_table_map_values" due to duplicate api name
    * Added unconfigure_400g_mode_for_port_group_onsvl api
        * API to unconfigure 400g mode for port group svl
    * Added configure_400g_mode_for_port_group_onsvl api
        * API to configure 400g mode for port group svl
    * Modified `configure_route_map_route_map_to_bgp_neighbor` API
        * Refactored to remove and optimize redundant codes
    * Modified `configure_bgp_redistribute_static` API
        * Added `route_map` to pass route-map to redistribute static command
    * Modified `configure_route_map` API
        * Added `set_extcommunity` to set extcommunity in route-map
    * Modified `unconfigure_route_map` API
        * Changed `permit` to Optional argument to delete whole route-map
    * Modified `restore_running_configuration` API
        * Added condition to avoid the case which Unicon capture prompt

* blitz
    * Fixed gnmi auto-validation, caused by modifying orginal rpcdata object in GnmiMessageConstructor


