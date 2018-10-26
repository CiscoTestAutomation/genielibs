'''NXOS implementation for Mcast clear triggers'''

# import genie.libs
from ..clear import TriggerClearIpMroute as TriggerClearIpMrouteBase, \
                    TriggerClearIpv6Mroute as TriggerClearIpv6MrouteBase, \
                    TriggerClearIpMrouteVrfAll as TriggerClearIpMrouteVrfAllBase, \
                    TriggerClearIpv6MrouteVrfAll as TriggerClearIpv6MrouteVrfAllBase


class TriggerClearIpMroute(TriggerClearIpMrouteBase):
    """Reset vrf default ipv4 Mroute using CLI command "clear ip mroute *"."""

    __description__ = """Reset vrf default ip Mroute using CLI command "clear ip mroute *".

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
        2. Reset vrf default route connections with command "clear ip mroute *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip mroute *']


class TriggerClearIpv6Mroute(TriggerClearIpv6MrouteBase):
    """Reset vrf default ipv6 Mroute using CLI command "clear ipv6 mroute *"."""

    __description__ = """Reset vrf default ipv6 Mroute using CLI command "clear ipv6 mroute *".

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
        2. Reset vrf default route connections with command "clear ipv6 mroute *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ipv6 mroute *']


class TriggerClearIpMrouteVrfAll(TriggerClearIpMrouteVrfAllBase):
    """Reset all the vrf ipv4 Mroute using CLI command "clear ip mroute * vrf all"."""

    __description__ = """Reset all the vrf ipv4 Mroute using CLI command "clear ip mroute * vrf all".

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
        2. Reset vrf default route connections with command "clear ip mroute * vrf all"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip mroute * vrf all']


class TriggerClearIpv6MrouteVrfAll(TriggerClearIpv6MrouteVrfAllBase):
    """Reset all the vrf ipv6 Mroute using CLI command "clear ipv6 mroute * vrf all"."""

    __description__ = """Reset all the vrf ipv6 Mroute using CLI command "clear ipv6 mroute * vrf all".

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
        2. Reset vrf default route connections with command "clear ipv6 mroute * vrf all"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ipv6 mroute * vrf all']


class TriggerClearIpRoutingMulticast(TriggerClearIpMrouteBase):
    """Reset all ip multicast route connections using CLI command "clear routing ip multicast *"."""

    __description__ = """Reset all ip multicast route connections using CLI command "clear routing ip multicast *".

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
        2. Reset vrf default route connections with command "clear routing ip multicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ip multicast *']


class TriggerClearRoutingMulticast(TriggerClearIpMrouteBase):
    """Reset all multicast route connections using CLI command "clear routing multicast *"."""

    __description__ = """Reset all multicast route connections using CLI command "clear routing multicast *".

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
        2. Reset vrf default route connections with command "clear routing multicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing multicast *']


class TriggerClearV4RouteMulticast(TriggerClearIpMrouteBase):
    """Reset all V4 multicast route using CLI command "clear routing ipv4 multicast *"."""

    __description__ = """Reset all V4 multicast route using CLI command "clear routing ipv4 multicast *".

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
        2. Reset vrf default route connections with command "clear routing ipv4 multicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ipv4 multicast *']


class TriggerClearV6RouteMulticast(TriggerClearIpv6MrouteBase):
    """Reset all V6 multicast route using CLI command "clear routing ipv6 multicast *"."""

    __description__ = """Reset all V6 multicast route using CLI command "clear routing ipv6 multicast *".

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
        2. Reset vrf default route connections with command "clear routing ipv6 multicast *"
        3. Learn routing Ops again, verify the uptime of route(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear routing ipv6 multicast *']