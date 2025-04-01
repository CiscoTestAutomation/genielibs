--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_ipv6_dhcp_pool
        * API to configure_ipv6_dhcp_pool
    * Added API configure_vrf_rd_rt
        * added api to configure vrf rd and rt on the device
    * Added API enable_ip_classless
        * API to enable ip classless on the device
    * Added configure_radius_server_dtls_ip
        * API to configure radius server dtls ip
    * Added configure_interface_media_type_backplane
    * Added unconfigure_device_sampler
        * API to unconfigure a sampler on an IOS-XE device.
    * Added configure_radius_server_dtls_idletimeout
        * API to configure radius server dtls idletimeout
    * Added unconfigure_boot_system_switch_all_flash
        * API to unconfigure boot system variable on all switches in the stack.
        * Example no boot system switch all flashtestAll
    * Added API configure_interfaces_uplink
        * Added API to configure_interfaces_uplink
    * Added API configure_interfaces_no_uplink
        * Added API to configure_interfaces_no_uplink
    * Added configure_ip_pim_bsr_rp_candidate
        * API to Configure ip pim candidate rp or bsr for both global and VRF contexts.
    * Added API configure_radius_server_dtls_connection
    * Added new API to Release DHCP on interface
        * API to execute release dhcp on interface
    * Added new API to Renew DHCP on interface
        * API to execute renew dhcp on interface
    * Added new API to Execute 'clear ipv6 dhcp conflict *' on device
        * API to Execute 'clear ipv6 dhcp conflict' on device
    * Added new API to Configure service-policy type control default on interface
        * API to configure service-policy type control default on interface
    * Added new API to Configure ip dhcp class static on device
        * API to configure ip dhcp class static on device
    * Added configure_vlan_config_device_tracking
        * API to configure vlan configuration <vlan_number>
    * Added configure_pbr_route_map_nhop_verify_availability
        * API for configure pbr route map with next hop verify availability
    * Added unconfigure_exporter
        * API to unconfigure flow exporter on device.
    * Added configure_radius_server_with_dtls
        * configure api for radius_server_with_dtls
    * Added unconfigure_interface_media_type_backplane
        * API to unconfigure backplane media_type on interface.
    * Added configure_dhcp_pool_ztp
        * API to configure DHCP pool for ZTP.
    * PBR
        * Added api_configure_pbr_route_map_add_set
            * API to add set action to route map
    * Added API configure_radius_server_dtls_watchdoginterval
    * API to Configure radius server dtls watchdoginterval
    * SLA
        * Added configure_ip_sla_icmp_echo
        * Added unconfigure_ip_sla
        * Added configure_ip_sla_schedule
        * Added unconfigure_ip_sla_schedule
        * Added configure_ip_sla_at_track

* api to configure backplane media_type on interface.

* pbr
    * Added API configure_pbr_route_map_nhop_recursive
        * configure api for PBR route map nhop recursive


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Updated api unconfigure_hw_module_breakout
        * updated api with module_number and port_number to support hw-module breakout module cli
    * Updated api configure_hw_module_breakout
        * updated api with module_number and port_number to support no hw-module breakout module cli
    * Updated api verify_ignore_startup_config
        * updated api to make it optional to check for switch_ignore_startup_config variable to be exist in show romvar 'rommon_variables' output when it's not setted.
    * Updated api function name from configure_pae to configure_product_analytics
        * updated api for cli change from PAE to product-analytics
    * Updated api function name from unconfigure_pae to unconfigure_product_analytics
        * updated api for cli change from no PAE to no product-analytics
    * Deleted UT files for configure_pae and unconfigure_pae
        * deleted UT files for configure_pae and unconfigure_pae
    * Updated api execute_install_one_shot
        * updated api with optional arguments post_reload_wait_time and error_pattern

* generic
    * Modified `execute_clear_line` API
        * Changed disconnect_termserver argument to default to True
        * Update logic to avoid disconnecting twice


