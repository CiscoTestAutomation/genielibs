--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* iosxe
    * Added configure_autoboot API
        * Sets the configuration register to 0x2102.
    * Added device tracking API for IOSXE.
        * API to verify device tracking database: verify_device_tracking_database
    * Added unit test coverage for the new API.
    * Added certificate storage APIs for inventory, reference discovery, deletion, verification, and storage usage reporting.
    * Allowed extra time to inventory large certificate directories over slow console connections.
    * Made stack deletion idempotent when IOS XE synchronizes an active member's certificate removal to its standby member.
    * Added stack and dual-RP implementations that operate through connected member subconnections and their local ``nvram:`` storage.
    * Added VRF and global address-family route-replicate configure APIs.
        * API to configure_vrf_route_replicate_from_vrf.
        * API to unconfigure_vrf_route_replicate_from_vrf.
        * API to configure_global_route_replicate_from_vrf.
        * API to unconfigure_global_route_replicate_from_vrf.
    * Added unit test coverage for the new APIs.
    * Added verify_ip_access_list
        * API to verify IP access list
    * Added BGP VRF cleanup APIs.
        * API to unconfigure_bgp_address_advertisement.
        * API to unconfigure_bgp_advertise_l2vpn_evpn.
    * Added unit test coverage for the new APIs.
    * Added iosxe dot1q tunnel configuration view API support
        * New API support for 'configure_interface_switchport_dot1q_tunnel' CLI command to configure dot1q tunnel on interface
    * Added SDK API support for
        * configure_interface_spanning_tree_port_priority
        * configure_interface_spanning_tree_vlan_cost
        * unconfigure_interface_spanning_tree_vlan_cost
        * configure_spanning_tree_pathcost_method
    * Added unit test coverage for spanning-tree APIs.
    * Added running-config verify APIs for IOSXE.
        * API to verify_show_running_config_section.
    * Added unit test coverage for the new API.

* iosxe/cat9k/c9800
    * Added ``configure_wireless_management`` API to configure the C9800 WMI uplink, Layer 3 interface, routes, wireless binding, and AP management credentials.
    * Updated ``configure_management_ip`` to allow callers to disable fallback to the generic device management VRF, keeping the WMI in the global VRF.
    * Added unit coverage for WMI orchestration, input validation, same-VRF gateway conflict handling, and management VRF fallback behavior.
    * Corrected ``configure_management_routes`` to render IPv6 entries with ``ipv6 route`` commands, including VRF routes.
    * Added APIs
        * configure_ap_tx_power
        * configure_rrm_dca_channel
        * verify_ap_fabric_summary
        * verify_ap_mode
        * verify_access_tunnel_summary
        * verify_ha_state
        * verify_installation_mode
        * verify_wireless_process

* iosxr
    * Added configure_static_routing_route
        * API to configure a static route, taking ``prefix``, ``next_hop``, an optional ``address_family`` (``ipv4``/``ipv6``) and an optional ``vrf``. Returns the configuration that was applied and raises ``SubCommandFailure`` when the device rejects it.
    * Added unconfigure_static_routing_route
        * API to remove a static route, taking the same arguments as ``configure_static_routing_route`` so only the exact route that was configured is removed.
    * Added get_routing_route_next_hop
        * API to look up the next hop details for a route, taking ``route``, an optional ``address_family`` (derived from ``route`` when not given) and an optional ``vrf``.


--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* iosxe
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_mdns_gateway_globally
        * test_api_unconfigure_mdns_global_service_buffer
        * test_api_unconfigure_mdns_location_filter
        * test_api_unconfigure_mdns_remote_cache_enable
        * test_api_unconfigure_mdns_remote_cache_max_limit
        * test_api_unconfigure_mdns_remote_purge_timer
        * test_api_unconfigure_mdns_service_policy
        * test_api_unconfigure_mdns_service_policy_vlan
        * test_api_unconfigure_mdns_trust
        * test_api_unconfigure_service_type_mdns_service_definition
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified configure_interface_storm_control_level API
        * Updated the API to return the output of the configuration command instead of None.
        * Updated unit test in test_api_configure_interface_storm_control_level.py accordingly.
    * Improved cleanup performance by verifying free space with a bounded filesystem query after each deletion batch.
    * Protected running images and system, configuration, and NVRAM files.
    * Updated configure_autoboot to use execute_set_config_register so platform-specific boot behavior and HA connection handling are preserved for IOS XE devices.
    * Added C9800 and C9800-CL support for the full ``config-register 0x2102`` command. Physical Catalyst 9000 platforms continue to use their ``boot manual`` equivalent.
    * Modified configure_ikev2_profile_pre_share
        * modified configure_ikev2_profile_pre_share
    * Modified send_break_boot API to stop sending additional console break characters after detecting the ROMMON switch: prompt.
    * Modified configure_management_master_key to increase the master key configure timeout from 120s to 300s, fixing a ConfigureManagement clean stage timeout on some platforms (e.g. IE9xxx) when no master key is yet configured and key generation takes longer than the previous timeout. Also added defensive handling for the 'New key:' and 'Confirm key:' prompts in case a platform prompts interactively instead of accepting the key inline.
    * Improved IE3K and IE9K ROMMON recovery error reporting when the default ROMMON boot command fails and no golden image is available.
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_ipv6_mld_snooping
        * test_api_configure_ipv6_mld_snooping_querier
        * test_api_configure_ipv6_mld_snooping_querier_version
        * test_api_configure_ipv6_mld_snooping_vlan_querier_version
        * test_api_unconfigure_ipv6_mld_snooping
        * test_api_unconfigure_ipv6_mld_snooping_querier
        * test_api_unconfigure_ipv6_mld_snooping_querier_version
        * test_api_unconfigure_ipv6_mld_snooping_vlan_querier_version
        * test_api_config_no_keepalive_intf
        * test_api_config_qinq_encapsulation_on_interface
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Fixed IE3K ROMMON recovery when hostname learning is enabled and the configured hostname differs from the device hostname.
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_interface_template_with_default_ipv6_nd_raguard_policy
        * test_api_configure_ipv6_dhcp_guard_on_interface
        * test_api_configure_ipv6_nd_raguard_on_interface
        * test_api_remove_device_tracking_policy
        * test_api_unconfigure_device_tracking_binding
        * test_api_unconfigure_device_tracking_on_interface
        * test_api_unconfigure_ipv6_dhcp_guard_on_interface
        * test_api_unconfigure_ipv6_nd_raguard_on_interface
        * test_api_configure_debug_snmp_packets
        * test_api_configure_logging_snmp_trap
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified configure_ospf_routing
        * api configure_ospf_routing now supports segment routing, fast-reroute, microloop, flex-algo, and bfd options
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_dynamic_path_in_tunnel
        * test_api_unconfigure_ip_rsvp_bandwidth
        * test_api_unconfigure_ldp_discovery_targeted_hello_accept
        * test_api_config_ip_multicast_routing_vrf_distributed
        * test_api_config_ip_pim
        * test_api_config_ip_pim_vrf
        * test_api_config_multicast_routing_mvpn_vrf
        * test_api_config_pim_acl
        * test_api_config_rp_address
        * test_api_config_standard_acl_for_ip_pim
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Modified send_break_boot
        * Fixed break-boot recovery after a refused console connection to use the actual detected device state and reliably reach ROMMON.
        * Preserved existing connected and multi-console behavior.
    * Enhanced ``configure_management_ntp``
        * Added support for configuring the NTP server in the management VRF.
    * Modified the following unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_switchport_port_security_maximum
        * test_api_configure_radius_server
        * test_api_configure_tacacs_server
        * test_api_unconfigure_radius_server
        * test_api_clear_device_tracking_counters
        * test_api_clear_device_tracking_database
        * test_api_clear_device_tracking_messages
        * test_api_configure_device_tracking_on_interface
        * configure_interface_template_with_default_device_tracking_policy
        * configure_interface_template_with_default_ipv6_dhcp_guard_policy
    * Removed mock_data.yaml files for the above tests as they are no longer needed
    * Fixed question-mark command cleanup to send Ctrl-A followed by Ctrl-K instead of Ctrl-C.
    * Added unit coverage to verify the control sequence used by ``question_mark_retrieve``.
    * Modified unconfigure_key_config_key_password_encrypt
        * Added backward-compatible password argument alongside old_key
        * no key config-key password-encrypt
    * Removed duplicate unconfigure_key_config_key_password_encrypt from platform
    * Modified execute_set_config_register
        * Added the optional preserve_console_speed argument. At rommon, when explicitly enabled for '0x0', writes each connection's hex(current & 0x1820) so its console-speed bits survive.
        * Retained the Cat9K manual-boot behavior; Cat9K does not execute confreg when console-speed preservation is requested.
        * Added support for the argument to the C9800 override, which retains the IOS-XE config-register behavior.
    * Modified password_recovery
        * Explicitly requests console-speed preservation when setting '0x0'.

* generic
    * Improved ``free_up_disk_space`` reliability and safety by batching deletions, reusing directory listings, and stopping when free space cannot be verified.

* apic
    * Restricted cleanup to valid regular files while preserving protected-file behavior.

* iosxr
    * Improved handling of regular files, directories, and symlinks during cleanup.

* nxos
    * Restored cleanup of file entries from ``dir`` output without permission metadata while excluding directory names ending in ``/``.

* iosxe/cat9k/c9800
    * Organized C9800 API tests under the Cat9K C9800 hierarchy.

* iosxe/cat9k/c9800/c9800_cl
    * Moved the management-IP API that defaults to ``no switchport`` under the C9800-CL submodel hierarchy so physical C9800 devices use the generic IOS XE behavior.
    * Moved GRUB-specific boot interruption defaults from physical C9800 to C9800-CL.

* iosxe/ir1k/ir1101
    * Added a platform-specific configure_no_boot_manual override
        * Uses the existing configure_autoboot API to set the configuration register to 0x2102 instead of sending the unsupported no boot manual command.


--------------------------------------------------------------------------------
                                    Modified
--------------------------------------------------------------------------------

* iosxe
    * Enhanced "execute_monitor_capture_access_list"
        * Added optional parameters interface,direction,file_path


