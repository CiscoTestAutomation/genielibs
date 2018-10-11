'''NXOS implementation for routing clear triggers'''

# import genie.libs
from ..clear import TriggerClearIpRouteVrfAll as TriggerClearRouteVrfAll, \
                    TriggerClearIpv6RouteVrfAll as TriggerClearV6RouteVrfAll, \
                    TriggerClearIpRouteVrfDefault, \
                    TriggerClearIpv6RouteVrfDefault


class TriggerClearIpRouteVrfAll(TriggerClearRouteVrfAll):
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


class TriggerClearIpv6RouteVrfAll(TriggerClearV6RouteVrfAll):
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


class TriggerClearIpRoute(TriggerClearIpRouteVrfDefault):
    """Reset vrf default ipv4 route connections using CLI command "clear ip route *"."""

    __description__ = """Reset vrf default ip route connections using CLI command "clear ip route *".

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
        2. Reset vrf default route connections with command "clear ip route *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip route *']


class TriggerClearIpv6Route(TriggerClearIpv6RouteVrfDefault):
    """Reset vrf default ipv6 route connections using CLI command "clear ipv6 route *"."""

    __description__ = """Reset vrf default ipv6 route connections using CLI command "clear ipv6 route *".

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
        1. Learn routing Ops object and store the route ipv6 address(es)
           if has any, otherwise, SKIP the trigger
        2. Reset vrf default route connections with command "clear ipv6 route *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ipv6 route *']


class TriggerClearIpRouting(TriggerClearIpRouteVrfDefault):
    """Reset vrf default ip routing using CLI command "clear routing ip *"."""

    __description__ = """Reset vrf default ip routing using CLI command "clear routing ip *".

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
        2. Reset vrf default route connections with command "clear routing ip *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ip *']


class TriggerClearRouting(TriggerClearIpRouteVrfDefault):
    """Reset vrf default routing using CLI command "clear routing *"."""

    __description__ = """Reset vrf default routing using CLI command "clear routing *".

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
        1. Learn routing Ops object and store the route(s)
           if has any, otherwise, SKIP the trigger
        2. Reset vrf default route connections with command "clear routing *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing *']


class TriggerClearIpv6Routing(TriggerClearIpv6RouteVrfDefault):
    """Reset all ipv6 routing using CLI command "clear routing ipv6 *"."""

    __description__ = """Reset all ipv6 routing using CLI command "clear routing ipv6 *".

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
        2. Reset vrf default route connections with command "clear routing ipv6 *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ipv6 *']


class TriggerClearRoutingUnicast(TriggerClearIpRouteVrfDefault):
    """Reset all unicast route connections using CLI command "clear routing unicast *"."""

    __description__ = """Reset vrf default ip route connections using CLI command "clear routing unicast *".

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
        2. Reset vrf default route connections with command "clear routing unicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing unicast *']


class TriggerClearIpRoutingUnicast(TriggerClearIpRouteVrfDefault):
    """Reset all ip unicast routing using CLI command "clear routing ip unicast *"."""

    __description__ = """Reset all ip route connections using CLI command "clear routing ip unicast *".

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
        2. Reset vrf default route connections with command "clear routing ip unicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ip unicast *']


class TriggerClearIpv6RoutingUnicast(TriggerClearIpv6RouteVrfDefault):
    """Reset all ip unicast routing using CLI command "clear routing ipv6 unicast *"."""

    __description__ = """Reset all ip route connections using CLI command "clear routing ipv6 unicast *".

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
        2. Reset vrf default route connections with command "clear routing ipv6 unicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ipv6 unicast *']
