'''Implementation for vlan unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from pyats.utils.objects import NotExists

# Which key to exclude for Vlan Ops comparison
vlan_exclude = ['maker']

class TriggerUnconfigConfigVlan(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned vlan(s)."""
    
    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned vlan(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            method (`str`): Method to recover the device configuration,
                            Support methods:
                            'checkpoint': Rollback the configuration by checkpoint
                            'local': Rollback the configuration by locally saved config
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
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                vlan: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Vlan Ops object and store the "unshut" vlan(s) if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned vlan with Vlan Conf object
        4. Verify the vlan(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Vlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                        'requirements':[['info','vlans','(?P<vlan>^([2-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1][0][0][0-1]))$'\
                                                            ,'vlan_id','(?P<vlan>^([2-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1][0][0][0-1]))$'],
                                                        ['info','vlans','(?P<vlan>.*)','shutdown',False]],
                                        'kwargs': {'attributes': ['info']},
                                        'all_keys':True,
                                        'exclude': vlan_exclude}},
                      config_info={'conf.vlan.Vlan':{
                                     'requirements':[['device_attr', '{uut}', 'vlan_attr', '(?P<vlan>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'vlanid': '(?P<vlan>.*)'}}}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements': [['info','vlans', NotExists('(?P<vlan>.*)')]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': vlan_exclude}},
                      num_values={'vlan':1})



class TriggerUnconfigConfigVlanVnsegment(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned vlan(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned vlan(s).

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
            Optional:
                method (`str`): Method to recover the device configuration,
                                Support methods:
                                'checkpoint': Rollback the configuration by checkpoint
                                'local': Rollback the configuration by locally saved config
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
                static:
                    The keys below are dynamically learnt by default.
                    However, they can also be set to a custom value when provided in the trigger datafile.

                    vlan: `str`
                    vn_segment_id: `int`
                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                         OR
                         interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn Vlan Ops object and store the "unshut" vlan(s) if has any, otherwise, SKIP the trigger
            2. Save the current device configurations through "method" which user uses
            3. Unconfigure the learned vn_segment_id with Vlan Conf object
            4. Verify the vlan(s) from step 3 are no longer existed
            5. Recover the device configurations to the one in step 2
            6. Learn Vlan Ops again and verify it is the same as the Ops in step 1

        """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                          'requirements':[['info','vlans','(?P<vlan>.*)','vn_segment_id','(?P<vn_segment_id>.*)']],
                                          'kwargs':{'attributes':['info[vlans][(.*)][vn_segment_id]']},
                                          'all_keys':True,
                                          'exclude': vlan_exclude}},
                      config_info={'conf.vlan.Vlan':{
                                     'requirements':[['device_attr','{uut}','vlan_attr','(?P<vlan>.*)',
                                                      'vn_segment_id','(?P<vn_segment_id>.*)']],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements':[['info','vlans',NotExists('(?P<vlan>.*)')]],
                                    'kwargs':{'attributes':['info[vlans][(.*)][vn_segment_id]']},
                                    'exclude': vlan_exclude}},
                      num_values={'vlan':1})
