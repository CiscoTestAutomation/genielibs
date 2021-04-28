--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* COM
    * Modified connect stage
        * Corrected the schema to support the current arguments
    * Modified Device Recovery
        * To fix an edge-case where clean should have continued after the device connection was verified.


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* COM
    * Modified copy_to_device stage
        * Added copy_attempts_sleep argument for sleeping between copy attempts
    * Modified copy_to_linux stage
        * Added copy_attempts_sleep argument for sleeping between copy attempts


