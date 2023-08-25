--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* generic
    * Change logic for copy_to_device to check for local file size before trying from remote server


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * CopyToDevice clean stage
        * Added check to verify the current running image and skip the stage.


