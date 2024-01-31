--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Removed remove_routing_ip_route
    * Modified configure_pppoe_enable_interface
        * modified api to configure ppp-max-payload
    * Modified unconfigure_pppoe_enable_interface
        * modified api to unconfigure ppp-max-payload
    * Modified get_firmware_version to handle stack switches
    * Modified unconfigure_app_hosting_appid
        * Added 'appid' argument
    * Modified configure_fnf_flow_record
        * added new fields

* iosxr
    * Modified FileUtils

* sdk-pkg
    * iosxe
        * Fix the copy_file_with_scp api mock data


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_mdns_remote_purge_timer
        * API to configure enable configure mdns remote purge timer
    * Added unconfigure_mdns_remote_purge_timer
        * API to unconfigure mdns remote purge timer
    * Added unconfigure_mdns_global_service_buffer
        * API to unconfigure mdns global service buffer
    * Added clear_mdns_cache_remote
        * API to clear mdns cache remote
    * Added configure_mdns_remote_cache_enable
        * API to configure mdns remote cache enable
    * Added unconfigure_mdns_remote_cache_enable
        * API to unconfigure mdns remote cache enable
    * Added configure_mdns_remote_cache_max_limit
        * API to configure mdns remote cache max limit
    * Added unconfigure_mdns_remote_cache_max_limit
        * API to unconfigure mdns remote cache max limit
    * Added configure_mdns_global_service_buffer
        * API to configure mdns global service buffer
    * Added configure_ip_on_atm_interface
        * added api to configure_ip_on_atm_interface
    * Added unconfigure_ip_on_atm_interface
        * added api to unconfigure_ip_on_atm_interface
    * Added get_module api
    * Added hw_module_beacon_rp_toggle
        * API to turn beacon on/off for RP and R1
    * Added hw_module_beacon_rp_status
        * API to fetch beacon status for RP and R1
    * Added hw_module_beacon_slot_status
        * API to fetch beacon status for slot
    * Added hw_module_beacon_rp_active_standby_status
        * API to fetch status of the beacon for active/standby RP
    * Added clear_lacp_counters
        * added api to clear_lacp_counters
    * Added clear_active_punt_ios_cause
        * added api to clear_active_punt_ios_cause
    * Modified configure_interface_switchport_access_vlan
        * Modified the configure_interface_switchport_access_vlan API interface to swichport
    * Added configure_hw_module_switch_number_ecomode_led
        * hw-module switch number ecomode led
    * Added unconfigure_hw_module_switch_number_ecomode_led
        * no hw-module switch number ecomode led
    * Modified copy_file_with_scp
    * Modified copy_file_with_sftp

* cheetah
    * Added execute_archive_download
        * Added new API execute_archive_download


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_virtual_template
        * modified api to configure ipv6_pool_name
    * Modified configure_bba_group
        * modified api to configure tag ppp-max-payload
    * Modified configure_device_classifier_command
        * added optional timeout value
    * Modified configure_device_classifier
        * added optional timeout value


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API clear_ip_dhcp_snooping_statistics
        * API added to clear ip dhcp snooping statistics


