| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   20.1        |


----------------------------------------------------------------------------
                        New
----------------------------------------------------------------------------
* SDK
    * Added new api write_erase_reload_device_without_reconfig.
* Utils
    * Added compared_with_running_config
    * Added diff_configuration

* NXOS
    * Added platform execute api "execute_write_erase"

* Common OS
    * Added execute api "execute_reload"
    
--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

* NXOS
    * Updated restore.py in abstracted_libs
        * 'show config-replace log verify' added when configure replace is failed
* IOSXE
    * Updated verify_ospf_database_contains_sid_neighbor_address_pairs
        * To fix issue with certain outputs
    * Updated check_traffic_expected_rate
        * To fix issue with comparing values
* IOSXR
    * Fixed API verify_no_isis_neighbor