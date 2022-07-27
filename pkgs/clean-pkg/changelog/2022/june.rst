--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean
    * clean.py
        * Added support for clean template
    * stages.py
        * Updated clean stages schema
    * template/iosxe
        * Added default template for iosxe
    * template/sdwan
        * Added default template for sdwan


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* genie.libs.clean
    * Updated reload stage
        * update the command for the path from rommon to diable, so the device will not boot from rommon and instead throw an exception. after the connect it will restore the original value for the rommon to diasable path command.
