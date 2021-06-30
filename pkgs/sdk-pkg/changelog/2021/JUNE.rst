--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* blitz
    * blitz.py
        * Fixed bug that caused regex filtered variables not to be saved
    * updated 'save_variable'
        * changed logging message from info to debug.
    * Modified decorator 'add_result_as_extra'
        * Fixed a bug which was missing validation of return from action
    * Enhanced logging for Dq filter via include/exclude
        * Show Dq Filtered result and update message to be clearer
    * Updated Blitz class
        * Allow pyATS Health Check action to save variable inside of action
    * Modified add_result_as_extra for pyATS Health Check
        * Save health data to runtime variable instead of saving to file
        * Added webex notification support
        * Save variable which can be used in pyATS Health Check webex notification
    * Modified save_variable function
        * logging massage is changed from info to debug
    * Modified internal func '_find_saved_variable'
        * add handling for API which has argument 'section'

* nxos
    * Added retry mechanism to nxapi_method_nxapi_rest
    * Modified health_core API
        * Added FileUtils support to copy core file to remote device

* iosxe, isoxr, nxos, apic
    * Update copy_from_device and copy_to_device APIs to support HTTP transport incuding proxy support
    * Removed copy_to_script_host API (use copy_from_device instead)

* iosxe
    * Modified default_interface
        * Fixed docstring
    * Modified health_memory API
        * Fixed calculation in case pid is same
    * Modified health_core API
        * Added FileUtils support to copy core file to remote device
    * enhanced API 'health_cpu'
        * updated logic for speed up
    * enhanced API 'health_memory'
        * updated logic for speed up
    * enhanced API 'config_ip_on_interface'
        * Add argument for ipv6 address and configure if it is passed
    * updated 'get_ospf_interfaces'
        * added new argument 'ospf_process_id'. But keep 'bgp_as' for backward compatibility

* api utils
    * Modified API `verify_pcap_packet`
        * Added support to check the fragmented captured packet.
    * Modified API `verify_pcap_dscp_bit`
        * To verify the Expected destination IP address.
        * To verify the Expected protocol message type.
    * Modified API `verify_pcap_mpls_packet`
        * To verify the Expected source port number.
        * To verify the Expected destination port number.
        * To verify the Expected protocol message type.
        * To handle the port_and_or operation.
    * Modified API `web_interaction`
        * To handle the result status when time limit exceeded.

* utils
    * Modified copy_from_device
        * return output from FileUtils copyfile

* iosxr
    * Modified health_core API
        * Added FileUtils support to copy core file to remote device

* utils
    * added 'only_connected' to API 'get_devices'
        * check if device is connected and return only connected ones
    * added 'with_os' to API 'get_devices'
        * return dict with device name and os as key/value pair


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* blitz
    * 'execute' action
        * Added `result_status' to support result change only for `passed` based on user input.
    * markup.py
        * Added apply_regex_findall to search for patterns in a string
    * blitz.py
        * Modified _filter_and_save_action_output to expect regex_findall
    * Support attachment for pyATS Health Check webex notification
    * actions.py
        * Added `result_status' to support result change only for `passed` based on user input
    * actions_helper.py
        * Added `result_status' to support result change only for `passed` based on user input
    * advanced_actions.py
        * Modified custom_substep_message in loop to support the use of %VARIABLES{}
    * markup.py
        * Added save_output_to_file to save the output of an action to a specified file
    * blitz.py
        * Modified _filter_and_save_action_output to expect file_name and append arguments
    * add webex notification support for pyATS Healtch Check
    * 'execute' action
        * Added `connection_alias' to support different connections
    * 'parse' action
        * Added `connection_alias' to support different connections
        * Added `context' to use different context
    * 'configure' action
        * Added `connection_alias' to support different connections
    * 'configure_dual' action
        * Added `connection_alias' to support different connections

* api utils
    * Added API `web_interaction`
        * To return result of user choice for manual steps. same capability with WebInteraction.
    * Added API `verify_pcap_ldp_packet`
        * To verify the LDPHello and LDPKeepAlive packet

* utils
    * add 'verify_device_connection'
        * check device connectivity and return Boolean. have reconnect feature

* nxos/n9k
    * add 'health_core' for N9K
        * copy_from_device with default timeout 600 secs and use-kstack

* iosxe
    * API Utils
        * Added API `verify_device_tracking_policies`
        * Added API `verify_ip_mac_binding_in_network`
        * Added API `verify_ip_mac_binding_not_in_network`
        * Added API `verify_ip_mac_binding_count`


