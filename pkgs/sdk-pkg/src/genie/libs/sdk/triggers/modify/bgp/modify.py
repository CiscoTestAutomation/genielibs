'''Implementation for bgp modify triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# TODO: Better Mapping text to explain what does what

# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time', 'totals',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability', 'send_community',
               'distance_internal_as', 'distance_extern_as',
               'bgp_neighbor_counters', 'reset_reason',
               'holdtime', 'keepalive_interval', 'password_text']


class TriggerModifyBgpNeighborAsn(TriggerModify):
    """Modify and revert the remote-as number for
    dynamically learned "established" BGP neighbor(s)."""

    __description__ = """Modify and revert the remote-as number for
    dynamically learned "established" BGP neighbor(s).

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
        1. Learn BGP Ops object and store the "established" BGP neighbor(s) which has 
           remote-as configured. SKIP the trigger if there is no BGP neighbor(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the remote-as number of the learned BGP neighbor(s) from step 1
           with BGP Conf object
        4. Verify the remote-as number of learned BGP neighbor(s) from step 3
           changes to the modified number in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1
    """
    
    # Add more keys to be excluded for this trigger only
    bgp_exclude = bgp_exclude + ['aggregate_address_as_set', 
                                 'aggregate_address_ipv4_address', 
                                 'aggregate_address_ipv4_mask', 
                                 'aggregate_address_summary_only',
                                 'distance_local', 'disable_connected_check']

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'neighbor',
                                                           '(?P<neighbor>.*)', 'remote_as',
                                                           '(?P<remote_as>.*)'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                           'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                           '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                           'address_family', '(?P<address_family>.*)',
                                                           'session_state', 'established'],
                                                          ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                          'all_keys':True, 
                                          'kwargs':{'attributes':['info']},
                                          'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'nbr_remote_as',
                                                    88]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'remote_as', 88],
                                                  ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor',
                                                   '(?P<neighbor>.*)', 'session_state', '(?P<session_state>(idle|active).*)'],
                                                  ['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'session_state', '(?P<af_sstate>(idle|active).*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1})


class TriggerModifyBgpNeighborCluster(TriggerModify):
    """Modify and revert the cluster id for dynamically learned BGP instance(s)."""

    __description__ = """Modify and revert the cluster id for dynamically learned BGP instance(s).

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
        1. Learn BGP Ops object and store the BGP instance(s) which has cluster id
           configured. SKIP the trigger if there is no BGP instance(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the cluster id of the learned BGP neighbor(s) from step 1
           with BGP Conf object
        4. Verify the cluster id of learned BGP neighbor(s) from step 3
           changes to the modified id in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)',
                                             'vrf', '(?P<vrf>.*)', 'cluster_id', '(?P<cluster_id>.*)'],
                                                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True, 
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                 'cluster_id', '1.1.1.1']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                     '(?P<vrf>.*)', 'cluster_id', '1.1.1.1']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':'all', 'instance':1, 'neighbor':1,
                                  'address_family':1})


class TriggerModifyBgpNeighborRoutemapIn(TriggerModify):
    """Modify and revert the inbound route-map for dynamically learned BGP neighbors(s)."""

    __description__ = """Modify and revert the inbound route-map for dynamically learned BGP neighbors(s).

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
        1. Learn BGP Ops object and store the BGP neighbors(s) which has inbound route-map
           configured. SKIP the trigger if there is no BGP neighbors(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the inbound route-map of the learned BGP neighbor(s) from step 1
           with BGP Conf object
        4. Verify the inbound route-map of learned BGP neighbor(s) from step 3
           changes to the modified name in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Create a name for router map in
    new_name = 'bgp_' + time.ctime().replace(' ', '_').replace(':', '_')

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                          'address_family', '(?P<address_family>.*)',
                                                          'route_map_name_in', '(?P<route_map>.*)'],
                                                         ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True, 
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_in',
                                                    new_name]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_in', new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})


class TriggerModifyBgpNeighborRoutemapOut(TriggerModify):
    """Modify and revert the outbound route-map for dynamically learned BGP neighbors(s)."""
    
    __description__ = """Modify and revert the outbound route-map for dynamically learned BGP neighbors(s).

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
        1. Learn BGP Ops object and store the BGP neighbors(s) which has outbound route-map
           configured. SKIP the trigger if there is no BGP neighbors(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the outbound route-map of the learned BGP neighbor(s) from step 1
           with BGP Conf object
        4. Verify the outbound route-map of learned BGP neighbor(s) from step 3
           changes to the modified name in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Create a name for router map in
    new_name = 'bgp_' + time.ctime().replace(' ', '_').replace(':', '_')

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                         '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                         'address_family', '(?P<address_family>.*)',
                                                         'route_map_name_out', '(?P<route_map>.*)'],
                                                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                         'all_keys':True, 
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_out',
                                                    new_name]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_out', new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})
