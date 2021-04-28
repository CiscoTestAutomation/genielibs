--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* NXOS, NXOS/ACI
    * added `get_show_tech` API
    * added `copy_to_script_host` API
    * added `is_connected_via_vty` API

* IOSXE
    * added `get_show_tech` API
    * added `copy_to_script_host` API
    * added `is_connected_via_vty` API
    * Added API `health_cpu`
    * Added API `health_memory`
    * Added API `health_logging`
    * Added API `health_core`

* IOSXR
    * added `get_show_tech` API
    * added `copy_to_script_host` API
    * added `is_connected_via_vty` API
    * Added API `health_cpu`
    * Added API `health_memory`
    * Added API `health_logging`
    * Added API `health_core`

* APIC
    * added `get_show_tech` API
    * added `copy_to_script_host` API

* Linux
    * Added `socat_relay` API

* SDK libs
    * Updated `post_execute_command` processor to support device API calls

* FileServer
    * Added `http` protocol support to FileServer

* Common
    * Added `get_local_ip` API to lookup local IP address

* NXOS
    * health APIs for pyATS Health Check
        * Added API `health_cpu`
        * Added API `health_memory`
        * Added API `health_logging`
        * Added API `health_core`

* API Utils
    * Add get_single_interface API
        * To Get Single Interface Via Link In Testbed Yaml


--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* Junos
    * Fixed API `default_interface`
        * changed from raising exception to returning boolean

* IOSXE
    * Modified API `get_platform_cpu_load_detail`
        * Updated to use API `health_cpu`
    * Modified API `get_platform_memory_usage_detail`
        * Updated to use API `health_memory`
    * Modified API `get_platform_logging`
        * Updated to use API `health_logging`
    * Modified API `get_platform_core`
        * Updated to use API `health_core`
    * Modified API `get_platform_cpu_load_detail`
        * Updated to use API `health_cpu`
    * Modified API `get_platform_memory_usage_detail`
        * Updated to use API `health_memory`
    * Modified API `get_platform_logging`
        * Updated to use API `health_logging`
    * Modified API `get_platform_core`
        * Updated to use API `health_core`

* IOSXR
    * Modified API `get_platform_cpu_load_detail`
        * Updated to use API `health_cpu`
    * Modified API `get_platform_memory_usage_detail`
        * Updated to use API `health_memory`
    * Modified API `get_platform_logging`
        * Updated to use API `health_logging`
    * Modified API `get_platform_core`
        * Updated to use API `health_core`
    * Modified get_available_space
        * Added handling of the unit (kbytes/bytes) and convert.
    * Modified verify_file_exists
        * Add support of empty folder corner case
    * Modified Install_Image_And_Packages in clean-pkg
        * Fixed Regex Error
        * Add support for complex filepath (using several folders)

* Common API
    * Modified API `verify_device_connection_state`
        * Added handling in case device object doesn't have attribute `is_ha`

* Blitz
    * Modified decorator in Blitz for pyATS Health Check
        * Added handling for new pyATS Health Check data format
    * Modified `callback_blitz_dispatcher_gen`
        * To pass `name` info from section with loop to action
    * Modified blitz.py
        * Fixed error where failures in a parallel call wouldn't end the testcase when `continue false` is set
    * Fixed `custom_verification_message` handling
    * Modified notify_wait to recognize a device gnmi connection.
    * NETCONF subsccribe operation was forming invalid RPC message.
    * The rpc-error was not printing in log.
    * The selected flag was ignored checking return values.

* nxos
    * Modified ReloadFabricModule
        * changed the extended class from TriggerReloadLC to  TriggerReloadFabric

* API utils
    * common API `get_interface_from_yaml`
        * removed `*args` and changed to `testbed_topology`


