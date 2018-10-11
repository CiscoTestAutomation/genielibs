'''Common implementation for routing clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker','updated']


class TriggerClearIpRouteVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)',
                                 'address_family', 'ipv4',
                                 'routes', '(?P<route>.*)',
                                 'next_hop', 'next_hop_list','(?P<index>.*)',
                                 'updated', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                        'requirements': [ \
                                                ['info', 'vrf', '(?P<vrf>.*)',
                                                 'address_family', 'ipv4',
                                                 'routes', '(?P<route>.*)',
                                                 'active', True]],
                                        'kwargs': {'attributes': \
                                                ['info[vrf][(.*)][address_family][ipv4][routes][(.*)]']},
                                        'exclude': exclude}},
                      verify_ops={'ops.routing.routing.Routing':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][address_family][ipv4][routes][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route': 'all', 'af': 'all'})


class TriggerClearIpv6RouteVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)',
                                 'address_family', 'ipv6',
                                 'routes', '(?P<route>.*)',
                                 'next_hop', 'next_hop_list', '(?P<index>.*)',
                                 'updated', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                        'requirements': [ \
                                            ['info', 'vrf', '(?P<vrf>.*)',
                                             'address_family', 'ipv6',
                                             'routes', '(?P<route>.*)',
                                             'active', True]],
                                        'kwargs': {'attributes': \
                                                ['info[vrf][(.*)][address_family][ipv6][routes][(.*)]']},
                                        'exclude': exclude}},
                      verify_ops={'ops.routing.routing.Routing':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                                 'info[vrf][(.*)][address_family][ipv6][routes][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route': 'all', 'af': 'all'})


class TriggerClearIpRouteVrfDefault(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>^default$)',
                                 'address_family', 'ipv4',
                                 'routes', '(?P<route>.*)',
                                 'next_hop', 'next_hop_list','(?P<index>.*)',
                                 'updated', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                            'requirements': [ \
                                                ['info', 'vrf', '(?P<vrf>^default$)',
                                                 'address_family', 'ipv4',
                                                 'routes', '(?P<route>.*)',
                                                 'active', True]],
                                        'kwargs': {'attributes': \
                                                ['info[vrf][(.*)][address_family][ipv4][routes][(.*)]']},
                                            'exclude': exclude}},
                      verify_ops={'ops.routing.routing.Routing':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][address_family][ipv4][routes][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 1, 'route': 'all', 'af': 'all'})


class TriggerClearIpv6RouteVrfDefault(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>^default$)',
                                 'address_family', 'ipv6',
                                 'routes', '(?P<route>.*)',
                                 'next_hop', 'next_hop_list','(?P<index>.*)',
                                 'updated', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                            'requirements': [ \
                                                ['info', 'vrf', '(?P<vrf>^default$)',
                                                 'address_family', 'ipv6',
                                                 'routes', '(?P<route>.*)',
                                                 'active', True]],
                                        'kwargs': {'attributes': \
                                                ['info[vrf][(.*)][address_family][ipv6][routes][(.*)]']},
                                            'exclude': exclude}},
                      verify_ops={'ops.routing.routing.Routing':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                                  'info[vrf][(.*)][address_family][ipv6][routes][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 1, 'route': 'all', 'af': 'all'})
