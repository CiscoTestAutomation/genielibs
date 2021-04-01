--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* genie.conf
    * Modified Interface class, updated ipv6 type to ipv6_or_list_of_ipv6

* IOSXE
    * Modified clean stage 'install_image' directory lookup

* Junos
    * Modified verify_chassis_environment_component_present
        * Enhanced code to return proper result
    * Modified verify_log_exists
        * Enhanced code to return correct response

* UTILS
    * Modified validate_clean to do linting on the clean yaml


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* IOSXE
    * Modified apply_configuration clean stage
        * Added option to copy config directly to startup
    * Added ping API

* IOS
    * Added delete_local_file API
    * Added get_config_from_file API
    * Added start_packet_capture API
    * Added stop_packet_capture API
    * Added export_packet_capture API
    * Added clear_packet_buffer API
    * Added ping_interface_success_rate API
    * Added change_hostname API
    * Added save_running_config_configuration API
    * Added set_clock API
    * Added scp API
    * Added delete_files API
    * Added verity_ping API
    * Added get_md5_hash_of_file
    * Added ping API

* IOSXR
    * Added ping API

* NXOS
    * Added ping API


