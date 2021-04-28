'''NXOS implementation for ISSU triggers'''

# Python
import sys
import argparse
import logging
from os.path import basename

# ATS
from pyats import aetest
from pyats.utils.objects import R
from pyats.utils.objects import Not

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import TriggerIssu as CommonIssu

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'rp_uptime', 'sn', 'main_mem',
                    'switchover_reason', 'config_register',
                    'image', 'disk_used_space', 'disk_free_space',
                    'version', 'rp_boot_image']

platform_exclude_lxc = ['maker', 'rp_uptime', 'sn', 'main_mem',
                        'switchover_reason', 'config_register',
                        'image', 'disk_used_space', 'disk_free_space',
                        'version', 'rp_boot_image', 'rp']

class TriggerIssuLxc(CommonIssu):
    """Do LXC ISSU on device."""

    __description__ = """"Do LXC ISSU on device.

     trigger_datafile:
         Mandatory:
             timeout:
                 max_time (`int`): Maximum wait time for the trigger,
                                 in second. Default: 180
                 interval (`int`): Wait time between iteration when looping is needed,
                                 in second. Default: 15
     steps:
         1. Learn Platform Ops object and store the state of active rp, otherwise, SKIP the trigger
         2. Do Issue on device.
         3. Learn Platform Ops again and the ops are the same as the Ops in step 1

     """

    # Parse argv for '--issu_upgrade_image'
    def parse_args(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('--issu_upgrade_image',
                            default=None,
                            help='URL path of the ISSU upgrade image')
        args, unknown = parser.parse_known_args(argv)
        self.parameters['upgrade_image'] = args.issu_upgrade_image

    mapping = Mapping(
        requirements={
            'ops.platform.platform.Platform': {
                'requirements': [
                    ['slot', 'rp', '(?P<rp>.*)', 'state',
                        '(?P<status>active)']
                ],
                'exclude': platform_exclude_lxc}},
        verify_ops={
            'ops.platform.platform.Platform': {
                'requirements': [
                    ['slot', 'rp', Not('(?P<rp>.*)'), 'state',
                        '(?P<status>active)']
                ],
                'exclude': platform_exclude_lxc}},
        num_values={'rp': 'all', 'status': 'all'})


class TriggerIssuNative(CommonIssu):
    """Do Native ISSU on device."""

    __description__ = """"Do Native ISSU on device.

     trigger_datafile:
         Mandatory:
             timeout:
                 max_time (`int`): Maximum wait time for the trigger,
                                 in second. Default: 180
                 interval (`int`): Wait time between iteration when looping is needed,
                                 in second. Default: 15
     steps:
         1. Learn Platform Ops object and store the state of active rp, otherwise, SKIP the trigger
         2. Do Issue on device.
         3. Learn Platform Ops again and the ops are the same as the Ops in step 1

     """

    # Parse argv for '--issu_upgrade_image'
    def parse_args(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('--issu_upgrade_image',
                            default=None,
                            help='URL path of the ISSU upgrade image')
        args, unknown = parser.parse_known_args(argv)
        self.parameters['upgrade_image'] = args.issu_upgrade_image

    mapping = Mapping(
        requirements={
            'ops.platform.platform.Platform': {
                'requirements': [
                    ['slot', 'rp', '(?P<active_rp>.*)', 'state', 'active']],
                'all_keys': False,
                'exclude': platform_exclude}},
        verify_ops={
            'ops.platform.platform.Platform': {
                'requirements': [
                    ['slot', 'rp', '(?P<active_rp>.*)', 'state', 'active']],
                'all_keys': False,
                'exclude': platform_exclude}},
        num_values={'active_rp': 1})
