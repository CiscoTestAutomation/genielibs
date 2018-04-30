'''
IOSXE Implementation for BGP ShutNoShut triggers
'''

# import python
from collections import OrderedDict

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut


# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'distance_internal_as', 'routing_table_version',
               'total_memory']


class TriggerShutNoShutBgpNeighbors(TriggerShutNoShut):

    mapping = Mapping(\
            requirements={\
                'ops.bgp.bgp.Bgp': {
                    'requirements':[\
                        ['info', 'instance', '(?P<instance>.*)',
                        'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'session_state', 'established'],
                        ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                    'all_keys':True, 
                    'kwargs':
                        {'attributes':['info']},
                    'exclude': bgp_exclude}},
            config_info={\
                'conf.bgp.Bgp': {
                    'requirements':[\
                        ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                        'neighbor_attr', '(?P<neighbor>.*)', 'nbr_shutdown', True]],
                    'verify_conf':False,
                    'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
            verify_ops={\
                'ops.bgp.bgp.Bgp': {
                    'requirements':[\
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'session_state', 'idle'],
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'shutdown', True]],
                    'kwargs':
                        {'attributes':['info']},
                    'exclude': bgp_exclude}},
            num_values={'instance':1, 'vrf':1, 'neighbor': 'all'})
