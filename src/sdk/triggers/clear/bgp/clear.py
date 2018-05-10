'''Common implementation for bgp clear triggers'''

# import ats
from ats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['keepalives','total', 'total_bytes', 'up_time', 'opens', 'capability',
           'updates', 'notifications', 'foreign_port', 'local_port', 'totals',
           'bgp_table_version', 'route_refresh', 'maker', 'callables',
           'connections_dropped', 'connections_established', 'last_reset',
           'bgp_negotiated_keepalive_timers', 'distance_extern_as',
           'reset_reason', 'holdtime', 'keepalive_interval']

class TriggerClearBgp(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    mapping_extra_args = {'ops':'ops_obj', 'relation':'sign',
                          'threshold_time':'compare_time'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})

    # Verify callable definition
    verify = CompareUptime.compare_uptime
    ops_lib = 'ops.bgp.bgp.Bgp'

    # Arguments for verify callable
    # Must be dictionary, key is argument from verify callable,
    # value should be the value to pass into the callable
    verify_func_args = {'r_obj': [R(['info', 'instance', '(?P<instance>.*)', 'vrf',
                                     '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                     'up_time', '(.*)'])]}


class TriggerClearBgpAll(TriggerClearBgp):
    pass
class TriggerClearIpBgpSoft(TriggerClearBgp):
    pass

class TriggerClearBgpNeighbor(TriggerClearBgp):
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1',
                                  'neighbor':'1'})

class TriggerClearBgpNeighborSoft(TriggerClearBgpNeighbor):
    pass


class TriggerClearBgpNeighborIpv4(TriggerClearBgp):

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\d\.]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})

class TriggerClearBgpNeighborIpv6(TriggerClearBgp):

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\w\:]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})

class TriggerClearBgpNeighborSoftIpv4(TriggerClearBgpNeighborIpv4):
    pass

class TriggerClearBgpNeighborSoftIpv6(TriggerClearBgpNeighborIpv6):
    pass


class TriggerClearIpRouteAll(TriggerClearBgp):
    pass

class TriggerClearBgpVpnv4UnicastVrfAll(TriggerClearBgp):

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp': {
                                            'requirements': [ \
                                                [['info', 'instance', '(?P<instance>.*)',
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                 'address_family','(?P<af>(vpnv4 unicast).*)',
                                                 'session_state', 'established']],
                                                [['routes_per_peer', 'instance', 'default',\
                                                 'vrf', '(?P<vrf>.*)','neighbor','(?P<neighbor>.*)',\
                                                 'address_family', '(?P<af>(vpnv4 unicast).*)','(.*)']]],
                                            'all_keys': True,
                                            'kwargs': {'attributes': ['routes_per_peer','info']},
                                            'exclude': exclude + ['msg_sent','msg_rcvd','up_down','tbl_ver']}},
                       num_values={'vrf': 'all','neighbor': 'all', 'af': 'all'})

    verify_func_args = {'r_obj': [R(['routes_per_peer', 'instance', 'default',
                                     'vrf', '(?P<vrf>.*)','neighbor','(?P<neighbor>.*)',
                                     'address_family', '(?P<af>vpnv4 unicast.*)',
                                     'up_down', '(.*)'])]}

class TriggerClearBgpVpnv6UnicastVrfAll(TriggerClearBgp):
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp': {
                                            'requirements': [ \
                                                [['info', 'instance', '(?P<instance>.*)',
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                 'address_family', '(?P<af>(vpnv6 unicast).*)',
                                                 'session_state', 'established']],
                                                [['routes_per_peer', 'instance', 'default', \
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', \
                                                 'address_family', '(?P<af>(vpnv6 unicast).*)', '(.*)']]],
                                            'all_keys': True,
                                            'kwargs': {'attributes': ['routes_per_peer','info']},
                                            'exclude': exclude + ['msg_sent', 'msg_rcvd', 'up_down', 'tbl_ver']}},
                                            num_values={'vrf': 'all', 'neighbor': 'all', 'af': 'all'})

    verify_func_args = {'r_obj': [R(['routes_per_peer', 'instance', 'default',
                                     'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                     'address_family', '(?P<af>vpnv6 unicast.*)',
                                     'up_down', '(.*)'])]}

class TriggerClearIpBgpVrfAll(TriggerClearBgp):
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp': {
                                            'requirements': [ \
                                                [['info', 'instance', '(?P<instance>.*)',
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                 'address_family', '(?P<af>.*)',
                                                 'session_state', 'established']],
                                                [['routes_per_peer', 'instance', '(?P<instance>.*)', \
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', \
                                                 'address_family', '(?P<af>ipv4.*)', '(.*)']]],
                                            'all_keys': True,
                                            'kwargs': {'attributes': ['info','routes_per_peer']},
                                            'exclude': exclude + ['msg_sent', 'msg_rcvd', 'up_down', 'tbl_ver']}},
                                            num_values={'vrf': 'all', 'neighbor': 'all', 'af': 'all'})

    verify_func_args = {'r_obj': [R(['routes_per_peer', 'instance', 'default',
                                     'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                     'address_family', '(?P<af>ipv4.*)',
                                     'up_down', '(.*)'])]}

class TriggerRestartBgp(TriggerClearBgp):

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp': {
                                            'requirements': [ \
                                                ['info', 'instance', '(?P<instance>.*)',
                                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                 'address_family', '(?P<af>.*)',
                                                 'session_state', 'established'],
                                                ['info','instance','(?P<instance>.*)','bgp_id', '(?P<bgp_id>.*)']
                                            ],
                                            'all_keys': True ,
                                            'kwargs': {'attributes': ['info']},
                                            'exclude': exclude}},
                                            num_values={'vrf': 'all', 'instance': 'all',
                                                        'neighbor': 'all', 'bgp_id': 'all'})
