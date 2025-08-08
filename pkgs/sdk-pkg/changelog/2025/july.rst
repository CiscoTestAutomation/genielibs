--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe/cat9k
    * c9500x
        * Added execute_install_one_shot
            * API to execute_install_one_shot
    * c9610
        * Added configure_hw_module_switch_slot_shutdown
            * API to configure hw-module switch {switch_num} slot {slot} shutdown, hw-module switch {switch_num} subslot {subslot} shutdown.
        * Added unconfigure_hw_module_switch_slot_shutdown
            * API to unconfigure hw-module switch {switch_num} slot {slot} shutdown, hw-module switch {switch_num} subslot {subslot} shutdown.

* iosxe
    * Added API to  clear_vlan
        * API to execute clear vlan
    * Added execute_clear_zone_pair
        * API to execute clear zone-pair {subcommand}
    * Added new api configure_default_cdp_timer
    * Added configure_loopdetect
        * New API to configure loopdetect
    * Added unconfigure_loopdetect
        * New API to unconfigure loopdetect
    * Added execute_monitor_capture_match_any_interface_both
    * Added execute_show_monitor_capture_buffer_brief
    * Added execute_show_platform_hardware_qfp_active_feature_alg_statistics_sip_l7_data_clear
        * New API to execute show platform hardware qfp active feature alg statistics sip l7data clear
    * pki
        * execute_monitor_event_trace_crypto_pki
    * Added API unconfigure_flow_record_from_monitor
        * API to unconfigure_flow_record_from_monitor.
    * Added configure_flow_record_with_match
        * API to Configures Flow record with match values on Device
    * Added configure_flow_record_with_collect
        * API to Configures Flow record with collect values on Device
    * pki
        * Added remove_pki_certificate_chain
    * Added configure_remote_span_monitor_session
        * API to configure_remote_span_monitor_session
    * Added API execute_diagnostic_start_module_port
        * Added API to execute_diagnostic_start_module_port
    * pki
        * Added configure_trustpool_clean
        * Added unconfigure_trustpool_clean
    * Added API get_show_flow_monitor_cache_format_table_output
        * API to get_show_flow_monitor_cache_format_table_output.
    * Added API configure_Usb
        * API to enable usb
    * Added API unconfigure_Usb
        * API to disable usb
    * Added configure_controller_vdsl
        * Added configure_controller_vdsl to configure controller vdsl
    * Added API to configure facility alarm power-supply disable
    * Added API to unconfigure facility alarm power-supply disable
    * Added API to configure facility alarm power-supply notify
    * Added API to unconfigure facility alarm power-supply notify
    * Added API to configure facility alarm power-supply relay
    * Added API to unconfigure facility alarm power-supply relay
    * Added API to configure facility alarm power-supply syslog
    * Added API to unconfigure facility alarm power-supply syslog
    * IE3k
        * Added API to configure facility alarm sdcard enable
        * Added API to unconfigure facility alarm sdcard enable
        * Added API to configure facility alarm sdcard notify
        * Added API to unconfigure facility alarm sdcard notify
        * Added API to configure facility alarm sdcard relay
        * Added API to unconfigure facility alarm sdcard relay
        * Added API to configure facility alarm sdcard syslog
        * Added API to unconfigure facility alarm sdcard syslog
    * ie3k
        * Added new api configure_power_supply_dual
        * Added new api unconfigure_power_supply_dual
    * Added API simulate_partition_sdflash
        * API to simulate partition of sdflash
    * Added API simulate_format_sdflash
        * API to simulate format of sdflash

* sdk/iosxe
    * rommon/configure
        * Added the ability to specify an image path that takes precedence over device clean image

* iosxe/platform
    * Added execute_rommon_reset api

* iosxe/asr1k
    * Added execute_set_config_register api
    * Added execute_rommon_reset api

* iosxe/isr4k
    * Added execute_set_config_register api
    * Added execute_rommon_reset api
    * configure
        * Added new apis configure_autoboot and configure_boot_manual.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* cleaning api ut's
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
            * configure_ip_role_based_acl
            * configure_ip_subnet_to_sgt_mapping_vrf
            * configure_ip_to_sgt_mapping_vrf
            * cts_refresh_environment_data
            * cts_refresh_pac
            * cts_refresh_policy
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
            * configure_label_mode_all_explicit_null
            * configure_ospf_internal_external_routes_into_bgp
            * configure_ospf_redistribute_in_bgp
            * configure_redestribute_ospf_metric_in_bgp
            * configure_redistribute_connected
            * configure_route_map_route_map_to_bgp_neighbor
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
            * configure_cts_enforcement_interface
            * configure_cts_enforcement_logging
            * configure_cts_role_based_monitor
            * configure_cts_role_based_permission
            * configure_cts_role_based_permission_default
            * configure_host_ip_to_sgt_mapping
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
            * configure_sdm_prefer
            * configure_sdm_prefer_core
            * configure_sdm_prefer_custom_fib
            * configure_sdm_prefer_custom_template
            * debug_platform_memory_fed_backtrace
            * debug_platform_memory_fed_callsite
            * debug_platform_software_fed_drop_capture
            * debug_platform_software_fed_drop_capture_action
            * debug_platform_software_fed_drop_capture_buffer

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * configure_router_bgp_maximum_paths
            * configure_router_bgp_neighbor_ebgp_multihop
            * configure_router_bgp_neighbor_remote_as
    * IOSXE
        * Updated unittests to new testing method
            * configure_avb
            * unconfigure_avb
            * configure_bfd_neighbor_on_interface
            * disable_bfd_on_isis_ipv6_address
            * enable_bfd_on_isis_ipv6_address
            * unconfigure_bfd_neighbor_on_interface
            * unconfigure_bfd_on_interface
            * unconfigure_bfd_value_on_interface

* iosxe
    * policy map priority express api
        * modified the api logic to get the percent key value from the correct level of the parsed output.
        * added the percent key value to the api output.
        * modified the api to get the kbps value from the correct level of the parsed output.
        * added the kbps key value to the api output.
    * Api Health CPU
        * modfied the api logic to get the five_sec_cpu key value from the correct level of the parsed output.
    * Modified config_extended_acl
        * Added a logging statement for ACLs
    * Modified configure_ip_acl
        * Added a logging statement for ACLs
    * Modified configure_ip_acl_with_any
        * Added a logging statement for ACLs
    * Modified configure_ipv4_ogacl_src_dst_nw
        * Added a logging statement for ACLs
        * Added a port type and port number arguments
    * Added configure_generic_command
        * Added a new UT method to configure generic commands
    * Updated with latest UT method to all of the below mentioned API UT's
        * config_extended_acl
        * configure_ip_acl
        * configure_ip_acl_with_any
        * configure_ipv4_ogacl_src_dst_nw
    * Modified Acmsave
        * Added a dialog statement for overwrite
    * Modified perform_telnet API
        * Handled Telnet authentication failure scenarios
        * Ensured False is returned when prompt is not reached, authentication fails or login fails
    * Modified perform_ssh API
        * Handled ssh authentication failure scenarios
        * Ensured False is returned when prompt is not reached, authentication fails or login fails
    * Modified
        * Updated configure_span_monitor_session API with optional argument vlan id to configure the vlan monitor session as source.

* sdk-pkg
    * moved the proxy disconnect to execute api

* sdk
    * Blitz
        * Yang
            * Added option to run gNMI subscribe in async mode

* sdk/iosxe
    * management/configure
        * Update configure_management_credentials api to remove enable secret and re-configure the password

* utils
    * copy to device
        * Fixed server block resolution to strictly match protocol and address in copy_to_device.

* iosxe/rommon/utils
    * Updated device_rommon_boot api to handle boot from rommon for stack devices.
    * Updated device_rommon_boot api to execute config register and reset command.
    * Updated device_rommon_boot api to handle grub prompts.

* iosxe/platform
    * Updated execute_set_config_register api

* iosxe/cat9k
    * Updated unconfigure_ignore_startup_config

* os/iosxe/cat9k/c9300/configure
    * update configure_ignore_startup_config and unconfigure_ignore_startup_config api to handle dual rp and stack devices

* os/iosxe/cat9k/c9500/configure
    * update configure_ignore_startup_config and unconfigure_ignore_startup_config api to handle dual rp and stack devices

* os/iosxe/rommon
    * update configure_rommon_tftp_ha to use image handler to update TFTP_FILE


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Modify verfify_iox_enabled
        * Modified api to check list of services in 'running' state to check iox enabled in device .


