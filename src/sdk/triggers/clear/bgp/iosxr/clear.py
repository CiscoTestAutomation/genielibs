'''NXOS implementation for bgp clear triggers'''


# Genie Libs
from genie.libs.sdk.triggers.clear.bgp.clear import TriggerClearBgp


class TriggerClearBgpAll(TriggerClearBgp):
    """Hard reset all the BGP connections using CLI command
    "clear bgp instance all *" and "clear bgp instance all vrf all *".
    """
    
    __description__ = """Hard reset all the BGP connections using CLI command
    "clear bgp instance all *" and "clear bgp instance all vrf all *".

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
        2. Hard reset all the BGP connections with command "clear bgp instance all *"
           and "clear bgp instance all vrf all *"
        3. Learn BGP Ops again, verify the uptime of BGP "established" neighbor(s) is reset,
           and verify it is the same as the Ops in step 1 except the uptime

    """

    # These variables are NOT for user to change,
    # only specific for this trigger
    clear_cmd = ['clear bgp instance all *', 'clear bgp instance all vrf all *']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<='

