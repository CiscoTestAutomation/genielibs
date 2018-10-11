'''IOSXR Implementation for Interface unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# import ats
from ats import aetest

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'in_crc_errors',
                     'in_discards', 'accounting']

## IOSXR TriggerUnconfigConfigEthernetInterface implemented seperately since it
## doesn't need port_channel_member = False as in NXOS.


class TriggerUnconfigConfigEthernetInterface(TriggerUnconfigConfig):

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>(GigabitEthernet|gigabitEthernet|TenGigE|HundredGigE)[0-9\/]+)',
                                                         'enabled', True],
                                                        ['info', '(?P<name>(GigabitEthernet|gigabitEthernet|TenGigE|HundredGigE)[0-9\/]+)',
                                                         'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>.*)','access_vlan'],
                                                        ['info', '(?P<name>.*)','switchport_enable'],
                                                        ['info', '(?P<name>.*)','switchport_mode'],
                                                        ['info', '(?P<name>.*)','trunk_vlans'],
                                                        ['info', '(?P<name>.*)','vrf'],
                                                        ['info', '(?P<name>.*)','duplex_mode'],
                                                        ['info', '(?P<name>.*)','mac_address'],
                                                        ['info', '(?P<name>.*)','oper_status']],
                                        'exclude': interface_exclude}},
                      num_values={'name': 1})
