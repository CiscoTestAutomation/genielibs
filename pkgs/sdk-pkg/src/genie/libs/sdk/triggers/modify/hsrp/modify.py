'''Implementation for hsrp modify triggers'''

# import python
import time

from ats.datastructures.logic import Not

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify


# Which key to exclude for HSRP Ops comparison
hsrp_exclude = ['maker', 'active_ip_address', 'standby_ip_address',
                'active_router', 'hello_msec_flag', 'hold_msec_flag',
                'hello_msec', 'hold_msec', 'hello_sec', 'hold_sec',
                'active_ipv6_address', 'standby_ipv6_address']


class TriggerModifyHsrpIpv4StateActiveToStandby(TriggerModify):
    """Modify and revert the priority for dynamically learned HSRP ipv4 active group(s)."""

    __description__ = """Modify and revert the priority for dynamically learned HSRP ipv4 active group(s).

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
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn HSRP Ops object and store the HSRP ipv4 group(s) which is active and
           have standby connected. SKIP the trigger if there is no HSRP group(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the priority of the learned HSRP group(s) from step 1 to the lowest value
           with HSRP Conf object
        4. Verify the priority of the learned HSRP group(s) from step 3
           changes to the modified value in step 3,
           verify the state of the learned HSRP group(s) change from "active" to "standby"
        5. Recover the device configurations to the one in step 2
        6. Learn HSRP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.hsrp.hsrp.Hsrp':{
                                          'requirements':[['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'priority', '(?P<priority>.*)'],
                                                          ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'hsrp_router_state', 'active'],
                                                          ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'standby_router', '(?P<standby_router>^(?!unknown).*$)'],
                                                           ],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': hsrp_exclude}},
                      config_info={'conf.hsrp.Hsrp':{
                                     'requirements':[['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'group_number', '(?P<group_number>.*)'],
                                                     ['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'address_family', 'ipv4'],
                                                     ['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'priority', 1]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.hsrp.hsrp.Hsrp':{
                                    'requirements':[['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'hsrp_router_state', 'standby'],
                                                    ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'priority', 1],
                                                    ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv4', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'standby_router', 'local'], 
                                                    ],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': hsrp_exclude}},
                      num_values={'interface':1, 'group_number':1})


class TriggerModifyHsrpIpv6StateActiveToStandby(TriggerModify):
    """Modify and revert the priority for dynamically learned HSRP ipv6 active group(s)."""
    __description__ = """Modify and revert the priority for dynamically learned HSRP ipv6 active group(s).

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
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn HSRP Ops object and store the HSRP ipv6 group(s) which is active and
           have standby connected. SKIP the trigger if there is no HSRP group(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the priority of the learned HSRP group(s) from step 1 to the lowest value
           with HSRP Conf object
        4. Verify the priority of the learned HSRP group(s) from step 3
           changes to the modified value in step 3,
           verify the state of the learned HSRP group(s) change from "active" to "standby"
        5. Recover the device configurations to the one in step 2
        6. Learn HSRP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.hsrp.hsrp.Hsrp':{
                                          'requirements':[['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'priority', '(?P<priority>.*)'],
                                                          ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'hsrp_router_state', 'active'],
                                                          ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'standby_router', '(?P<standby_router>^(?!unknown).*$)'],
                                                           ],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': hsrp_exclude}},
                      config_info={'conf.hsrp.Hsrp':{
                                     'requirements':[['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'group_number', '(?P<group_number>.*)'],
                                                     ['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'address_family', 'ipv6'],
                                                     ['device_attr', '{uut}', 'interface_attr',
                                                      '(?P<interface>.*)', 'priority', 1]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.hsrp.hsrp.Hsrp':{
                                    'requirements':[['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'hsrp_router_state', 'standby'],
                                                    ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'priority', 1],
                                                    ['info', '(?P<interface>.*)', 'address_family',
                                                           'ipv6', 'version', '(?P<version>.*)',
                                                           'groups', '(?P<group_number>.*)', 'standby_router', 'local'], 
                                                    ],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': hsrp_exclude}},
                      num_values={'interface':1, 'group_number':1})


