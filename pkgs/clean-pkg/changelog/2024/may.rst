--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * The clean stages 'verify_running_image' and 'copy_to_device' were using the 'xe_version' field
    * Also fixed the wrong default type when calling get on a dict in 'verify_running_image'.

* clean/stages
    * iosxe
        * update install remove inactive stage to check for the image before remvoving image and packages.

* clean
    * Modified recovery_processor
        * Added condition to check if device has is_ha attribute


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean/iosxe
    * Connect
        * Added logic to iosxe connect stage to support HA recovery.

* iosxe/cat9k
    * Added new clean stage `install_image`

* clean
    * Modified clean.py
        * Added resources to NOT_A_STAGE variable.


