--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * tftp boot stage
        * check the length of image befor trying to boot the device. add ether_port


--------------------------------------------------------------------------------
                                      Key.                                      
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified tftp boot stage
        * edit ecovery_en_password name and add it to docstring.
    * Modified device recovery to fix grub menu logic
    * Modify image hander, upload reload service arguments with image_to_boot
    * Modified install_image stage
        * check the current image and skip the stage if the image for instalation is the

* common
    * Updated power_cycle stage, added sleep_after_connect.
    * Modified copy_to_device stage
        * to fix a bug when retrieving the running image in order to protect it from deletion
    * Modified copy_to_linux stage
        * to fix a bug for renaming the file.
    * Added prompt_recovery to copy_to_device and set the default value to False,

* clean/iosxe
    * Modified install_image stage
        * to fix the issue when packages.conf does not exist

* generic
    * Modify recovery processor, only recover device if it has been connected


