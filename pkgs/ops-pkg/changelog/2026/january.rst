--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_execute_set_memory_debug_incremental_starting_time
        * test_api_clear_cts_counters_ipv4
        * test_api_clear_cts_counters_ipv6
        * test_api_configure_cts_aaa_methods
        * test_api_configure_interface_cts_role_based_sgt_map
        * test_api_debug_platform_software_fed_switch_active_punt_packet_capture
        * test_api_debug_software_cpm_switch_pcap
        * test_api_debug_vdsl_controller_slot_dump_internal
        * test_api_disable_debug
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_cdp
        * test_api_unconfigure_cdp_holdtime
        * test_api_enable_cpp_system_default_on_device
        * test_api_execute_clear_control_plane
        * test_api_configure_device_sensor_filter_list_lldp
        * test_api_configure_hw_module_switch_number_usbflash
        * test_api_configure_service_private_config_encryption
        * test_api_cry_key_generate_rsa_encryption
        * test_api_hw_module_switch_num_usbflash_security_password
        * test_api_snmp_server_engine_id_local
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * cat9k/c9500/rev1/platform.py
        * Fix KeyError when merging standby RP redundancy data during platform learning

* iosxr
    * Modified Platform
        * Added full_slot to platform ops model


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* platform/nxos/rev2/platform.py
    * Added Rev2 platform support for transceiver slot parsing, Fan, and fixed logic for rp and lc


