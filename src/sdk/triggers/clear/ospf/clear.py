'''Common implementation for ospf clear triggers'''

# python
from functools import partial

# genie libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear, verify_clear_callable
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
  
    verify_func_args={'r_obj': [['info', 'vrf', '(?P<vrf>.*)', 'address_family','(?P<af>.*)',
                                 'instance' , '(?P<instance>.*)', 'areas','(?P<area>).*',
                                 'interfaces', '(?P<intf>.*)',
                                 'neighbors', '(?P<neighbor>.*)',
                                 'last_state_change', '(.*)']],
                      'relation': '<',
                      'threshold_time': 'compare_time',
                      'ops': 'ops'}

    mapping = Mapping(requirements={'ops.ospf.ospf.Ospf':{
                                          'requirements': [\
                                              ['info', 'vrf', '(?P<vrf>.*)', 'address_family','(?P<af>.*)',
                                               'instance', '(?P<instance>.*)', 'areas','(?P<area>.*)',
                                               'interfaces', '(?P<intf>.*)',
                                               'neighbors', '(?P<neighbor>.*)','(.*)']],
                                          'all_keys': True,
                                          'kwargs': {'attributes':['info']},
                                          'exclude': exclude }},
                      verify_ops={'ops.ospf.ospf.Ospf':{
                                    'requirements':[[partial(verify_clear_callable,
                                                      verify_func=CompareUptime.compare_uptime,
                                                      verify_func_args=verify_func_args)]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': exclude + ['link_data']}},
                      num_values={'vrf':'all', 'instance':'all','neighbor':'all' , 'intf':'all', 'area': 'all'})


class TriggerRestartOspf(TriggerClearIpOspfNeighborVrfAll):
    pass