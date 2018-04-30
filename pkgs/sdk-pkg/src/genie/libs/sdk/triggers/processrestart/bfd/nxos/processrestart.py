'''
Implementation for Bfd Restart triggers
'''

# Genie Libs
from genie.libs.sdk.triggers.processrestart.processrestart import TriggerProcessRestart

exclude = ['last_restart_date', 'state_start_date',
           'last_terminate_reason', 'reboot_state',
           'previous_pid']

class TriggerProcessCrashRestartBfd(TriggerProcessRestart):
    """Restart the running Bfd process(es) with linux command "kill -6 <process>",
    expecting process crashes and generates a core."""
    
    __description__ = """Restart the running Bfd process(es) with linux command "kill -6 <process>",
    expecting process crashes and generates a core.

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
        1. Learn Bfd process(es) with command "show system internal sysmgr service name bfd",
           and store the "running" process(es) if has any, otherwise, SKIP the trigger
        2. Restart the learned Bfd process(es) from step 1 with command "kill -6 <process>"
           in linux shell mode
        3. Verify the pid of Bfd process(es) from step 2 is changed,
           restart count of Bfd process(es) from step 2 is increased by 1,
           the count of "SYSMGR-2-SERVICE_CRASHED:" in log is 1 per Bfd process from step 2,
           and only 1 core generated on bfd per Bfd process from step 2

    """
    process = 'bfd'
    method = 'crash'
    crash_method = '6'
    verify_exclude = exclude

class TriggerProcessKillRestartBfd(TriggerProcessRestart):
    """Restart the running Bfd process(es) with Linux command "kill -9 <process>"."""

    __description__ = """Restart the running Bfd process(es) with Linux command "kill -9 <process>"

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
        1. Learn Bfd process(es) with command "show system internal sysmgr service name bfd",
           and store the "running" process(es) if has any, otherwise, SKIP the trigger
        2. Restart the learned Bfd process(es) from step 1 with command "kill -9 <process>"
           in linux shell mode
        3. Verify the pid of Bfd process(es) from step 2 is changed,
           and restart count of Bfd process(es) from step 2 is increased by 1

    """
    process = 'bfd'
    method = 'crash'
    crash_method = '9'
    verify_exclude = exclude
