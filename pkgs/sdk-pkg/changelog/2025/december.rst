--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* iosxe/install
    * Added dialog from failed senario in install one shot
    * Added dialog from failed senario in install one shot

* iosxe/cat9k/c9400
    * Added dialog from failed senario in install one shot

* utils
    * Added get_server_certificate_pem API

* iosxe
    * dns
        * configure_ip_host
            * Added VRF support
        * unconfigure_ip_host
            * Added VRF support

* iosxr
    * dns
        * added configure_ip_host
        * added unconfigure_ip_host
    * pki
        * added configure_trustpoint
        * added unconfigure_trustpoint
        * added configure_pki_authenticate_certificate

* nxos
    * dns
        * added configure_ip_host
        * added unconfigure_ip_host
    * pki
        * added configure_trustpoint
        * added unconfigure_trustpoint
        * added configure_pki_authenticate_certificate


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_bgp_tcpao API
        * API to configure BGP TCP Authentication Option for bgp neighbor
    * Added unconfigure_bgp_tcpao API
        * API to remove BGP TCP Authentication Option for bgp neighbor
    * Added configure_tcp_keychain API
        * API to configure TCP-AO keychain on device
    * Added remove_tcp_keychain API
        * API to remove TCP-AO keychain from device
    * Added configure_bgp_md5 API
        * API to configure BGP MD5 authentication on BGP router
    * Added unconfigure_bgp_md5 API
        * API to unconfigure BGP MD5 authentication on BGP router
    * PKI
        * configure_pki_export_advanced
        * configure_pki_import_advanced
        * change_pki_certificate_hash
    * sdk-pkg
        * Updated configure_management_gnmi api
            * Made default value of 'secure_server' parameter as True.
    * Added configure_bgp_ipv6_dampening
        * New API to configure bgp dampening parameters for IPV6 address family
    * PKI
        * execute_return_crypto_pki_server
    * Added unconfigure_ip_ssh_client_algorithm_kex API support for the CLI command
        * New API support for 'unconfigure ip ssh client algorithm kex' CLI command to unconfigure key exchange algorithms for SSH client on IOSXE devices.
    * Added unconfigure_ip_ssh_server_algorithm_kex API support for the CLI command
        * New API support for 'unconfigure ip ssh server algorithm kex' CLI command to unconfigure key exchange algorithms for SSH server on IOSXE devices.
    * sdk-pkg
        * Updated `configure_management_credentials` and `unconfigure_management_credentials` APIs to use secret password instead of plain text password.
        * Updated `configure_management_ssh` to set modulus size to 4096 bits while generating RSA keys.
    * Added 'execute_test_platform' to iosxe test_platform-execute.py file.
        * New API support for 'test platform' cli.
    * Added API to execute test led cli command
    * Added suport for verify ping api to support new parameters
    * Added execute_test_platform_hardware_sensor_value_cm
        * API to execute_test_platform_hardware_sensor_value_cm
    * Added API get_alarm_contact_relay_mode to retrieve the alarm contact relay mode configuration.
    * Added API get_interfaces_connect_status to retrieve interfaces with connect/not connect status.
    * configure_aaa_group_radius_interface
        * Added support for IPv6 address configuration
        * Added 'protocol' parameter to specify protocol type (default is 'ip')
        * Added 'forwarding' parameter to enable/disable vrf forwarding
    * unconfigure_aaa_group_radius_interface
        * Added support for IPv6 address unconfiguration
        * Added 'protocol' parameter to specify protocol type (default is 'ip')
        * Added 'forwarding' parameter to enable/disable vrf forwarding

* sdk-pkg
    * update ruamel.yaml.clib to avoid break from 0.2.15 release

* apis/utils.py
    * Default to SCP for file copy operations using the copy_from_device and copy_to_device APIs

* nxos/utils
    * Device Boot Recovery


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Updated api configure_key_config_key_password_encrypt
        * updated api with new dialog pattern
    * Updated api unconfigure_key_config_key_password_encrypt
        * updated api with new dialog pattern
    * Install
        * Added statement in execute_install_one_shot.
        * Added install_timeout to execute_install_activate.
    * cat9k/c9500x
        * Added __init__ file.
    * Modified perform_telnet API
        * Added support to execute command on remote_device before exit the telnet.
    * Added new parameter in API configure_crypto_ikev2_proposal
    * configure_radius_interface_vrf Added support for IPv6 address configuration
        * Added 'protocol' parameter to specify protocol type (default is 'ip')
    * unconfigure_radius_interface_vrf Added support for IPv6 address unconfiguration
        * Added 'protocol' parameter to specify protocol type (default is 'ip')
    * configure_radius_group Added support for IPv6 address configuration
        * Added 'ipv6_addr' in server_config to configure IPv6 address for RADIUS server


