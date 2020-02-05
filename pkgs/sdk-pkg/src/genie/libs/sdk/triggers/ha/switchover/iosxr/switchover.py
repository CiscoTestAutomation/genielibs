'''IOSXR implementation for Switchover triggers'''

# import python
import logging

# import pyats
from pyats import aetest
from pyats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerSwitchover as CommonSwitchover

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'total_free_bytes', 'rp_uptime']


class TriggerSwitchover(CommonSwitchover):
    """Do switchover on device."""
    
    __description__ = """Do switchover on device.

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
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                active_rp: `str`
                standby_rp: `str`
                virtual_device: `str`
                active_device: `str`
                standby_device: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Platform Ops object and store the "active" RP and "standby" RP
           if has any, otherwise, SKIP the trigger
        2. Do switchover by command "redundancy switchover"
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
                                              'vd_ms_red_state', 'Primary'],
                                            ['virtual_device', '(?P<virtual_device>.*)',
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
