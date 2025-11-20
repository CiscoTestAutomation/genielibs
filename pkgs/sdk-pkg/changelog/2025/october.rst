--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe/c9200_480p
    * Added APIs to retrieve device recovery details and tftp boot command details for C9200-48P devices

* iosxe
    * Added unconfigure_device_sgt
        * API to execute no cts sgt
    * Added execute_hardware_qfp_active_feature_nat_datapath_pap_laddrpergaddr
        * show platform hardware qfp active feature nat datapath pap laddrpergaddr
    * Added API execute_platform_hardware_chassis_fantray_oir
        * Added API to execute_platform_hardware_chassis_fantray_oir
    * Added API disable_bfd_static_route
        * Added API to disable_bfd_static_route
    * Added API disable_ospf_bfd_all_interfaces
        * Added API to disable_ospf_bfd_all_interfaces
    * Added API configure_crypto_pki_certificate_map
    * Added API unconfigure_crypto_pki_certificate_map
    * Added API unconfigure_crypto_map
        * Added API to unconfigure_crypto_map
    * Added API configure_dynamic_cmap
        * Added API to configure_dynamic_cmap
    * Added API configure_pki_vrf_trustpoint
    * Added API unconfigure_pki_vrf_trustpoint
    * Added API remove_grant_auto
    * Added API crypto_pki_trustpool_import
    * Added API configure_trustpool_policy
    * Added API unconfigure_trustpool_policy
    * Added API unconfigure_autovpn
    * Added configure_diagnostic_schedule_module_test_all_daily
        * API to schedule diagnostic on module daily at specified time
    * Added unconfigure_diagnostic_schedule_module_test_all_daily
        * API to unschedule diagnostic on module daily at specified time
    * Added support for configuring IPv6 local pool on IOSXE devices.
    * Added configure_cts_reconciliation_period
        * API to configure CTS SXP reconciliation period
    * Added unconfigure_cts_reconciliation_period
        * API to unconfigure CTS SXP reconciliation period
    * Added configure_cts_retry_period
        * API to configure CTS SXP retry period
    * Added unconfigure_cts_retry_period
        * API to unconfigure CTS SXP retry period
    * Added unconfigure_cts_sxp_default_source
        * API to unconfigure source IPv4 and IPv6 address
    * Added configure_cts_sxp_default_source
        * API to configure source IPv4 and IPv6 address
    * Added API configure_class_map_match_protocol_attribute
        * Added API to configure class map match protocol attribute
    * Added API configure_mpls_ldp_neighbor_labels_accept
    * Added API unconfigure_mpls_ldp_neighbor_labels_accept
    * Added API configure_mpls_ldp_session_protection
    * Added API unconfigure_mpls_ldp_session_protection
    * PKI
        * import_pkcs12_tftp
        * export_pkcs12_tftp
    * Added API execute_crypto_pki_server_advanced
    * Added API unconfigure_crypto_map_entry
        * Added API to unconfigure_crypto_map_entry
    * Added support for unconfiguring IPv6 local pool on IOSXE devices.
    * Added API configure_crypto_pki_export_pkcs12_terminal
        * Added API to configure_crypto_pki_export_pkcs12_terminal
    * Added execute_show_debug to debug-execute.py file.
        * New API support for 'show debug' cli.
    * Added execute_show_platform_hardware_qfp_active_feature_nat_datapath_bind to platform-execute.py
        * New API support for 'show platform hardware qfp active feature nat datapath bind' cli
    * Added execute_show_platform_hardware_qfp_active_feature_td_datapath_statistics_clear to platform-execute.py
        * New API support for 'execute_show_platform_hardware_qfp_active_feature_td_datapath_statistics_clear' cli
    * Added execute_show_policy_firewall_config_platform to platform-execute.py file.
        * New API support for 'show policy-firewall config platform' cli with filter options.
    * Added execute_test_voice_port_detector_ring_trip to platform-execute.py
        * New API support for 'test voice port {port} detector ring-trip {on-off-disable}' cli
    * Added API for get_monitor_event_trace_crypto_ipsec_event_from_boot_detail
        * 'show monitor event-trace crypto ipsec event from-boot detail'
    * Added new API to configure EAP-FAST method profile
        * API to configure EAP-FAST method profile
    * Added new API to unconfigure EAP-FAST method profile
        * API to unconfigure EAP-FAST method profile
    * Added new API to configure EAP-FAST method password
        * API to configure EAP-FAST method password
    * Added new API to unconfigure EAP-FAST method password
        * API to unconfigure EAP-FAST method password
    * Added new API to configure MAB request attribute 2 password
        * API to configure MAB request attribute 2 password
    * Added new API to unconfigure MAB request attribute 2 password
        * API to unconfigure MAB request attribute 2 password
    * Added new API to configure dot1x credential profile
        * API to configure dot1x
    * Added API to attach an alarm profile to an interface.
    * Added API to detach an alarm profile from an interface.
    * Added API to configure/unconfigure input alarm facility
    * Added `get_environment_alarm_contact`
    * Added API get_hardware_led_status to retrieve the hardware LED status of a device.
    * Fixed an issue where unconfiguring alarm contact did not work as expected.
    * Added execute_show_ethernet_cfm_maintenance_points_remote,execute_show_ethernet_cfm_maintenance_points_local,execute_show_ethernet_cfm_errors to ethernet-execute.py file.
        * New API support for 'show ethernet cfm maintenance-points remote' cli.
        * New API support for 'show ethernet cfm maintenance-points local' cli.
        * New API support for 'show ethernet cfm errors' cli.
    * Added 'execute_show_monitor_event_trace_crypto_all' and 'execute_show_monitor_event_trace_crypto_ipsec_event_clock' to iosxe crypto-execute.py file.
        * New API support for 'show monitor event-trace crypto all' cli.
        * New API support for 'show monitor event-trace crypto ipsec event clock {hh}{mm}' cli.
    * Added show_tech_support_firewall to support - tech_support.py
        * New API support for 'show tech-support firewall' cli
    * Added test_platform_software_process_exit_forwarding_manager to iosxe-platform-execute.py
        * New API support for 'test platform software process exit forwarding-manager {processor} {state}' cli

* c9800-cl
    * Added configure_autoboot
        * API to execute configure autboot

* sdk-pkg
    * iosxe
        * Update the execute_copy_run_to_start api to return a boolean indicating success or failure
        * Added new api collect install log to debug the install image failures
    * 9300
        * Added support to collect install logs to debug failure in 9300 platform
    * iosxe/c9400
        * Added execute clear install state api for c9400 devices
    * iosxe/cat8k
        * Added execute_rommon_reset and execute_config_register api for cat8k devices

* iosxe/stack
    * Added API configure_crypto_autovpn_vpn_registry
        * Added API to configure_crypto_autovpn_vpn_registry
    * Added API configure_virtual_template_for_autovpn
        * Added API to configure_virtual_template_for_autovpn
    * Added API configure_crypto_ikev2_profile_autovpn
        * Added API to configure_crypto_ikev2_profile_autovpn
    * Added API configure_dmvpn_tunnel
        * Added API to configure DMVPN tunnel
    * Added API configure_dynamic_tunnel.
    * Added API get_platform_default_dir
        * Added API to get_platform_default_dir
    * Added API free_up_disk_space
        * Added API to free up disk space
    * Added API unconfigure_crypto_keyring
        * Added API to unconfigure keyring.

* added api configure_trust_device_on_interface
    * Added API to configure trust device on interface

* iosxe/dual_rp
    * Added API get_platform_default_dir
        * Added API to get_platform_default_dir
    * Added API free_up_disk_space
        * Added API to free up disk space

* powercycler module
    * Added
        * Support for power cycling of virtual machines in vCenter


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_route_map_permit to fix a integration case
        * When default_recursive is passed as True do not configure set vrf clause
    * Modified configure_route_map_permit to add few arguments
        * Added normal_nhop_ip for direct next hop address
    * Modified unconfigure_route_map_permit to add few arguments
        * Added normal_nhop_ip for direct next hop address
    * Modified API configure_access_map_match_ip_mac_address
        * Modified to support all output
    * Fixed API configure_crypto_map_entry
        * Fixed API to configure_crypto_map_entry
    * rommon
        * Setting the context of boot cmd to grub_breakboot handler.
        * Removed the escape character pattern from the connection dialog to not interfere with the breakboot detection.
    * Added new parameters in API configure_crypto_pki_server
    * Added new parameters in API configure_trustpoint
    * Fixed an issue in API configure_crypto_pki_download_crl
    * Added new Day choices in unconfigure_crypto_pki_download_crl
    * Pki
        * Added additional dialogs to configure_pki_enroll.
        * Added additional dialogs to change_pki_server_state
    * fixed API configure_crypto_pki_profile.
    * fixed API unconfigure_crypto_pki_profile.
    * Added parameters split_horizon, passive_interface and af_interface_shutdown to the API configure_eigrp_named_networks_with_af_interface to enhance its functionality.
    * updated remote_prefix, remote_ipv6_prefix parameters to use in correct CLI
    * updated API configure_ikev2_proposal with additional arguments to configure.
        * Added arguments ake_algos, ake_required
    * FlexVPN Fixed the issue where the API did not correctly configure NHRP redirect for IPv4 and IPv6 in FlexVPN tunnel interfaces.
    * updated API with additional arguments to configure.
    * Added new parameters in API configure_tunnel_with_ipsec
    * Health
        * Added a support to handle the notifying for new core files added.
    * Enhanced existing API `set_platform_soft_trace_debug` to handle `rp="RP"` case by
    * No changes were made to the switch-specific logic.
    * updated API with additional arguments to configure.
    * rommon
        * Fix the attribute error in send_break_boot api.
    * execute_install_one_shot
        * Added install_timeout post install to wait for reload.
    * Modified get_flow_monitor_cache_format_table_output to take timeout as input parameter as the output was getting truncated
    * Added timeout parameter to the API
    * Modified question_mark_retrieve API
        * Fixed prompt regex handling in question_mark_retrieve API to support flexible trailing characters.
    * Modified device_rommon_boot
        * Updated the code to extract the TFTP image from recovery information and provide it to the ROMMON TFTP configuration api's.
    * Modified delete_files
        * Enhanced to handle both relative and absolute file paths.
    * Made few changes in 'unconfigure_alarm_contact'

* iosxe/cat9k/c9400
    * Modified execute_install_one_shot to execute when device reloads

* iosxe/c8kv
    * rommon
        * Added `send_break_boot` api for c8kv devices to send break sequence during bootup to enter rommon mode.

* utils
    * Added build_export_filename
        * Added build_export_filename to preserve .tar.gz extension when copying files from device to local system.
    * Added configure_stealthwatch_cloud_monitor & unconfigure_stealthwatch_cloud_monitor
        * Added unconfigure_stealthwatch_cloud_monitor to configure stealtchwatch CLI & unconfigure them.

* generic
    * Update copy_to_device and copy_from_device APIs
        * use 'ip route get' to get source IP address of proxy host

* iosxe/ie3k
    * Modified
        * Included missing arguments of `execute_set_config_register` to match its function signature to the base API.

* updated timeout for api
    * Iosxe
        * Added the timeout fpr API.

* iosxe/c9400
    * Modified execute_install_one_shot api reverted the condtion for output from PR-3757

* fix the gh auth issue in jenkinsfile.

* updated unittests
    * IOSXE
        * Updated below API unit tests with the latest unit testing methodology
            * copy_file_with_scp

* iosxe/install
    * Modified execute_install_activate to execute when device reloads
    * Fixed the modification and removed the execution of default reload when 'command=cmd' called.

* iosxe/rommon/utils

* triggers
    * Removed all usage of deprecated pkg_resources module in favor of importlib.metadata where possible.


