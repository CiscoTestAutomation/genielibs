--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* com
    * Modified copy_to_device
        * So the stage continues even if a file cannot be deleted when freeing up disk space.
    * Modified Device Recovery
        * To respect current result in case device recovery did nothing

* iosxe
    * Modified install_image stage dialogs so clean can enter 'y' at the reload prompt

* ioxe
    * Modified clean stage 'install_image'
        * Updated execute error pattern
    * Modified clean stage 'install_package'
        * Updated execute error pattern

* apic clean
    * Modified fabric_upgrade stage to upgrade only if needed
    * Added copy_to_device stage for APIC and included disk space check and cleanup if needed

* filetransferutils
    * Modified APIC plugin, added deletefile implementation

* sdk
    * Added new APIs for APIC