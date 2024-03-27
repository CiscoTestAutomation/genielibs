--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added
        * Added support for <processor_slot> in <request platform software system shell> command.
    * Added upgrade_rom_monitor_capsule_golden
        * upgrade rom-monitor capsule golden switch active R0
    * Added new API `get_cpu_instant_interval` to extract CPU utilization instant and CPU utilization interval.
    * Added new API `get_cpu_min_max_avg` to extract minimum, maximum, and average CPU utilization values.
    * Added API configure_l2_traceroute
        * Added API to configure l2 traceroute
    * Added API unconfigure_l2_traceroute
        * Added API to unconfigure l2 traceroute
    * Added unconfigure_record_configs_from_flow_monitor
        * Added API to unconfigure_record_configs_from_flow_monitor
    * Added unconfigure_flow_exporter
        * Added API to unconfigure_flow_exporter
    * Added new api 'execute_test_cable_diagnostics_tdr_interface'
        * Executes 'test cable disgnostics tdr interface'
    * Added `get_port_speed_info` to retrieve port_speed status for repective interfaces.
    * Added get_interfaces_transceiver_supported_dom API
        * Added API to get the DOM type for the given transceivers list
    * Added new api `verify_last_reload_reason` to verify the Last Reload reason.
    * Added unconfigure_spanning_tree_portfast_on_interface
        * added api to unconfigure_spanning_tree_portfast_on_interface
    * Added new api `get_mac_table_entries` to generate MAC table entries with VLAN, MAC address, interfaces, and their associated VRFs.
    * Added `get_platform_memory_status` to generate VLAN information with VLAN ID, VLAN name, VLAN state and its associated VRFs.
    * Added `get_boot_time` to retrieve boot_time in timeticks format.
    * Added configure_smartpower_interface_level
        * API to configure SmartPower interface level
    * Added unconfigure_smartpower_interface_level
        * API to unconfigure SmartPower interface level
    * Added configure_smartpower_interface_name
        * API to configure SmartPower interface name
    * Added unconfigure_smartpower_interface_name
        * API to unconfigure SmartPower interface name
    * Added configure_smartpower_interface_role
        * API to configure SmartPower interface role
    * Added unconfigure_smartpower_interface_role
        * API to unconfigure SmartPower interface role
    * Added configure_smartpower_interface_domain_default
        * API to configure SmartPower default interface domain

* nxos
    * Added get_standby_supervisor_slot
        * New API to get standby supervisor slot number
    * Added get_active_supervisor_slot
        * New API to get acive supervisor slot number
    * Added get_slots_by_state
        * New API to get list of all the slot/module match the given status
    * Added get_fm_slots
        * New API to get list of FM(Fabric Modules) which match the given status
    * Added get_lc_slots
        * New API to get list of LC(Linecard Modules) which match the given status
    * Added get_current_boot_image
        * New API to get current boot image name
    * Added get_next_reload_boot_image
        * New API to get next reload boot image name


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* blitz
    * Modified verifiers_find_xpath
        * Decoded response Xpath can contain integers as keys, so cast all keys as strings.
    * Modified gnmi_util.GnmiMessage.process_update
        * Decoded response had an extra dict from jsonVal, so corrected logic.

* iosxe
    * Modified config_identity_ibns
        * Modified the api to config_identity_ibns


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_fnf_flow_record
        * Modified API to configure collect configs
    * Modified configure_flow_record_match_datalink
        * Modified API to configure match datalink vlan and ethertypes
    * Modified configure_flow_exporter
        * Modified API to configure export-protocol


