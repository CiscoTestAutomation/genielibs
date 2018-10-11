'''Implementation for bgp modify triggers'''

# import python
import time
import collections

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.bgp import modify

class TriggerModifyBgpNeighborRoutemapIn(modify.TriggerModifyBgpNeighborRoutemapIn):

    config_info = collections.OrderedDict()
    config_info['conf.route_policy.RoutePolicy'] =\
                     {'requirements':[],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'name': modify.TriggerModifyBgpNeighborRoutemapIn.new_name}}}

    config_info['conf.bgp.Bgp'] =\
                     {'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_in',
                                    modify.TriggerModifyBgpNeighborRoutemapIn.new_name]],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}

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
                                        'exclude': modify.bgp_exclude}},
                      config_info=config_info,
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_in', modify.TriggerModifyBgpNeighborRoutemapIn.new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': modify.bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})


class TriggerModifyBgpNeighborRoutemapOut(modify.TriggerModifyBgpNeighborRoutemapOut):

    config_info = collections.OrderedDict()
    config_info['conf.route_policy.RoutePolicy'] =\
                     {'requirements':[],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'name': modify.TriggerModifyBgpNeighborRoutemapOut.new_name}}}

    config_info['conf.bgp.Bgp'] =\
                     {'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_out',
                                    modify.TriggerModifyBgpNeighborRoutemapOut.new_name]],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}

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
                                        'exclude': modify.bgp_exclude}},
                      config_info=config_info,
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_out', modify.TriggerModifyBgpNeighborRoutemapOut.new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': modify.bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})
