
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.4         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* NXOS
    * API
        * Added the DME apis (CLI version of the NXAPI GUI)

* IOSXE
    * API
        * Added get_cef_internal_primary_interface
        * Added get_cef_internal_repair_interface
        * Added get_acl_hit_counts
        * Added execute_install_package
        * Added execute_uninstall_package
        * Added get_boot_variables for CAT9K

* Triggers
    * Blitz
        * Custom actions can now be created in Python and used in Blitz
        * Added Include/Exclude with Dq.
        * Multiple filters can be applied to an action output and multiple variables can be saved
        * Numerical outputs of an action can be validated within a range
        * Added bash_console action
        * Continue is now default True, and can be set to False in datafile
        * Added action, section and testcase description
        * Added empty parser support

* APIC
    * API
        * Added apic_rest_get
        * Added apic_rest_post
        * Added apic_rest_delete

* LINUX
    * API
        * Added copy_data_to_device
        * Added read_data_from_device
        * Added trex_copy_json
        * Added start_trex_process
        * Added is_process_started
        * Added trex_save_configuration

* Utils
    * Added string_to_number
    * Added number_to_string
    * Added get_list_items
    * Added get_dict_items
    * Added save_info_to_file


--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

* IOSXE
    * SDK
        * Fixed warning for python3.8
    * API
        * Fixed verify_mpls_forwarding_table_local_label_for_subnet memory error
        * Fixed verify_mpls_forwarding_table_has_prefix_in_subnet_range memory error
        * Enhanced export_packet_capture to support customized export path
        * Fixed get_syslog_maximum_ospf_down_time get negative value
        * Fixed get_syslog_maximum_bgp_down_time get negative value

* General
    * API
        * Enhanced copy_pcap_file to support customized command
    * API
        * Enhanced verify_current_image and nxos: get_running_images
    * API
        * Enhanced execute_power_cycle_device to wait custom amount before powercycling device on

* Triggers
    * SDK
        * Removed sleep_processor from ShutNoShut, Modify, UnconfigConfig Trigger Templates
    * Blitz
        * Fixed bug where having two of the same blitz triggers in order would crash
    * Switchover
        * Updated nxos TriggerSwitchover platform_exclude to have 'main_mem' key
    * TriggerReloadEthernetModule
        * Fix applied to capture lc numbers properly to report reload properly
    * SDK
        * Moved delete plugin step in HA triggers to the CommonCleanup section


* Utils
    * Fixed get_username_password for non-default credentials

