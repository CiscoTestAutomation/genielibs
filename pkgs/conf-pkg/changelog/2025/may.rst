--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* conf
    * NXOS
        * Added ParsedInterfaceName class to handle interface name parsing


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* nxos
    * Modified neighbor.py
        * Added new class IfNeighbor to configure interface as neighbor in bgp
    * Modified bgp.py
        * Added new managed attribute interface_neighbors to support interface neighbor configuration
    * Modified interface.py
        * Added support to configure mac address under port-channel interfaces
    * Modified test_interface.py and test_bgp.py
        * Added new unittest for new support


