--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* health
    * Enhanced device connectivity check
        * Updated logic with pcall for speed up
    * Added pyats_health default template 'health_yamls/pyats_health.yaml'
        * default template is used with '--health-checks'
    * Added 'force_all_connected' as health_settings
        * pyATS Health Check requires that all devices are connected by default. It can be disabled by this setting.
    * Modified internal functions
        * To support 'hide_processor' which you can hide specific processor from log

* health plugin
    * Added '--health-webex' argument
        * Added webex notification feature with notification template
    * Added '--health-remote-device' argument
        * Specify remote device information for copy files to remote
    * Added '--health-mgmt-vrf' argument
        * Specify Mgmt Vrf which is reachable to remote device
    * Added '--health-threshold' argument
        * Specify threshold for cpu, memory and etc
    * Added '--health-show-logging-keywords' argument
        * Specify show logging keywords to search
    * Added '--health-core-default-dir' argument
        * Specify directories where searching core file or etc
    * Added '--health-tc-sections' argument
        * same with '--health-sections' and `--health-sections` is now deprecated
    * Added '--health-tc-uids' argument
        * same with '--health-tc-uids' and `--health-uids` is now deprecated
    * Added '--health-tc-groups' argument
        * same with '--health-tc-groups' and `--health-groups` is now deprecated


--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* health
    * pyats_health default template
        * Added save variable name 'health_value' for webex notification
    * Fixed internal logic to remove redundant run
        * Fixed a bug which causes redundant run with multiple health args

* health plugin
    * Modified saving health data
        * Save health result data to health_results.json in post_task
    * Added support multiple values to arguments
        * each health argument if applicable supports multiple values by delimiter ' '(space)


