--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* common
    * Modified clean infrastructure
        * To properly log exceptions generated in the parent process
    * Modified stage schema validation
        * To support the 'source' key

* clean recovery
    * Removed exception when connecting to device in rommon

* generic
    * Modified 'reload' clean stage, fixed check_modules logic

* iosxe
    * Fixed iosxe clean abstraction issue

* iosxr
    * Added
        * verify_running_image


