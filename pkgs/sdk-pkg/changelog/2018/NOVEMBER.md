| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v3.1.6      |

--------------------------------------------------------------------------------
                               YAML FILES
--------------------------------------------------------------------------------
* NXOS
    * Add Verify_RunningConfigVrf and Verify_RunningConfigTrm in verification_nxos_datafile.yaml

--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * Add Junos libraries ( Juniper devices ) for getting management interface.
    * Add Junos libraries to initial executed commands for terminal length and width.
    * Add default ( general ) libs for InitExecCommands and fix up ManagementInterface
      to not let it explode when there is no abstracted libs for these functions.
    * Add abstracted libraries for abstracting the configuration retrival command.
    * Add Junos libraries for checking 'show version'
    * Add Junos libraries for getting default directory on device.

--------------------------------------------------------------------------------
                               VERIFICATIONS
--------------------------------------------------------------------------------
* Junos
    * Add new verifications
        * Verify_ConfigurationSystemNtpSet
        * Verify_InterfacesTerse
        * Verify_NtpAssociations
        * Verify_NtpStatus
* NXOS
    * Add Trm verifications
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
        * Verify_FabricMulticastIpSaAdRoute_vrf_all
        * Verify_ForwardingDistributionMulticastRoute
        * Verify_FabricMulticastGlobals
        * Verify_FabricMulticastIpL2Mroute_vni_all
        * Verify_BgpL2vpnEvpn

* Verification Generator Script
    * Enhance script to automatelly generate Junos verifications file.

--------------------------------------------------------------------------------
                               TRIGGERS
--------------------------------------------------------------------------------
* NXOS
    * Enhance TriggerAddRemoveMsdpKeepaliveHoldtime to let it sleep after the
      actions to have it re-connect

    * Add Trm Triggers
        * TriggerDisableEnableNgmvpn
        * TriggerAddRemoveRouteTargetMvpn
        * TriggerAddRemoveRouteTargetEvpn
        * TriggerAddRemoveAdvertiseEvpnMulticast
        * TriggerProcessKillRestartNgmvpn
        * TriggerProcessCrashRestartNgmvpn
        * TriggerUnconfigConfigBgpAddressFamilyIpv4Mvpn
        * TriggerUnconfigConfigBgpNeighborAddressFamilyIpv4Mvpn
        * TriggerUnconfigConfigRouteTargetEvpn
        * TriggerUnconfigConfigRouteTargetMvpn
        * TriggerUnconfigConfigAdvertiseEvpnMulticast

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v3.1.5      |

--------------------------------------------------------------------------------
                                YAML
--------------------------------------------------------------------------------

* IOS:
    * add IOS trigger&verification yamls files, to include 
      one trigger TriggerShutNoShutLoopbackInterface
      and platform/interface/vrf related verifications


| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v3.1.4      |

--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * Fix IOSXR subsection save_bootvar by using unicon conn.admin_execute()
      for executing admin commands

--------------------------------------------------------------------------------
                               YAML FILES
--------------------------------------------------------------------------------
* NXOS
    * Add NTP Verify_NtpPeerStatus and Verify_NtpPeers in verification_nxos_datafile.yaml
    * Add feature ntp to pts_datafile.yaml


| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v3.1.3      |

--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * Fix IOSXR subsection save_bootvar by using unicon conn.admin_execute()
      for executing admin commands
