--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_spanning_tree_bridge_assurance
        * API for configure spanning tree bridge assurance
    * Added unconfigure_spanning_tree_bridge_assurance
        * API for unconfigure spanning tree bridge assurance
    * Added configure_spanning_tree_portfast_bridge_assurance
        * API for configure spanning tree portfast bridge assurance
    * Added unconfigure_spanning_tree_portfast_bridge_assurance
        * API for unconfigure spanning tree portfast bridge assurance
    * Added configure_spanning_tree_portfast_bridge_assurance_on_interface
        * API for configure spanning tree portfast bridge assurance on interface
    * Added unconfigure_spanning_tree_portfast_bridge_assurance_on_interface
        * API for unconfigure spanning tree portfast bridge assurance on interface
    * Added configure_vlan_dot1q_tag_native
        * API to configure vlan dot1q tag native
    * Added unconfigure_vlan_dot1q_tag_native
        * API to unconfigure vlan dot1q tag native
    * Added configure_switchport_trunk_native_vlan_tag
        * API to configure switchport trunk native vlan tag
    * Added configure_auto_off_optics
        * Added configure_auto_off_optics
    * Added unconfigure_auto_off_optics
        * Added unconfigure_auto_off_optics
    * Added test_platform_software_fru_fake_insert_remove
        * New API to execute test platform software fed switch {switch_num} fru {action}
    * Added new API to not set config register value in IOT devices
        * This is done to avoid this setting in clean install of IOT devices.
    * Added configure_medium_p2p_interface
        * Configure medium p2p on interface
    * Added unconfigure_medium_p2p_interface
        * Unconfigure medium p2p on interface
    * Added configure_access_list_extend_with_dst_address_and_port
        * New API to configures access-list extend with destination address and ports on device
    * Added configure_access_list_extend_with_port
        * New API to configures access-list extend with port on device
    * Added configure_access_list_extend_with_dst_address_and_gt_port
        * New API to configures access-list extend with destination address and gt port on device
    * Added configure_access_list_extend_with_range_and_eq_port
        * New API to configures access-list extend with range and eq port on device
    * Added configure_access_list_extend
        * New API to configures access-list extend on device
    * Added configure_ipv6_address_on_hsrp_interface
        * Added configure_ipv6_address_on_hsrp_interface
    * Added configure_spanning_tree_portfast under c9610
        * New API to configures spanning-tree portfast under c9610
    * Added configure_fnf_flow_record_match_flow
        * added api to configure flow record match flow
    * Added configure_ip_sgacl
        * API for configure the ip agacl rules
    * Added unconfigure_ip_sgacl
        * API for unconfigure ip sgacl
    * Added clear_platform_qos_statistics_iif_id
        * added clear platform hardware qos statistics internal cpu policer API
    * Added monitor_capture_start_capture_filter
        * Execute monitor_capture_start_capture_filter
    * Added monitor_capture_file_location_flash
        * Execute monitor_capture_file_location_flash
    * Added monitor_capture_class_map
        * Execute monitor_capture_class_map
    * Added monitor_capture_clear
        * Execute monitor_capture_clear
    * Added unconfigure_aaa_accounting_dot1x_default_start_stop_group
        * New API to unconfigure "no aaa accounting dot1x default start-stop group {server_group_name}"

* added unconfigure_switchport_trunk_native_vlan_tag
    * API to unconfigure switchport trunk native vlan tag

* generic/nxos
    * Added configure_hostname
        * New API to configure hostname on device.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Fixed configure_hw_module_switch_number_auto_off_led
        * Changed ecomode to auto-off
    * Fixed unconfigure_hw_module_switch_number_auto_off_led
        * Changed ecomode to auto-off
    * Fixed configure_stack_power_auto_off
        * Changed ecomode to auto-off
    * Fixed unconfigure_stack_power_auto_off
        * Changed ecomode to auto-off
    * Fixed configure_default_stack_power_auto_off
        * Changed ecomode to auto-off
    * Modified API configure_ikev2_profile_pre_share
        * Added local_interface parameter
        * Added logic and command to execute if local_interface parameter is provided
    * Fixed configure_boot_level_licence
        * Added optional agruments advantage and essentials
    * Removed duplicate entry of configure_interface_monitor_session_shutdown_erspan_dest, configure_interface_monitor_session_mtu and configure_interface_monitor_session_no_mtu
    * Modified configure_management_vty_lines API
        * Added stackable check for configure_management_vty_lines API using stackable parameter
    * Fixed configure_ipv6_address_on_hsrp_interface
        * Changed version to groupnumber

* nxos
    * Removed duplicate TriggerAddRemoveBgpNetworkIPv4 trigger from trigger_datafile_nxos.yaml file
    * Removed duplicate iteration attribute under Verify_BgpIpMvpnRouteType_vrf_all_route_type_4 from verification_datafile_nxos.yaml file