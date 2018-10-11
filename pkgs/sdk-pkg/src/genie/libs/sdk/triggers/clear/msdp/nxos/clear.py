'''NXOS implementation for Msdp clear triggers'''

# import genie.libs
from ..clear import TriggerClearMsdpPeer as TriggerClearMsdpPeerBase, \
                    TriggerClearMsdpStatistics as TriggerClearMsdpStatisticsBase, \
                    TriggerClearMsdpPolicyStatisticsSaPolicyIn as TriggerClearMsdpPolicyStatisticsSaPolicyInBase, \
                    TriggerClearMsdpPolicyStatisticsSaPolicyOut as TriggerClearMsdpPolicyStatisticsSaPolicyOutBase, \
                    TriggerClearMsdpSaCache as TriggerClearMsdpSaCacheBase, \
                    TriggerClearMsdpRoute as TriggerClearMsdpRouteBase


class TriggerClearMsdpPeer(TriggerClearMsdpPeerBase):
    """Reset msdp peer using CLI command "clear ip msdp peer x.x.x.x [ vrf <vrf> ]"."""

    __description__ = """Reset msdp peer using CLI command "clear ip msdp peer x.x.x.x [ vrf <vrf> ]".

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
        1. Learn Msdp Ops object and store the peer(s)
           if has any, otherwise, SKIP the trigger
        2. Reset msdp peers with command "clear ip msdp peer x.x.x.x [ vrf <vrf> ]"
        3. Learn Msdp Ops again, verify the elapsed_time of peer(s) is reset,
           and verify it is the same as the Ops in step 1 except the elapsed_time

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp peer (?P<peer>.*) vrf (?P<vrf>.*)']


class TriggerClearMsdpStatistics(TriggerClearMsdpStatisticsBase):
    """Reset msdp statistics using CLI command "clear ip msdp statistics x.x.x.x [vrf <vrf> ]"."""

    __description__ = """Reset msdp statistics using CLI command
    "clear ip msdp statistics x.x.x.x [vrf <vrf> ]".

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
        1. Learn Msdp Ops object and store the peer(s)
           if has any, otherwise, SKIP the trigger
        2. Reset msdp peers with command "clear ip msdp statistics x.x.x.x [vrf <vrf> ]"
        3. Learn Msdp Ops again, verify the discontinuity_time of peer(s) is reset,
           and verify it is the same as the Ops in step 1 except the discontinuity_time

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp statistics (?P<peer>.*) vrf (?P<vrf>.*)']


class TriggerClearMsdpPolicyStatisticsSaPolicyIn(TriggerClearMsdpPolicyStatisticsSaPolicyInBase):
    """Reset msdp peer statistics sa_policy in using CLI command
    "clear ip msdp policy statistics sa-policy x.x.x.x in"."""

    __description__ = """Reset msdp peer statistics sa_policy in using CLI command
    "clear ip msdp policy statistics sa-policy x.x.x.x in".

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
        1. Learn Msdp Ops object and store the peer(s) which has sa_policy in configured
           if has any, otherwise, SKIP the trigger
        2. Reset msdp peers with command "clear ip msdp policy statistics sa-policy x.x.x.x in"
        3. Learn Msdp Ops again, verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp policy statistics sa-policy (?P<peer>.*) in']


class TriggerClearMsdpPolicyStatisticsSaPolicyOut(TriggerClearMsdpPolicyStatisticsSaPolicyOutBase):
    """Reset msdp peer statistics sa_policy out using CLI command
    "clear ip msdp policy statistics sa-policy x.x.x.x out"."""

    __description__ = """Reset msdp peer statistics sa_policy out using CLI command
    "clear ip msdp policy statistics sa-policy x.x.x.x out".

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
        1. Learn Msdp Ops object and store the peer(s) which has sa_policy in configured
           if has any, otherwise, SKIP the trigger
        2. Reset msdp peers with command "clear ip msdp policy statistics sa-policy x.x.x.x out"
        3. Learn Msdp Ops again, verify it is the same as the Ops in step 1

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp policy statistics sa-policy (?P<peer>.*) out']


class TriggerClearMsdpSaCache(TriggerClearMsdpSaCacheBase):
    """Reset sa-cache for msdp groups using CLI command "clear ip msdp sa-cache x.x.x.x [vrf <vrf> ]"."""

    __description__ = """Reset sa cache for msdp groups using CLI command
    "clear ip msdp sa-cache x.x.x.x [vrf <vrf> ]".

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
        1. Learn Msdp Ops object and store the msdp sa-cache group(s)
           if has any, otherwise, SKIP the trigger
        2. Reset msdp sa-cache groups with command "clear ip msdp sa-cache x.x.x.x [vrf <vrf> ]"
        3. Learn Msdp Ops again, verify the uptime of group(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp sa-cache (?P<group>.*) vrf (?P<vrf>.*)']


class TriggerClearMsdpRoute(TriggerClearMsdpRouteBase):
    """Reset sa-cache for msdp groups using CLI command "clear ip msdp route x.x.x.x [ vrf < vrf> ]"."""

    __description__ = """Reset sa cache for msdp groups using CLI command
    "clear ip msdp route x.x.x.x [ vrf < vrf> ]".

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
        1. Learn Msdp Ops object and store the msdp sa-cache group(s)
           if has any, otherwise, SKIP the trigger
        2. Reset msdp sa-cache groups with command "clear ip msdp route x.x.x.x [ vrf < vrf> ]"
        3. Learn Msdp Ops again, verify the uptime of group(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ip msdp route (?P<group>.*) vrf (?P<vrf>.*)']
