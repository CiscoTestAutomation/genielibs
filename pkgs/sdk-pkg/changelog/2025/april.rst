--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added configure_ntp_auth_key
        * API to configure NTP authentication key.
    * Added configure_ntp_authenticate
        * API to configure NTP authentication.
    * Added configure_ntp_trusted_key
        * API to configure NTP trusted key.
    * Added configure_ntp_server_with_auth
        * API to configure NTP server with authentication.
    * Added configure_no_ntp
        * API to remove complete NTP configuration.
    * Added configure_tftp_server
        * API to configure a TFTP server with the specified file path.
    * Added configure_vlan_and_no_shutdown
        * API to configure VLAN and no shutdown on a device.
    * Added API configure_radius_server_dtls_port
        * API to Configure radius server dtls port
    * C9400
        * Added execute_install_one_shot
            * API to execute_install_one_shot
    * Added configure_logging_ipv6
        * API to configure logging ipv6
    * Added unconfigure_data_mdt
        * API to unconfigure data mdt
    * Added no ip pim send-rp-announce Loopback0 scope 10
    * Added API configure_ipv6_logging_with_transport_and_facility
        * API to Configure IPv6 logging with transport and facility on the device.
    * Added API redirect_igmp_snooping_group_info
        * API to redirect igmp snooping from the command output to a file in bootflash of the device
    * Added support for below to get output in bootflash
        * show tech-support platform layer3 multicast group_ipadd {grp} srcIp {src_ip}
        * show tech-support platform layer3 multicast vrf {vrf} group_ipv6Addr {grp_ipv6} srcv6Ip {src_ipv6}
        * show tech-support platform layer3 multicast group_ipv6Addr {grp_ipv6} srcv6Ip {src_ipv6}
    * Added API show_tech_support_platform_interface
        * API to get show tech-support platform interface <interface_name> to copy device output to a file in bootflash
        * API to get show tech-support platform interface port-channel <port_id> to copy device output to a file in bootflash
    * Added API show_tech_support_platform_l2
        * API to Redirect the VLAN, interface, or port-channel-specific information from the command output to a file in bootflash of the device
    * Added API show_tech_support_platform_l2_matm
        * API to get VLAN or MAC address-specific information from the command output to a file in bootflash of the device
    * Added API show_tech_support_platform_mld_snooping
        * API to get show tech-support platform mld_snooping Group_ipv6Addr {grp_ipv6} vlan {vlan_id} | redirect bootflash{file_name} to copy device output to a file in bootflash
    * Added API show_tech_support_platform_monitor
        * API to get show tech-support platform monitor <session_id> to copy device output to a file in bootflash
    * Added configure_fec_auto_off
        * API to configure fec auto/off on 10G interface.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_snmp_server_user API
        * Added support for 3des as a valid priv_method
        * Modified to return device CLI output
    * Modified APi configure_ip_pim_bsr_rp_candidate
        * Fixed handling of rp and bsr flags to ensure proper configuration.
        * Added handling with negate_bsr and negate_rp to ensure accurate unconfiguration.
    * Modified
        * Updated configure_span_monitor_session API with optional argument to specify the monitor session source.

* apis
    * APIUTGenerator
        * Fix issue where API exclusion list is not properly loaded from the test arguments YAML file.

* iosxr
    * Modified
        * Removed install commit from admin mode

* sdk-pkg
    * Modified triggers and blitz
        * Fixed issue where job would get stuck during subscription poll and subscription once

* all os
    * Modified Blitz action yang_snapshot_restore to use better Xpaths
        * Xpaths with nodes that are missing prefixes are now prefixed with the

* sdk
    * Bumped pyans1 version


--------------------------------------------------------------------------------
                                    Removed                                     
--------------------------------------------------------------------------------

* iosxe
    * Removed unconfigure_route_map
        * Removed duplicate api unconfigure_route_map.


--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* iosxe
    * Modified Ospf unconfigure_route_map
        * Modified datatype of route_map from int to str in comments.


