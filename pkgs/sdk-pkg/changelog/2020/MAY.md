
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.5         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------

* IOS API:
    * Added save_running_config
    * Added copy_file_to_running_config
    * Added restore_running_config
    * Added remove_running_config
    * Added remove_tacacs_server
    * Added search_running_config
    * Added get_running_config_dict
    * Added get_running_config_hostname
    * Added get_running_config_section_dict
    * Added get_running_config
    * Added get_running_config_section
    * Added get_config_commands_from_running_config

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

* Blitz
    * Fixed logging message

* Processors:
    * Fixed PyYAML deprecated message

* Common API:
    * Enhanced modify_filename to support user provided unique filename

* NXOS API:
    * Fixed verify_module_status to support module state of 'Ready'

* IOSXE API:
    * Fixed verify_module_status to support module state of 'Ready'
    * Fixed get_boot_variables to not return empty items in boot_images list
    * Fixed iosxe/cat9k get_boot_variables to use correct parser
