'''Implementation for Interface unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# import pyats
from pyats import aetest
from pyats.utils.objects import Not, NotExists

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_discards',
                     'unnumbered', '(Tunnel.*)', 'accounting']


class TriggerUnconfigConfigLoopbackInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned Loopback interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned Loopback interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Loopback interface(s) from step 1 
           with Interface Conf object
        4. Verify the Loopback interface(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    loopback_exclude = interface_exclude + ['oper_status', 'enabled', 'status']

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>(Loopback||Lo|loopback)[0-9]+)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<interface>.*)')]],
                                       'exclude': loopback_exclude}},
                      num_values={'interface':1})


class TriggerUnconfigConfigPhysicalTrunkInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned
    physical (non-Loopback, non-Vlan, non-Null, non-Tunnel, non-subinterface etc.) "trunk" interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned
    physical (non-Loopback, non-Vlan, non-Null, non-Tunnel, non-subinterface etc.) "trunk" interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        1. Learn Interface Ops object and store the "up" physical "trunk" interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned physical interface(s) from step 1 
           with Interface Conf object
        4. Verify the physical interface(s) from step 3 are "down",
           verify the configurations are all gone for the learned physical interface(s)
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>[E|e]thernet[\d\/\.]+)',
                                                        'switchport_mode', 'trunk'],
                                                        ['info', '(?P<interface>[E|e]thernet[\d\/\.]+)',
                                                        'port_channel', 'port_channel_member', False]],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>.*)', 'oper_status', '(.*)'],
                                                       ['info', '(?P<interface>.*)', 'enabled', False],
                                                       ['info', '(?P<interface>.*)', 'port_channel',
                                                        'port_channel_member', False],
                                                       ['info', '(?P<interface>.*)', 'mac_address', '([\w\.]+)'],
                                                       ['info', '(?P<interface>.*)', '(.*)']],
                                       'exclude': interface_exclude + ['(Vlan.*)']}},
                      num_values={'interface':1})


class TriggerUnconfigConfigVirtualTrunkInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned
    virtual "trunk" (port-channel) interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned
    virtual "trunk" (port-channel) interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        1. Learn Interface Ops object and store the "up" virtual "trunk" interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned virtual interface(s) from step 1 
           with Interface Conf object
        4. Verify the virtual interface(s) from step 3 are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>[p|P]ort-channel[\d\.]+)',
                                                        'switchport_mode', 'trunk']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<interface>.*)')]],
                                       'exclude': interface_exclude}},
                      num_values={'interface':1})


class TriggerUnconfigConfigEthernetInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned Ethernet interface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned Ethernet interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Ethernet interface(s) from step 1 
           with Interface Conf object
        4. Verify the configurations are all gone for the learned Ethernet interface(s)
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """


    def remove_related_subinterface(item, interface, **kwargs):
        # Easiest way is to split at the dot, and see if it exists in name
        modified_item = item.split('.')[0]

        # If it remained the same, dont waste time
        if item == modified_item:
            return False

        # See if the modified_item exists in the list of name
        if modified_item in interface:
            return True
        return False

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+$)',
                                                         'enabled', True],
                                                        ['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+$)',
                                                         'port_channel', 'port_channel_member', False],
                                                        ['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+$)',
                                                         'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>.*)', 'vrf', 'default'],
                                                        ['info', '(?P<interface>.*)', 'enabled', False],
                                                        ['info', '(?P<interface>.*)', 'oper_status', 'down'],
                                                        ['info', '(?P<interface>.*)', 'delay', '(\d+)'],
                                                        ['info', '(?P<interface>.*)', 'bandwidth', '(\d+)'],
                                                        ['info', '(?P<interface>.*)', 'encapsulation', 'encapsulation', '(\S+)'],
                                                        ['info', '(?P<interface>.*)', 'mac_address', '(\S+)'],
                                                        ['info', '(?P<interface>.*)', 'medium', '(\S+)'],
                                                        ['info', '(?P<interface>.*)', 'mtu', '(\d+)'],
                                                        ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude +\
                                                   [remove_related_subinterface, '(Vlan.*)']}},
                      num_values={'interface': 1})


class TriggerUnconfigConfigEthernetInterfaceSub(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned Ethernet SubInterface(s)."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned Ethernet SubInterface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        1. Learn Interface Ops object and store the "up" Ethernet SubInterface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Ethernet SubInterface(s) from step 1 
           with Interface Conf object
        4. Verify the learned Ethernet SubInterface(s) are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'enabled', True],
                                                        ['info', '(?P<interface>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', NotExists('(?P<interface>.*)')]],
                                        'exclude': interface_exclude + ['(Vlan.*)']}},
                      num_values={'interface': 1})


class TriggerUnconfigConfigVlanInterface(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically learned Vlan interface(s)."""
    
    __description__ = """Unconfigure and reapply the whole configurations of dynamically learned Vlan interface(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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
        1. Learn Interface Ops object and store the "up" Vlan interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned Vlan interface(s) from step 1 
           with Interface Conf object
        4. Verify the learned Vlan interface(s) are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    vlan_exclude = interface_exclude + ['oper_status']

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<interface>(Vlan|vlan)[0-9]+)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', NotExists('(?P<interface>.*)')]],
                                       'exclude': vlan_exclude}},
                      num_values={'interface':1})
    
