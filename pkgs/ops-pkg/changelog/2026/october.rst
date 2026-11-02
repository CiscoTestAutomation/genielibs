--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxr
    * Modified Platform (rev1)
        * chassis_sn now uses the show inventory Rack 0 serial when present. show diag details / admin show diag chassis (including the Rack 0 Top Assembly and Second Serial Number blocks) are used only as a fallback, and a mismatch with inventory is logged as a warning. Fixes NCS5500 fixed chassis reporting the board serial.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* platform ops
    * IOSXE
        * Added normalized member inventory, member fallback, modularity, chassis type, confidence, and member-count evidence for stacks, StackWise Virtual systems, and dual-route-processor systems.
        * Publish member-qualified modular cards, MPAs, and optics in the slot tree so consumers do not parse inventory commands independently.
        * Treat any non-Ready stack or StackWise Virtual member, including transitional states, as inconclusive, and replace stale member inventory on relearn.
    * IOSXR
        * Added normalized modularity, dual-route-processor, and fixed-system standalone evidence from learned platform data.


