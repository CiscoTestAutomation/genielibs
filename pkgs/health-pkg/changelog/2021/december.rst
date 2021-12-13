--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* health
    * Updated logic for reasons why health is not running
        * show the reason in case device is not connected
    * Fixed a case that health says PASSED even though device is not connected
    * Optimized logic for `--health-tc-groups` argument
    * Adjusted `pyats_health.yaml` template due to above.

* health plugin
    * Updated logic to save 'pyats_health.yaml' for '--health-checks'
        * To reflect values based on given parameters for '--health-checks'
    * Updated health yaml template
        * to save a case which have one TC without separated connect section


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* health plugin
    * Added '--health-clear-logging' argument
        * To clear logging every health logging check
    * Updated health yaml template
        * added 'clear_logging' for '--health-clear-logging' argument


