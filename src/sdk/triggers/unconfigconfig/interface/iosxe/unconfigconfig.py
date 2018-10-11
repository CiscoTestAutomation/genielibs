'''Implementation for Interface unconfigconfig triggers'''

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig
from genie.libs.sdk.triggers.unconfigconfig.interface.unconfigconfig import \
    TriggerUnconfigConfigEthernetInterface as UncfgCfgInterface

# import ats
from ats import aetest

# Which key to exclude for Interface Ops comparison
interface_exclude = ['maker', 'last_change','in_rate','in_rate_pkts',
                     'out_rate', 'out_rate_pkts', 'in_octets',
                     'in_pkts', 'in_unicast_pkts', 'out_octets',
                     'out_pkts', 'out_unicast_pkts', 'out_multicast_pkts',
                     'in_multicast_pkts', 'last_clear', 'in_broadcast_pkts',
                     'out_broadcast_pkts', 'bandwidth', 'load_interval',
                     'port_speed', 'in_crc_errors', 'in_errors',
                     'in_discards', '(Tunnel.*)', 'accounting']



# for physical interfaces, the interface won't be removed, only can be defaulted.
# all keys and values will return to default value when physical interfaces being unconfigured
class TriggerUnconfigConfigPhysicalInterface(TriggerUnconfigConfig):
    '''Trigger class for UnconfigConfig physical interfaces action'''

    @aetest.test
    def verify_unconfigure(self, uut, abstract, steps):
        '''Verify that the unconfiguration was done correctly and Ops state is 
           as expected.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            self.mapping.verify_ops(device=uut, abstract=abstract,
                                    steps=steps)
        except Exception as e:
            self.failed('Failed to verify the '
                        'unconfigure feature\n{e}'.format(e=str(e)))


class TriggerUnconfigConfigPhysicalTrunkInterface(TriggerUnconfigConfigPhysicalInterface):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>\w+Ethernet[\d\/\.]+)',
                                                        'switchport_mode', 'trunk'],
                                                       ['info', '(?P<name>\w+Ethernet[\d\/\.]+)',
                                                        'port_channel', 'port_channel_int', '(?P<port_int>.*)']],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', 'oper_status', 'down'],
                                                       ['info', '(?P<name>.*)', 'enabled', False],
                                                       ['info', '(?P<name>.*)', 'port_channel',
                                                        'port_channel_member', False],
                                                       ['info', '(?P<name>.*)', 'mac_address', '([\w\.]+)'],
                                                       ['info', '(?P<name>.*)', '(.*)'],
                                                       ['info', '(?P<port_int>.*)', 'port_channel', 'port_channel_member_intfs', '(.*)'],
                                                       ['info', '(Port-channel.*)', 'mac_address', '(.*)'],
                                                       ['info', '(Port-channel.*)', 'phys_address', '(.*)']],
                                       'exclude': interface_exclude}},
                      num_values={'name':1})



class TriggerUnconfigConfigEthernetInterface(UncfgCfgInterface):

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>\w+Ethernet[0-9\/]+$)', 'enabled', True],
                                                        ['info', '(?P<name>.*)', 'port_channel', 'port_channel_member', False],
                                                        ['info', '(?P<name>.*)', 'oper_status', 'up']],
                                        'exclude': interface_exclude,
                                        'include_management_interface': False}},
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
                                                        ['info', '(?P<name>.*)','enabled'],
                                                        ['info', '(?P<name>.*)','duplex_mode'],
                                                        ['info', '(?P<name>.*)','mac_address'],
                                                        ['info', '(?P<name>.*)','oper_status']],
                                        'exclude': interface_exclude +\
                                                   [UncfgCfgInterface.remove_related_subinterface]}},
                      num_values={'name': 1})


class TriggerUnconfigConfigEthernetInterfaceSub(TriggerUnconfigConfig):

    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'enabled', True],
                                                        ['info', '(?P<name>(GigabitEthernet|gigabitEthernet|Ethernet|ethernet)[0-9\/]+\.[0-9]+)',
                                                         'oper_status', 'up']],
                                        'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                        'requirements':[],
                                        'verify_conf':False,
                                        'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                               'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                        'requirements':[['info', '(?P<name>.*)','enabled', False]],
                                        'exclude': interface_exclude}},
                      num_values={'name': 1})


class TriggerUnconfigConfigVirtualTrunkInterface(TriggerUnconfigConfig):

    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>[p|P]ort-channel[\d\.]+)',
                                                        'switchport_mode', 'trunk'],
                                                       ['info', '(?P<name>[p|P]ort-channel[\d\.]+)',
                                                        'port_channel', 'port_channel_member', False]],
                                       'exclude': interface_exclude}},
                      config_info={'conf.interface.Interface':{
                                       'requirements':[],
                                       'verify_conf':False,
                                       'kwargs':{'mandatory':{'name': '(?P<name>.*)',
                                                              'attach': False}}}},
                      verify_ops={'ops.interface.interface.Interface':{
                                       'requirements':[['info', '(?P<name>.*)', '(.*)']],
                                       'exclude': interface_exclude}},
                      num_values={'name':1})
