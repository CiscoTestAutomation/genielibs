'''IOSXE ASR1K implementation for ISSU triggers'''

# Python
import sys
import argparse
import logging

# ATS
from ats import aetest
from ats.utils.objects import R

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
