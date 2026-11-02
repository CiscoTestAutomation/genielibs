--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* ios-xe
    * Modified interface configuration models to classify AppGigabitEthernet and FiveGigabitEthernet ports as physical Ethernet interfaces.

* ios-xr
    * Modified ParsedInterfaceName to publish structured rack, slot, CPU instance, port, CPU path, and RSIP fields for CPU-qualified interface names.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxr
    * Added ParsedInterfaceName
        * Added support for optics port names such as '0/0/2/-PORT-0', which the base parser does not recognize
        * All other interface names continue to be parsed by the base class


