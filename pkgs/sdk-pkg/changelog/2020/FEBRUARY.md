| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   20.2        |


--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* IOSXE
    * Added get_bgp_mpls_labels
    * Added verify_ip_bgp_route
    * Added get_mpls_label_stack
    * Added verify_route_known_via
    * Added verify_cef_labels
* LINUX
    * Created Linux APIs for routem process management
        * Added learn_routem_configs
        * Added learn_process_pids
        * Added kill_processes
        * Added start_routem_process 
* Blitz
    * Added configure_replace action
    * Added save_config_snapshot action
    * Added restore_config_snapshot action
	* Added run_genie_sdk action
    * Added mark up filter so user can filter action's output
	* Added prompt handler for configure and execute action
	* Added tgn action for ixia api support
    * Added print action
* Utils
    * Added dynamic_diff_parameterized_running_config
    * Added dynamic_diff_create_running_config
--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOSXE
    * Updated get_routing_mpls_label
        * To support vrf
    * Updated verify_traceroute
        * Updated condition check and added logging message
    * Updated get_ip_bgp_route
        * To get only best path
    * Updated get_segment_routing_policy_active_path_hop_labels
        * To add ignore_first_label flag
    * Updated get_segment_routing_policy_in_state
        * To Add expected_color and expected_endpoint parameters
	* Updated subsection configure_replace
		* To use proper timeout value for each devices
* IOSXR
    * Fixed subsection configure_replace to check file exist before replace operation
	* Updated configure_ntp_server
        * To fix issue with unconfigure
    * Updated verify_synced_ntp_server
        * To add iteration to verify
* NXOS
    * Updated utils.py copy_to_device function:
        * To support use-kstack option for N3K/N9K
    * Updated restore.py in abstracted_libs
        * 'show config-replace log verify' added when configure replace is failed
* General
    * Fixed API get_time_source_from_output to support more various output
* Blitz
    * Updated action_parallel to save the result of the actions implemented in parallel in the main processor

