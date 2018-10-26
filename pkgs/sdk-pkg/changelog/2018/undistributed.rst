* Please follow the template we introduced in OCTOBER.md file.
* Every Trigger/verification need to be added under the corresponding feature.

=======
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |               |

Features
========
* Added callable (from genie.libs.sdk.libs.utils.triggeractions iport configure_add_attributes)
  for Conf object method add_xxx() to avoind duplicated codes in overwritting the triggers subsections.
* Updated nxos ha by using latset filetransfer arguments

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
