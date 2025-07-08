--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added acm_merge
        * New API to execute acm merge  with timeout and without timeout
    * Added API generate_dummy_file
        * API to generate dummy file
    * ie3k
        * Added new api execute_copy_noverify
    * Added acm_save to the IOSXE SDK
        * API to execute acm save commands
    * Added acm_rollback to the IOSXE SDK
        * API to execute acm rollback commands
    * Added API change_file_permissions
        * API to give full permissions to file
    * Added destroy_guestshell
        * API to destroy guestshell
    * Added acm_configlet_create
        * New API to execute acm configlet create flashabc
    * Added acm_configlet_remove
        * New API to execute acm configlet remove flashabc
    * Added acm_configlet_delete
        * New API to execute acm configlet modify demo delete 1
    * Added acm_configlet_insert
        * New API to execute acm configlet modify demo insert 1 vlan 15
    * Added acm_configlet_replace
        * New API to execute acm configlet modify demo replace 1 vlan 15
    * Added unconfigure_policy_map_shape_on_device
        * API to unconfigure policy_map shape on device
    * Added clear_nat_statistics
        * API to execute  clear_nat_statistics on the device
    * Added API configure_interfaces_uplink
        * Added API to configure_interfaces_uplink
    * Added API configure_interfaces_no_uplink
        * Added API to configure_interfaces_no_uplink
    * Added configure_ospf_retransmit_interval
        * API to configure_ospf_retransmit_interval
    * Added unconfigure_vlan_to_sgt_mapping
        * API to unconfigure vlan sgt
    * Added API unconfigure_ipv6_flow_monitor_sampler
        * API to configure unconfigure_ipv6_flow_monitor_sampler.
    * Added acm_confirm_commit
        * New API to execute acm confirm-commit
    * Added acm_cancel_commit
        * New API to execute acm cancel-commit
    * Added configure_ipv6_flow_monitor_on_interface
        * API to configure IPv6 flow monitor with sampler on an interface
    * Added API unconfig_flow_monitor_on_vlan_interface
    * Added acm_rules
        * New API to execute acm rules
    * Added acm_replace
        * New API to execute acm replace with timeout and without timeout
    * Added force
        * API execute_install_one_shot to execute with force argument
    * Added acm_rules
        * New API to execute acm rules flashabc
    * Added execute_factory_reset
        * API to factory reset the device.
    * configure_logging_tls_profile
        * configure_logging_tls_profile
    * configure_syslog_server_tls_profile
        * configure_syslog_server_tls_profile
    * unconfigure_logging_tls_profile
        * unconfigure_logging_tls_profile
    * unconfigure_syslog_server_tls_profile
        * unconfigure_syslog_server_tls_profile
    * change_cipher_from_tls_profile
        * change_cipher_from_tls_profile
    * configure_logging_discrimnator
        * configure_logging_discrimnator
    * unconfigure_logging_discrimnator
        * unconfigure_logging_discrimnator
    * apply_logging_discrimnator
        * apply_logging_discrimnator
    * unapply_logging_discrimnator
        * unapply_logging_discrimnator
    * configure_pki_import_cert
        * configure_pki_import_cert
    * pki
        * Added configure_crypto_pki_download_crl
        * Added unconfigure_crypto_pki_download_crl
    * Added count_trace_in_logging
        * API to count trace in logging

* api
    * IOSXE
        * Added execute_reload_verify API for IE3K devices
        * Added execute_reload_noverify API for IE3K devices

* os/iosxe/c9800
    * Added api configure_management_ip.

* iosxe/c8kv
    * Added configure_autoboot
        * API to configure autoboot


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* updated api unit tests
    * IOSXE
        * Updated unittests to new testing method
            * configure_pnp_startup_vlan
            * unconfigure_pnp_startup_vlan
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_access_map_match_ip_address_action_forward
            * unconfigure_ace
            * unconfigure_acl
            * unconfigure_acl_with_src_dsc_net
            * unconfigure_as_path_acl
            * unconfigure_filter_vlan_list
            * unconfigure_ip_sgacl
            * unconfigure_ipv6_acl
            * unconfigure_ipv6_acl_ace
        * Removed the mock yaml under 'unconfigure_extended_acl_deny' as we do not have any API for it.
    * IOSXE
        * Updated unittests to new testing method
            * clear_arp_cache
            * clear_ip_arp_inspection
            * configure_arp_access_list_permit_ip_host
            * configure_ip_arp_inspection_filter
            * configure_ip_arp_inspection_log_buffer
            * configure_ip_arp_inspection_on_interface
            * configure_ip_arp_inspection_validateip
            * configure_ip_arp_inspection_vlan
            * configure_ip_arp_inspection_vlan_logging
            * unconfigure_arp_access_list
            * unconfigure_ip_arp_inspection_filter
            * unconfigure_ip_arp_inspection_log_buffer
            * unconfigure_ip_arp_inspection_on_interface
            * unconfigure_ip_arp_inspection_validateip
            * unconfigure_ip_arp_inspection_vlan
            * unconfigure_ip_arp_inspection_vlan_logging
    * IOSXE
        * Updated unittests to new testing method
            * unconfigure_mac_access_group_mac_acl_in_out
            * unconfigure_mac_acl
            * unconfigure_standard_acl
            * configure_app_hosting_appid_docker
            * configure_app_hosting_appid_iperf_from_vlan
            * configure_app_hosting_appid_trunk_port
            * configure_app_hosting_resource_profile
            * configure_app_management_networking
            * configure_thousand_eyes_application
            * confirm_iox_enabled_requested_storage_media
            * enable_usb_ssd_verify_exists
            * unconfigure_app_hosting_appid

* iosxe
    * Modified configure_ipv6_logging_with_discriminator
        * Added conditional logic to handle syslog_host and discriminator_name parameters.
    * Added API debug_software_cpm_switch_pcap_drop
        * Added API to debug_software_cpm_switch_pcap_drop
    * Added API debug_software_cpm_switch_feature
        * Added API to debug_software_cpm_switch_feature
    * Added API debug_software_cpm_switch_pcap
        * Added API to debug_software_cpm_switch_pcap
    * Added API debug_software_cpm_switch_pcap_count
        * Added API to debug_software_cpm_switch_pcap_count
    * Fix the configure rommon tftp to get `tftp_server` from recovery.
    * Modified configure_fnf_flow_record
        * Modified the API to configure "match routing vrf input" if match_vrf is True.
    * Modified configure_ipv6_flow_monitor_sampler
        * Modified the API to configure sampler based on direction.
    * Modified fix for execute_install_one_shot API.
        * Converted output to string for the result verification.
    * Modified "configure_management_ssh" API
        * added ip ssh source-interface command
    * cat9k
        * Modified configure_ignore_startup_config
            * Added handling for standby connections to prevent failures when standby is locked
            * Skip standby devices since configuration is already applied with "switch all" command
        * Modified unconfigure_ignore_startup_config
            * Added debug logging for troubleshooting function calls
            * Added handling for standby connections to prevent failures when standby is locked
            * Skip standby devices since configuration is already applied with "switch all" command
    * Modified configure_logging_ipv6
        * Added conditional logic to handle syslog_host and transport parameters.
    * Added unconfigure_logging_facility_and_trap
        * API to unconfigure logging facility and trap.
    * Modified configure_ipv6_logging_with_transport_and_facility
        * Added conditional logic to handle transport_protocol parameters.
        * Removed cli "no logging facility local0", "no logging trap debugging"

* updated unittests
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * configure_call_home_alert_group_config_snapshot
            * configure_call_home_contact_email_addr
            * configure_call_home_contract_id
            * configure_call_home_copy_profile
            * configure_call_home_customer_id
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * configure_call_home_data_privacy
            * configure_call_home_http_proxy
            * configure_call_home_http_resolve_hostname_ipv4_first
            * configure_call_home_http_secure_server_identity_check
            * configure_call_home_phone_number

* cleaning api ut's
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
            * configure_access_list_extend_with_range_and_eq_port
            * configure_access_map_match_ip_address_action_forward
            * configure_bgp_address_advertisement
            * configure_bgp_advertise_l2vpn_evpn
            * configure_bgp_auto_summary
            * configure_bgp_best_path_as_path_multipath_relax
    * Iosxe
        * Updated with latest UT mathod to all of the below mentioned API UT's
            * config_ip_tcp_mss
            * config_refacl_global_timeout
            * configure_access_list_extend
            * configure_access_list_extend_with_dst_address_and_gt_port
            * configure_access_list_extend_with_dst_address_and_port
            * configure_access_list_extend_with_port
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's
    * Iosxe
        * Updated with latest UT method to all of the below mentioned API UT's

* sdk
    * IOSXE
        * Updated `send_break_boot`
            * Set buffer to an empty string before processing the dialog
    * IOSXE
        * Updated `configure_rommon_tftp_ha`
            * Change to look for rommon information in `management` attribute instead of `rommon` attribute due to service conflict.

* updated error pattern for copy /verify
    * Iosxe
        * Ie3k
            * Passed the Error_pattern to match the execution error of api.


--------------------------------------------------------------------------------
                        Configure_Ipv6_Dhcp_Relay_Trust                         
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                            Configure_Ldra_Interface                            
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                   Unconfigure_Ipv6_Dhcp_Client_Vendor_Class                    
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
              Unconfigure_Ipv6_Dhcp_Relay_Destination_Ipv6Address               
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                     Unconfigure_Ipv6_Dhcp_Relay_Option_Vpn                     
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
              Unconfigure_Ipv6_Dhcp_Relay_Source_Interface_Intf_Id              
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                       Unconfigure_Ipv6_Dhcp_Relay_Trust                        
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                        Configure_Ip_Nhrp_Map_Multicast                         
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                    Configure_Ip_Nhrp_Map_Multicast_Dynamic                     
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                          Configure_Ip_Nhrp_Network_Id                          
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                             Configure_Ip_Nhrp_Nhs                              
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                           Configure_Ip_Nhrp_Redirect                           
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                              Configure_Nhrp_Group                              
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                       Unconfigure_Ip_Nhrp_Map_Multicast                        
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                   Unconfigure_Ip_Nhrp_Map_Multicast_Dynamic                    
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                         Unconfigure_Ip_Nhrp_Network_Id                         
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                            Unconfigure_Ip_Nhrp_Nhs                             
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                          Unconfigure_Ip_Nhrp_Redirect                          
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                             Unconfigure_Nhrp_Group                             
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                     Unconfigure_Tunnel_Mode_Gre_Multipoint                     
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                      Configure_Tunnel_Mode_Gre_Multipoint                      
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                            Configure_Tunnel_Source                             
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                        Unconfigure_Interface_Tunnel_Key                        
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                       Unconfigure_Ip_Nhrp_Authentication                       
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                          Unconfigure_Ip_Nhrp_Holdtime                          
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                            Unconfigure_Ip_Nhrp_Map                             
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                                     Update                                     
--------------------------------------------------------------------------------

* iosxe
    * Updated doc string for config_macsec_keychain_on_device api
        * Added doc string for these arguments  key, crypt_algorithm


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified unconfigure switch provision
        * Modified API to unconfigure switch provision using switch model


