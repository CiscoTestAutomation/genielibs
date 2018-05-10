'''NXOS implementation for ipv6 clear triggers'''

# Genie Libs
from ..clear import TriggerClearIPv6NeighborVrfAll


class TriggerClearIPv6NeighborVrfAll(TriggerClearIPv6NeighborVrfAll):
    """Reset all the ipv6 neighbors using CLI command "clear ipv6 neighbor vrf all force-delete"."""

    __description__ = """Reset all the ipv6 neighbors using CLI command "clear ipv6 neighbor vrf all force-delete".

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
        1. Learn Nd Ops object and store the ipv6 neighbores
           if has any, otherwise, SKIP the trigger
        2. Reset all the ipv6 neighbors using CLI command "clear ipv6 neighbor vrf all force-delete"
        3. Learn Nd Ops again, verify the lifetime of neighbor(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """
    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear ipv6 neighbor vrf all force-delete']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign = '<='
