'''Implementation for bgp addremove triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove

# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'distance_extern_as', 'totals',
               'reset_reason', 'holdtime', 'keepalive_interval']

route_map_exclude = ['maker']

bgp_exclude_keepalive = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id']

class TriggerAddRemoveBgpNeighborRoutemapPrefixlist(TriggerAddRemove):
    """Apply the inbound dynamically learned "prefix-list" route-map
    to the dynamically learned BGP neighbor(s), and remove the
    added route-map configurations.
    """

    __description__ = """Apply the inbound dynamically learned "prefix-list" route-map
    to the dynamically learned BGP neighbor(s), and remove the
    added route-map configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbor(s) if has any,
           otherwise, SKIP the trigger. Learn RoutePolicy Ops object
           to store the route-map name with prefix-list configured if has any,
           otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the inbound route-map (step 1) to learned
           BGP neighbor(s) from step 1 with BGP Conf object
        4. Verify the BGP neighbor(s) from step 3 has inbound route-map (step 1) configured
        5. Remove the route-map (step 1) configurations from the learned
           BGP neighbor(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.route_policy.route_policy.RoutePolicy':{
                                            'requirements':[['info', '(?P<info>.*)',
                                                             'statements', '(?P<statements>.*)',
                                                             'conditions',
                                                             'match_prefix_list', '(?P<match_prefix_list>.*)']],
                                            'exclude': route_map_exclude},
                                        'ops.bgp.bgp.Bgp':{
                                            'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                             'vrf', '(?P<vrf>.*)',
                                                             'neighbor', '(?P<neighbor>.*)',
                                                             'address_family', '(?P<address_family>.*)',
                                                             'bgp_table_version', '(?P<bgp_table_version>.*)'],
                                                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                            'all_keys': True,
                                            'kwargs':{'attributes':['info']},
                                            'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'vrf_attr', '(?P<vrf>.*)',
                                                       'neighbor_attr','(?P<neighbor>.*)',
                                                       'address_family_attr', '(?P<address_family>.*)',
                                                       'nbr_af_route_map_name_in', '(?P<info>.*)']],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                      'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                        'vrf', '(?P<vrf>.*)',
                                                        'neighbor', '(?P<neighbor>.*)',
                                                        'address_family', '(?P<address_family>.*)',
                                                        'route_map_name_in', '(?P<info>.*)']],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': bgp_exclude}},
                      num_values={'info':1, 'statements':'all', 'match_prefix_list':1, 'instance':1, 'vrf':1, 'address_family':1, 'neighbor':1, 'bgp_id':1, 'bgp_table_version':1})


class TriggerAddRemoveBgpNeighborRoutemapWeight(TriggerAddRemove):
    """Apply the inbound dynamically learned "weight" route-map
    to the dynamically learned BGP neighbor(s), and remove the
    added route-map configurations.
    """

    __description__ = """Apply the inbound dynamically learned "weight" route-map
    to the dynamically learned BGP neighbor(s), and remove the
    added route-map configurations.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP neighbor(s) if has any,
           otherwise, SKIP the trigger. Learn RoutePolicy Ops object
           to store the route-map name with weight configured if has any,
           otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of the inbound route-map (step 1) to learned
           BGP neighbor(s) from step 1 with BGP Conf object
        4. Verify the BGP neighbor(s) from step 3 has inbound route-map (step 1) configured
        5. Remove the route-map (step 1) configurations from the learned BGP
           neighbor(s) from step 1
        6. Recover the device configurations to the one in step 2
        7. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    mapping = Mapping(requirements={'ops.route_policy.route_policy.RoutePolicy':{
                                            'requirements':[['info', '(?P<info>.*)',
                                                             'statements', '(?P<statements>.*)',
                                                             'actions',
                                                             'set_weight', '(?P<set_weight>.*)']],
                                            'exclude': route_map_exclude},
                                        'ops.bgp.bgp.Bgp':{
                                            'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                             'vrf', '(?P<vrf>.*)',
                                                             'neighbor', '(?P<neighbor>.*)',
                                                             'address_family', '(?P<address_family>.*)',
                                                             'bgp_table_version', '(?P<bgp_table_version>.*)'],
                                                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                            'all_keys': True,
                                            'kwargs':{'attributes':['info']},
                                            'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'vrf_attr', '(?P<vrf>.*)',
                                                       'neighbor_attr','(?P<neighbor>.*)',
                                                       'address_family_attr', '(?P<address_family>.*)',
                                                       'nbr_af_route_map_name_in', '(?P<info>.*)']],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                      'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                        'vrf', '(?P<vrf>.*)',
                                                        'neighbor', '(?P<neighbor>.*)',
                                                        'address_family', '(?P<address_family>.*)',
                                                        'route_map_name_in', '(?P<info>.*)']],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': bgp_exclude}},
                      num_values={'info':1, 'statements':'all', 'set_weight':1, 'instance':1, 'vrf':1, 'address_family':1, 'neighbor':1, 'bgp_id':1, 'bgp_table_version':1})

