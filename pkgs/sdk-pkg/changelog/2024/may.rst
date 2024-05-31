--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added new API verify_dual_port_interface_media_type
        * Added new API to verify the media type of dual port interface.
    * Added verify_yang_management_process API
        * command show platform software yang-management process
    * Added verify_yang_management_process_state API
        * command show platform software yang-management process state
    * Added clear_configuration_lock API
        * command clear configuration lock
    * Added verify_is_syncing_done API
        * This is to validate the netconf way of sync status of a device!
    * Added `get_platform_fan_speed` to retrieve fan_speed of respective fan components under iosxe/cat9k/c9400
    * Added configure_cdp_run API
        * Added API for cdp run
    * Added unconfigure_cdp_run API
        * Added API for no cdp run
    * Added configure_diagnostic_monitor_module API
        * Added API for diagnostic monitor threshold module {mod_num} test {test_name} failure count {failure_count}
    * Added unconfigure_diagnostic_monitor_module API
        * Added API for no diagnostic monitor threshold module {mod_num} test {test_name} failure count {failure_count}
    * Added configure_diagnostic_schedule_module API
        * Added API for diagnostic schedule module {mod_num} test all
    * Added unconfigure_diagnostic_schedule_module API
        * Added API for no diagnostic schedule module {mod_num} test all
    * Added configure_diagnostic_monitor_interval_module API
        * Added API for diagnostic monitor interval module {mod_num} test {test_name} {time} {millisec} {days}
    * Added unconfigure_diagnostic_monitor_interval_module API
        * Added API for no diagnostic monitor interval module {mod_num} test {test_name} {time} {millisec} {days}
    * Added configure_hw_module_slot_upoe_plus API
        * Added API for hw-module slot {slot_num} upoe-plus
    * Added `get_platform_component_type_id_info` that retrieves name, type and id for platform components.
    * Added `get_platform_component_temp_info` to retrieve cname, temp_instant, temp_avg, temp_min, temp_max, temp_interval, alarm_status, alarm_threshold and alarm_severity.
    * Added API configure_dual_port_interface_media_type
        * Added API to configure dual port media type on interface
    * Added `get_platform_component_firmware_info` to retrieve name and firmware_version for their respective platform components.
    * Added configure_ecomode_optics
    * Added unconfigure_ecomode_optics
    * Added new API configure_interface_range_shutdown
        * Added new API to configure interface range shutdown.
    * Added new API configure_interface_range_no_shutdown
        * Added new API to configure interface range no shutdown.

* added unconfigure_hw_module_slot_upoe_plus api
    * Added API for no hw-module slot {slot_num} upoe-plus

* iosxe/rommon
    * Added `configure_rommon_tftp_ha` to configure rommon variables on HA device.
    * Renamed ipv6_address argument to use_ipv6 on `configure_rommon_tftp` api.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modify enable_ipv6_dhcp_server
        * Updated API to add dhcp server without pool name
    * Modify configure_radius_interface
        * Updated API to Support IPv4 and IPv6
    * Modify unconfigure_radius_interface
        * Updated API to Support IPv4 and IPv6
    * Fixed configure_smartpower_level
    * Fixed unconfigure_smartpower_level
    * Update show commands to use numeric

* nxos
    * Add use_kstack=True as default for NXOS copy APIs


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* cheetah
    * Added retries field
        * Added retries field to execute_archive_download to retry image downloads if fails first time


