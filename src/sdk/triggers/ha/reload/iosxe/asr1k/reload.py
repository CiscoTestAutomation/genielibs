'''IOSXE implementation for Reload triggers'''

# import python
import logging

# import ats
from ats import aetest
from ats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerReload as CommonReload, \
                       TriggerReloadLc

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
                                            [['slot', 'lc', '(?P<lc>.*)',
                                              'state', 'ok']],
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
                                          ['slot', 'lc', '(?P<lc>.*)',
                                           'state', 'ok'],
                                          ['slot', 'oc', '(?P<oc>.*)',
                                           'state', '(ok, active|ok, standby|ok|ps, fail)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all', 'lc': 'all', 'oc': 'all'})


class TriggerReloadActiveFP(TriggerReloadLc):
    """Reload active "ESP" slot on device."""

    __description__ = """Reload active "ESP" slot on device.

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
        1. Learn Platform Ops object and store the "fabric" Lc(s)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "hw-module slot <lc> reload"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             ['slot', 'oc', '(?P<active_fp>.*)',
                                             'state', 'ok, active'],
                                             ['slot', 'oc', '(?P<active_fp>.*)',
                                             'name', '(.*ESP.*)'],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'oc', '(?P<active_fp>.*)',
                                             'state', 'ok, active']],
                                    'exclude': platform_exclude}},
                      num_values={'active_fp': 1})


class TriggerReloadActiveRP(TriggerReloadLc):
    """Reload active supervisor slot on device."""
    
    __description__ = """Reload active supervisor slot on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'active'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Platform Ops object and store the "ok, active" RP and "ok, standby" RP
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "hw-module slot <lc> reload"
        3. Learn Platform Ops again and verify the roles of 
           "ok, active" RP and "ok, standby" RP are swapped,
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    @aetest.test
    def reload(self, uut, abstract, steps):
        '''Reload and reconnect to device
           The actual command is same to switchover

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.ha = abstract.sdk.libs.abstracted_libs.ha.HA(device=uut)
        try:
            self.ha.switchover(timeout=self.timeout, steps=steps)
        except Exception as e:
            self.failed('Failed to reload active RP', from_exception=e)

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<active_rp>.*)',
                                              'redundancy_state', 'ACTIVE'],
                                             ['slot', 'rp', '(?P<active_rp>.*)',
                                              'state', 'ok, active']],
                                            [['slot', 'rp', '(?P<standby_rp>.*)',
                                              'redundancy_state', 'STANDBY HOT'],
                                             ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'ok, standby']],
                                            [['redundancy_communication', True]],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'redundancy_state', 'STANDBY HOT'],
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'state', 'ok, standby'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'redundancy_state', 'ACTIVE'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'state', 'ok, active']],
                                    'exclude': platform_exclude}},
                      num_values={'active_rp':1, 'standby_rp':1})


class TriggerReloadStandbyRP(TriggerReloadLc):
    """Reload standby supervisor slot on device."""

    __description__ = """Reload standby supervisor slot on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'active'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Platform Ops object and store the "ok, standby" RP
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "hw-module slot <lc> reload"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             [['slot', 'rp', '(?P<standby_rp>.*)',
                                              'redundancy_state', 'STANDBY HOT'],
                                             ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'ok, standby']],
                                             [['redundancy_communication', True]]
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'redundancy_state', 'STANDBY HOT']],
                                    'exclude': platform_exclude}},
                      num_values={'standby_rp':1})