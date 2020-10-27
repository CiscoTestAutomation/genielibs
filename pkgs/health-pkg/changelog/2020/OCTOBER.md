| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.heath``    |  20.10        |

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyATS Health Check
    * Added legacy_cli argument for easypy command
    * Removed restriction health args in health yaml
        * Now all the items under same section don't need to have health args
    * Added reconnect feature
        * pyATS Health Check reconnects device in case device crashes/reloads
    * Added to convert testbed object from pyATS to Genie for pyATS run:
    * Removed processor tag restriction in health.yaml:
        * mixed `pre`/`post`/etc under same section is possible
    * Enhanced to not show up the section in log which is not supposed to run
        * see executed sections only in log
    * Enhanced to run section with non-connected device
        * if both connected and non-connected devices in same section, only action with connected device will run
