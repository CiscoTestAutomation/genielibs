--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* iosxe
    * Add API "get_show_output_line_count"

--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* iosxr
    * Modified clean stage 'install_image_and_packages'
    * Updated to install image directly from tftp path
    * Updated install commit to mark fail if aborted
    * Updated to remove inactive packages
    * Updated to add sleep before doing install commit

* clean
    * Image handler update image names when using change_order_if_pass

* clean
    * reload
        * Added `via` argument to specify which connection to use on reconnect