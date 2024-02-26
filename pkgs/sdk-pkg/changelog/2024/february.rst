--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added unconfigure_policy_map_with_pps
        * New API to unconfigure policy-map pps
    * Added api test_configure_cdp_1
        * added api for validate show interface {interface}
    * Added configure_ip_http_client_secure_trustpoint
        * API to configure_ip_http_client_secure_trustpoint
    * Added hw_module_filesystem_security_lock
        * API to enable/disable filesystem's security-lock
    * Added API verify_interface_capabilities_multiple_media_types
        * Added API to verify the interface media type
    * Added API verify_interfaces_transceiver_supported
        * Added API to verify the transceivers supported in the device
    * Updated `configure_management_gnmi` API to support secure server
    * Modified `generate_rsa_ssl_key` API to support legacy 3des
    * Modified `get_file_contents` API, added removal of carriage return option
    * Modified `configure_pki_import`, added device key and root CA options
    * Added new api `generate_pkcs12` to generate pkcs12 file.
    * Added API unconfigure_ip_igmp_querier_query_interval
        * Added API for unconfigure ip igmp querier query interval
    * Added API unconfigure_ip_igmp_querier_max_response_time
        * Added API for unconfigure ip igmp querier max response time
    * Added API unconfigure_ip_igmp_querier_tcn_query_count
        * Added API for unconfigure ip igmp querier tcn query count
    * Added API unconfigure_ip_igmp_querier_tcn_query_interval
        * Added API for unconfigure ip igmp querier tcn query interval
    * Added API unconfigure_ip_igmp_querier_timer_expiry
        * Added API for unconfigure ip igmp querier timer expiry

* api utils
    * Add
        * check_and_wait decorator

* makefile
    * Added pyasyncore dependency to fix pysnmp script


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* linux
    * Add api get_valid_ipv4_address
        * added api to validate and return ipv4 address
    * Add api get_ip_route_for_ipv4
        * added api to get the routing ip form routing table
    * Modified get_snmp_snmpwalk
        * Added timeout parameter to increase timeout of execute operation

* iosxe/rommon
    * configure
        * Updated `configure_rommon_tftp` API to set TFTP_FILE as the rommon variable.
    * utils
        * Updated `device_rommon_boot` API with a an option to boot using TFTP_FILE.

* iosxe
    * Modified configure_sdm_prefer_custom_template
        * added parameters custom_template, entried and priority
    * Modified get_snmp_snmpwalk
        * Added timeout parameter to increase timeout of execute operation
    * `get_running_config_dict` API
        * Added `output` parameter to pass the output of `show running-config` command.


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_virtual_template
        * modified api to configure ipv6_pool_name


