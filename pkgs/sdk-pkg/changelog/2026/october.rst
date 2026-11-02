--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified device_recovery_boot to pass the console start command and connection index to the selected IOS XE SD-WAN recovery worker.
    * Modified the following VLAN API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * config_vlan_range
        * config_vlan_tag_native
        * configure_vtp_domain
        * configure_vtp_password
        * configure_vtp_pruning
        * configure_vtp_trunk_interface
        * configure_vtp_version
        * unconfig_ip_on_vlan
        * unconfigure_default_switchport_trunk_vlan
        * execute_vtp_primary
    * Removed the mock_data.yaml fixtures for these tests.
    * Fixed recursive disk cleanup to skip directories that disappear during traversal and continue processing other removable files.
    * Refactored the following multicast API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_ipv6_pim_bsr_candidate_rp
        * test_api_configure_ipv6_pim_rp_address
        * test_api_configure_mld_version
        * test_api_configure_pim_register_source
        * test_api_configure_static_ip_pim_rp_address
        * test_api_configure_static_ipv6_pim_rp_address
        * test_api_disable_ip_igmp_snooping_report_suppression
        * test_api_enable_ip_igmp_snooping_report_suppression
        * test_api_unconfig_ip_multicast_routing_vrf_distributed
        * test_api_unconfig_ip_pim_vrf
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Modified the following NAT API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * execute_clear_ip_nat_translation
        * execute_clear_nat64_statistics
        * execute_clear_nat64_statistics_failure
        * execute_clear_nat64_statistics_global
        * execute_clear_nat64_statistics_interface
        * execute_clear_nat64_statistics_pool
        * execute_clear_nat64_statistics_prefix_stateful
        * execute_clear_nat64_translations_all
        * execute_clear_nat64_translations_protocol
        * execute_clear_nat_translation
    * Removed the mock_data.yaml fixtures for these tests.
    * Refactored the following multicast API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_ip_igmp_ssm_map_enable
        * test_api_configure_ip_pim_rp_candidate_priority
        * test_api_configure_ip_igmp_ssm_map_query_dns
        * test_api_configure_ip_msdp_cache_sa_state
        * test_api_configure_ip_msdp_peer
        * test_api_configure_ip_pim_bsr_candidate
        * test_api_configure_ip_pim_enable_bidir_enable
        * test_api_configure_ip_pim_rp_address
        * test_api_configure_ip_pim_ssm
        * test_api_configure_ip_msdp_vrf_peer
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Modified C8KV device_rommon_boot
        * Preserve the configured GRUB golden-image entry when recovery also contains TFTP image metadata.
    * Modified device_rommon_boot
        * Stop a ROMMON TFTP retry when the assignment returns a set usage error, before readback or boot.
    * Modified
        * configure_snmpv3_user
            * Added read_view, write_view as optional
        * configure_radius_server_secure
            * modified `SECURITY WARNING` message as log.debug
        * unconfigure_snmp_server_user
            * No entry/changes
        * configure_snmp_host_version
            * Added security_level as optional
            * Added input validation for CR/LF injection
        * unconfigure_snmp_host_version
            * Added security_level as optional
            * Added input validation for CR/LF injection
        * configure_snmp_server_host
            * Added security_level as optional
            * Added input validation for CR/LF injection
        * unconfigure_snmp_server_host
            * Added security_level as optional
            * Added input validation for CR/LF injection
        * copy_startup_config_to_scp
            * Added vrf as optional parameter to append vrf to the SCP copy command
    * Refactored the following OSPF API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_ip_ospf_mtu_ignore
        * test_api_unconfigure_ipv6_ospf_mtu_ignore
        * test_api_unconfigure_ipv6_ospf_routing_on_interface
        * test_api_unconfigure_ipv6_router_ospf
        * test_api_unconfigure_neighbor_under_ospf
        * test_api_unconfigure_ospf_area_type
        * test_api_unconfigure_ospf_cost
        * test_api_unconfigure_ospf_from_interface
        * test_api_unconfigure_ospf_network_non_broadcast
        * test_api_unconfigure_ospf_on_device
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Fixed ROMMON TFTP configuration, including HA and C9200 boot URLs, to use actual image paths rather than serialized Clean metadata.
    * Reject invalid or ambiguous TFTP images before boot. An explicit TFTP request no longer falls back to a configured golden image; existing local golden-image behavior is unchanged.
    * Reuse the provider-selected TFTP transport path across inner and outer boot retries without translating it again.
    * Stop boot on ROMMON command usage errors. On C9300/C9200 Cat9k paths, verify the environment value before each boot and reject missing or mismatched values rather than booting a stale image.
    * Matching Clean and SDK builds are required for TFTP image normalization; older Clean builds fail with an actionable import error before boot.
    * Modified send_break_boot
        * Honored configured terminal-server login prompts during breakboot reconnect and waited for device boot output before sending BREAK.
    * Refactored the following multicast API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_clear_ipv6_mld_counters
        * test_api_configure_debug_ip_pim
        * test_api_configure_igmp_version
        * test_api_configure_ip_forward_protocol_nd
        * test_api_configure_ip_igmp_access_group
        * test_api_configure_ip_igmp_join_group_source
        * test_api_configure_ip_igmp_snooping_last_member_query_interval
        * test_api_configure_ip_igmp_snooping_tcn_flood
        * test_api_configure_ip_igmp_snooping_vlan_mrouter_interface
        * test_api_configure_ip_igmp_ssm_map
    * Removed the mock_data.yaml files for these tests because they are no
    * Modified C9800-CL device_rommon_boot
        * Preserve the configured GRUB golden-image entry when recovery also contains TFTP image metadata.
    * Refactored the following API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_clear_dmvpn
        * test_api_clear_dmvpn_statistics
        * test_api_clear_ip_nhrp
        * test_api_clear_ipv6_nhrp
        * test_api_clear_bgp_all_as
        * test_api_clear_ip_bgp
        * test_api_clear_ip_bgp_af_as
        * test_api_execute_crypto_pki_server
        * test_api_execute_test_opssl_nonblockingsession_client
        * test_api_execute_test_opssl_nonblockingsession_server_stop
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Refactored the following multicast API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_configure_ip_pim_vrf_ssm_default
        * test_api_configure_ipv6_mld_access_group
        * test_api_configure_ipv6_mld_join_group_acl
        * test_api_configure_ipv6_mld_snooping_enhance
        * test_api_configure_ipv6_mld_snooping_vlan_mrouter_interface
        * test_api_configure_ipv6_mld_snooping_vlan_static_interface
        * test_api_configure_ipv6_mld_vlan
        * test_api_configure_ipv6_mld_vlan_immediate_leave
        * test_api_configure_ipv6_multicast_routing
        * test_api_configure_ipv6_pim_bsr_candidate_bsr
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Refactored the following API unit tests to use unittest.mock.Mock instead of mock_device_cli
        * test_api_unconfigure_interface_ospfv3_ipsec_esp
        * test_api_unconfigure_ip_prefix_list
        * test_api_unconfigure_ospfv3_ipsec_ah
        * test_api_unconfigure_ospfv3_ipsec_esp
        * test_api_unconfigure_ospfv3_network
        * test_api_unconfigure_redistribute_eigrp_under_ospf
        * test_api_unconfigure_route_map
        * test_api_clear_ip_ospf_rib
        * test_api_unconfig_pim_acl
        * test_api_monitor_event_trace_clear
    * Removed the mock_data.yaml files for these tests because they are no longer needed.
    * Modified request_system_shell to apply its timeout to commands executed inside the system shell.
    * Modified request_system_shell to attempt a bounded return to enable mode after a command failure without replacing the original error.
    * Added Cat8k send_break_boot
        * Interrupt boot at the system bootstrap banner using Telnet BREAK to reach ROMMON during password recovery.
    * Updated generic send_break_boot
        * Match the default console activity pattern on three or more consecutive dots.
        * Handle terminal-server authentication prompts while connecting to interrupt boot.

* iosxe/cat9k/c9800
    * Added a platform-specific configure_no_boot_manual override
        * Uses the existing configure_autoboot API to set the configuration register to 0x2102 instead of sending the unsupported no boot manual command.

* iosxe/isr1k
    * Added a platform-specific configure_no_boot_manual override
        * Uses the existing configure_autoboot API to set the configuration register to 0x2102 instead of sending the unsupported no boot manual command.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* generic sdk apis
    * Added ``collect_ping_failure_diagnostics`` to capture Cisco and optional Linux endpoint state immediately after a failed ping. The API logs each command result and continues if a diagnostic command fails.

* iosxe
    * Added IE3K and IE9K ROMMON recovery support for emergency images in ``emgy:`` and ``emgy0:``. Intentional ROMMON boot now tries emergency images before the configured Clean recovery image and then tries normal boot-filesystem images in the platform's configured regex order.

* sdk/apis/iosxe/cat9k/c9800/platform/get
    * Added C9800 APIs to verify AP registration and collect bounded failure diagnostics, including AP uptime.


--------------------------------------------------------------------------------
                                    Changed                                     
--------------------------------------------------------------------------------

* sdk/apis/cheetah/ap/verify
    * Changed AP operation-state and controller verification APIs to perform immediate checks and removed the obsolete ``max_time`` and ``check_interval`` arguments.


