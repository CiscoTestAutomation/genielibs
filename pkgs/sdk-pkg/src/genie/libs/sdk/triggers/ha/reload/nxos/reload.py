'''NXOS implementation for Reload triggers'''

# import python
import logging

# import pyats
from pyats import aetest
from pyats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerReload as CommonReload, \
                       TriggerReloadLc

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'disk_used_space','disk_total_space',
                    'rp_uptime', 'sn', 'disk_free_space',
                    'image', 'kickstart_image', 'main_mem']


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
        1. Learn Platform Ops object and store the "ok|active|ha-standby|standby" slot(s)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload"
        3. Learn Platform Ops again and verify the state of RP(s) is 
           "active|ha-standby", verify every LC status is "ok",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'rp', '(?P<rp>.*)',
                                             'state', '(?P<status>active|ha-standby)'],
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'state', '(?P<lc_status>ok|active|standby)']
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'rp', '(?P<rp>.*)',
                                             'state', '(active|ha-standby)'],
                                            ['slot', 'rp', '(?P<rp>.*)',
                                             'redundancy_state', '(active|ha-standby)'],
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'state', '(ok|active|standby)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all', 'lc': 'all'})


class TriggerReloadActiveSystemController(TriggerReloadLc):
    """Reload active system controller module on device."""
    
    __description__ = """Reload active system controller module on device.

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
        1. Learn Platform Ops object and store the "active" and "standby"
           system controller if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload module <lc>"
        3. Learn Platform Ops again and verify the roles of 
           "active" system controller and "standby" system controller are swapped,
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'active'],
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'name', 'System Controller'],
                                            ['slot', 'oc', '(?P<standby_sys_con>.*)',
                                             'state', 'standby'],
                                            ['slot', 'oc', '(?P<standby_sys_con>.*)',
                                             'name', 'System Controller'],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'standby'],
                                            ['slot', 'oc', '(?P<standby_sys_con>.*)',
                                             'state', 'active']],
                                    'exclude': platform_exclude}},
                      num_values={'oc': 1,
                                  'standby_sys_con': 1})


class TriggerReloadStandbySystemController(TriggerReloadLc):
    """Reload standby system controller module on device."""

    __description__ = """Reload standby system controller module on device.

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
        1. Learn Platform Ops object and store the "active" and "standby"
           system controller if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload module <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """
    '''Reload standby system controller'''

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'standby'],
                                             ['slot', 'oc', '(?P<oc>.*)',
                                             'name', 'System Controller'],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'standby']],
                                    'exclude': platform_exclude}},
                      num_values={'oc': 1})


class TriggerReloadFabricModule(TriggerReloadLc):
    """Reload fabric module on device."""

    __description__ = """Reload fabric module on device.

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
        2. Do reload by command "reload module <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'ok'],
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'name', '(?P<name>.*Fabric.*)'],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'oc', '(?P<oc>.*)',
                                             'state', 'ok']],
                                    'exclude': platform_exclude}},
                      num_values={'oc': 'all'})


class TriggerReloadEthernetModule(TriggerReloadLc):
    """Reload Ethernet module on device."""

    __description__ = """Reload Ethernet module on device.

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
        1. Learn Platform Ops object and store the "Ethernet" Lc(s)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload module <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'state', 'ok'],
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'name', '(?P<name>.*Ethernet.*)'],
                                          ],
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'state', 'ok']],
                                    'exclude': platform_exclude}},
                      num_values={'lc': 'all'})


class TriggerReloadActiveRP(TriggerReloadLc):
    """Reload active supervisor module on device."""

    __description__ = """Reload active supervisor module on device.

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
        2. Do reload by command "reload module <lc>"
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
                                            ['slot', 'rp', '(?P<active_rp>.*)',
                                              'redundancy_state', 'active'],
                                            ['slot', 'rp', '(?P<active_rp>.*)',
                                              'state', 'active'],
                                            ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'redundancy_state', 'ha-standby'],
                                            ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'ha-standby'],
                                            ['slot', 'lc', '(?P<lc>.*)',
                                             'state', '(?P<lc_status>ok|active|standby)']
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'redundancy_state', 'ha-standby'],
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'state', 'ha-standby'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'redundancy_state', 'active'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'state', 'active'],
                                          ['slot', 'lc', '(?P<lc>.*)',
                                           'state', '(ok|active|standby)']],
                                    'exclude': platform_exclude}},
                      num_values={'active_rp':1, 'standby_rp':1, 'lc':1})


class TriggerReloadStandbyRP(TriggerReloadLc):
    """Reload standby supervisor module on device."""

    __description__ = """Reload standby supervisor module on device.

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
        2. Do reload by command "reload module <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                             ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'redundancy_state', 'ha-standby'],
                                             ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'ha-standby'],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'redundancy_state', 'ha-standby']],
                                    'exclude': platform_exclude}},
                      num_values={'standby_rp':1})
