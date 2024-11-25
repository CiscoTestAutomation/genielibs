--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API execute_test_sfp_port_lpn_fake_insert
        * Added API to execute_test_sfp_port_lpn_fake_insert
    * Added API execute_test_sfp_port_lpn_fake_remove
    * Added API platform_hardware_fed_switch_phy_debug
        * Added API to platform_hardware_fed_switch_phy_debug
    * Added API debug_software_cpm_switch_pcap
        * Added API to enable disable software cpm switch
    * Added API's to configure cli commands for policy-map.
        * API to configure_policy_map_with_police_cir_percentage
        * API to configure_policy_map_parameters
    * Added API's to configure cli commands for speed auto.
        * API for configure_interface_speed_auto
    * Added execute_diagnostic_start_switch_port
        * API to execute_diagnostic_start_switch_port
    * Added execute_test_platform_hardware_cman
        * API to execute_test_platform_hardware_cman
    * Added request_platform_hardware_pfu
        * API to request_platform_hardware_pfu
    * Added remove_default_ipv6_sgacl
        * API to clear default IPv6 SGACL
    * Added API request_platform_software_trace_rotate_all
        * Added request_platform_software_trace_rotate_all api
    * Added set_platform_soft_trace_ptp_debug
        * added api for set platform software trace fed active ptp_proto debug
    * Added unconfigure_parameter_map_subscriber
        * API to unconfigure "parameter-map type subscriber attribute-to-service {parameter_map_name}"
    * Added unconfigure_policy_map_set_cos_cos_table
        * New API to unconfigure policy map set cos cos table

* added api to execute_test_sfp_port_lpn_fake_remove


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* api utils
    * Modified api_unittest_generator
        * Refactored code to streamline `configure` and `execute` API unit tests
        * Removed dependency on mock data yaml files for `configure` and `execute` API unit tests

* iosxe
    * health cpu api
        * Update the API to handle the scenario when the parser dont has the key
    * Modified verify_ignore_startup_config
        * fixed next_config_register Key Error
    * Health
        * Update the health cpu to include `show processes cpu platform` command
    * Modified configure_masked_unmasked_credentials
        * Added parameter view
    * Modified
        * Updated execute_install_one_shot to use reload service instead of execute
    * Recovery
        * Modified send_break_boot to send context with username, password and enable_password

* sdk-pkg
    * Update load_image api in utils.py


