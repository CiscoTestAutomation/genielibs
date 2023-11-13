--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API configure_paramter_map
        * API for configuring the parameter map with all the sub-commands included
    * Added API unconfigure_paramter_map
        * API for unconfiguring the parameter map
    * Added __init__.py for vdsl folder
        * Added __init__.py for vdsl folder
    * Added added_api_rep_admin_vlan_configure API
        * API to configure rep admin vlan
    * Added configure_ospfv3_network_type
        * New API to configure ospfv3 network type
    * Added configure_ospfv3_interface
        * New API to configure ospfv3 interface
    * Added clear_ip_dhcp_snooping_binding_on_interface
        * API for clear ip dhcp snooping binding on interface
    * Added configure_device_policy_tracking
        * API for configure device policy tracking
    * Added configure_source_tracking_on_interface
        * API for configure source tracking on interface
    * Added configure_interface_range_dhcp_channel_group_mode
        * New API to configure interface range channel-group 1 mode desirable
    * Added unconfigure_interface_range_dhcp_channel_group_mode
        * New API to unconfigure interface range channel-group 1 mode desirable
    * Added configure_ip_sftp_password
        * API to configure ip sftp password
    * Added unconfigure_ip_sftp_password
        * API to unconfigure ip sftp password
    * Added configure_ip_scp_password
        * API to configure ip scp password
    * Added unconfigure_ip_scp_password
        * API to unconfigure ip scp password
    * Added config_interface_prpchannel
        * added api to config_interface_prpchannel
    * Added unconfig_interface_prpchannel
        * added api to unconfig_interface_prpchannel
    * Added `configure_management_ntp` API
    * Added format_directory
        * API to format {directory}
    * Added configure_vtp_pruning
        * API to vtp pruning
    * Added unconfigure_vtp_pruning
        * API to no vtp pruning
    * Added configure_switchport_trunk_pruning_vlan
        * API to configure switchport trunk pruning vlan
    * Added unconfigure_switchport_trunk_pruning_vlan
        * API to configure no switchport trunk pruning vlan
    * Added configure_periodic_time_range
        * API to configure periodic time range
    * Added unconfigure_periodic_time_range
        * API to unconfigure periodic time range
    * Added configure_absolute_time_range
        * API to configure absolute time range
    * Added unconfigure_absolute_time_range
        * API to unconfigure absolute time range
    * Added configure_hw_module_slot_logging_onboard_voltage API
        * Added API for hw-module slot {slot} logging onboard voltage
    * Added unconfigure_hw_module_slot_logging_onboard_voltage API
        * Added API for no hw-module slot {slot} logging onboard voltage
    * Added configure_hw_module_slot_logging_onboard_temperature API
        * Added API for hw-module slot {slot} logging onboard temperature
    * Added unconfigure_hw_module_slot_logging_onboard_temperature API
        * Added API for no hw-module slot {slot} logging onboard temperature
    * Added configure_hw_module_slot_logging_onboard_environment API
        * Added API for hw-module slot {slot} logging onboard environment
    * Added unconfigure_hw_module_slot_logging_onboard_environment API
        * Added API for no hw-module slot {slot} logging onboard environment
    * Added configure_clear_logging_onboard_slot_temperature API
        * Added API for clear  logging  onboard  slot {slot}  temperature
    * Added configure_clear_logging_onboard_slot_voltage API
        * Added API for clear  logging  onboard  slot {slot}  voltage
    * Added configure_clear_logging_onboard_slot_environment API
        * Added API for clear  logging  onboard  slot {slot}  Environment
    * Added configure_ip_sftp_username
        * API to configure ip sftp username
    * Added unconfigure_ip_sftp_username
        * API to unconfigure ip sftp username
    * Added configure_ip_scp_username
        * API to configure ip scp username
    * Added unconfigure_ip_scp_username
        * API to unconfigure ip scp username
    * Added configure_snmp_mib_bulkstat_transfer
        * API to configure snmp mib bulkstat transfer
    * Added copy_file_with_sftp
        * API to copy file from device to sftp host
    * Added copy_file_with_scp
        * API to copy file from device to scp host
    * Added api to execute more file
        * API to execute more file on device and get the output
    * Added execute_install_package_reloadfast
        * API to execute install package reloadfast
    * Added api to execute set platform hardware rom-monitor virtualization
        * API to execute set platform hardware rom-monitor virtualization on device and get the output
    * Added configure_interface_vlan_range_priority
        * API to set vlan interface priority
    * Added configure_interface_vlan_priority
        * API to set vlan interface rnage priority
    * Added unconfigure_ipv6_router_ospf
        * New API for no ipv6 router ospf {ospf_process_id}
    * Added api to configure service compress-config
        * API to configure service compress-config on device
    * Added api unconfigure service compress-config
        * API to unconfigure service compress-config on device
    * Added api configure_ip_igmp_querier_query_interval
        * API to configure ip igmp querier query interval
    * Added api configure_ip_igmp_querier_tcn_query_count
        * API to configure ip igmp querier tcn query count
    * Added configure_spanning_tree_etherchannel_misconfig
        * added api to configure_spanning_tree_etherchannel_misconfig
    * Added unconfigure_spanning_tree_etherchannel_misconfig
        * added api to unconfigure_spanning_tree_etherchannel_misconfig

* added configure_hw_module_logging_onboard api
    * Added API for hw-module slot {slot} logging onboard

* added unconfigure_hw_module_logging_onboard api
    * Added API for no hw-module slot {slot} logging onboard


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_bandwidth_remaining_policy_map
        * Fixed the mandatory argument to optional "class_names=None,bandwidth_list=None"
    * Modified enable_usb_ssd_verify_exists
        * Fixed the time argument to timeout
    * Fixed logic for get_mgmt_ip_and_mgmt_src_ip_addresses when passing IP address
    * Modify configure_enable_nat_scale
        * added boolean variables nat_aot and nat_scale
    * Modify configure_disable_nat_scale
        * added boolean variables nat_aot and nat_scale
    * Modified change_configure_crypto_pki_server_eaptls
        * Passing kwargs and condition to configure_crypto_pki_server
    * Modified change_configure_crypto_pki_server_pki
        * Passing kwargs and condition to configure_crypto_pki_server
    * Removed
        * Removed duplicate keyword configure_stack_power_stack and unconfigure_stack_power_stack
        * Removed corresponding UT as well for those keywords.

* nxos
    * Modified
        * Updated nxapi_method_nxapi_rest API to handle output of type RESPONSE
    * Fixed logic for get_mgmt_ip_and_mgmt_src_ip_addresses when passing IP address

* blitz
    * Fix gnmi_util to enclose leaf-list entries within [].
    * Fixed negative test handling for gnmi get
    * Fixed decoding of proto encoding in Gnmi
    * Added better logging for Gnmi

* iosxr
    * Fixed logic for get_mgmt_ip_and_mgmt_src_ip_addresses when passing IP address

* genie.libs.sdk
    * Fixed RPC Verifier regex substitution usage
    * Added check for allowed fields for OptFields class, log warning for unknown fields


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Modify configure_scale_vrf_via_tftp
        * add both ipv4 and ipv6 address family


