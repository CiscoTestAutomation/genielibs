'''Common implementation for ipv6 triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker','age','active_timers']

class TriggerClearIPv6NeighborVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
  
    verify_func_args={'r_obj': [['info', 'interfaces', '(?P<interface>.*)',
                                 'neighbors', '(?P<neighbor>.*)', 'age', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.nd.nd.Nd':{
                                          'requirements':[\
                                              ['info', 'interfaces', '(?P<interface>.*)'
                                               ,'neighbors', '(?P<neighbor>.*)','(?P<nbr_contents>.*)']],
                                          'kwargs': {'attributes': ['info[interfaces][(.*)][neighbors][(.*)][age]']},
                                          'exclude': exclude}},
                      verify_ops={'ops.nd.nd.Nd':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes': ['info[interfaces][(.*)][neighbors][(.*)][age]']},
                                    'exclude': exclude}},
                      num_values={'interface': 'all', 'neighbor': 'all'})
