* Please follow the template we introduced in NOVEMBER.md file.
* Every Trigger/verification need to be added under the corresponding feature.

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |               |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* JUNOS
    * Added verify_file_size
    * Added verify_ldp_session
--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOS
    * Added get_platform_default_dir
    * Added get_platform_core

* IOSXE
    * Added get_platform_default_dir
    * Added get_platform_core
    * Added get_platform_logging

* IOSXR
    * Added get_platform_default_dir
    * Added get_platform_core

* NXOS
    * Added get_platform_default_dir
    * Added get_platform_core

* JUNOS
    * Added get_platform_default_dir
    * Modified get_file_size

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* NXOS
    * Fixed nxapi_method_nxapi_rest for get methods not returning data
