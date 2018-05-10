'''Common implementation for ospf clear triggers'''

# import ats
from ats.utils.objects import R

from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

# Ignore keys when doing the diff with Ops objects for save_snapshot and
# verify_clear, it will be used for LearnPollDiff.ops_diff callable
exclude = ['maker', 'age', 'checksum', 'seq_num','dead_timer',
           'last_state_change' ,'spf_runs_count','hello_timer','nbr_event_count']

class TriggerClearIpOspfNeighborVrfAll(TriggerClear):

    # Argument with dynamic value for verify callable
    # As verify callable can be re-used in multiple triggers
    # with different variable names. This dictionary is used to map
    # dynamic argument name to actual script argument name
    # <expected argument_name for callable>: <script argument name>
    mapping_extra_args = {'ops':'ops_obj', 'relation':'sign',
                          'threshold_time':'compare_time'}

    mapping = Mapping(requirements={'ops.ospf.ospf.Ospf':{
                                          'requirements': [\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'address_family','(?P<af>.*)',
                                               'instance', '(?P<instance>.*)', 'areas','(?P<area>.*)',
                                               'interfaces', '(?P<intf>.*)',
                                               'neighbors', '(?P<neighbor>.*)','(.*)']],
                                          'all_keys': True,
                                          'kwargs': {'attributes':['info']},
                                          'exclude': exclude }},
                      num_values={'vrf':'all', 'instance':'all','neighbor':'all' , 'intf':'all', 'area': 'all'})

    # Verify callable definition
    verify = CompareUptime.compare_uptime

    # Arguments for verify callable
    # Must be dictionary, key is argument from verify callable,
    # value should be the value to pass into the callable
    verify_func_args = {'r_obj': [R(['info', 'vrf', '(?P<vrf>.*)', 'address_family','(?P<af>.*)',
                                     'instance' , '(?P<instance>.*)', 'areas','(?P<area>).*',
                                     'interfaces', '(?P<intf>.*)',
                                     'neighbors', '(?P<neighbor>.*)',
                                     'last_state_change', '(.*)'])]}


class TriggerRestartOspf(TriggerClearIpOspfNeighborVrfAll):
    pass