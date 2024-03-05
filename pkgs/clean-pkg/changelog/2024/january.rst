--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified copy_to_device clean stage, update logic for image mapping when image is already loaded


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cheetah
    * Added LoadApImage
        * Added new clean stage load_ap_image

* stages/iosxe
    * Updated connect stage to support rommon boot

* iosxe
    * Added configure_type_access_list_action
        * API to configure ip/mac access-list with permission


