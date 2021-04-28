--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* Health
    * Modified internal functions
        * To handle Blitz loop against devices properly
        * To handle `common_api` key in case no device in action


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* Health Plugin
    * added `--health-config` to pyats command
        * To load health setting from health_config.yaml
    * create `health_results.json`
        * To have health data from results.json separately
        * Add `health_settings` to health_results.json from health config

* Health
    * Modified `add_result_as_extra` decorator in Blitz
        * Moved health data to health_results.json and have minimum data in extra
        * Added `health_data` to store each health action result in health_results.json


