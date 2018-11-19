'''Implementation for TRM unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from collections import OrderedDict
from ats.utils.objects import NotExists
from ats import aetest


# Which key to exclude for TRM Ops comparison
trm_exclude = ['maker']


class TriggerUnconfigConfigRouteTargetMvpn(TriggerUnconfigConfig):
    """Unconfigure route-target mvpn and reapply the whole configurations of dynamically learned Vrf."""

    __description__ = """Unconfigure route-target mvpn and reapply the whole configurations of dynamically learned Vrf.

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                    method (`str`): Method to recover the device configuration,
                                  Support methods:
                                    'checkpoint': Rollback the configuration by
                                                  checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config file on disk (iosxr)
            Optional:
                tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                     restored to the reference rate,
                                     in second. Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                   in second. Default: 10
                timeout_recovery:
                    Buffer recovery timeout when the previous timeout has been exhausted,
                    to make sure the devices are recovered before ending the trigger

                    max_time (`int`): Maximum wait time for the last step of the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15

        steps:
            1. Learn Vrf Conf object and check rt_mvpn is available
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the rt_mvpn with Vrf Conf object
            4. Verify the mvpn from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vrf Conf obj again and verify it is the same as the Ops in step 1

        """
    mapping = Mapping( \
        requirements={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr', '(?P<rt>.*)', \
                      'rt_type', '(?P<rt_type>.*)'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr', '(?P<rt>.*)',
                      '_protocol_attr', '(?P<protocol_name>^(mvpn).*)', 'rt_mvpn', True],
                    ['device_attr', '{uut}', 'vrf_name', '(?P<vrf>.*)']],
                'exclude': trm_exclude,
                'all_keys': True,
                'kwargs': {'attributes': ['vrf[vrf][(.*)]']}},
            'ops.vrf.vrf.Vrf':{
                 'requirements': [ \
                     ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                 'all_keys': False,
                 'kwargs': {'attributes': ['info']},
                 'exclude': trm_exclude}},
        config_info={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'rt_type', '(?P<rt_type>.*)'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', 'route_target_attr', '(?P<rt>.*)',\
                     'protocol_attr', '(?P<protocol_name>.*)', 'rt_mvpn', False]],
                'verify_conf': False,
                'kwargs': {'mandatory': {'name': '(?P<vrf>.*)'}}}},
        verify_ops={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr','(?P<rt>.*)',
                     '_protocol_attr', '(?P<protocol_name>(?!mvpn).*)', '(.*)']],
                'exclude': trm_exclude,
                'kwargs': {'attributes': ['vrf[vrf][(.*)]']},
                'missing': True},
            'ops.vrf.vrf.Vrf':{
                'requirements': [ \
                    ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                'kwargs': {'attributes': ['info']},
                'missing': False,
                'exclude': trm_exclude}},
        num_values={'protocol_name': 1, 'vrf': 1, 'rt': 1, 'rt_type': 1, 'af': 1})

class TriggerUnconfigConfigRouteTargetEvpn(TriggerUnconfigConfig):
    """Unconfigure route-target evpn and reapply the whole configurations of dynamically learned Conf Vrf."""

    __description__ = """Unconfigure route-target evpn and reapply the whole configurations of dynamically learned Vrf.

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                    method (`str`): Method to recover the device configuration,
                                  Support methods:
                                    'checkpoint': Rollback the configuration by
                                                  checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config file on disk (iosxr)
            Optional:
                tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                     restored to the reference rate,
                                     in second. Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                   in second. Default: 10
                timeout_recovery:
                    Buffer recovery timeout when the previous timeout has been exhausted,
                    to make sure the devices are recovered before ending the trigger

                    max_time (`int`): Maximum wait time for the last step of the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15

        steps:
            1. Learn Vrf Conf object and check rt_evpn is available
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the rt_evpn with Vrf Conf object
            4. Verify the evpn from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vrf Conf obj again and verify it is the same as the Ops in step 1

        """
    mapping = Mapping( \
        requirements= {\
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr', '(?P<rt>.*)', \
                     'rt_type', '(?P<rt_type>.*)'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr', '(?P<rt>.*)',
                      '_protocol_attr', '(?P<protocol_name>^(evpn).*)', 'rt_evpn', True],
                    ['device_attr', '{uut}', 'vrf_name', '(?P<vrf>.*)']],
                'exclude': trm_exclude,
                'all_keys': True },
            'ops.vrf.vrf.Vrf':{
                 'requirements': [ \
                     ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                 'kwargs': {'attributes': ['info']},
                 'exclude': trm_exclude}},
        config_info={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'rt_type', '(?P<rt_type>.*)'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'protocol_attr', 'evpn', 'rt_evpn', False]
                ],
                'verify_conf': False,
                'kwargs': {'mandatory': {'name': '(?P<vrf>.*)'}}}},
        verify_ops={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<af>.*)', '_route_target_attr','(?P<rt>.*)',
                     '_protocol_attr', '(?P<protocol_name>(?!evpn).*)', '(.*)']],
                'exclude': trm_exclude,
                'missing': True},
            'ops.vrf.vrf.Vrf':{
                'requirements': [ \
                    ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                'kwargs': {'attributes': ['info']},
                'missing': False,
                'exclude': trm_exclude}},
        num_values={'protocol_name': 1, 'vrf': 1, 'rt': 1, 'af': 1})

class TriggerUnconfigConfigAdvertiseEvpnMulticast(TriggerUnconfigConfig):
    """Unconfigure advertise evpn multisite and reapply the whole configurations of dynamically learned Conf Vxlan."""

    __description__ = """Unconfigure advertise evpn multisite and reapply the whole configurations of dynamically learned Vxlan.

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                    method (`str`): Method to recover the device configuration,
                                  Support methods:
                                    'checkpoint': Rollback the configuration by
                                                  checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config file on disk (iosxr)
            Optional:
                tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                     restored to the reference rate,
                                     in second. Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                   in second. Default: 10
                timeout_recovery:
                    Buffer recovery timeout when the previous timeout has been exhausted,
                    to make sure the devices are recovered before ending the trigger

                    max_time (`int`): Maximum wait time for the last step of the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15

        steps:
            1. Learn Vxlan Conf object and check advertise_evpn_multisite is available
               if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the advertise_evpn_multisite with Vxlan Conf object
            4. Verify the  advertise evpn multisite from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vxlan Conf obj again and verify it is the same as the Ops in step 1

        """

    mapping = Mapping( \
        requirements={ \
            'conf.vxlan.Vxlan': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'advertise_evpn_multicast', True]],
                'exclude': trm_exclude}},
        config_info={ \
            'conf.vxlan.Vxlan': {
                'requirements': [['device_attr', '{uut}', 'advertise_evpn_multicast', True]],
                'verify_conf': False,
                'kwargs': {}}},
        verify_ops={ \
            'conf.vxlan.Vxlan': {
                'requirements': [ \
                    ['device_attr', '{uut}', NotExists('advertise_evpn_multicast')]],
                'missing': False,
                'exclude': trm_exclude}},
        num_values={})
