'''Common implementation for interface clear triggers'''

# Python
import time
import logging

# ATS
from ats import aetest
from ats.utils.objects import R

# Genie
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.clear.clear import TriggerClear
from genie.libs.sdk.libs.utils.triggeractions import CompareUptime

log = logging.getLogger(__name__)


# List of values to exclude for interface ops
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_crc_errors', 'in_errors',
                     'accounting']


class TriggerClearCounters(TriggerClear):

    mapping_extra_args = {'ops':'ops_obj', 'relation':'sign',
                          'threshold_time':'compare_time'}

    # Learn interface ops for all interfaces on device
    mapping = Mapping(\
                    requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>[\w\-\/]+$)', 'enabled', '(?P<enabled>.*)']],
                                       'exclude': interface_exclude}},
                    num_values={'name': 'all'})

    # Verify callable definition
    verify = CompareUptime.compare_uptime
    ops_lib = 'ops.interface.interface.Interface'

    # Arguments for verify callable
    verify_func_args = {'r_obj': [R(['info', '(?P<name>.*)',
                                     'counters', 'last_clear', '(.*)'])]}