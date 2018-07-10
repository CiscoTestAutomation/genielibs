'''
Implementation for BGP ShutNoShut triggers
'''

# import python
from collections import OrderedDict

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut


# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'routing_table_version',
               'total_memory', 'distance_extern_as', 'totals',
               'reset_reason', 'holdtime', 'keepalive_interval', 'password_text']

interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']


class TriggerShutNoShutBgp(TriggerShutNoShut):
    """Shut and unshut BGP protocol by shutdown/no shutdown the dynamically
    learned BGP instance(s)."""

    __description__ = """Shut and unshut BGP protocol by shutdown/no shutdown the dynamically
    learned BGP instance(s).

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
        1. Learn BGP Ops object and store the instance(s) and neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned BGP instance(s) from step 1 with BGP Conf object
        3. Verify the state of BGP instance(s) and
           state of neighbor(s) from step 2 are "shutdown"
        4. Unshut the BGP instance(s)
        5. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Add more keys to be excluded for this trigger only
    bgp_exclude = bgp_exclude + ['aggregate_address_as_set', 
                                 'aggregate_address_ipv4_address', 
                                 'aggregate_address_ipv4_mask', 
                                 'aggregate_address_summary_only',
                                 'distance_local', 'address_family']

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', '(?P<neigh_info>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                         'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}',
                                                      'protocol_shutdown', True]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'protocol_state',
                                                      'shutdown'],
                                                     ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                      '(?P<vrf>.*)', 'neighbor',
                                                      '(?P<neighbor>.*)', 'session_state', 
                                                      'shut (admin)'],
                                                     ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                      '(?P<vrf>.*)', 'neighbor',
                                                      '(?P<neighbor>.*)', 'shutdown', 
                                                      True]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':'all', 'vrf':'all', 'neighbor':'all'})


class TriggerShutNoShutBgpNeighbors(TriggerShutNoShut):
    """Shut and unshut dynamically learned BGP neighbor(s)."""

    __description__ = """Shut and unshut dynamically learned BGP neighbor(s).

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
        1. Learn BGP Ops object and store the "established" neighbor(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned BGP neighbor(s) from step 1 with BGP Conf object
        3. Verify the state of BGP neighbor(s) from step 2 is "shutdown"
        4. Unshut the BGP neighbor(s)
        5. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Add more keys to be excluded for this trigger only
    bgp_exclude = bgp_exclude + ['aggregate_address_as_set', 
                                 'aggregate_address_ipv4_address', 
                                 'aggregate_address_ipv4_mask', 
                                 'aggregate_address_summary_only',
                                 'distance_local']

    mapping = Mapping(\
            requirements={\
                'ops.bgp.bgp.Bgp': {
                    'requirements':[\
                        ['info', 'instance', '(?P<instance>.*)',
                        'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)',
                        'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'address_family', '(?P<address_family>.*)',
                        'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                    'all_keys':True,
                    'kwargs':
                        {'attributes':['info']},
                    'exclude': bgp_exclude}},
            config_info={\
                'conf.bgp.Bgp': {
                    'requirements':[\
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                        'neighbor_attr', '(?P<neighbor>.*)', 'nbr_shutdown', True]],
                    'verify_conf':False,
                    'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
            verify_ops={\
                'ops.bgp.bgp.Bgp': {
                    'requirements':[\
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'session_state', 'shut (admin)'],
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'address_family', '(?P<address_family>.*)',
                        'session_state', 'shut (admin)'],
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'shutdown', True]],
                    'kwargs':
                        {'attributes':['info']},
                    'exclude': bgp_exclude}},
            num_values={'instance':1, 'vrf':1, 'neighbor': 'all'})


class TriggerShutNoShutBgpLoopbackInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned loopback interface(s)."""
    
    __description__ = """Shut and unshut the dynamically learned loopback interface(s).

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
        1. Learn BGP Ops object and verify if has any update-source interface(s),
           and learn Interface Ops to verify if has any IP/IPv6 Loopback interface(s)
           that existed in the BGP update-source interface(s). Store the filtered
           BGP update-source Loopback interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the BGP learned update-source Loopback interface(s) from step 1
           with Interface Conf object
        3. Verify the state of learned update-source Loopback interface(s)
           from step 2 is "down"
        4. Unshut the update-source Loopback interface(s)
        5. Learn BGP Ops and Interface Ops again and
           verify them are the same as the Ops in step 1

    """

    # Add more keys to be excluded for this trigger only
    interface_exclude = interface_exclude + ['ipv6']

    requirements = OrderedDict()
    requirements['ops.bgp.bgp.Bgp'] = {
        'requirements':[['info', 'instance', '(?P<instance>.*)',
                         'vrf', '(?P<vrf>.*)',
                         'neighbor', '(?P<neighbor>.*)',
                         'update_source', '(?P<name>.*)']],
        'kwargs':{'attributes':['info']},
        'exclude': bgp_exclude + ['distance_local']}

    requirements['ops.interface.interface.Interface'] = {
        'requirements':[['info', '(?P<name>l|Loopback[0-9\s]+)',
                         'oper_status', 'up']],
        'exclude': interface_exclude}

    mapping = Mapping(requirements = requirements,
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down']],
                                      'exclude': interface_exclude + ['(mti.*)'] + ['(tunnel.*)']}},
                      num_values={'instance': 1, 'vrf': 1, 'neighbor': 1,
                                  'update_source': 1, 'name': 1,
                                  'ipv6': 1, 'status': 1})
