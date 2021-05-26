--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* nxos
    * Modified delete_unprotected_files API
        * Added allow_failure argument to silently allow file deletion to fail
    * Modified restore_running_config
        * Update Unicon reply dialog pattern for restore_running_config

* iosxe
    * Modified delete_unprotected_files API
        * Added allow_failure argument to silently allow file deletion to fail
    * Modified restore_running_config
        * Update Unicon reply dialog pattern for restore_running_config

* com
    * Modified free_up_disk_space API
        * Added allow_deletion_failure argument to silently allow file deletion to fail

* blitz
    * Modified 'add_result_as_extra' decorator for pyATS Health Check
        * Fixed multi process issue with loop and parallel
    * Check if NETCONF subscribe operation RPC message contains lxml objects.

* ios
    * Modified restore_running_config
        * Update Unicon reply dialog pattern for restore_running_config


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* ios
    * Added 'get_boot_variables' API for IOS

* iosxe
    * Fixed unconfigconfigOspf
        * Fixed Verify_unconfig in unconfigconfigOspf to handle empty parser exception which happens when there is only one OSPF instance configured
        * Method handles empty parser exception and now looks for OSPF ID in list of OSPF IDs in parsed output
    * Added VRF argument to 'configure_ntp_server' API

* common api
    * Added 'arithmetic_operations' API to calculate operands.

* utils
    * added new API 'get_bool'
        * simple API to return boolean result against value such as string, integer, dict, list and so on
    * added new API 'get_testcase_name'
        * to get testcase name from 'runtime' object

* blitz
    * added support to evaluate just value without operator
        * 'if $VARIABLES{test}' will return boolean result based on content of test. no operator required. if variable is not ready/initialized, it will be treated as 'None'