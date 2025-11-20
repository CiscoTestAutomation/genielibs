--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified configure_enable_aes_encryption API
        * Added support to handle Old Masteer key prompt.

* clean-pkg/stages
    * iosxe
        * Updated ping_gateway in ConfigureManagement stage to attempt ping multiple times
    * iosxe
        * Increased the default reload_wait from 30 seconds to 150 seconds to allow sufficient time to match the reload patterns.
    * iosxe
        * Updated install image logic to skip the "Check for previous uncommitted install operation" step when the show install active output has no packages to commit.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean
    * IOSXE
        * Update clean install images to retry install image if there is not enough space after cleaning unprotected files.
    * IOSXE/cat9k
        * Delete clean install images logic for car9k stack devices to use the logic from IOSXE.

* iosxe
    * clean-pkg
        * Updated install image stage to collect debug logs on failure


