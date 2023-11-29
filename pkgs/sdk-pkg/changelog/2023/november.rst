--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* linux
    * Added API get_snmp_snmpwalk_version3
        * API added to 'snmpwalk -v {version} -u {username} {passprs} {passphrase} {var} {security_level} {security} {security_method}'
    * Added API  configure_pki_authenticate_certificate
        * API added to configure_pki_authenticate_certificate(certificate={cert}, label_name={tp1_name})


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added unconfigure_interface_speed
        * New API to unconfigure interface speed
    * Added clear_ipv6_neighbors
        * New API to clear ipv6 neighbors
    * Added unconfigure_filter_vlan_list
        * API for unconfigure filter vlan list
    * Added configure_access_map_match_ip_mac_address
        * API for configure access map match ip mac address
    * Added configure_acl_protocol_port
        * API for configure acl protocol port
    * Added configure_ip_acl_with_any
        * API for configure ip acl with any
    * Added configure_shutdown_vlan_interface_range
        * API to shut the vlan interface range {vlan_id_from}-{vlan_id_to}
    * Added configure_no_shutdown_vlan_interface_range
        * API to unshut the vlan interface range {vlan_id_from}-{vlan_id_to}
    * Added execute_crypto_pki_server
        * added api to execute crypto pki server
    * Added execute_test_opssl_nonblockingsession_client
        * added api to  execute opssl nonblockingsession client
    * Added execute_test_opssl_nonblockingsession_server_stop
        * added api to execute opssl nonblockingsession server stop
    * Added execute_test_opssl_nonblockingsession_server_start
        * added api to execute opssl nonblockingsession server start
    * Updated configure_pki_trustpoint
        * Updated configure pki trustpoint
    * Added configure_spanning_tree_mst_priority
        * New API to configure spanning tree mst priority
    * Added hw_module_sub_slot_reload
        * added api to hw_module_sub_slot_reload
    * Added configure_ospf_vrf_lite
        * New API for configuring vrf-lite capabilty under OSPF {ospf_process_id}
    * Added unconfigure_time_range
        * API to unconfigure time-range
    * Added configure_device_tracking_logging
        * API to configure device tracking logging
    * Added unconfigure_device_tracking_logging
        * API to unconfigure device tracking logging
    * Added configure_object_group
        * API to configure object group
    * Added configure_telemetry_ietf_parameters
    * Added unconfigure_ip_dhcp_snooping_limit_rate
        * API for unconfiguring dhcp snooping rate limit
    * Added configure_ip_dhcp_snooping_verify_mac_address
        * API for configuring dhcp snooping verify mac_address
    * Added unconfigure_ip_dhcp_snooping_verify_mac_address
        * API for unconfiguring dhcp snooping verify mac_address
    * Added configure_dhcp_snooping_verify_no_relay_agent_address
        * API for configuring dhcp snooping verify no_relay_agent_address
    * Added unconfigure_dhcp_snooping_verify_no_relay_agent_address
        * API for unconfiguting dhcp snooping verify no_relay_agent_address
    * Added configure_dhcp_snooping_track_server_dhcp_acks
        * API for configure dhcp snooping track server dhcp-acks
    * Added unconfigure_dhcp_snooping_track_server_dhcp_acks
        * API for unconfigure dhcp snooping track server dhcp-acks
    * Added enable_cpp_system_default_on_device
        * New API to enable cpp system-default on device
    * Added enable_switchport_protected_on_interface
        * New API to enable switchport protected on interface
    * Added clear_ip_pim_rp_mapping
        * New API to clear ip pim rp-mapping
    * Added configure_event_manager
        * API to configure event manager with applet name
    * Added execute_event_manager_run_with_reload
        * API to execute event manager with embeded applet name
    * Added get_snmp_snmpwalk_sysname
        * API to get snmp snmpwalk sysname description

* added execute_clear_control_plane
    * New API to execute clear control-plane all on device


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modify configure_pki_export
        * added return vlaue as self signed  certificate
    * Modify api configure_pki_enroll
        * added the serial number in subject name as an argument
    * Modified execute_reload_fast
        * Modified the exeute_reload_fast API
    * Modified execute_install_one_shot
        * Modified the execute_install_one_shot API to upgrade the image using reloadfast
    * Modified request_system_shell
        * Fixed the dialog,added new statement to handle shell prompt.
    * Modified platform exclude values for reload.py trigger
    * Modified platform exclude values for switchover.py trigger

* genie.libs.sdk
    * Modified process_sequencial_operational_state to set sequence to False as we are no longer trimming reponses

* blitz
    * Fix to enclose list entries within square brackets when building GNMI request
    * changed reference of "try_lock" function from yangexec to netconf_util.
    * Modified configure_replace action
        * added 'timeout' argument
    * Modified restore_config_snapshot action
        * added 'timeout' argument
    * Modified save_config_snapshot action
        * added 'timeout' argument
    * Modified
        * Netconf subscriptions were not tracked and did not account for multiple streams.
    * Fixed negative test handling for netconf.

* linux
    * Modify kill_processes API
        * added `sudo` argument

* processor
    * Modified check_memory_leaks processor for IOSXE
        * added 'timeout' argument

* abstracted_libs
    * Modified restore_configuration function
        * added 'timeout' argument
    * Modified save_configuration function
        * added 'timeout' argument

* utils
    * Modified copy_to_device/copy_from_device to support obtaining proxy device from servers section


