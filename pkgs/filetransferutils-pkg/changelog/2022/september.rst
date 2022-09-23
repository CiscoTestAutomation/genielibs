--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* common
    * Modified filetransferutils/fileserver/protocols/http.py
        * Added ForkingMixIn to the HTTP handler in order to avoid socket blocking

* iosxe
    * Fix the error pattern list to ignore the common error open message
        * Replace 'Error opening' & 'Error' by 'Error(?! opening tftp//255\.255\.255\.255)'


