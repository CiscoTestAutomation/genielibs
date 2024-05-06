--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_platform_acl_egress_dscp_enable
        * API for configure platform acl egress dscp enable
    * Added unconfigure_platform_acl_egress_dscp_enable
        * API for unconfigure platform acl egress dscp enable
    * Added API configure_fec_on_interface
        * Added API to configure_fec_on_interface
    * Added API unconfigure_fec_on_interface
        * Added API to unconfigure_fec_on_interface
    * Added configure_smartpower_domain
    * Added unconfigure_smartpower_domain
    * Added configure_smartpower_importance
    * Added unconfigure_smartpower_importance
    * Added configure_smartpower_name
    * Added unconfigure_smartpower_name
    * Added configure_smartpower_role
    * Added unconfigure_smartpower_role
    * Added configure_smartpower_keywords
    * Added unconfigure_smartpower_keywords
    * Added configure_smartpower_level
    * Added unconfigure_smartpower_level
    * Added configure_smartpower_role_default
    * Added configure_smartpower_name_default
    * Added configure_smartpower_management_default
    * Added configure_smartpower_level_default
    * Management
        * Update configure_management_http API.
    * running_config/get
        * Update get_running_config_dict  API.
    * Modified configure_management_vty_lines
        * Added code to ignore the 'none' from the transport input.
    * Added configure_smartpower_interface_endpoint_default
        * API to configure SmartPower default interface endpoint
    * Added configure_smartpower_interface_importance_default
        * API to configure SmartPower default interface importance
    * Added configure_smartpower_interface_keywords_default
        * API to configure SmartPower default interface keywords
    * Added configure_smartpower_interface_level_default
        * API to configure SmartPower default interface level
    * Added configure_smartpower_interface_management_default
        * API to configure SmartPower default interface management
    * Added configure_smartpower_interface_name_default
        * API to configure SmartPower default interface name
    * Added configure_smartpower_interface_neighbor_default
        * API to configure SmartPower default interface neighbor
    * Added configure_smartpower_interface_role_default
        * API to configure SmartPower default interface role
    * Added API configure_ptp_neighbor_propagation_delay_threshold
        * Added API to configure ptp neighbor-propagation-delay-threshold
    * Added API unconfigure_ptp_neighbor_propagation_delay_threshold
        * Added API to unconfigure ptp neighbor-propagation-delay-threshold
    * Added configure_smartpower_domain_default
    * Added configure_smartpower_endpoint_default
    * Added configure_smartpower_importance_default
    * Added configure_smartpower_keywords_default
    * Added configure_smartpower_activitycheck
        * API to configure SmartPower activitycheck
    * Added unconfigure_smartpower_activitycheck
        * API to unconfigure SmartPower activitycheck
    * Added configure_smartpower_interface_importance
        * API to configure SmartPower interface importance
    * Added unconfigure_smartpower_interface_importance
        * API to unconfigure SmartPower interface importance
    * Added configure_smartpower_interface_keywords
        * API to configure SmartPower interface keywords
    * Added unconfigure_smartpower_interface_keywords
        * API to unconfigure SmartPower interface keywords
    * Added configure_hw_module_slot_breakout
        * API to Configure a native port into four breakout ports of the specified slot
    * Added unconfigure_hw_module_slot_breakout
        * API to Unconfigure a native port into four breakout ports of the specified slot
    * Added configure_stack_power_ecomode
    * Added unconfigure_stack_power_ecomode
    * Added configure_default_stack_power_ecomode
    * Add API `is_management_interface`

* ios
    * running_config/configure
        * update restore_running_config API.

* iosxr
    * Add API `is_management_interface`
    * Add API `clear_standby_console`

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_bandwidth_remaining_policy_map
        * Added argument to searialize the policy name in the API,  Example  policy_name = ["child1", "child2", "parent"]
    * Updated `transceiver_intf_components` to retrieve vendor_name, vendor_part, vendor_rev, serial_no, form_factor and connector_type for their repsective transceiver interfaces.
    * Modified copy_startup_config_to_tftp
    * Modified copy_running_config_to_tftp
    * Modified copy_startup_config_to_flash_memory
    * Modified copy_running_config_to_flash_memory
    * Modified clear_crypto_gkm
        * Modified regex for clear_crypto_gkm API
    * Added new api execute_clear_console.
    * Fix clear_counters
        * added optional timeout value
    * Fix clear_interface_counters
        * added optional timeout value and dialog handling
    * Modified configure_l2vpn_vfi_context_vpls
        * Added argument to delete vfi_name
    * Modified unconfigure_l2vpn_vfi_context_vpls
        * Added argument to delete vfi_name
    * Modified verify_mka_session
        * Modified the api to verify_mka_session. Existing API always giving Wrong output eventhough session is in secured state. Verified compatability everything is working fine with latets changes.
    * Modified config_identity_ibns
        * Modified the api to config_identity_ibns. Existing API always configuring access-session closed. Now added condition for that.
    * Modified clear_access_session
        * Modified the api to clear_access_session. Existing API always expecting interface to convert even interface not provided also. Now changed the condition for that.

* abstracted_libs
    * Modified Restore class
        * Added kwargs parameter to restore_configuration method

* ios
    * Modified Restore class
        * Added kwargs parameter to restore_configuration method

* nxos
    * Modified Restore class
        * Added kwargs parameter to restore_configuration method

* iosxr
    * Modified Restore class
        * Added kwargs parameter to restore_configuration method


