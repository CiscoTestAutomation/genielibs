'''IOSXE ASR1K implementation for ISSU triggers'''

# Python
import sys
import argparse
import logging

# ATS
from pyats import aetest
from pyats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import TriggerIssu as CommonIssu

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'rp_uptime', 'sn', 'main_mem',
                    'switchover_reason', 'config_register']


class TriggerIssu(CommonIssu):
    """Do ISSU on device."""

    __description__ = """"Do ISSU on device.

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

                 (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)
     steps:
         1. Learn Platform Ops object and store the state of active rp ans standby rp
            if has any, otherwise, SKIP the trigger
         2. Do Issue on device.
         3. Learn Platform Ops again and the ops are the same as the Ops in step 1

     """

    # Parse argv for '--issu_upgrade_image'
    def parse_args(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('--issu_upgrade_image',
                            default=None,
                            help='URL path of the ISSU upgrade image')
        self.parameters['upgrade_image'] = parser.parse_args(argv).issu_upgrade_image

    mapping = Mapping(\
                requirements={\
                    'ops.platform.platform.Platform':{
                        'requirements': [\
                            [['slot', 'rp', '(?P<active_rp>.*)', 'state', 'ok, active'],
                            ['slot', 'rp', '(?P<active_rp>.*)', 'issu', 'in_progress', False]],
                            [['slot', 'rp', '(?P<standby_rp>.*)', 'state', 'ok, standby'],
                            ['slot', 'rp', '(?P<standby_rp>.*)', 'issu', 'in_progress', False]]],
                        'all_keys': True,
                        'exclude': platform_exclude}},
                verify_ops={\
                    'ops.platform.platform.Platform':{
                        'requirements': [\
                            ['slot', 'rp', '(?P<active_rp>.*)', 'state', 'ok, active'],
                            ['slot', 'rp', '(?P<standby_rp>.*)', 'state', 'ok, standby']],
                        'exclude': platform_exclude}},
                num_values={'active_rp':1, 'standby_rp':1})
