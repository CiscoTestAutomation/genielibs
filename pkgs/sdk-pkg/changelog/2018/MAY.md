# May 8th

* Normalized all the ats.tcl imports in the package.

* New clear triggers added.
	* TriggerClearIPv6NeighborVrfAll
	* TriggerClearIpOspfNeighborVrfAll
	* TriggerRestartOspf
	* TriggerClearIpRouteVrfAll
	* TriggerClearIpv6RouteVrfAll
	* TriggerRestartBgp
	* TriggerClearIpBgpVrfAll
	* TriggerClearBgpVpnv6UnicastVrfAll
	* TriggerClearBgpVpnv4UnicastVrfAll

# May 22nd

* Added package library to CesMonitor.

# May 23nd

* New Vxlan triggers added
    - TriggerUnconfigConfigNveSourceInterfaceLoopback
    - TriggerUnconfigConfigNveVniAssociateVrf
    - TriggerUnconfigConfigEvpn
    - TriggerUnconfigConfigEvpnVni
    - TriggerUnconfigConfigEvpnMsiteBgwDelayRestoreTime
    - TriggerUnconfigConfigInterfaceEvpnMsiteDciTracking
    - TriggerUnconfigConfigInterfaceEvpnMsiteFabricTracking
    - TriggerUnconfigConfigNveAdvertiseVirtualRmac
    - TriggerUnconfigConfigNvOverlayEvpn
    - TriggerUnconfigConfigNveVniMcastgroup
    - TriggerAddRemoveNveAdvertiseVirtualRmac
    - TriggerAddRemoveEvpnMsiteBgwDelayRestoreTime
