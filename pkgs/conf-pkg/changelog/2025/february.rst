--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* nxos
    * Fix feature service-acceleration
        * change vrf submode config to single line config and update unit tests
        * `vrf vrf1 module-affinity 1` is now in a single line instead of `vrf vrf1\n  module-affinity 1\n exit`
    * Fix interface conf model
        * Subinterfaces can now handle `mac_address` attribute for nxos.

* conf
    * Device
        * Updated Device conf learn_interface_mac_addresses to ignore case
    * Interface
        * Added sp7 and sp8 port speeds
        * IOSXE
            * Moved interface configurations
            * Moved switchport configurations
        * IOSXR
            * Added HundredGigabitEthernetInterface
            * Added FourHundredGigabitEthernetInterface
        * NXOS
            * Changed parent class of VirtualInterface to Interface
            * Added _build_config_interface_submode to PortchannelInterface


