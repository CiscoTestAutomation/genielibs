--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe/cat9k
    * Updated the rommon boot clean stage by adding recovery credentials and

* iosxe
    * Updated dialogs on reload clean stage to support asr1k.
    * Added new clean stage RommonBoot for iosxe
    * Added `directory` key to `install_image` stage schema
        * To specify a directory where packages.conf is created
    * Added `skip_boot_variable` keyto `install_image` stage schema
        * To skip boot variable handling in `install_image` stage


