'''Common implementation for ipv6 triggers'''

# import ats
from ats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear
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
    mapping_extra_args = {'ops':'ops_obj', 'relation':'sign',
                          'threshold_time':'compare_time'}

    mapping = Mapping(requirements={'ops.nd.nd.Nd':{
                                          'requirements':[\
                                              ['info', 'interfaces', '(?P<interface>.*)'
                                               ,'neighbors', '(?P<neighbor>.*)','(.*)']],
                                          'kwargs': {'attributes': ['info[interfaces][(.*)][neighbors][(.*)][age]']},
                                          'exclude': exclude}},
                      num_values={'interface': 'all', 'neighbor': 'all'})

    # Verify callable definition
    verify = CompareUptime.compare_uptime
    ops_lib = 'ops.nd.nd.Nd'
    # Arguments for verify callable
    # Must be dictionary, key is argument from verify callable,
    # value should be the value to pass into the callable
    verify_func_args = {'r_obj': [R(['info', 'interfaces', '(?P<interface>.*)','neighbors', '(?P<neighbor>.*)',
                                     'age', '(.*)'])]}
