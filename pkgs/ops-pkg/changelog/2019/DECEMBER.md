|-----------------------------------------|
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.ops``      | 19.12         |

---------------------------------------------------------------------------------------------------
                       Fixed
* IOSXR
    * OPS 
        * Updated ops according to schema for routing
    * Verifications
        * Renamed Verify_L2routeEvpnMacIp to Verify_L2routeEvpnMacIpAll
        * Renamed Verify_ControllersFiaDiagshellL2show to Verify_ControllersFiaDiagshellL2showLocation
        * Removed Verify_InterfaceSwitchport because the class used is not supported on iosxr
        * Removed Verify_L2routeEvpnMac because the class used is not supported on iosxr

* IOSXE
    * OPS
        * Updated acl:
            * Fix tcp/udp/ip under l3 into ipv4/ipv6


---------------------------------------------------------------------------------------------------
                        New
---------------------------------------------------------------------------------------------------
* IOSXR
    * OPS
        * Added ops for msdp

* IOS
    * OPS
        * Added ops for platform

* NSOX
    * OPS 
        * Added ops for isis
        * Added ops for acl
        * Added ops for fdb

* IOSXE (Cat9K)
    * OPS
        * Added ops for acl
        * Added ops for platform

