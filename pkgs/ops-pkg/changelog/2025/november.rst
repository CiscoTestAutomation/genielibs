--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * platform
        * Added support for learning hardware revisions from 'show version' command
        * Added support for learning linecard hardware versions from 'show module' command

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * platform
        * Fixed hardware revision parsing to properly extract from 'show version' switch data
        * Fixed data structure handling to move hardware revision to root level when consistent across switches
        * Fixed linecard hardware version mapping from module data to slot structure

