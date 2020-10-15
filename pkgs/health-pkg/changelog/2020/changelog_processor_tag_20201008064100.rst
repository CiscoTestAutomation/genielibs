--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------

* pyATS Health Check
    * Removed processor tag restriction in health.yaml:
        * mixed `pre`/`post`/etc under same section is possible
    * Enhanced to not show up the section in log which is not supposed to run
        * see executed sections only in log
    * Enhanced to run section with non-connected device
        * if both connected and non-connected devices in same section, only action with connected device will run