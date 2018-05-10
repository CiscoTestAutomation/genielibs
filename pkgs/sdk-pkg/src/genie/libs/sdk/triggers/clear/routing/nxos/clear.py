'''NXOS implementation for routing clear triggers'''

# import genie_libs
from ..clear import TriggerClearIpRouteVrfAll, \
                    TriggerClearIpv6RouteVrfAll


class TriggerClearIpRouteVrfAll(TriggerClearIpRouteVrfAll):
    """Reset all ip route connections using CLI command "clear ip route vrf all *"."""

    __description__ = """Reset all the ip route connections using CLI command "clear ip route vrf all *".

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
        1. Learn routing Ops object and store the route IP(s)
           if has any, otherwise, SKIP the trigger
        2. Reset all the route connections with command "clear ip route vrf all *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip route vrf all *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign = '<'


class TriggerClearIpv6RouteVrfAll(TriggerClearIpv6RouteVrfAll):
    """Reset all ipv6 routes connections using CLI command "clear ipv6 route vrf all *"."""

    __description__ = """Reset all the ipv6 route connections using CLI command "clear ipv6 route vrf all *".

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
           1. Learn routing Ops object and store the route IPv6(s)
              if has any, otherwise, SKIP the trigger
           2. Reset all the route connections with command "clear ip route vrf all *"
           3. Learn routing Ops again, verify the uptime of route(s) is reset,
              and verify it is the same as the Ops in step 1 except the uptime
    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ipv6 route vrf all *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign = '<'


