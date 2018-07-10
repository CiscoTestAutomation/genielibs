'''Implementation for interface shutnoshut triggers'''

# import ats
from ats.utils.objects import Not, NotExists

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

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'switchport_mode', 'trunk'],
                                                       ['info', '(?P<name>.*)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][port_channel]']},
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][port_channel]']},
                                       'exclude': interface_exclude}},
                      num_values={'name': 1})


class TriggerShutNoShutVlanInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                       ['info', '(?P<name>.*)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                       'all_keys': True,
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'name': 1, 'mtu': 1})


class TriggerShutNoShutHsrpIpv4VlanInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<name>.*)', 'ipv4', '(?P<ipv4>.*)']],
                                        'exclude': interface_exclude + ['ipv6']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'address_family','ipv4','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'enabled', False],
                                                       ['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv6']}},
                      num_values={'name': 1})


class TriggerShutNoShutHsrpIpv6VlanInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'oper_status', 'up'],
                                                         ['info', '(?P<name>.*)', 'ipv6', '(?P<ipv6>.*)']],
                                        'exclude': interface_exclude + ['ipv4','status']},
                                    'ops.hsrp.hsrp.Hsrp': {
                                        'requirements': [['info', '(?P<name>Vlan[0-9]+)', 'address_family','ipv6','(.*)']],
                                        'exclude': hsrp_exclude }},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude + ['ipv4','status']}},
                      num_values={'name': 1})


class TriggerShutNoShutLoopbackInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>(Loopback|Lo|loopback)[0-9]+)', 'oper_status', 'up'],
                                                       ['info', '(?P<name>(Loopback|Lo|loopback)[0-9]+)', '(?P<af>ipv4|6)', Not('unnumbered')]
                                       ],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down']],
                                       'exclude': interface_exclude}},
                      num_values={'name': 1})


class TriggerShutNoShutEthernetInterface(TriggerShutNoShut):

    def remove_related_subinterface(item, name, **kwargs):
        """Check if interface (item) needs to remove sub-interfaces
        by checking with the given main interface (name).

           Args:
               item (`str`): Interface name to be checked if need to remove the sub-interfaces.
               name (`str`): Interface name that needs to remove the sub-interfaces.
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
        if modified_item in name:
            return True
        return False

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>\w+Ethernet[\d\/]+$)', 'oper_status', 'up'],
                                            ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude,
                                        'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][port_channel]']},
                                        'include_management_interface': False}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['enabled', False]],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>.*)', 'enabled', False],
                                            ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                            ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]',
                                                                  'info[(.*)][port_channel]']},
                                        'exclude': interface_exclude +\
                                                   [remove_related_subinterface]}},
                      num_values={'name': 1})


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
                                       'requirements':[['info', '(?P<name>Vlan1)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]']},
                                       'all_keys': True,
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                        'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                  'info[(.*)][switchport_enable]',
                                                                  'info[(.*)][enabled]',
                                                                  'info[(.*)][oper_status]']},
                                       'exclude': interface_exclude}},
                      num_values={'name': 1})


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
                                       'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'ipv4', '(?P<ip>.*)', 'ip', '(?P<ipaddr>.*)'],
                                                       ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                       'all_keys': True,
                                       'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][ipv4][(.*)]']},
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                       'kwargs': {'attributes': ['info[(.*)][port_channel]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][ipv4][(.*)]']},
                                       'exclude': interface_exclude}},
                      num_values={'name': 1})


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
                                       'requirements':[['info', '(?P<name>\w+Ethernet[\d\/]+$)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', True],
                                                       ['info', '(?P<name>.*)', 'switchport_mode', 'static access'],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
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
                                                        'interfaces', '(?P<name>.*)', 'entry_type', 'static']],
                                       'all_keys': True,
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'exclude': fdb_exclude + ['mac_addresses']},
                                    'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', '(?P<name>.*)',
                                                        'clients', '(?P<client>.*)', 'status', 'authorized']],
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]']},
                                       'all_keys': True,
                                       'exclude': dot1x_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                       'kwargs': {'attributes': ['info[(.*)][switchport_mode]',
                                                                 'info[(.*)][oper_status]',
                                                                 'info[(.*)][enabled]',
                                                                 'info[(.*)][switchport_enable]',
                                                                 'info[(.*)][operational_mode]']},
                                       'missing': False,
                                       'exclude': interface_exclude},
                                  'ops.fdb.fdb.Fdb':{
                                       'requirements':[['info', 'mac_table', 'vlans', '(?P<vlan>.*)',
                                                        'mac_addresses', '(?P<client>.*)']],
                                       'kwargs':{'attributes':['info[mac_table][vlans][(.*)]']},
                                       'missing': True,
                                       'exclude': fdb_exclude + ['mac_addresses']},
                                    'ops.dot1x.dot1x.Dot1x':{
                                       'requirements':[['info', 'interfaces', '(?P<name>.*)']],
                                       'kwargs':{'attributes':['info[interfaces][(.*)][clients][(.*)][status]']},
                                       'all_keys': True,
                                       'missing': True,
                                       'exclude': dot1x_exclude + ['attributes']}},
                      num_values={'name': 'all'})
