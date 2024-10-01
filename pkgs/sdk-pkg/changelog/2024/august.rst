--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_macro_name
        * API to configure 'macro name {macro_name}'.
    * Enhanced existing api configure_macro_global_apply
        * Modified API to configure 'macro global apply {macro_name} {variables} {values} '.
    * Added configure_ip_pim_vrf_ssm_range
        * API to configure ip pim vrf ssm range
    * Added unconfigure_ip_pim_vrf_ssm_range
        * API to unconfigure ip pim vrf ssm range
    * Added configure_ip_msdp_vrf_peer
        * API to configure msdp vrf peer
    * Added unconfigure_ip_msdp_vrf_peer
        * API to unconfigure msdp vrf peer
    * Added config_prp_sup_vlan_aware
        * prp channel-group 1 supervisionFrameOption vlan-aware-enable
    * Added unconfig_prp_sup_vlan_aware
        * no prp channel-group 1 supervisionFrameOption vlan-aware-enable
    * Added config_prp_sup_vlan_aware_allowed_vlan_list
        * prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan 30,40
    * Added unconfig_prp_sup_vlan_aware_allowed_vlan_list
        * no prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan
    * Added config_prp_static_vdan_entry
        * prp channel-group 1 vdanMacaddress 000001000011 vlan-id 10
    * Added unconfig_prp_static_vdan_entry
        * no prp channel-group 1 vdanMacaddress 000001000011
    * Added config_prp_sup_vlan_aware_reject_untagged
        * prp channel-group 1 supervisionFrameOption vlan-aware-reject-untagged
    * Added def unconfig_prp_sup_vlan_aware_reject_untagged(device, interface)
        * no prp channel-group 1 supervisionFrameOption vlan-aware-reject-untagged
    * Added config_prp_sup_vlan_id
        * prp channel-group 1 supervisionFrameoption vlan-id 10
    * Added unconfig_prp_sup_vlan_id
        * no prp channel-group 1 supervisionFrameoption vlan-id 10
    * Added config_prp_sup_vlan_tagged
        * prp channel-group 1 supervisionFrameOption vlan-tagged
    * Added unconfig_prp_sup_vlan_tagged
        * no prp channel-group 1 supervisionFrameOption vlan-tagged
    * Updated the config using f-strings
        * config = f"prp channel-group {interface} supervisionFrameOption vlan-aware-enable"
    * Updated api config_prp_static_vdan_entry as configure_prp_static_vdan_entry_with_vlan
        * prp channel-group 1 vdanMacaddress 000001000011 vlan-id 10
    * Added configure_prp_static_vdan_entry
        * prp channel-group 1 vdanMacaddress 000001000012
    * Added configure_interface_cts_role_based_sgt_map
        * API to configure interface cts role based sgt map
    * Added unconfigure_interface_cts_role_based_sgt_map
        * API to unconfigure interface cts role based sgt map
    * Added debug_platform_software_fed_drop_capture
        * added api to debug_platform_software_fed_drop_capture
    * Added debug_platform_software_fed_drop_capture_action
        * added api to debug_platform_software_fed_drop_capture_action
    * Added debug_platform_software_fed_drop_capture_buffer
        * added api to debug_platform_software_fed_drop_capture_buffer
    * Added configure_ignore_startup_config
        * added api to configure_ignore_startup_config
    * Added unconfigure_ignore_startup_config
        * added api to unconfigure_ignore_startup_config
    * Added verify_ignore_startup_config
        * added api to verify_ignore_startup_config
    * Added new API get_interfaces_switchport_state
        * get_interfaces_switchport_state - Get switchport state for interfaces
    * Added configure_radius_attribute_policy_name_globally
    * Added unconfigure_radius_attribute_policy_name_globally
    * Added configure_radius_attribute_policy_name_under_server
    * Added unconfigure_radius_attribute_policy_name_under_server
    * Added configure_radius_attribute_policy_name_under_servergroup
    * Added unconfigure_radius_attribute_policy_name_under_servergroup

* iosxe/cat9k
    * Added send_break_boot
        * send break boot command for cat9k devices

* sdk/triggers
    * blitz
        * Added new action check_yang_subscribe


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * send_break_boot
        * update the pattern for break boot for iosxe
    * Fixed clear_logging_onboard_rp_active_standby
        * added optional variable 'log_name'
    * Fixed confirm_iox_enabled_requested_storage_media
        * Added mod_storage_string and sso_storage_strings to support modular
    * Fixed configure_app_management_networking
        * Fixed returns True or False instead of none
    * Fixed issue with 'verify_interface_config_duplex' API
        * API not working fine when any other config present under interface for auto duplex.
    * Fixed issue with 'verify_interface_config_speed' API
        * API not working fine when any other config present under interface for auto speed.
    * Modified verify_current_image
        * Added provision to compare images based on regex if regex_search parameter is True
    * ASR1K
        * Added verify_current_image
            * Passing regex_search as True to compare images based on regex
    * Modified configure_management
        * Added `alias_as_hostname` argument
        * Allows user to use the alias as the device hostname
    * Modified health_logging
        * Fixed logic error with log count

* execute
    * execute power cycle
        * add try except for destroying device object.

* abstracted_libs
    * Modified __init__.py file to import all modules available in the abstracted_libs folder

* power cycler
    * snmp client
        * update the logic to work with tuple instead of iterator.