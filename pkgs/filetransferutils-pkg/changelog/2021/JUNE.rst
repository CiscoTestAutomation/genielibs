--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* common
    * Modified send_cli_to_device
        * Changed to return output after execution of cli command

* nxos
    * Modified copyfile
        * check both source and destination for server name
        * add check if server name is just number (module number)


