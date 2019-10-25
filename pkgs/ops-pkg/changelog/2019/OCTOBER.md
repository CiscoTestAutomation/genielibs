|-----------------------------------------|
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.ops``      | 19.10         |

-----------------------------------------------------------------------------
                                Nd
-----------------------------------------------------------------------------
* IOSXE
    * Updated Nd ops to support custom vrf, interface values
* NXOS
    * Updated Nd ops to support custom vrf, interface values
* IOSXR
    * Added Nd ops to support custom vrf, interface values

-----------------------------------------------------------------------------
                                OSPF
-----------------------------------------------------------------------------
* NXOS
    * Updated OSPF ops to support custom vrf, interface, and neighbor arguments

-----------------------------------------------------------------------------
                                LAG
-----------------------------------------------------------------------------
* IOSXR
    * Updated LAG ops to prevent updating non-existent keys

--------------------------------------------------------------------------------------------------
                                ROUTING
--------------------------------------------------------------------------------------------------
* NXOS
    * Updated ROUTING ops to support custom vrf, address_family, interface, protocol, and route arguments
    * Fixed issue where exclude keys are not correctly inherited
* IOSXE
    * Fixed issue where exclude keys are not correctly inherited
* IOSXR
    * Fixed issue where exclude keys are not correctly inherited
