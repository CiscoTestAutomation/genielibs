'''IOSXE Implementation for bgp modify triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id']


class TriggerModifyBgpNeighborAsn(TriggerModify):

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
                                                   '(?P<neighbor>.*)', 'session_state', 'idle']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1})


class TriggerModifyBgpNeighborCluster(TriggerModify):

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)',
                                             'vrf', 'default', 'cluster_id', '(?P<cluster_id>.*)'],
                                                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                                    'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      config_info={'conf.bgp.Bgp':{
                                     'requirements':[['device_attr', '{uut}', 'vrf_attr', 'default',
                                                 'cluster_id', '1.0.0.1']],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                     'default', 'cluster_id', '1.0.0.1']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':1, 'neighbor':1, 'address_family':1})


class TriggerModifyBgpNeighborRoutemapIn(TriggerModify):

    # Create a name for router map in
    new_name = 'bgp_' + time.ctime().replace(' ', '_').replace(':', '_')

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>(?!:).*)',
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
