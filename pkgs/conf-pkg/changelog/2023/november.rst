--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* Interface section
    * Modified __init__.py
        * Updated the switch port modes to cover private_vlan access and trunk modes
    * Modified NXOS EthernetInterface
        * Updated the file with CLI's to handle private vlan configuration
* Vlan section
    * Modified NXOS Vlan
         * Updated the file with CLI's to handle private vlan configuration
         
--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* nxos
    * Added macsec conf
        * added macsec cli for conf model


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* nxos
    * keychain
        * fixed typo for crypto algorithm AES_256_CMAC


