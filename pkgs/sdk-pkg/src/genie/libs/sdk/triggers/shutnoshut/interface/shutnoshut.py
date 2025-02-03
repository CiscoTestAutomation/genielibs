'''Implementation for interface shutnoshut triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for BGP Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets', 'in_errors',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts','bandwidth','duplex_mode',
                     '(Tunnel.*)', 'accounting']


class TriggerShutNoShutTrunkInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned trunk interface(s)."""

    __description__ = """Shut and unshut the dynamically learned trunk interface(s).

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

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" trunk interface(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned trunk interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned trunk interface(s) from step 2 is "down"
        4. Unshut the trunk interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'switchport_mode', 'trunk'],
                                                       ['info', '(?P<interface>.*)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'port_channel',
                                                        'port_channel_int', '(?P<port_int>.*)'],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                       'all_keys': True,
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<port_int>.*)', 'enabled', False],
                                                       ['info', '(?P<port_int>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['(Vlan.*)']}},
                      num_values={'interface': 1, 'port_int': 'all'})


class TriggerShutNoShutEthernetInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Ethernet interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Ethernet interface(s).

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

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" Ethernet interface(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Ethernet interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Ethernet interface(s) from step 2 is "down"
        4. Unshut the Ethernet interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', r'(?P<interface>Ethernet(\S+))', 'oper_status', 'up'],
                                            ['info', '(?P<interface>.*)', 'enabled', True],
                                            ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>.*)', 'enabled', False],
                                            ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                            ['info', '(.*)', 'enabled', False]],
                                        'exclude': interface_exclude}},
                      num_values={'interface': 1})


class TriggerShutNoShutVlanInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Vlan interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Vlan interface(s).

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

               interface: `str`
               mtu: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" Vlan interface(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Vlan interface(s) from step 2 is "down"
        4. Unshut the Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        
    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                       ['info', '(?P<interface>.*)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1, 'mtu': 1})


class TriggerShutNoShutLoopbackInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Loopback interface(s)."""
    
    __description__ = """Shut and unshut the dynamically learned Loopback interface(s).

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

               interface: `str`

               (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                     OR
                     interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" Loopback interface(s)
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Loopback interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Loopback interface(s) from step 2 is "down"
        4. Unshut the Loopback interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        
    """

    loopback_exclude = interface_exclude + ['oper_status', 'enabled', 'status']

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>(Loopback|Lo|loopback)[0-9]+)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': loopback_exclude}},
                      num_values={'interface': 1})
