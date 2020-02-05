'''NXOS Implementation for Vxlan addremove triggers'''

import logging
import time
log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from pyats import aetest
from collections import OrderedDict

# ATS
from pyats.utils.objects import NotExists, Not

trm_exclude =['maker']

class TriggerAddRemoveRouteTargetMvpn(TriggerAddRemove):
    """Add route-target mvpn then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add route-target mvpn then restore the
                               configuration by re-applying the whole running configuration

       trigger_datafile:
           Mandatory Arguments:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger in seconds.
                                     Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
                   method (`str`): Method to recover the device configuration.
                                   Supported methods:
                                       'checkpoint': Rollback the configuration
                                                     using checkpoint (nxos),
                                                     archive file (iosxe),
                                                     load the saved running-config
                                                     file on disk (iosxr)
           Optional Arguments:
               tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                    restored to the reference rate in seconds.
                                    Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic
                                  is resumed in seconds. Default: 10
               timeout_recovery:
                   Buffer recovery timeout make sure devices are recovered at the
                   end of the trigger execution. Used when previous timeouts have
                   been exhausted.
                   max_time (`int`): Maximum wait time for the last step of the
                                     trigger in seconds. Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
               static:
                   The keys below are dynamically learnt by default.
                   However, they can also be set to a custom value when provided in the trigger datafile.

                    vrf: `str`
                    address_family: `str`
                    rt: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
       Steps:
           1. Learn Vrf Conf object configured on device. SKIP the trigger if there
              is no vrf configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Add route-target mvpn that using Genie Vrf Conf.
           4. Verify the newly route-target mvpn under Vrf is reflected in
              device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn Vrf Conf object again and verify it is the same as step 1.
    """

    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        time.sleep(60)
        super().verify_configuration(uut, abstract, steps)

    PROTOCOL = 'mvpn'
    requirements = OrderedDict()
    requirements['conf.vrf.Vrf'] = {
        'requirements': [
            ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', '_route_target_attr', '(?P<rt>.*)',
              '_protocol_attr', NotExists(PROTOCOL)],
            ['device_attr', '{uut}', 'vrf_name', '(?P<vrf>.*)']],
        'all_keys': True,
        'exclude': trm_exclude}

    requirements['ops.vrf.vrf.Vrf'] = {
        'requirements': [['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
        'kwargs': {'attributes': ['info']},
        'exclude': trm_exclude}

    mapping = Mapping( \
        requirements= requirements,
        config_info={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'rt_type', 'both'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'protocol_attr', 'mvpn', 'rt_mvpn', True]
                ],
                'verify_conf': False,
                'kwargs': {'mandatory': {'name': '(?P<vrf>.*)'}}}},
        verify_ops={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', '_route_target_attr', '(?P<rt>.*)',
                     '_protocol_attr', 'mvpn', 'rt_mvpn', True]],
                'exclude': trm_exclude},
            'ops.vrf.vrf.Vrf': {
                'requirements': [ \
                    ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                'kwargs': {'attributes': ['info']},
                'exclude': trm_exclude}},
        num_values={'vrf': 1, 'rt': 1, 'address_family': 1})

class TriggerAddRemoveRouteTargetEvpn(TriggerAddRemove):
    """Add route-target evpn then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add route-target evpn then restore the
                            configuration by re-applying the whole running configuration

       trigger_datafile:
           Mandatory Arguments:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger in seconds.
                                     Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
                   method (`str`): Method to recover the device configuration.
                                   Supported methods:
                                       'checkpoint': Rollback the configuration
                                                     using checkpoint (nxos),
                                                     archive file (iosxe),
                                                     load the saved running-config
                                                     file on disk (iosxr)
           Optional Arguments:
               tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                    restored to the reference rate in seconds.
                                    Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic
                                  is resumed in seconds. Default: 10
               timeout_recovery:
                   Buffer recovery timeout make sure devices are recovered at the
                   end of the trigger execution. Used when previous timeouts have
                   been exhausted.
                   max_time (`int`): Maximum wait time for the last step of the
                                     trigger in seconds. Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
               static:
                   The keys below are dynamically learnt by default.
                   However, they can also be set to a custom value when provided in the trigger datafile.

                    vrf: `str`
                    rt: `str`
                    address_family: `str`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
       Steps:
           1. Learn Vrf Conf object configured on device. SKIP the trigger if there
              is no vrf configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Add route-target evpn that using Genie Vrf Conf.
           4. Verify the newly route-target evpn under Vrf is reflected in
              device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn Vrf Conf object again and verify it is the same as step 1.
    """

    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        time.sleep(30)
        super().verify_configuration( uut, abstract, steps)

    PROTOCOL = 'evpn'
    requirements = OrderedDict()
    requirements['conf.vrf.Vrf'] = {
        'requirements': [
            ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', '_route_target_attr', '(?P<rt>.*)',
             '_protocol_attr', NotExists(PROTOCOL),  NotExists('(.*)')],
            ['device_attr', '{uut}', 'vrf_name', '(?P<vrf>.*)']],
        'all_keys': True,
        'exclude': trm_exclude}

    requirements['ops.vrf.vrf.Vrf'] = {
        'requirements': [['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
        'kwargs': {'attributes': ['info']},
        'exclude': trm_exclude}

    mapping = Mapping( \
        requirements=requirements,
        config_info={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'rt_type', 'both'],
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', 'route_target_attr', '(?P<rt>.*)', \
                     'protocol_attr', 'evpn', 'rt_evpn', True]
                ],
                'verify_conf': False,
                'kwargs': {'mandatory': {'name': '(?P<vrf>.*)'}}}},
        verify_ops={ \
            'conf.vrf.Vrf': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'address_family_attr', '(?P<address_family>.*)', '_route_target_attr', '(?P<rt>.*)',
                     '_protocol_attr', 'evpn', 'rt_evpn', True]],
                'exclude': trm_exclude},
            'ops.vrf.vrf.Vrf': {
                'requirements': [ \
                    ['info', 'vrfs', '(?P<vrf>.*)', '(.*)']],
                'kwargs': {'attributes': ['info']},
                'exclude': trm_exclude}},
        num_values={'vrf': 1, 'rt': 1, 'address_family': 1})

class TriggerAddRemoveAdvertiseEvpnMulticast(TriggerAddRemove):
    """Add advertise evpn multicast then restore the
        configuration by reapplying the whole running configuration"""

    __description__ = """Add advertise evpn multicast then restore the
                               configuration by re-applying the whole running configuration

       trigger_datafile:
           Mandatory Arguments:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger in seconds.
                                     Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
                   method (`str`): Method to recover the device configuration.
                                   Supported methods:
                                       'checkpoint': Rollback the configuration
                                                     using checkpoint (nxos),
                                                     archive file (iosxe),
                                                     load the saved running-config
                                                     file on disk (iosxr)
           Optional Arguments:
               tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                    restored to the reference rate in seconds.
                                    Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic
                                  is resumed in seconds. Default: 10
               timeout_recovery:
                   Buffer recovery timeout make sure devices are recovered at the
                   end of the trigger execution. Used when previous timeouts have
                   been exhausted.
                   max_time (`int`): Maximum wait time for the last step of the
                                     trigger in seconds. Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15

       Steps:
           1. Learn Vxlan Conf object configured on device. SKIP the trigger if there
              is no vrf configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Add advertise evpn multicast that using Genie Vxlan Conf.
           4. Verify the newly advertise evpn multicast is reflected in
              device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn Vxaln Conf object again and verify it is the same as step 1.
    """

    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        time.sleep(30)
        super().verify_configuration(uut, abstract, steps)

    mapping = Mapping( \
        requirements={ \
            'conf.vxlan.Vxlan': {
                'requirements': [ \
                    ['device_attr', '{uut}', NotExists('advertise_evpn_multicast')]],
                'exclude': trm_exclude}},
        config_info={ \
            'conf.vxlan.Vxlan': {
                'requirements': [['device_attr', '{uut}', 'advertise_evpn_multicast', True]],
                'verify_conf': False,
                'kwargs': {}}},
        verify_ops={ \
            'conf.vxlan.Vxlan': {
                'requirements': [ \
                    ['device_attr', '{uut}', 'advertise_evpn_multicast', True]],
                'exclude': trm_exclude}},
        num_values={})
