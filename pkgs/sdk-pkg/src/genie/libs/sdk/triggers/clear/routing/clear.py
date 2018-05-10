'''Common implementation for routing clear triggers'''

from ats.utils.objects import R

from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker','updated']

class TriggerClearIp(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    mapping_extra_args = {'ops':'ops_obj', 'relation':'sign',
                          'threshold_time': 'compare_time'}

    mapping = Mapping(requirements={'ops.routing.routing.Routing':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)',
                                               'address_family', '(?P<af>.*)',
                                               'routes', '(?P<route>.*)',
                                               'active', True]],
                                          'kwargs':{'attributes': ['info']},
                                          'exclude': exclude}},
                      num_values={'vrf':'all', 'route':'all',
                                  'af':'all'})

    # Verify callable definition
    verify = CompareUptime.compare_uptime
    ops_lib = 'ops.routing.routing.Routing'

    # Arguments for verify callable
    # Must be dictionary, key is argument from verify callable,
    # value should be the value to pass into the callable
    verify_func_args = {'r_obj': [R(['info', 'vrf', '(?P<vrf>.*)',
                                     'address_family', '(?P<af>.*)',
                                     'routes', '(?P<route>.*)',
                                     'next_hop', 'next_hop_list','(?P<index>.*)',
                                     'updated', '(.*)'])]}

class TriggerClearIpRouteVrfAll(TriggerClearIp):

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                            'requirements': [ \
                                                ['info', 'vrf', '(?P<vrf>.*)',
                                                 'address_family', 'ipv4',
                                                 'routes', '(?P<route>.*)',
                                                 'active', True]],
                                            'kwargs': {'attributes': ['info']},
                                            'exclude': exclude}},
                                            num_values={'vrf': 'all', 'route': 'all',
                                                        'af': 'all'})

    verify_func_args = {'r_obj': [R(['info', 'vrf', '(?P<vrf>.*)',
                                     'address_family', 'ipv4',
                                     'routes', '(?P<route>.*)',
                                     'next_hop', 'next_hop_list','(?P<index>.*)',
                                     'updated', '(.*)'])]}

class TriggerClearIpv6RouteVrfAll(TriggerClearIp):

    mapping = Mapping(requirements={'ops.routing.routing.Routing': {
                                        'requirements': [ \
                                            ['info', 'vrf', '(?P<vrf>.*)',
                                             'address_family', 'ipv6',
                                             'routes', '(?P<route>.*)',
                                             'active', True]],
                                        'kwargs': {'attributes': ['info']},
                                        'exclude': exclude}},
                                        num_values={'vrf': 'all', 'route': 'all',
                                                    'af': 'all'})

    verify_func_args = {'r_obj': [R(['info', 'vrf', '(?P<vrf>.*)',
                                     'address_family', 'ipv6',
                                     'routes', '(?P<route>.*)',
                                     'next_hop', 'next_hop_list', '(?P<index>.*)',
                                     'updated', '(.*)'])]}

