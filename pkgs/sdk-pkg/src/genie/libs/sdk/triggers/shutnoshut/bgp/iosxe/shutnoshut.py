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
    """Shut and unshut the dynamically learned BGP neighbore(s)."""

    __description__ = """Shut and unshut the dynamically learned BGP neighbore(s).

        trigger_datafile:
            Mandatory:
                timeout:
                    max_time (`int`): Maximum wait time for the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
            Optional:
                tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                     restored to the reference rate,
                                     in second. Default: 60
                tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                   in second. Default: 10
                timeout_recovery:
                    Buffer recovery timeout make sure devices are recovered at the end
                    of the trigger execution. Used when previous timeouts have been exhausted.

                    max_time (`int`): Maximum wait time for the last step of the trigger,
                                    in second. Default: 180
                    interval (`int`): Wait time between iteration when looping is needed,
                                    in second. Default: 15
                static:
                     The keys below are dynamically learnt by default.
                     However, they can also be set to a custom value when provided in the trigger datafile.

                     instance: `str`
                     vrf: `str`
                     neighbor: `str`
                     bgp_id: `int`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                          OR
                          interface: 'Ethernet1/1/1' (Specific value)
        steps:
            1. Learn BGP Ops object and verify if has established state, otherwise, Skip the trigger.
            2. Shut the BGP neighbor that learned from step 1 with BGP Conf object
            3. Verify the state of learned neighbor(s)
               from step 2 is "down"
            4. Unshut the BGP neighbor(s)
            5. Learn BGP Ops again and verify it is the same as the Ops in step 1

        """

    mapping = Mapping(\
            requirements={\
                'ops.bgp.bgp.Bgp': {
                    'requirements':[\
                        ['info', 'instance', '(?P<instance>.*)',
                        'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'session_state', '(?P<established>[E|e]stablished)'],
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
                        'session_state', '(?P<idle>[I|i]dle)'],
                        ['info', 'instance', '(?P<instance>.*)', 'vrf',
                        '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                        'shutdown', True]],
                    'kwargs':
                        {'attributes':['info']},
                    'exclude': bgp_exclude}},
            num_values={'instance':1, 'vrf':1, 'neighbor': 'all'})
