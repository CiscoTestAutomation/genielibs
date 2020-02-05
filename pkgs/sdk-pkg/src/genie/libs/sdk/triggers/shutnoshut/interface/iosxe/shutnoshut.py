'''Implementation for interface shutnoshut triggers'''

# import pyats
from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for BGP Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_errors', '(Tunnel.*)', 'status',
                     'accounting']

# Which key to exclude for hsrp Ops comparison
hsrp_exclude = ['maker', 'active_ip_address', 'standby_ip_address',
                'active_router', 'hello_msec_flag', 'hold_msec_flag',
                'hello_msec', 'hold_msec', 'hello_sec', 'hold_sec',
                'active_ipv6_address', 'standby_ipv6_address']

# Which key to exclude for dot1x Ops comparison
dot1x_exclude = ['maker', 'statistics', 'session']

# Which key to exclude for fdb Ops comparison
fdb_exclude = ['maker', 'total_mac_addresses']


class TriggerShutNoShutTrunkInterface(TriggerShutNoShut):
    """Shut and unshut dynamically learned trunk interface(s)"""

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
           1. Learn Interface Ops object and verify if has any enabled interface(s) with up status,
              and also switch port mode should be trunk
           2. Shut the Interface learned from step 1 with Interface Conf object
           3. Verify the state of learned interface(s) and switchport and
              from step 2 are "down"
           4. Unshut the trunk interface(s)
           5. Learn Interface Ops again and verify It is the same as the Ops in step 1

       """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'switchport_mode', 'trunk'],
                                                       ['info', '(?P<interface>.*)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][port_channel]']},
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<interface>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][port_channel]']},
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1})


class TriggerShutNoShutVlanInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned vlan interface(s)."""

    __description__ = """Shut and unshut the dynamically learned vlan interface(s).

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
            1. Learn Interface Ops object and store the "up" vlan interface(s)
               if has any, otherwise, SKIP the trigger.
            2. Shut the learned vlan interface(s) from step 1 with Interface Conf object
            3. Verify the state of learned vlan interface(s) from step 2 is "down"
            4. Unshut the vlan interface(s) with Interface Conf object
            5. Learn Interface Ops again and verify it is the same as the Ops in step 1

        """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                       ['info', '(?P<interface>.*)', 'enabled', True],
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
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'interface': 1, 'mtu': 1})


class TriggerShutNoShutHsrpIpv4VlanInterface(TriggerShutNoShut):
    """Shut and Unshut the dynamically learned Hsrp Ipv4 Vlan interface(s)."""

    __description__ = """Shut and Unshut the dynamically learned Hsrp Ipv4 Vlan interface(s).

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
        1. Learn Interface Ops object and verify if has any "up" "ipv4" Vlan interface(s),
           and learn Hsrp Ops verify if has any "up" "ipv4" Vlan interface(s) that exists
           in learned Vlan interface(s) from Interface Ops. Store the filtered
           "up" "ipv4" Vlan interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned Hsrp Ipv4 Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Hsrp Ipv4 Vlan interface(s) from step 2 is "down"
        4. Unshut the Hsrp Ipv4 Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<interface>.*)', 'ipv4', '(?P<ipv4>.*)']],
                                        'exclude': interface_exclude + ['ipv6']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'address_family','ipv4','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'enabled', False],
                                                       ['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'interface': 1})


class TriggerShutNoShutHsrpIpv6VlanInterface(TriggerShutNoShut):
    """Shut and Unshut the dynamically learned Hsrp Ipv6 Vlan interface(s)."""

    __description__ = """Shut and Unshut the dynamically learned Hsrp Ipv6 Vlan interface(s).

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
        1. Learn Interface Ops object and verify if has any "up" "ipv6" Vlan interface(s),
           and learn Hsrp Ops verify if has any "up" "ipv6" Vlan interface(s) that exists
           in learned Vlan interface(s) from Interface Ops. Store the filtered
           "up" "ipv6" Vlan interface(s) if has any, otherwise, SKIP the trigger
        2. Shut the learned Hsrp Ipv6 Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Hsrp Ipv6 Vlan interface(s) from step 2 is "down"
        4. Unshut the Hsrp Ipv6 Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1
        """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<interface>.*)', 'ipv6', '(?P<ipv6>.*)']],
                                        'exclude': interface_exclude + ['ipv4','status']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<interface>Vlan[0-9]+)', 'address_family','ipv6','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv4','status']}},
                      num_values={'interface': 1})


class TriggerShutNoShutLoopbackInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned loopback interface(s)."""

    __description__ = """Shut and unshut the dynamically learned loopback interface(s).

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
               1. Learn Interface Ops object and store the "up" loopback interface(s)
                  if has any, otherwise, SKIP the trigger.
               2. Shut the learned loopback interface(s) from step 1 with Interface Conf object
               3. Verify the state of learned loopback interface(s) from step 2 is "down"
               4. Unshut the loopback interface(s) with Interface Conf object
               5. Learn Interface Ops again and verify it is the same as the Ops in step 1

           """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>(Loopback|Lo|loopback)[0-9]+)', 'oper_status', 'up'],
                                                       ['info', '(?P<interface>(Loopback|Lo|loopback)[0-9]+)', '(?P<af>ipv4|6)', Not('unnumbered')]
                                       ],
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
                      num_values={'interface': 1})


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
                   1. Learn Interface Ops object and store the "up" Ethernet interface(s) and "False" port channel member,
                      if has any, otherwise, SKIP the trigger.
                   2. Shut the learned Ethernet interface(s) from step 1 with Interface Conf object
                   3. Verify the state of learned Ethernet interface(s) from step 2 is "down"
                   4. Unshut the Ethernet interface(s) with Interface Conf object
                   5. Learn Interface Ops again and verify it is the same as the Ops in step 1

               """

    def remove_related_subinterface(item, interface, **kwargs):
        """Check if interface (item) needs to remove sub-interfaces
        by checking with the given main interface (name).

           Args:
               item (`str`): Interface name to be checked if need to remove the sub-interfaces.
               interface (`str`): Interface name that needs to remove the sub-interfaces.
               **kwargs: Arbitrary keyword arguments.

           Returns:
               True: The item interface which needs sub-interfaces removal
               False: The item interface which doesn't need sub-interfaces removal
        """
        # Easiest way is to split at the dot, and see if it exists in name
        modified_item = item.split('.')[0]

        # If it remained the same, dont waste time
        if item == modified_item:
            return False

        # See if the modified_item exists in the list of name
        if modified_item in interface:
            return True
        return False

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>(\w+(e|E)thernet[\S]+|\w+(g|G)ig[\S]+))', 'oper_status', 'up'],
                                            ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude,
                                        'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][port_channel]']},
                                        'include_management_interface': False}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>.*)', 'enabled', False],
                                            ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                            ['info', '(?P<interface>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][port_channel]']},
                                        'exclude': interface_exclude +\
                                                   [remove_related_subinterface]}},
                      num_values={'interface': 1})


class TriggerShutNoShutNativeIpv4SviInterface(TriggerShutNoShut):
    """Shut and unshut Vlan 1 with ipv4 configured."""

    __description__ = """Shut and unshut Vlan 1 with ipv4 configured.

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
        1. Learn Interface Ops object and store the "up" Vlan 1 with ipv4 configured
           if has any, otherwise, SKIP the trigger
        2. Shut the Vlan 1 from step 1 with Interface Conf object
        3. Verify the state of Vlan 1 from step 2 is "down"
        4. Unshut the Vlan 1 with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """


    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan1)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]']},
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
                                                       ['info', '(?P<interface>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1})


class TriggerShutNoShutIpv4SviInterface(TriggerShutNoShut):
    """Shut and unshut Learned Vlan interface(s) with ipv4 configured."""

    __description__ = """Shut and unshut Learned Vlan interface(s) with ipv4 configured.

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
        1. Learn Interface Ops object and store the "up" Vlan interface(s) with ipv4 configured
           if has any, otherwise, SKIP the trigger
        2. Shut the learned Vlan interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Vlan interface(s) from step 2 is "down"
        4. Unshut the Vlan interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """


    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>Vlan[0-9]+)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'ipv4', '(?P<ip>.*)', 'ip', '(?P<ipaddr>.*)'],
                                                       ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                       'all_keys': True,
                                       'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][ipv4][(.*)]']},
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<interface>.*)', 'switchport_enable', False]],
                                       'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][ipv4][(.*)]']},
                                       'exclude': interface_exclude}},
                      num_values={'interface': 1})


class TriggerShutNoShutDot1xInterface(TriggerShutNoShut):
    """Shut and unshut the dynamically learned Dot1x Ethernet interface(s)."""

    __description__ = """Shut and unshut the dynamically learned Dot1x Ethernet interface(s).

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
                vlan: `str`
                client: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Interface Ops object and store the "up" Ethernet interface(s)
           if has any, otherwise, SKIP the trigger, then check if the status of dot1x is 'auth',
           and the peer mac-address in UUT's table is 'static', if not, SKIP the trigger
           And Learn Dot1x Ops object and store the dot1x interface whcih are from the
           interface ops.
        2. Shut the learned Dot1x Ethernet interface(s) from step 1 with Interface Conf object
        3. Verify the state of learned Dot1x Ethernet interface(s) from step 2 is "down"
        4. Unshut the Dot1x Ethernet interface(s) with Interface Conf object
        5. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>\w+Ethernet[\d\/]+$)', 'enabled', True],
                                                       ['info', '(?P<interface>.*)', 'switchport_enable', True],
                                                       ['info', '(?P<interface>.*)', 'switchport_mode', 'static access'],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                       'all_keys': True,
                                       'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][switchport_enable]',
                                                                 'info[(.*)][operational_mode]']},
                                       'exclude': interface_exclude},
                                    'ops.fdb.fdb.Fdb':{
                                       'requirements':[['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', '(?P<client>.*)',
                                                        'interfaces', '(?P<interface>.*)', 'entry_type', 'static']],
                                       'all_keys': True,
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'exclude': fdb_exclude + ['mac_addresses']},
                                    'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', '(?P<interface>.*)',
                                                        'clients', '(?P<client>.*)', 'status', 'authorized']],
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]']},
                                       'all_keys': True,
                                       'exclude': dot1x_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<interface>.*)', 'switchport_enable', False]],
                                       'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][switchport_enable]',
                                                                 'info[(.*)][operational_mode]']},
                                       'exclude': interface_exclude},
                                  'ops.fdb.fdb.Fdb':{
                                       'requirements':[['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', NotExists('(?P<client>.*)')]],
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'exclude': fdb_exclude + ['mac_addresses']},
                                    'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', NotExists('(?P<interface>.*)')]],
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]']},
                                       'all_keys': True,
                                       'exclude': dot1x_exclude + ['attributes']}},
                      num_values={'interface': 'all'})
