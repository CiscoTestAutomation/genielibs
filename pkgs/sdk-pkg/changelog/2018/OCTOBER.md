
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      | 3.1.2         |
| ``genie.libs.sdk``      | 3.1.1         |
| ``genie.libs.sdk``      | 3.1.0         |



# V3.1.2


--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * Added callable (from genie.libs.sdk.libs.utils.triggeractions iport configure_add_attributes)
      for Conf object method add_xxx() to avoind duplicated codes in overwritting
      the triggers subsections
    * Updated nxos ha by using latset filetransfer arguments
    * New functionality to display Triggers Requirements in English instead of
      dictionary

--------------------------------------------------------------------------------
                               Genie yaml files
--------------------------------------------------------------------------------
* Genie yaml files
    * Clean up the verification files by using verification generator script

--------------------------------------------------------------------------------
                                 IGMP
--------------------------------------------------------------------------------
* Triggers (NXOS)
    * TriggerUnconfigConfigIgmpEnable
    * TriggerUnconfigConfigIgmpVersion
    * TriggerUnconfigConfigIgmpJoinGroup
    * TriggerUnconfigConfigIgmpStaticGroup
    * TriggerModifyIgmpVersion
    * TriggerAddRemoveIgmpEnable
    * TriggerAddRemoveIgmpVersion
    * TriggerAddRemoveIgmpJoinGroup
    * TriggerAddRemoveIgmpStaticGroup

--------------------------------------------------------------------------------
                                 MLD
--------------------------------------------------------------------------------
* Triggers (NXOS)
    * TriggerUnconfigConfigMldEnable
    * TriggerUnconfigConfigMldVersion
    * TriggerUnconfigConfigMldJoinGroup
    * TriggerUnconfigConfigMldStaticGroup
    * TriggerModifyMldVersion
    * TriggerAddRemoveMldEnable
    * TriggerAddRemoveMldVersion
    * TriggerAddRemoveMldJoinGroup
    * TriggerAddRemoveMldStaticGroup

* PTS (NXOS)
    * Updated the dynamic keys in pts_datafile.yaml

--------------------------------------------------------------------------------
                                MSDP
--------------------------------------------------------------------------------
* PTS (NXOS)
    * Updated the dynamic keys in pts_datafile.yaml

--------------------------------------------------------------------------------
                                 ROUTING
--------------------------------------------------------------------------------
* Triggers (NXOS)
    * TriggerClearIpRoutingMulticast
    * TriggerClearRoutingMulticast
    * TriggerClearV4RouteMulticast
    * TriggerClearV6RouteMulticast


--------------------------------------------------------------------------------
                                TRM
--------------------------------------------------------------------------------
* verification (NXOS)
    * Verify_BgpIpMvpn
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_1
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_2
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_3
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_4
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_5
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_6
    * Verify_BgpIpMvpnRouteType_vrf_all_route_type_7
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_1
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_2
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_3
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_4
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_5
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_6
    * Verify_BgpIpMvpnRouteType_vrf_default_route_type_7
    * Verify_BgpIpMvpnSaadDetail
    * Verify_BgpL2vpnEvpn
    * Verify_FabricMulticastGlobals
    * Verify_FabricMulticastIpL2Mroute_vni_all
    * Verify_FabricMulticastIpSaAdRoute_vrf_all
    * Verify_ForwardingDistributionMulticastRoute



# V3.1.1

* Enhanced CES Monitor



# V3.1.0


--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------

* Libs
    * Added learn_system in sdk/libs subsection.py to learn specific attributes
    * Added get_uut, get_uut_neighbor in sdk/libs prepostprocessors to get uut/uut neighbors
    * Added learn_config built up from ShowRunPim in Pim conf object.

--------------------------------------------------------------------------------
                                VXLAN
--------------------------------------------------------------------------------

* Triggers (NXOS)
    * TriggerAddRemoveEvpnMsiteBgwDelayRestoreTime
    * TriggerAddRemoveNveVniMcastGroup
    * TriggerAddRemoveNveVniMultisiteIngressReplication
    * TriggerDisableEnableVnSegmentVlanWithNvOverlay
    * TriggerModifyEvpnMsiteBgwDelayRestoreTime
    * TriggerModifyEvpnRd
    * TriggerModifyNveMultisiteBgwInterface
    * TriggerModifyNveSourceInterfaceLoopback
    * TriggerModifyNveVniMcastGroup
    * TriggerModifyVlanVnsegment
    * TriggerShutNoShutNveLoopbackInterface
    * TriggerShutNoShutNveOverlayInterface
    * TriggerUnconfigConfigBgpAfL2vpnEvpnRewriteEvpnRtAsn
    * TriggerUnconfigConfigBgpL2vpnCapability
    * TriggerUnconfigConfigEvpn
    * TriggerUnconfigConfigEvpnMsiteBgw
    * TriggerUnconfigConfigEvpnMsiteBgwDelayRestoreTime
    * TriggerUnconfigConfigEvpnMsiteDciTracking
    * TriggerUnconfigConfigEvpnMsiteFabricTracking
    * TriggerUnconfigConfigEvpnVni
    * TriggerUnconfigConfigNvOverlayEvpn
    * TriggerUnconfigConfigNveSourceInterfaceLoopback
    * TriggerUnconfigConfigNveVniAssociateVrf
    * TriggerUnconfigConfigNveVniMcastGroup
    * TriggerUnconfigConfigNveVniMultisiteIngressReplication
    * TriggerUnconfigConfigVlanVnsegment
    * TriggerUnconfigConfigVxlanNveOverlayInterface

* verification (NXOS)
    * Verify_L2routeEvpnEternetSegmentAll
    * Verify_BgpL2vpnEvpnNeighbors
    * Verify_BgpL2vpnEvpnRouteType
    * Verify_BgpL2vpnEvpnSummary
    * Verify_L2routeFlAll
    * Verify_L2routeMacAllDetail
    * Verify_L2routeMacIpAllDetail
    * Verify_L2routeSummary
    * Verify_L2routeTopologyDetail
    * Verify_NveEthernetSegment
    * Verify_NveInterface
    * Verify_NveInterfaceDetail
    * Verify_NveMultisiteDciLinks
    * Verify_NveMultisiteFabricLinks
    * Verify_NvePeers
    * Verify_NveVni
    * Verify_NveVniSummary

--------------------------------------------------------------------------------
                                MSDP
--------------------------------------------------------------------------------

* Triggers (NXOS)
    * TriggerUnconfigConfigMsdpPeer
    * TriggerUnconfigConfigMsdpSaFilterIn
    * TriggerUnconfigConfigMsdpSaFilterOut
    * TriggerUnconfigConfigMsdpSaLimit
    * TriggerUnconfigConfigMsdpDescription
    * TriggerUnconfigConfigMsdpMeshGroup
    * TriggerUnconfigConfigMsdpKeepaliveHoldtime
    * TriggerUnconfigConfigMsdpReconnectInterval
    * TriggerUnconfigConfigMsdpOriginatorId
    * TriggerModifyMsdpOriginatorId
    * TriggerModifyMsdpSaFilterIn
    * TriggerModifyMsdpSaFilterOut
    * TriggerModifyMsdpSaLimit
    * TriggerModifyMsdpMeshGroup
    * TriggerModifyMsdpKeepaliveHoldtime      
    * TriggerModifyMsdpReconnectInterval      
    * TriggerModifyMsdpDescription      
    * TriggerModifyMsdpPeerConnectedSource      
    * TriggerModifyMsdpPeerAs
    * TriggerAddRemoveMsdpOriginatorId
    * TriggerAddRemoteMsdpSaFilterIn
    * TriggerAddRemoveMsdpSaFilterOut
    * TriggerAddRemoveMsdpSaLimit
    * TriggerAddRemoveMsdpMeshGroup
    * TriggerAddRemoveMsdpKeepaliveHoldtime
    * TriggerAddRemoveMsdpReconnectInterval
    * TriggerAddRemoveMsdpDescription
    * TriggerClearMsdpPeer
    * TriggerClearMsdpStatistics
    * TriggerClearMsdpPolicyStatisticsSaPolicyIn
    * TriggerClearMsdpPolicyStatisticsSaPolicyOut
    * TriggerClearMsdpSaCache
    * TriggerClearMsdpRoute
    * TriggerAddRemoveMsdpPeer

* Verifications (NXOS)
    * Verify_IpMsdpPeerVrf_vrf_all
    * Verify_IpMsdpPeerVrf_vrf_default
    * Verify_IpMsdpSaCacheDetailVrf_vrf_all
    * Verify_IpMsdpSaCacheDetailVrf_vrf_default
    * Verify_IpMsdpSummary_vrf_all
    * Verify_IpMsdpSummary_vrf_default

--------------------------------------------------------------------------------
                                 PIM
--------------------------------------------------------------------------------

* Triggers (NXOS)
    * TriggerShutNoShutAutoRpInterface
    * TriggerShutNoShutAutoRpVrfInterface
    * TriggerUnconfigConfigAutoRpInterface
    * TriggerUnconfigConfigAutoRpVrfInterface  
    * TriggerModifyPimNeighborFilter
    * TriggerUnconfigConfigPimNeighborFilter
    * TriggerAddRemovePimNeighborFilter
    * TriggerUnconfigConfigPimNbrInterface
    * TriggerUnconfigConfigPimNbrVrfInterface
    * TriggerShutNoShutPimNbrInterface
    * TriggerShutNoShutPimNbrVrfInterface

--------------------------------------------------------------------------------
                                 LISP
--------------------------------------------------------------------------------

* Verifications (IOSXE)
    * Verify_LispSession
    * Verify_LispPlatform
    * Verify_LispDynamicEidDetail
    * Verify_LispServiceIpv4
    * Verify_LispServiceIpv6
    * Verify_LispServiceEthernet
    * Verify_LispServiceIpv4Database
    * Verify_LispServiceIpv6Database
    * Verify_LispServiceEthernetDatabase
    * Verify_LispServiceIpv4MapCache
    * Verify_LispServiceIpv6MapCache
    * Verify_LispServiceEthernetMapCache
    * Verify_LispServiceIpv4RlocMembers
    * Verify_LispServiceIpv6RlocMembers
    * Verify_LispServiceEthernetRlocMembers
    * Verify_LispServiceIpv4ServerDetailInternal
    * Verify_LispServiceIpv6ServerDetailInternal
    * Verify_LispServiceEthernetServerDetailInternal
    * Verify_LispServiceIpv4ServerSummary
    * Verify_LispServiceIpv6ServerSummary
    * Verify_LispServiceEthernetServerSummary
    * Verify_LispServiceIpv4Smr
    * Verify_LispServiceIpv6Smr
    * Verify_LispServiceEthernetSmr
    * Verify_LispServiceIpv4Statistics
    * Verify_LispServiceIpv6Statistics
    * Verify_LispServiceEthernetStatistics
    * Verify_LispServiceIpv4Summary
    * Verify_LispServiceIpv6Summary
    * Verify_LispServiceEthernetSummary

--------------------------------------------------------------------------------
                                 MCAST
--------------------------------------------------------------------------------
* Triggers
    * TriggerClearIpMroute
    * TriggerClearIpv6Mroute
    * TriggerUnconfigConfigBsrRpInterface
    * TriggerUnconfigConfigBsrRpVrfInterface
    * TriggerShutNoShutBsrRpInterface
    * TriggerShutNoShutBsrRpVrfInterface
    * TriggerUnconfigConfigStaticRpInterface
    * TriggerUnconfigConfigStaticRpVrfInterface
    * TriggerShutNoShutStaticRpInterface
    * TriggerShutNoShutStaticRpVrfInterface

--------------------------------------------------------------------------------
                                 ROUTING
--------------------------------------------------------------------------------
* Triggers
    * TriggerClearIpRoute
    * TriggerClearIpv6Route
    * TriggerClearIpRouting
    * TriggerClearRouting
