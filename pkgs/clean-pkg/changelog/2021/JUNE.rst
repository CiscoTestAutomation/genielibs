--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* iosxe
    * Modified get_bgp_neighbors_in_state API, fixed regex expression

* com
    * Updated clean stage 'delete_files_from_server'
        * updated docstring to mention supporting only ftp and sftp and schema

* iosxe
    * Modified device recovery
        * To properly match rommon prompts
        * When the 'Press RETURN to get started' prompt is seen, wait until the buffer is settled to send RETURN.


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* com
    * Modified
        * Modified 'connect' clean stage to include 'via' argument

* apic
    * Add `apply_configuration` clean stage for REST interactions


