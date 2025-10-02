--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages/iosxe
    * connect
        * Added optional logout argument (default True) to accommodate various scenarios.

* iosxe
    * Modified InstallImage
        * Added logic to handle ISSU in progress scenario.
    * Fixed the logic of InstallRemoveSmu stage and added support to handle uncommitted SMU images

* clean
    * IOSXE/cat9k
        * Update clean install images to use execute service and pass install timeout.
    * IOSXE/cat9k
        * Update clean install images to do configure no boot manual on the device.

* iosxe/cat9k/install_image
    * Added 'rommon_vars' to install_image stage to support setting rommon variables when booting an image in rommon mode.

* iosxe/install_image
    * add image_to_boot to install image

* clean-pkg
    * Fix syntax warning
    * Added support for matching interfaces by alias in ConfigureInterfaces.

* iosxe/connect
    * Removed duplicate configure boot manual in connect stage.


