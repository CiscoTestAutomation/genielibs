'''IOSXR implementation for Reload triggers'''

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
platform_exclude = ['maker', 'total_free_bytes', 'rp_uptime']


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
        1. Learn Platform Ops object and store the "IOS XR RUN|OK" slot(s)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "admin reload location all"
        3. Learn Platform Ops again and verify the state of RP(s) is 
           "Active|Standby", verify every LC status is "IOS XR RUN|OK",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<rp>.*)',
                                              'state', 'IOS XR RUN']],
                                            [['slot', 'lc', '(?P<lc>.*)',
                                              'subslot', '(?P<subslot>.*)',
                                              'state', '(IOS XR RUN|OK)']],
                                            [['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<member>.*)',
                                              'vd_ms_red_state', '(Primary|Backup)']],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'state', 'IOS XR RUN'],
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'redundancy_state', '(Active|Standby)'],
                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'membership', '(?P<member>.*)',
                                           'vd_ms_red_state', '(Primary|Backup)'],
                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'vd_dSDRsc_nod', '([\w\/]+)'],
                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'vd_dSDRsc_partner_node', '([\w\/]+)'],
                                          ['slot', 'lc', '(?P<lc>.*)',
                                           'subslot', '(?P<subslot>.*)',
                                           'state', '(IOS XR RUN|OK)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all', 'lc': 'all', 'subslot': 'all',
                                  'virtual_device': 'all', 'member': 'all'})


class TriggerReloadActiveRP(TriggerReloadLc):
    """Reload active supervisor node on device.

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
        1. Learn Platform Ops object and store the "active" RP and "standby" RP
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "admin reload location <lc>"
        3. Learn Platform Ops again and verify the roles of 
           "active" RP and "standby" RP are swapped,
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<active_rp>.*)',
                                              'redundancy_state', 'Active'],
                                             ['slot', 'rp', '(?P<active_rp>.*)',
                                              'state', 'IOS XR RUN']],
                                            [['slot', 'rp', '(?P<standby_rp>.*)',
                                              'redundancy_state', 'Standby'],
                                             ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'IOS XR RUN']],
                                            [['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<active_device>.*)',
                                              'vd_ms_red_state', 'Primary']],
                                            [['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<standby_device>.*)',
                                              'vd_ms_red_state', 'Backup']],
                                            [['redundancy_communication', True]],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'redundancy_state', 'Standby'],
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'state', 'IOS XR RUN'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'redundancy_state', 'Active'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'state', 'IOS XR RUN'],

                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'membership', '(?P<active_device>.*)',
                                           'vd_ms_red_state', 'Backup'],
                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'membership', '(?P<standby_device>.*)',
                                           'vd_ms_red_state', 'Primary'],

                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'vd_dSDRsc_nod', '(?P<standby_device>.*)'],
                                          ['virtual_device', '(?P<virtual_device>.*)',
                                           'vd_dSDRsc_partner_node', '(?P<active_device>.*)']],
                                    'exclude': platform_exclude}},
                      num_values={'active_rp':1, 'standby_rp':1,
                                  'virtual_device': 1, 'active_device':1,
                                  'standby_device': 1})


class TriggerReloadStandbyRP(TriggerReloadLc):
    """Reload standby supervisor node on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'standby'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Platform Ops object and store the "standby" RP
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "admin reload location <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             ['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<standby_device>.*)',
                                              'vd_ms_red_state', 'Backup'],
                                             ['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<standby_device>.*)',
                                              'vd_ms_status', 'IOS XR RUN'],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                           ['virtual_device', '(?P<virtual_device>.*)',
                                            'membership', '(?P<standby_device>.*)',
                                            'vd_ms_red_state', 'Backup']],
                                    'exclude': platform_exclude}},
                      num_values={'virtual_device':1, 'standby_device': 1})


class TriggerReloadOirEdge(TriggerReloadLc):
    """Reload MPA node on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'lc'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Platform Ops object and store the "MPA" LC
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "admin reload location <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             ['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<lc>.*)',
                                              'vd_ms_type', 'LC'],
                                             ['virtual_device', '(?P<virtual_device>.*)',
                                              'membership', '(?P<lc>.*)',
                                              'vd_ms_status', 'IOS XR RUN'],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                           ['virtual_device', '(?P<virtual_device>.*)',
                                            'membership', '(?P<lc>.*)',
                                            'vd_ms_status', 'IOS XR RUN'],],
                                    'exclude': platform_exclude}},
                      num_values={'lc':'all', 'virtual_device':'all'})
