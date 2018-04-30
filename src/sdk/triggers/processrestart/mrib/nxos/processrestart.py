'''
Implementation for Mrib Restart triggers
'''

# Genie Libs
from genie.libs.sdk.triggers.processrestart.processrestart import TriggerProcessRestart

exclude = ['last_restart_date', 'state_start_date',
           'last_terminate_reason', 'reboot_state',
           'previous_pid']


class TriggerProcessCrashRestartMrib(TriggerProcessRestart):
    """Restart the running Mrib process(es) with linux command "kill -6 <process>",
      expecting process crashes and generates a core. This will cause device to switchover."""
    
    __description__ = """Restart the running Mrib process(es) with linux command "kill -6 <process>",
    expecting process crashes and generates a core. This will cause device to switchover.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Mrib process(es) with command "show system internal sysmgr service name mrib",
           and store the "running" process(es) if has any, otherwise, SKIP the trigger
        2. Restart the learned Mrib process(es) from step 1 with command "kill -6 <process>"
           in linux shell mode
        3. Reconnect to the router due to the router switchover after restarting process mrib.
           Verify the pid of Mrib process(es) from step 2 is changed,
           restart count of Mrib process(es) from step 2 is increased by 1,
           the count of "SYSMGR-2-SERVICE_CRASHED:" in log is 1 per Mrib process from step 2,
           and only 1 core generated on mrib per Mrib process from step 2

    """
    process = 'mrib'
    method = 'crash'
    crash_method = '6'
    verify_exclude = exclude


class TriggerProcessKillRestartMrib(TriggerProcessRestart):
    """Restart the running Mrib process(es) with Linux command "kill -9 <process>"."""

    __description__ = """Restart the running Mrib process(es) with Linux command "kill -9 <process>".
    This will cause device to switchover.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Mrib process(es) with command "show system internal sysmgr service name mrib",
           and store the "running" process(es) if has any, otherwise, SKIP the trigger
        2. Restart the learned Mrib process(es) from step 1 with command "kill -9 <process>"
           in linux shell mode
        3. Reconnect to the router due to the router switchover after restarting process mrib.
           Verify the pid of Mrib process(es) from step 2 is changed,
           and restart count of Mrib process(es) from step 2 is increased by 1

    """
    process = 'mrib'
    method = 'crash'
    crash_method = '9'
    verify_exclude = exclude
