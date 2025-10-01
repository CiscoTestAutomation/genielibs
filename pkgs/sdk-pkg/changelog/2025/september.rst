--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added execute_test_platform_hardware_sensor_value
        * API to execute_test_platform_hardware_sensor_value
    * Added enable_cts_sxp
    * Added disable_cts_sxp
    * Added configure_cts_sxp_default_password
    * Added unconfigure_cts_sxp_default_password
    * Added enable_cts_sxp_connection
    * Added disable_cts_sxp_connection
    * Added API to get the maximum and minimum temperature from the device alarm settings.
    * cat8k
        * Added api to configure no boot manual
    * c8kv
        * Added api to configure no boot manual
    * Added execute_clear
        * API to execute clear {parameter}
    * Added API configure_ipv6_cef
    * Added API unconfigure_ipv6_cef
    * Modified API `configure_standard_access_list`
        * Made 'wild_mask' as optional argument.
    * Modified API `unconfigure_standard_access_list`
        * Made 'wild_mask' as optional argument.
    * Added API to configure/unconfigure Relay mode negative
    * Added API test_platform_hardware_powersupply_oir
        * Added API for doing PSU OIR
    * cat9kv
        * Added API test_platform_hardware_chassis_fantray_action
        * Added API configure_autolc_shutdown_priority
    * Added clear_cts_environment_data
        * API to clear cts environment-data
    * Modified configure_ip_role_based_acl
        * Added support for source and destination port range
    * Added API unconfig_trust_points
        * Added API to unconfig_trust_points
    * IKE
        * configure_isakmp_key_simple
        * unconfigure_isakmp_key_simple
    * Added API execute_hw_module_beacon_fan_tray
    * Added API execute_hw_module_subslot_oir
    * Added API configure_platform_ip_multicast_ssdp
    * Added API unconfigure_platform_ip_multicast_ssdp
    * Added API to configure alarm profile
    * Added API to unconfigure alarm profile
        * Added support for configuring alarm profiles with options such as contact, severity, description, name, trigger, and type.
        * The API allows setting the configuration options to 'no' and specifying the expected settings for power supply alarms.
        * Added support for configuring and unconfiguring notifications for alarm profiles.
        * Added support for configuring and unconfiguring relay settings for alarm profiles.
        * Added support for configuring and unconfiguring syslog settings for alarm profiles.
    * Added API configure_extended_access_list
        * Added API to configure_extended_access_list
    * Added API configure_ptp_ttl
    * Added API unconfigure_ptp_ttl
    * Added execute_trim_crypto_pki_certificate
        * API to execute_trim_crypto_pki_certificate
    * Added config API configure_ikev2_disconnect_revoked_peers
    * Added API to configure facility alarm temperature primary
        * Added support for configuring the primary temperature threshold for facility alarms.
        * The API allows setting the temperature threshold to 'high' and specifying the value.
    * Added API to unconfigure facility alarm temperature primary
        * Added support for unconfiguring the primary temperature threshold for facility alarms.
        * The API allows removing the temperature threshold configuration.
        * Added support for configuring and unconfiguring notifications for primary temperature alarms.
        * Added support for configuring and unconfiguring relay settings for primary temperature alarms.
        * Added support for configuring and unconfiguring syslog settings for primary temperature alarms.
    * Added API configure_with_submode
        * Added API to configure_with_submode
    * Added API configure_with_submode
        * Added API to configure_with_submode

* iosxe/cat9k
    * c9400
        * Added new api to execute config register


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Fixed issue with 'question mark' not working in certain command modes.
    * Unconfigure_banner
        * Added fix for Unconfigure_banner to make it compatible
    * Modified
        * Added support for handling reload triggered by `%PMAN-5-EXITACTION reload action requested`

* sdk-pkg
    * Fix syntax warning

* iosxe/sdk-pkg
    * Updated the configure management vrf api


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Added logic for to execute log messages
        * Added logic for to execute log messages beased on the edit operations
    * Modified unconfigure_modify_ikev2_profile
        * Modified the api unconfigure_modify_ikev2_profile
    * Modified configure_radius_group
        * Modified the configure_radius_group to add changes for ipv6 source interface.


