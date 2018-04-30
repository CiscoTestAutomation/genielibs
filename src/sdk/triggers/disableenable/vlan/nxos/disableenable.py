'''NXOS implementation for Vlan disable/enable triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable


# Which key to exclude for Mcast Ops comparison
vlan_exclude = ['maker']


class TriggerDisableEnableVlanInterface(TriggerDisableEnable):
    """Disable and enable feature interface-vlan when it is enabled."""

    __description__ = """Disable and enable feature interface-vlan when it is enabled.

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
        1. Learn Vlan Ops object and verify if interface-vlan is enabled, if not, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable interface-vlan feature with command "no feature interface-vlan"
           via Vlan Conf object
        4. Verify the state of feature interface-vlan is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature interface-vlan is "enabled" and 
           learn Vlan Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                        'requirements': [['info', 'vlans', 'interface_vlan_enabled', True]],
                                        'kwargs': {'attributes':['info']},
                                        'exclude': vlan_exclude}},
                      config_info={'conf.vlan.Vlan':{
                                    'requirements':[['device_attr', '{uut}','interface_vlan_enabled', 'disabled']],
                                    'verify_conf': False}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements': [['info', 'vlans', 'interface_vlan_enabled', False]],
                                    'kwargs': {'attributes': ['info']},
                                    'exclude': vlan_exclude}})


    feature_name = 'interface-vlan'


class TriggerDisableEnableVnSegmentVlan(TriggerDisableEnable):
    """Disable and enable feature vn-segment-vlan-based when it is enabled."""
  
    __description__ = """Disable and enable feature vn-segment-vlan-based when it is enabled.

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
        1. Learn Vlan Ops object and verify if vn-segment-vlan-based is enabled,
           if not, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable vn-segment-vlan-based feature with command "no feature vn-segment-vlan-based"
           via Vlan Conf object
        4. Verify the state of feature vn-segment-vlan-based is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature vn-segment-vlan-based is "enabled" and 
           learn Vlan Ops again and verify it is the same as the Ops in step 1


    """

    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                        'requirements': [['info', 'vlans', 'vn_segment_vlan_based_enabled', True]],
                                        'kwargs': {'attributes':['info']},
                                        'exclude': vlan_exclude}},
                      config_info={'conf.vlan.Vlan':{
                                    'requirements':[['device_attr', '{uut}','vn_segment_vlan_based_enabled', 'disabled']],
                                    'verify_conf': False}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements': [['info', 'vlans', 'vn_segment_vlan_based_enabled', False]],
                                    'kwargs': {'attributes': ['info']},
                                    'exclude': vlan_exclude}})

    feature_name = 'vnseg_vlan'