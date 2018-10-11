'''IOSXE implementation for Reload triggers'''

# import python
import logging

# import ats
from ats import aetest
from ats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerReload as CommonReload

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'rp_uptime', 'sn', 'main_mem',
                    'switchover_reason', 'config_register']


class TriggerReload(CommonReload):
    """Reload the whole device."""
    
    __description__ = """Reload the whole device.

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
        1. Learn Platform Ops object and store the "ok, active|ok, standby|Ready" slot(s)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload"
        3. Learn Platform Ops again and verify the state of RP(s) is 
           "ok, active|ok, standby", verify every LC status is "Ready",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<rp>.*)',
                                              'state', '(ok, active|ok, standby|Ready)']],
                                            [['slot', 'oc', '(?P<oc>.*)',
                                              'state', '(ok, active|ok, standby|ok|ps, fail)']],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'state', '(ok, active|ok, standby|Ready)'],
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'redundancy_state', '(ACTIVE|STANDBY HOT)'],
                                          ['slot', 'oc', '(?P<oc>.*)',
                                           'state', '(ok, active|ok, standby|ok|ps, fail)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all', 'oc': 'all'})
