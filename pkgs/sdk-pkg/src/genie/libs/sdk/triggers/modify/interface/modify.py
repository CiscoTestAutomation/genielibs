'''Implementation for interface modify triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify
from genie.libs.conf.interface import IPv4Addr, IPv6Addr
from genie.libs.conf.base import IPv4Address, IPv6Address

# import python
from functools import partial
from pyats.utils.objects import Not

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_discards', 'accounting']


class TriggerModifyEthernetMtu(TriggerModify):
    """Modify and revert the mtu for dynamically learned Ethernet interface(s)."""

    __description__ = """Modify and revert the mtu for dynamically learned Ethernet interface(s).

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
                mtu: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Interface Ops object and store the "up" Ethernet interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the mtu of the learned Ethernet interface(s) from step 1
           with Interface Conf object
        4. Verify the mtu of the learned Ethernet interface(s) from step 3
           changes to the modified value in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [['info', r'(?P<interface>e|Ethernet[0-9\/\s]+$)', 'mtu', '(?P<mtu>.*)'],
                                                         ['info', '(?P<interface>.*)', 'enabled', True],
                                                         ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False],
                                                         ['info', '(?P<interface>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                      'requirements':[['mtu', 9216]],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                             'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<interface>.*)', 'mtu', 9216],
                                                       ['info', '(?P<interface>.*)', 'bandwidth', r'(\d+)']],
                                      'exclude': interface_exclude}},
                      num_values={'interface': 1, 'mtu': 1})


class TriggerModifySwitchportModeTrunkToAccess(TriggerModify):
    """Modify and revert the mode ("trunk" to "access") for dynamically learned switchport interface(s)."""

    __description__ = """Modify and revert the mode ("trunk" to "access") for dynamically learned switchport interface(s).

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
        1. Learn Interface Ops object and store the "up" "trunk" interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the mode of the learned "trunk" interface(s) from step 1 to "access"
           with Interface Conf object
        4. Verify the mode of the learned "trunk" interface(s) from step 3
           changes to "access" in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<interface>.*)', 'switchport_mode', 'trunk'],
                                            ['info', '(?P<interface>.*)', 'enabled', True],
                                            ['info', '(?P<interface>.*)', 'oper_status', 'up'],
                                            ['info', '(?P<interface>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['switchport_mode', 'access']],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<interface>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements': [\
                                            ['info', '(?P<interface>.*)', 'switchport_mode', 'access'],
                                            ['info', '(?P<interface>.*)', 'enabled', False],
                                            ['info', '(.*)', 'switchport_mode', r'(\w+)']],
                                        'exclude': interface_exclude + ['(Vlan.*)']}},
                      num_values={'interface': 1})


class TriggerModifyLoopbackInterfaceIp(TriggerModify):
    """Modify and revert the ipv4 address for dynamically learned Loopback interface(s)."""

    __description__ = """Modify and revert the ipv4 address for dynamically learned Loopback interface(s).

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
    steps:
        1. Learn Interface Ops object and store the "up" "ipv4" Loopback interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the ipv4 address of the learned Loopback interface(s) from step 1
           with Interface Conf object
        4. Verify the ipv4 address of the learned Loopback interface(s) from step 3
           changes to the modified value in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # configuration steps callable
    def configure_intf_ip(self, conf_obj, ip, mask, **kwargs):
        ipv4 = IPv4Addr(device=kwargs['device'])
        ipv4.ipv4 = IPv4Address(ip)
        ipv4.prefix_length = mask
        conf_obj.add_ipv4addr(ipv4)
        conf_obj.build_config()

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [['info', r'(?P<name>[l|L]oopback\d+)',
                                                          'ipv4', '(?P<ip_mask>.*)', 'ip', '(?P<ip>.*)'],
                                                         ['info', r'(?P<name>[l|L]oopback\d+)',
                                                          'ipv4', '(?P<ip_mask>.*)', 'prefix_length', '(?P<mask>.*)']],
                                        'all_keys':True,
                                        'exclude': interface_exclude,
                                        'all_keys': True}},
                      config_info={'conf.interface.Interface':{
                                      'requirements':[[partial(configure_intf_ip, ip='10.254.254.254',
                                                                                  mask='32')]],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                             'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<name>.*)',  'ipv4', '10.254.254.254/32',
                                                        'prefix_length', '32'],
                                                       ['info', '(?P<name>.*)',  'ipv4', '10.254.254.254/32',
                                                        'ip', '10.254.254.254']],
                                      'exclude': interface_exclude}},
                      num_values={'name': 1, 'ip_mask': 1, 'ip' : 'all', 'mask': 'all'})


class TriggerModifyLoopbackInterfaceIpv6(TriggerModify):
    """Modify and revert the ipv6 address for dynamically learned Loopback interface(s)."""

    __description__ = """Modify and revert the ipv6 address for dynamically learned Loopback interface(s).

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

    steps:
        1. Learn Interface Ops object and store the "up" "ipv6" Loopback interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the ipv6 address of the learned Loopback interface(s) from step 1
           with Interface Conf object
        4. Verify the ipv6 address of the learned Loopback interface(s) from step 3
           changes to the modified value in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # configuration steps callable
    def configure_intf_ipv6(self, conf_obj, ip, mask, **kwargs):

        # add old ipv6 attributes in conf_object
        # for remove the original ipv6 configurations        
        ipv6 = IPv6Addr(device=kwargs['device'])
        for ipInfo in self.keys:
            if 'ip' in ipInfo:
                ipv6.ipv6 = IPv6Address(ipInfo['ip'])
            if 'mask' in ipInfo:
                ipv6.ipv6_prefix_length = ipInfo['mask']
            conf_obj.add_ipv6addr(ipv6)

        # remove all existing ipv6 configurations
        conf_obj.build_unconfig(attributes={'ipv6addr':None})
        # clear the used attribtues
        conf_obj.ipv6addr.clear()

        # configure new ipv6 address
        ipv6 = IPv6Addr(device=kwargs['device'])
        ipv6.ipv6 = IPv6Address(ip)
        ipv6.ipv6_prefix_length = mask
        conf_obj.add_ipv6addr(ipv6)
        conf_obj.build_config()

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [['info', r'(?P<name>[l|L]oopback\d+)',
                                                          'ipv6', '(?P<ip_mask>.*)', 'ip', '(?P<ip>.*)'],
                                                         ['info', r'(?P<name>[l|L]oopback\d+)',
                                                          'ipv6', '(?P<ip_mask>.*)', 'prefix_length', '(?P<mask>.*)']],
                                        'exclude': interface_exclude,
                                        'all_keys': True}},
                      config_info={'conf.interface.Interface':{
                                      'requirements':[[partial(configure_intf_ipv6, ip='10:254::254:254',
                                                                                  mask='64')]],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                             'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<name>.*)',  'ipv6', '10:254::254:254/64',
                                                        'prefix_length', '64'],
                                                       ['info', '(?P<name>.*)',  'ipv6', '10:254::254:254/64',
                                                        'ip', '10:254::254:254'],
                                                       ['info', '(?P<name>.*)',  '(ipv6)', r'([\w\/\.\:]+)']],
                                      'exclude': interface_exclude}},
                      num_values={'name': 1, 'ip_mask': 1, 'ip' : 'all', 'mask': 'all'})


class TriggerModifySviInterfaceIp(TriggerModify):
    """Modify and revert the ipv4 address for dynamically learned Svi (Vlan) interface(s)."""

    __description__ = """Modify and revert the ipv4 address for dynamically learned Svi (Vlan) interface(s).

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

    steps:
        1. Learn Interface Ops object and store the "up" "ipv4" Vlan interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the ipv4 address of the learned Vlan interface(s) from step 1
           with Interface Conf object
        4. Verify the ipv4 address of the learned Vlan interface(s) from step 3
           changes to the modified value in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # configuration steps callable
    def configure_intf_ip(self, conf_obj, ip, mask, **kwargs):
        ipv4 = IPv4Addr(device=kwargs['device'])
        ipv4.ipv4 = IPv4Address(ip)
        ipv4.prefix_length = mask
        conf_obj.add_ipv4addr(ipv4)
        conf_obj.build_config()

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [\
                                            ['info', '(?P<name>Vlan[0-9]+)', 'ipv4', '(?P<ip_mask>.*)', 'ip', '(?P<ip>.*)'],
                                            ['info', '(?P<name>Vlan[0-9]+)', 'ipv4', '(?P<ip_mask>.*)', 'prefix_length', '(?P<mask>.*)']],
                                        'exclude': interface_exclude,
                                        'all_keys': True}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[\
                                            [partial(configure_intf_ip, ip='10.254.254.254', mask='24')]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                    'requirements': [\
                                        ['info', '(?P<name>.*)',  'ipv4', '10.254.254.254/24', 'prefix_length', '24'],
                                        ['info', '(?P<name>.*)',  'ipv4', '10.254.254.254/24', 'ip', '10.254.254.254']],
                                    'exclude': interface_exclude}},
                      num_values={'name': 1, 'ip_mask': 1, 'ip' : 'all', 'mask': 'all'})


class TriggerModifyVlanMtu(TriggerModify):
    """Modify and revert the mtu for dynamically learned Vlan interface(s)."""
    
    __description__ = """Modify and revert the mtu for dynamically learned Vlan interface(s).

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

    steps:
        1. Learn Interface Ops object and store the "up" Vlan interface(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the mtu of the learned Vlan interface(s) from step 1
           with Interface Conf object
        4. Verify the mtu of the learned Vlan interface(s) from step 3
           changes to the modified value in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn Interface Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [['info', '(?P<name>(Vlan|vlan)[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                         ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                      'requirements':[['mtu', 9216]],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                             'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<name>.*)', 'mtu', 9216],
                                                       ['info', '(?P<name>.*)', 'bandwidth', r'(\d+)']],
                                      'exclude': interface_exclude}},
                      num_values={'name': 1, 'mtu': 1})
