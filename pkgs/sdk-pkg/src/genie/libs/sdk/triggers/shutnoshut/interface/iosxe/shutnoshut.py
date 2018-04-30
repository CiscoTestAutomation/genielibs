'''Implementation for interface shutnoshut triggers'''

# ats
from ats.utils.objects import Not

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import TriggerShutNoShut

# Which key to exclude for BGP Ops comparison
# Those keys need to be verified with Takashi
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'in_errors', '(Tunnel.*)', 'status']

hsrp_exclude = ['maker', 'active_ip_address', 'standby_ip_address',
                'active_router', 'hello_msec_flag', 'hold_msec_flag',
                'hello_msec', 'hold_msec', 'hello_sec', 'hold_sec',
                'active_ipv6_address', 'standby_ipv6_address']

class TriggerShutNoShutTrunkInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'switchport_mode', 'trunk'],
                                                       ['info', '(?P<name>.*)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'duplex_mode', 'auto'],
                                                       ['info', '(?P<name>.*)', 'port_speed', 'auto'],
                                                       ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                       'exclude': interface_exclude}},
                      num_values={'name': 1})


class TriggerShutNoShutVlanInterface(TriggerShutNoShut):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>Vlan[0-9]+)', 'mtu', '(?P<mtu>.*)'],
                                                       ['info', '(?P<name>.*)', 'enabled', True],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[['enabled', False]],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'ipv6', '(.*)', 'status', '(\w+)']],
                                       'exclude': interface_exclude}},
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
                                            ['info', '(?P<name>.*)', 'duplex_mode', '(\w+)'],
                                            ['info', '(?P<name>.*)', 'port_speed', '(\w+)'],
                                            ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                        'exclude': interface_exclude +\
                                                   [remove_related_subinterface]}},
                      num_values={'name': 1})
