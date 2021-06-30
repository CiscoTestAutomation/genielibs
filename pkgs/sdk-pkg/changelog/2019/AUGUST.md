| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v19.8       |

----------------------------------------------------------------------------
                abstracted_libs/nxos/n7k/subsection.py
----------------------------------------------------------------------------
    * Updated save_device_inforamtion to skip for non-default VDC devices

----------------------------------------------------------------------------
                            apis
----------------------------------------------------------------------------
    * Added make json to collect all api functions
	* 400 api functions are now abstracted and can be directly called with device.apis()
    * Added VIRL api functions
    * https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/apis

----------------------------------------------------------------------------
                            triggers
----------------------------------------------------------------------------
Blitz
	* Blitz triggers now support calling all the api functions
VIRL
        * Added TriggerStopStartSimulation
