'''NXOS implementation for bgp clear triggers'''


# Genie Libs
from ..clear import TriggerClearBgp, \
                    TriggerClearBgpNeighbor, \
                    TriggerClearBgpNeighborIpv4,\
                    TriggerClearBgpNeighborIpv6,\
                    TriggerClearBgpNeighborSoftIpv6,\
                    TriggerClearBgpNeighborSoftIpv4, \
                    TriggerClearIpRouteAll,\
                    TriggerClearBgpVpnv4UnicastVrfAll,\
                    TriggerClearBgpVpnv6UnicastVrfAll,\
                    TriggerClearIpBgpVrfAll,\
                    TriggerRestartBgp


class TriggerClearBgpAll(TriggerClearBgp):
    """Hard reset all the BGP connections using CLI command "clear bgp vrf all all *"."""
    
    __description__ = """Hard reset all the BGP connections using CLI command "clear bgp vrf all all *".

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Hard reset all the BGP connections with command "clear bgp vrf all all *"
        3. Learn BGP Ops again, verify the uptime of BGP "established" neighbor(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<='


class TriggerClearIpBgpSoft(TriggerClearBgp):
    """Soft reset all the BGP connections using CLI command 'clear ip bgp * soft'."""

    __description__ = """Soft reset all the BGP connections using CLI command "clear ip bgp * soft".

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear ip bgp * soft"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """    
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip bgp * soft']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='>'


class TriggerClearBgpNeighbor(TriggerClearBgpNeighbor):
    """Hard reset the BGP neighbors using CLI command 'clear bgp all <neighbor id>'."""

    __description__ = """Hard reset the BGP neighbors using CLI command "clear bgp all <neighbor id>".

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp all <neighbor id>"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*)']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<='


class TriggerClearBgpNeighborSoft(TriggerClearBgpNeighbor):
    """Soft reset the BGP neighbors using CLI command "clear bgp vrf all all <neighbor id> soft".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp vrf all all <neighbor id> soft"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*) soft']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='>'

class TriggerClearBgpNeighborIpv4(TriggerClearBgpNeighborIpv4):
    """Soft reset the BGP neighbors for ipv4 address family using CLI command "clear bgp vrf all all <ipv4 neighbor id>".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp vrf all all <neighbor id>"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*)']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'

class TriggerClearBgpNeighborIpv6(TriggerClearBgpNeighborIpv6):
    """Soft reset the BGP neighbors for ipv6 address family using CLI command "clear bgp vrf all all <ipv6 neighbor id>".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp vrf all all <neighbor id>"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*)']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign = '<'

class TriggerClearBgpNeighborSoftIpv4(TriggerClearBgpNeighborSoftIpv4):
    """Soft reset the BGP neighbors for ipv4 address family using CLI command "clear bgp vrf all all <<ipv4 neighbor id>> soft".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp vrf all all <<ipv4 neighbor id>> soft"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*) soft']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='>'


class TriggerClearBgpNeighborSoftIpv6(TriggerClearBgpNeighborSoftIpv6):
    """Soft reset the BGP neighbors for ipv6 address family using CLI command "clear bgp vrf all all <<ipv6 neighborid>> soft".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear bgp vrf all all `ipv6_neighbor_id` soft"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp vrf all all (?P<neighbor>.*) soft']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='>'


class TriggerClearIpRouteAll(TriggerClearIpRouteAll):
    """Soft reset the BGP neighbors using CLI command "clear ip route *".

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn BGP Ops object and store the "established" BGP neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Soft reset all the BGP connections with command "clear ip route *"
        3. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip route *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='>'


class TriggerClearBgpVpnv4UnicastVrfAll(TriggerClearBgpVpnv4UnicastVrfAll):
    """Reset the BGP connections for vpnv4 uncast address family sessions with using CLI
        command "clear bgp vpnv4 unicast * vrf all".

               trigger_datafile:
                   Mandatory:
                       timeout:
                           max_time (`int`): Maximum wait time for the trigger,
                                           in second. Default: 180
                           interval (`int`): Wait time between iterations when looping is needed,
                                           in second. Default: 15
                   Optional:
                       tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                            restored to the reference rate,
                                            in second. Default: 60
                       tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                          in second. Default: 10

               steps:
                   1. Learn BGP Ops object and store the "established" BGP neighbor(s)
                      for vpnv4 unicast address family
                      if has any, otherwise, SKIP the trigger
                   2. Reset all the BGP connections with command "clear bgp vpnv4 unicast * vrf all"
                   3. Learn BGP Ops again and verify it is the same as the Ops in step 1
        """
    clear_cmd = ['clear bgp vpnv4 unicast * vrf all']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'

class TriggerClearBgpVpnv6UnicastVrfAll(TriggerClearBgpVpnv6UnicastVrfAll):
    """Reset the BGP connections for vpnv6 uncast address family sessions with using CLI
           command "clear bgp vpnv6 unicast * vrf all".

                  trigger_datafile:
                      Mandatory:
                          timeout:
                              max_time (`int`): Maximum wait time for the trigger,
                                              in second. Default: 180
                              interval (`int`): Wait time between iterations when looping is needed,
                                              in second. Default: 15
                      Optional:
                          tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                               restored to the reference rate,
                                               in second. Default: 60
                          tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                             in second. Default: 10

                  steps:
                      1. Learn BGP Ops object and store the "established" BGP neighbor(s)
                         for vpnv6 unicast address family
                         if has any, otherwise, SKIP the trigger
                      2. Reset all the BGP connections with command "clear bgp vpnv6 unicast * vrf all"
                      3. Learn BGP Ops again and verify it is the same as the Ops in step 1
           """
    clear_cmd = ['clear bgp vpnv6 unicast * vrf all']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'

class TriggerClearIpBgpVrfAll(TriggerClearIpBgpVrfAll):
    """Reset the BGP connections for IPv4 VRF address family sessions with using CLI command "clear ip bgp vrf all *".

           trigger_datafile:
               Mandatory:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger,
                                       in second. Default: 180
                       interval (`int`): Wait time between iterations when looping is needed,
                                       in second. Default: 15
               Optional:
                   tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                        restored to the reference rate,
                                        in second. Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                      in second. Default: 10

           steps:
               1. Learn BGP Ops object and store the "established" BGP neighbor(s)
                  if has any, otherwise, SKIP the trigger
               2. Reset all the BGP connections with command "clear ip route *"
               3. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """
    clear_cmd = ['clear ip bgp vrf all *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'

class TriggerRestartBgp(TriggerRestartBgp):
    """Restart the BGP instance using CLI command "restart bgp <bgp_id>".

       trigger_datafile:
           Mandatory:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger,
                                   in second. Default: 180
                   interval (`int`): Wait time between iterations when looping is needed,
                                   in second. Default: 15
           Optional:
               tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                    restored to the reference rate,
                                    in second. Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                  in second. Default: 10

       steps:
           1. Learn BGP Ops object and store the "established" BGP neighbor(s)
              if has any, otherwise, SKIP the trigger
           2. Soft reset all the BGP connections with command "clear ip route *"
           3. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """

    clear_cmd = ['restart bgp (?P<bgp_id>.*)']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'