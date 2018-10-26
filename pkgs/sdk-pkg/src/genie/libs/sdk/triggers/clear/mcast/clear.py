'''Common implementation for routing clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker', 'uptime']


class TriggerClearIpMroute(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    verify_func_args={'r_obj': [['table', 'vrf', '(?P<vrf>^default$)',
                                 'address_family', '(?P<af>ipv4)',
                                 'multicast_group', '(?P<group>.*)',
                                 'source_address', '(?P<source>.*)',
                                 'uptime', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                          'requirements':[\
                                              ['table', 'vrf', '(?P<vrf>^default$)',
                                               'address_family', '(?P<af>ipv4)',
                                               'multicast_group', '(?P<group>.*)',
                                               'source_address', '(?P<source>.*)', 'uptime', '(?P<uptime>.*)']],
                                          'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv4][multicast_group][(.*)][source_address][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.mcast.mcast.Mcast':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv4][multicast_group][(.*)][source_address][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route':'all',
                                  'af':'all'})


class TriggerClearIpv6Mroute(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    verify_func_args={'r_obj': [['table', 'vrf', '(?P<vrf>^default$)',
                                 'address_family', '(?P<af>ipv6)',
                                 'multicast_group', '(?P<group>.*)',
                                 'source_address', '(?P<source>.*)',
                                 'uptime', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                          'requirements':[\
                                              ['table', 'vrf', '(?P<vrf>^default$)',
                                               'address_family', '(?P<af>ipv6)',
                                               'multicast_group', '(?P<group>.*)',
                                               'source_address', '(?P<source>.*)', 'uptime', '(?P<uptime>.*)']],
                                          'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv6][multicast_group][(.*)][source_address][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.mcast.mcast.Mcast':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv6][multicast_group][(.*)][source_address][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route':'all',
                                  'af':'all'})
    

class TriggerClearIpMrouteVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    verify_func_args={'r_obj': [['table', 'vrf', '(?P<vrf>.*)',
                                 'address_family', '(?P<af>ipv4)',
                                 'multicast_group', '(?P<group>.*)',
                                 'source_address', '(?P<source>.*)',
                                 'uptime', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                          'requirements':[\
                                              ['table', 'vrf', '(?P<vrf>.*)',
                                               'address_family', '(?P<af>ipv4)',
                                               'multicast_group', '(?P<group>.*)',
                                               'source_address', '(?P<source>.*)', 'uptime', '(?P<uptime>.*)']],
                                          'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv4][multicast_group][(.*)][source_address][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.mcast.mcast.Mcast':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                               'table[vrf][(.*)][address_family][ipv4][multicast_group][(.*)][source_address][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route':'all',
                                  'af':'all'})


class TriggerClearIpv6MrouteVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    verify_func_args={'r_obj': [['table', 'vrf', '(?P<vrf>.*)',
                                 'address_family', '(?P<af>ipv6)',
                                 'multicast_group', '(?P<group>.*)',
                                 'source_address', '(?P<source>.*)',
                                 'uptime', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                          'requirements':[\
                                              ['table', 'vrf', '(?P<vrf>.*)',
                                               'address_family', '(?P<af>ipv6)',
                                               'multicast_group', '(?P<group>.*)',
                                               'source_address', '(?P<source>.*)', 'uptime', '(?P<uptime>.*)']],
                                          'kwargs':{'attributes': [
                                              'table[vrf][(.*)][address_family][ipv6][multicast_group][(.*)][source_address][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.mcast.mcast.Mcast':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': [
                                               'table[vrf][(.*)][address_family][ipv6][multicast_group][(.*)][source_address][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'route':'all',
                                  'af':'all'})
