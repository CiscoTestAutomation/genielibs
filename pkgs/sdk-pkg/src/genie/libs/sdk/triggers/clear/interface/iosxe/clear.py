'''
IOSXE implementation for interface clear triggers
'''

# Genie
from genie.libs.sdk.triggers.clear.interface.clear import TriggerClearCounters


class TriggerClearCountersInterfaceAll(TriggerClearCounters):
    """Clear counters on all interfaces using CLI command "clear counters"."""
    
    __description__ = """Clear counters on all interfaces using CLI command "clear counters".

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
        1. Learn Interface Ops object and store the interface(s)
           if has any, otherwise, SKIP the trigger
        2. Hard reset all the BGP connections with command "clear counters"
        3. Learn Interface Ops again, verify the counter of the learned interface(s)
           is reset, and verify it is the same as the Ops in step 1

    """  
    
    clear_cmd = ['clear counters']
    sign='<='