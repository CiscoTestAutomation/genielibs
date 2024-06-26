--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Fix usage of golden image in recovery
        * Consolidating lookup of golden_image from recovery_info so that it is properly used when defined.
    * Modified configure_rommon_tftp
        * Updated code to handle all possible variation of image handling
    * Modified device_rommon_boot
        * Changed sequence of condition when image is not passed in clean yaml
    * Modified delete_local_file
        * Added timeout to delete_local_file
    * Modified delete_unprotected_files to force delete
    * Modify get_boot_time
        * Added a check to split and parse the uptime_str more robustly by handling the 'hours' and 'minutes' parts individually.
        * Added initialization for hours and minutes to ensure they default to 0 if not found in uptime_str.
    * Modified request_system_shell
        * Added functionality to pass list of commands to execute
    * Fix copy_file API
        * Added timeout optional variable to the copy_file API to allow the user to


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added API config_replace_to_flash_memory_force
        * Added API to configure replace to flash memory force
    * Added `get_power_supply_info` to retrieve power_supply information of respective components under cat9k/c9300
    * udld
        * Added unconfigure_udld_recovery
    * Added configure_interface_dot1q_ethertype
    * Added configure_subinterface_second_dot1q
    * policy_map
        * Added configure_policy_map_set_cos_cos_table
            * command policy-map {policy-map name}
            * command class {class name}
            * command set cos cos table {table name}
    * table_map
        * Added configure_table_map_set_default
            * command table-map {table_map_name}
            * command default {copy or ignore or any value}
    * Added API verify_interface_status_duplex
        * This API is used to verify the interface status duplex
    * Added new API verify_cdp_neighbors_interface
        * Verifies if the CDP neighbors of a device are connected to the specified interface.
    * Added new API get_cdp_neighbor_port_id
        * Added new API to get the port id of the CDP neighbor.
    * Added configure_flow_monitor
        * New API to configure flow monitor
    * Added `get_power_supply_info` to retrieve power_supply information of respective components under cat9k/c9400.
    * Added `get_platform_fan_speed` to retrieve fan_speed of respective fan components under cat9k/c9300
    * Added configure_tunnel_mode_gre_multipoint
        * API for configure tunnel mode gre multipoint
    * Added unconfigure_tunnel_mode_gre_multipoint
        * API for unconfigure tunnel mode gre multipoint
    * Added configure_tunnel_source
        * API for configure tunnel source
    * Added unconfigure_tunnel_source
        * API for unconfigure tunnel source
    * Added configure_ip_nhrp_network_id
        * API for configure ip nhrp network id
    * Added unconfigure_ip_nhrp_network_id
        * API for unconfigure ip nhrp network id
    * Added configure_ip_nhrp_redirect
        * API for configure ip nhrp redirect
    * Added unconfigure_ip_nhrp_redirect
        * API for unconfigure ip nhrp redirect
    * Added configure_ip_nhrp_redirect
        * API for configure ip nhrp redirect
    * Added unconfigure_ip_nhrp_redirect
        * API for unconfigure ip nhrp redirect
    * Added configure_ip_nhrp_map
        * API for configure ip nhrp map
    * Added unconfigure_ip_nhrp_map
        * API for unconfigure ip nhrp map
    * Added configure_ip_nhrp_map_multicast
        * API for configure ip nhrp map multicast
    * Added unconfigure_ip_nhrp_map_multicast
        * API for unconfigure ip nhrp map multicast
    * Added configure_ip_nhrp_nhs
        * API for configure ip nhrp nhs
    * Added unconfigure_ip_nhrp_nhs
        * API for unconfigure ip nhrp nhs
    * Added configure_ip_nhrp_authentication
        * API for configure ip nhrp authentication
    * Added unconfigure_ip_nhrp_authentication
        * API for unconfigure ip nhrp authentication
    * Added configure_nhrp_group
        * API for configure ip nhrp group
    * Added unconfigure_ip_nhrp_group
        * API for unconfigure ip nhrp group
    * Added configure_ip_nhrp_map_multicast_dynamic
        * API for configure ip nhrp map multicast dynamic
    * Added unconfigure_ip_nhrp_map_multicast_dynamic
        * API for unconfigure ip nhrp map multicast dynamic
    * Added new API verify_interface_config_no_speed
        * Added new API to verify interface configuration without speed.




