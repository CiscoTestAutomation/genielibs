'''Common implementation for bgp clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
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
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})


class TriggerClearBgpAll(TriggerClearBgp):
    pass

class TriggerClearIpBgpSoft(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '>=',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})

class TriggerClearBgpNeighbor(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1',
                                  'neighbor':'1'})


class TriggerClearBgpNeighborSoft(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '>=',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1',
                                  'neighbor':'1'})


class TriggerClearBgpNeighborIpv4(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\d\.]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})


class TriggerClearBgpNeighborIpv6(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\w\:]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})


class TriggerClearBgpNeighborSoftIpv4(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '>=',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\d\.]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})

class TriggerClearBgpNeighborSoftIpv6(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '>=',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[
                                              ['info', 'instance', '(?P<instance>.*)',
                                              'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>^[\w\:]+$)',
                                              'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'1', 'instance':'1','neighbor':'1'})


class TriggerClearIpRouteAll(TriggerClearBgp):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '>=',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[\
                                              ['info', 'instance', '(?P<instance>.*)',
                                               'vrf', '(?P<vrf>.*)','neighbor', '(?P<neighbor>.*)',
                                               'session_state', 'established']],
                                          'kwargs':{'attributes':['info']},
                                          'exclude': exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude}},
                      num_values={'vrf':'all', 'instance':'all',
                                  'neighbor':'all'})

class TriggerClearBgpVpnv4UnicastVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['routes_per_peer', 'instance', 'default',
                                 'vrf', '(?P<vrf>.*)','neighbor','(?P<neighbor>.*)',
                                 'address_family', '(?P<af>vpnv4 unicast.*)',
                                 'up_down', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

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
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['routes_per_peer','info']},
                                    'exclude': exclude + ['msg_sent','msg_rcvd','up_down','tbl_ver']}},
                       num_values={'vrf': 'all','neighbor': 'all', 'af': 'all'})


class TriggerClearBgpVpnv6UnicastVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['routes_per_peer', 'instance', 'default',
                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'address_family', '(?P<af>vpnv6 unicast.*)',
                                 'up_down', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

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
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['routes_per_peer','info']},
                                    'exclude': exclude + ['msg_sent','msg_rcvd','up_down','tbl_ver']}},
                                            num_values={'vrf': 'all', 'neighbor': 'all', 'af': 'all'})


class TriggerClearIpBgpVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['routes_per_peer', 'instance', 'default',
                                 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'address_family', '(?P<af>ipv4.*)',
                                 'up_down', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

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
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info','routes_per_peer']},
                                    'exclude': exclude + ['msg_sent','msg_rcvd','up_down','tbl_ver']}},
                      num_values={'vrf': 'all', 'neighbor': 'all', 'af': 'all'})


class TriggerRestartBgp(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'instance', '(?P<instance>.*)', 'vrf',
                                 '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

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
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'instance': 'all', 'neighbor': 'all', 'bgp_id': 'all'})
