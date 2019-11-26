| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v19.11      |


----------------------------------------------------------------------------
                        Fixed
----------------------------------------------------------------------------
* IOSXE
    * Updated verify_segment_routing_traffic_eng_policies:
        * To support individual policies
        * To support multiple segments in explicit paths
        * To support verifying affinity type and affinities
    * Updated get_time_source_from_output:
        * To log error if no timestamp found in output
    * Updated verify_segment_routing_policy_state:
        * To support multiple policy
    * Updated configure_ntp_server:
        * To support auth key for ntp server
    * Updated restore.py save_configuration function:
        * To support copy config to stby-bootflash
    * Updated write_erase_reload_device:
        * Add augument reload_hostname
    * Updated verify_ip_precedence_ip_precedence:
        * Add augument exclude_src_ip
    * Updated verify_ntp_association_with_server:
        * Fix logical issue
    * Updated get_routing_route_count:
        * return number of subnets instead of networks
    * Updated verify_sid_in_ospf:
        * To support passing process_id and sid
    * Updated perform_issu:
        * Add argument 'timeout' for issu section timeout

* IOS
    * Updated restore.py save_configuration function:
        * To support argument copy_to_standby

* IOSXR
    * Updated restore.py save_configuration function:
        * To support argument copy_to_standby
    * Updated management_interface.py get_interface_name function:
        * show command changed to show ipv4 interface brief

* NXOS
    * Updated restore.py save_configuration function:
        * To support argument copy_to_standby

* JUNOS
    * Updated restore.py save_configuration function:
        * To support argument copy_to_standby

* COMMON
    * Updated configure.py change_configuration_using_jinja_templates functions
        * Removed unnessary spaces when rendering

----------------------------------------------------------------------------
                        New
----------------------------------------------------------------------------
* IOSXE
    * Added get_interface_packet_input_rate
    * Added get_inserted_interface_by_media_type
    * Added verify_flow_cache_record_exists
    * Added verify_bgp_neighbor_exist
    * Added get_ospf_process_id_on_interface
    * Added remove_interface_carrier_delay
    * Added remove_interface_ospf_bfd
    * Added get_neighbor_interface_and_device_by_link
    * Added verify_interface_config_carrier_delay
    * Added verify_interface_config_ospf_bfd
    * Added is_ospf_neighbor_established_on_interface
    * Added is_ospf_neighbor_state_changed_log
    * Added get_segment_routing_accumulated_path_metric

* IOSXR
  * Added configure_replace subsection
    * Added get_bgp_as
    * Added get_interface_ip_address
    * Added get_ospf_process_id_on_interface
    * Added verify_bgp_neighbor_exist
    * Added verify_bgp_neighbor_in_state

* COMMON
    * Added copy_to_server
* JUNOS
    * Added configure_ospf_interface_metric_cost
    * Added verify_ospf_interface_cost
