'''Implementation for interface modify triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# import python
from functools import partial

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'accounting']


class TriggerModifyEthernetMtu(TriggerModify):

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements': [['info', '(?P<name>\w+Ethernet[0-9\/]+$)', 'mtu', '(?P<mtu>.*)'],
                                                         ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                         ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude,
                                        'include_management_interface': False}},
                      config_info={'conf.interface.Interface':{
                                      'requirements':[['mtu', 9216]],
                                      'verify_conf':False,
                                      'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                             'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                      'requirements': [['info', '(?P<name>.*)', 'mtu', 9216],
                                                       ['info', '(?P<name>.*)', 'bandwidth', '(\d+)'],
                                                       ['info', '(.*)', 'mtu', '(\d+)']],
                                      'exclude': interface_exclude}},
                      num_values={'name': 1, 'mtu': 1})


class TriggerModifySwitchportModeTrunkToAccess(TriggerModify):

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[\
                                            ['info', '(?P<name>.*)', 'switchport_mode', 'trunk'],
                                            ['info', '(?P<name>.*)', 'enabled', True],
                                            ['info', '(?P<name>.*)', 'oper_status', 'up'],
                                            ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False]],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[['switchport_mode', 'access']],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements': [\
                                            ['info', '(?P<name>.*)', 'switchport_mode', '(.*access)'],
                                            ['info', '(?P<name>.*)', 'switchport_enable', False]],
                                        'exclude': interface_exclude + ['(Vlan.*)']}},
                      num_values={'name': 1})
