--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe/cat9k
    * Fixed the rommon boot clean stage by adding optional ether_port arg.

* generic
    * Modified copy_to_linux clean stage
        * Fix copy operation when local filesystem is used
    * Modified copy_to_device clean stage
        * Support dynamic http file server copy
            * Use dynamic http file server if origin.hostname is not specified
            * Add connection_alias for use with dynamic http file copy
    * Modified connect clean stage
        * Added `alias` option to specify connection alias to use


