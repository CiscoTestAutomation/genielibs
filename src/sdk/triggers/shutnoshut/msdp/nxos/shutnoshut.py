''' implementation for Msdp shut/noshut triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import \
                                      TriggerShutNoShut


exclude = ['maker', 'elapsed_time', 'discontinuity_time',
           'keepalive', 'total', 'up_time', 'expire', 'remote',
           'last_message_received', 'num_of_comparison', 'rpf_failure',
           'total_accept_count', 'total_reject_count', 'notification']


class TriggerShutNoShutMsdp(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Msdp peer(s)."""
    
    __description__ = """Shut and unshut the dynamically learned Msdp peer(s).

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
        1. Learn Vlan Ops object and store the Msdp 'established' peer(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Msdp peer(s) from step 1 with Msdp Conf object
        3. Verify the state of learned Msdp peer(s) from step 2 is "down"
        4. Unshut the Msdp peer(s) with Msdp Conf object
        5. Learn Msdp Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': exclude}},
                      config_info={'conf.msdp.Msdp':{
                                     'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'peer_attr', '(?P<peer>.*)', 'enable', False]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements': [\
                                    	['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                         '(?P<peer>.*)', 'session_state', 'admin-shutdown'],
                                    	['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                         '(?P<peer>.*)', 'enable', False]],
                                    'kwargs':{'attributes':['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 1, 'peer': 1})

