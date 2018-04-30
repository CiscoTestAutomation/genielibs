'''IOSXE Implementation for Vlan shutnoshut triggers'''

# ats
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for Vlan Ops comparison


vlan_exclude = ['maker']

class TriggerShutNoShutVlan(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Vlan instance(s)."""
    
    __description__ = """Shut and unshut the dynamically learned Vlan instance(s).

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
            timeout_recovery: 
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Vlan Ops object and store the Vlan instance(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Vlan instance(s) from step 1 with Vlan Conf object
        3. Verify the state of learned Vlan instance(s) from step 2 is "down"
        4. Unshut the Vlan instance(s) with Vlan Conf object
        5. Learn Vlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                        'requirements':[['info','vlans','(?P<vlanid>^([2-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1][0][0][0-1]))$',\
                                                         'vlan_id','(?P<vlanid>^([2-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1][0][0][0-1]))$']],
                                        'kwargs': {'attributes': ['info']},
                                        'exclude': vlan_exclude }},
                      config_info={'conf.vlan.Vlan':{
                                     'requirements':[['device_attr', '{uut}', 'vlan_attr', '(?P<vlanid>.*)','shutdown', True]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'vlanid': '(?P<vlanid>.*)'}}}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements': [['info','vlans','(?P<vlanid>.*)','shutdown', True],
                                                     ['info', 'vlans', '(?P<vlanid>.*)', 'state', 'shutdown']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': vlan_exclude}},
                      num_values={'vlanid': 1})


