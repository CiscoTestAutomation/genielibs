'''Common implementation for interface clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
from genie.libs.sdk.libs.utils.triggeractions import CompareCounters, CompareUptime

# List of values to exclude for interface ops
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_crc_errors', 'in_errors',
                     'accounting']


class TriggerClearCounters(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args_in={'r_obj': [['info', '(?P<interface>.*)',
                                    'counters', 'in_pkts', '(.*)']],
                         'relation': '<',
                         'threshold_counter': '(?P<in_pkts>.*)',
                         'ops': 'ops'}
  
    verify_func_args_out={'r_obj': [['info', '(?P<interface>.*)',
                                     'counters', 'out_pkts', '(.*)']],
                          'relation': '<',
                          'threshold_counter': '(?P<out_pkts>.*)',
                          'ops': 'ops'}

    verify_func_args={'r_obj': [['info', '(?P<interface>.*)',
                                 'counters', 'last_clear', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>[\w\-\/]+$)', 'enabled', True],
                                            ['info', '(?P<interface>[\w\-\/]+$)', 'oper_status', 'up'],
                                            ['info', '(?P<interface>[\w\-\/]+$)', 'counters',
                                             'in_pkts', '(?P<in_pkts>.*)'],
                                            ['info', '(?P<interface>[\w\-\/]+$)', 'counters',
                                             'out_pkts', '(?P<out_pkts>.*)']],
                                        'all_keys': True,
                                        'kwargs': {'attributes': \
                                                ['info[(.*)][enabled]',
                                                 'info[(.*)][counters]']},
                                    'exclude': interface_exclude}},
                      verify_ops={'ops.interface.interface.Interface':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareCounters.compare_counter,
                                                      verify_func_args=verify_func_args_in)],
                                                    [partial(verify_clear_callable,
                                                      verify_func=CompareCounters.compare_counter,
                                                      verify_func_args=verify_func_args_out)],
                                                    [partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                        'kwargs': {'attributes': \
                                                ['info[(.*)][enabled]',
                                                 'info[(.*)][counters]']},
                                    'exclude': interface_exclude}},
                      num_values={'interface': 'all'})
