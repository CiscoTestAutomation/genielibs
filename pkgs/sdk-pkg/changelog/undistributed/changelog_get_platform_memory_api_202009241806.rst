--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* IOS
    * Added get_platform_memory_usage api
    * Added get_platform_memory_usage_detail api
--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOSXE
    * Fixed get_platform_memory_usage_detail api
        * Added if condition to handle if process name has a '*' in it
