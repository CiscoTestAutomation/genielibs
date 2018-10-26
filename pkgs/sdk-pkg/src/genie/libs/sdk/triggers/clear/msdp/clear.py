'''Common implementation for routing clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime, CompareCounters

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker', 'elapsed_time', 'discontinuity_time',
           'keepalive', 'total', 'up_time', 'expire', 'remote',
           'last_message_received', 'num_of_comparison', 'rpf_failure',
           'total_accept_count', 'total_reject_count', 'notification']


class TriggerClearMsdpPeer(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)', 'peer', '(?P<peer>.*)', 'elapsed_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'peer':'all'})


class TriggerClearMsdpStatistics(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                 '(?P<peer>.*)', 'statistics', 'discontinuity_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'peer':'all'})


class TriggerClearMsdpPolicyStatisticsSaPolicyIn(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                 '(?P<peer>.*)', 'statistics', 'sa_policy',
                                 'in', '(?P<sa_filter_in>.*)', '(?P<match>.*)',
                                 'num_of_comparison', '(.*)']],
                      'relation': '<',
                      'threshold_counter': '(?P<num>.*)',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'statistics', 'sa_policy', 'in', '(?P<sa_filter_in>.*)',
                                               '(?P<match>.*)', 'num_of_comparison', '(?P<num>^(?!0).*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][statistics][sa_policy][in]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareCounters.compare_counter,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][statistics][sa_policy][in]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'peer':'all', 'num': 1})


class TriggerClearMsdpPolicyStatisticsSaPolicyOut(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                 '(?P<peer>.*)', 'statistics', 'sa_policy',
                                 'out', '(?P<sa_filter_out>.*)', '(?P<match>.*)',
                                 'num_of_comparison', '(.*)']],
                      'relation': '<',
                      'threshold_counter': '(?P<num>.*)',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'session_state', 'established'],
                                              ['info', 'vrf', '(?P<vrf>.*)', 'peer',
                                               '(?P<peer>.*)', 'statistics', 'sa_policy', 'out', '(?P<sa_filter_out>.*)',
                                               '(?P<match>.*)', 'num_of_comparison', '(?P<num>^(?!0).*)']],
                                          'all_keys': True,
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][peer][(.*)][session_state]',
                                              'info[vrf][(.*)][peer][(.*)][statistics][sa_policy][out]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareCounters.compare_counter,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][peer][(.*)][session_state]',
                                                             'info[vrf][(.*)][peer][(.*)][statistics][sa_policy][out]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'peer':'all', 'num': 1})
    

class TriggerClearMsdpSaCache(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)',
                                 'sa_cache', '(?P<sa>.*)', 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'sa_cache',
                                               '(?P<sa>.*)', 'group', '(?P<group>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][sa_cache][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][sa_cache][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'group':'all'})
    

class TriggerClearMsdpRoute(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)',
                                 'sa_cache', '(?P<sa>.*)', 'up_time', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.msdp.msdp.Msdp':{
                                          'requirements':[\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'sa_cache',
                                               '(?P<sa>.*)', 'group', '(?P<group>.*)']],
                                          'kwargs':{'attributes': [
                                              'info[vrf][(.*)][sa_cache][(.*)]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.msdp.msdp.Msdp':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[vrf][(.*)][sa_cache][(.*)]']},
                                    'exclude': exclude}},
                      num_values={'vrf': 'all', 'group':'all'})
