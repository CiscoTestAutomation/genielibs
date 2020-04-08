''' 
Interface Genie Ops Object for NXOS - CLI.
'''

import re

# super class
from genie.libs.ops.interface.interface import Interface as SuperInterface

# nxos show_interface
from genie.libs.parser.nxos.show_interface import ShowInterface, ShowVrfAllInterface,\
                                 ShowIpv6InterfaceVrfAll, ShowIpInterfaceVrfAll,\
                                 ShowInterfaceSwitchport
from genie.libs.parser.nxos.show_routing import ShowRoutingIpv6VrfAll, ShowRoutingVrfAll


class Interface(SuperInterface):
    '''Interface Genie Ops Object'''

    def convert_intf_name(self, item):
        return item.capitalize()

    def learn(self, interface=None, vrf=None, address_family=None):
        '''Learn Interface Ops'''
        ########################################################################
        #                               info
        ########################################################################
        self.callables = {'convert_intf_name': self.convert_intf_name}

        # Global source
        src = '[(?P<interface>{convert_intf_name})]'
        dest = 'info[(?P<interface>{convert_intf_name})]'
        req_keys_path = {'[description]': '[description]',
                        '[types]': '[type]',
                        '[oper_status]': '[oper_status]',
                        '[last_link_flapped]': '[last_change]',
                        '[phys_address]': '[phys_address]',
                        '[port_speed]': '[port_speed]',
                        '[mtu]': '[mtu]',
                        '[enabled]': '[enabled]',
                        '[encapsulations][first_dot1q]': '[vlan_id]',
                        '[mac_address]': '[mac_address]',
                        '[auto_negotiate]': '[auto_negotiate]',
                        '[duplex_mode]': '[duplex_mode]',
                        '[medium]': '[medium]',
                        '[delay]': '[delay]',
                        '[bandwidth]': '[bandwidth]',
                   }
        # vrf
        self.add_leaf(cmd=ShowVrfAllInterface,
                      src=src + '[vrf]',
                      dest=dest + '[vrf]', interface=interface, vrf=vrf)
        self.make()
        if vrf:
            for intf in self.info:
                for src_key_path, dest_key_path in req_keys_path.items():
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + src_key_path,
                                  dest=dest + dest_key_path,
                                  interface=intf)
        else:
            for src_key_path, dest_key_path in req_keys_path.items():
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + src_key_path,
                                  dest=dest + dest_key_path,
                                  interface=interface)




        req_keys = ['access_vlan', 'trunk_vlans', 'switchport_mode',
                    'switchport_enable', 'native_vlan']
        if vrf:
            for intf in self.info:
                for key in req_keys:
                    self.add_leaf(cmd=ShowInterfaceSwitchport,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=intf)

        # ======================================================================
        #                           flow_control
        # ======================================================================

        # flow_control
                self.add_leaf(cmd=ShowInterface,
                              src=src + '[flow_control]',
                              dest=dest + '[flow_control]', interface=intf)

        # ======================================================================
        #                           accounting
        # ======================================================================

        # accounting N/A

        # ======================================================================
        #                           port_channel
        # ======================================================================

        # port_channel
                self.add_leaf(cmd=ShowInterface,
                              src=src + '[port_channel]',
                              dest=dest + '[port_channel]', interface=intf)

                # ======================================================================
                #                           counters
                # ======================================================================
                # Global source
                src = '[(?P<interface>{convert_intf_name})][counters]'
                dest = 'info[(?P<interface>{convert_intf_name})][counters]'

                req_keys = ['in_pkts', 'in_octets', 'in_unicast_pkts',
                            'in_broadcast_pkts', 'in_multicast_pkts',
                            'in_discards', 'in_errors', 'in_unknown_protos',
                            'in_mac_pause_frames', 'in_oversize_frames',
                            'in_crc_errors', 'out_pkts', 'out_octets', 'out_unicast_pkts',
                            'out_broadcast_pkts', 'out_multicast_pkts', 'out_discard',
                            'out_errors', 'last_clear','out_mac_pause_frames']

                for key in req_keys:
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=intf)


                # Global source - counters | rate
                src = '[(?P<interface>{convert_intf_name})][counters][rate]'
                dest = 'info[(?P<interface>{convert_intf_name})][counters][rate]'

                req_keys = ['load_interval', 'in_rate', 'in_rate_pkts',
                            'out_rate', 'out_rate_pkts']

                for key in req_keys:
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=intf)

                # ======================================================================
                #                           encapsulation
                # ======================================================================


                # Global source
                src = '[(?P<interface>{convert_intf_name})][encapsulations]'
                dest = 'info[(?P<interface>{convert_intf_name})][encapsulation]'

                req_keys = ['encapsulation', 'first_dot1q', 'native_vlan']

                for key in req_keys:
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + '[{}]'.format(key),
                                  dest=dest + '[{}]'.format(key), interface=intf)
        else:
            for key in req_keys:
                self.add_leaf(cmd=ShowInterfaceSwitchport,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface)

            # ======================================================================
            #                           flow_control
            # ======================================================================

            # flow_control
            self.add_leaf(cmd=ShowInterface,
                          src=src + '[flow_control]',
                          dest=dest + '[flow_control]', interface=interface)

            # ======================================================================
            #                           accounting
            # ======================================================================

            # accounting N/A

            # ======================================================================
            #                           port_channel
            # ======================================================================

            # port_channel
            self.add_leaf(cmd=ShowInterface,
                          src=src + '[port_channel]',
                          dest=dest + '[port_channel]', interface=interface)

            # ======================================================================
            #                           counters
            # ======================================================================
            # Global source
            src = '[(?P<interface>{convert_intf_name})][counters]'
            dest = 'info[(?P<interface>{convert_intf_name})][counters]'

            req_keys = ['in_pkts', 'in_octets', 'in_unicast_pkts',
                        'in_broadcast_pkts', 'in_multicast_pkts',
                        'in_discards', 'in_errors', 'in_unknown_protos',
                        'in_mac_pause_frames', 'in_oversize_frames',
                        'in_crc_errors', 'out_pkts', 'out_octets', 'out_unicast_pkts',
                        'out_broadcast_pkts', 'out_multicast_pkts', 'out_discard',
                        'out_errors', 'last_clear', 'out_mac_pause_frames']

            for key in req_keys:
                self.add_leaf(cmd=ShowInterface,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface)

            # Global source - counters | rate
            src = '[(?P<interface>{convert_intf_name})][counters][rate]'
            dest = 'info[(?P<interface>{convert_intf_name})][counters][rate]'

            req_keys = ['load_interval', 'in_rate', 'in_rate_pkts',
                        'out_rate', 'out_rate_pkts']

            for key in req_keys:
                self.add_leaf(cmd=ShowInterface,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface)

            # ======================================================================
            #                           encapsulation
            # ======================================================================

            # Global source
            src = '[(?P<interface>{convert_intf_name})][encapsulations]'
            dest = 'info[(?P<interface>{convert_intf_name})][encapsulation]'

            req_keys = ['encapsulation', 'first_dot1q', 'native_vlan']

            for key in req_keys:
                self.add_leaf(cmd=ShowInterface,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface)

        # ======================================================================
        #                           ipv4
        # ======================================================================
        
        if not address_family or address_family.lower() == 'ipv4':
            # Global source
            src = '[(?P<interface>{convert_intf_name})][ipv4][(?P<ipv4>.*)]'
            dest = 'info[(?P<interface>{convert_intf_name})][ipv4][(?P<ipv4>.*)]'

            req_keys = ['ip', 'prefix_length', 'secondary']

            for key in req_keys:
                self.add_leaf(cmd=ShowIpInterfaceVrfAll,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface, vrf=vrf)
            if vrf:
                for intf in self.info:
                    self.add_leaf(cmd=ShowInterface,
                                  src=src + '[route_tag]',
                                  dest=dest + '[route_tag]', interface=intf)

            else:
            # route_tag
                self.add_leaf(cmd=ShowInterface,
                          src=src + '[route_tag]',
                          dest=dest + '[route_tag]', interface=interface)

            # secondary_vrf   --- This is not supported on NXOS
            # unnumbered
            self.add_leaf(cmd=ShowIpInterfaceVrfAll,
                          src='[(?P<interface>{convert_intf_name})][ipv4][unnumbered]',
                          dest='info[(?P<interface>{convert_intf_name})][ipv4][unnumbered]',
                          interface=interface, vrf=vrf)

            # get routing output
            self.add_leaf(cmd=ShowRoutingVrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][ubest_num]',
                          dest='info[routing_v4][(?P<vrf>.*)][(?P<ip>.*)][ubest_num]', vrf=vrf)

            # get routing output
            self.add_leaf(cmd=ShowRoutingVrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][mbest_num]',
                          dest='info[routing_v4][(?P<vrf>.*)][(?P<ip>.*)][mbest_num]', vrf=vrf)

            # get routing output
            self.add_leaf(cmd=ShowRoutingVrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][attach]',
                          dest='info[routing_v4][(?P<vrf>.*)][(?P<ip>.*)][attach]', vrf=vrf)

            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][best_route]'\
                  '[(?P<best_route>.*)][nexthop][(?P<nexthop>.*)][protocol][(?P<protocol>.*)]'
            dest = 'info[routing_v4][(?P<vrf>.*)][(?P<ip>.*)][best_route][(?P<best_route>.*)]'\
                   '[nexthop][(?P<nexthop>.*)][protocol][(?P<protocol>.*)]'

            req_keys = ['route_table', 'interface', 'preference', 'metric', 'protocol_id', 'attribute',
                        'tag', 'mpls', 'mpls_vpn', 'evpn', 'segid', 'tunnelid', 'encap']

            for key in req_keys:
                self.add_leaf(cmd=ShowRoutingVrfAll,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), vrf=vrf)

        # ======================================================================
        #                           ipv6
        # ======================================================================
        
        if not address_family or address_family.lower() == 'ipv6':
            # Global source
            src = '[(?P<interface>{convert_intf_name})][ipv6][(?P<ipv6>.*)]'
            dest = 'info[(?P<interface>{convert_intf_name})][ipv6][(?P<ipv6>.*)]'

            req_keys = ['ip', 'prefix_length', 'anycast', 'status']

            for key in req_keys:
                self.add_leaf(cmd=ShowIpv6InterfaceVrfAll,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), interface=interface, vrf=vrf)


            # get routing output
            self.add_leaf(cmd=ShowRoutingIpv6VrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][ubest_num]',
                          dest='info[routing_v6][(?P<vrf>.*)][(?P<ip>.*)][ubest_num]', vrf=vrf)

            # get routing output
            self.add_leaf(cmd=ShowRoutingIpv6VrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][mbest_num]',
                          dest='info[routing_v6][(?P<vrf>.*)][(?P<ip>.*)][mbest_num]', vrf=vrf)

            # get routing output
            self.add_leaf(cmd=ShowRoutingIpv6VrfAll,
                          src='[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][attach]',
                          dest='info[routing_v6][(?P<vrf>.*)][(?P<ip>.*)][attach]', vrf=vrf)

            src = '[vrf][(?P<vrf>.*)][address_family][(?P<af>.*)][ip][(?P<ip>.*)][best_route]'\
                  '[(?P<best_route>.*)][nexthop][(?P<nexthop>.*)][protocol][(?P<protocol>.*)]'
            dest = 'info[routing_v6][(?P<vrf>.*)][(?P<ip>.*)][best_route][(?P<best_route>.*)]'\
                   '[nexthop][(?P<nexthop>.*)][protocol][(?P<protocol>.*)]'

            req_keys = ['route_table', 'interface', 'preference', 'metric', 'protocol_id', 'attribute',
                        'tag', 'mpls', 'mpls_vpn', 'evpn', 'segid', 'tunnelid', 'encap']

            for key in req_keys:
                self.add_leaf(cmd=ShowRoutingIpv6VrfAll,
                              src=src + '[{}]'.format(key),
                              dest=dest + '[{}]'.format(key), vrf=vrf)

        # make to write in cache
        self.make(final_call=True)

        # eui_64
        # if has ip like 2001:db8::5054:ff:fed5:63f9, eui_64 is True
        p = re.compile(r'([a-z0-9]+):([\w\:]+)?ff:([a-z0-9]+):([a-z0-9]+)')
        if hasattr(self, 'info'): 
            for intf in self.info:
                # check vrf
                if 'vrf' in self.info[intf]:
                    if 'routing_v4' in self.info and \
                      self.info[intf]['vrf'] in self.info['routing_v4']:
                        dict_v4 = self.info['routing_v4'][self.info[intf]['vrf']]
                    else:
                        dict_v4 = {}

                    if 'routing_v6' in self.info and \
                      self.info[intf]['vrf'] in self.info['routing_v6']:
                          dict_v6 = self.info['routing_v6'][self.info[intf]['vrf']]
                    else:
                        dict_v6 = {}
                else:
                    continue

                for key in self.info[intf]:
                    if key == 'ipv4' or key == 'ipv6':
                        for ip in self.info[intf][key].keys():
                            if p.match(ip):
                                self.info[intf][key][ip]['eui_64'] = True

                            # route_tag and origin of ipv4/ipv6
                            self.ret_dict = {}
                            routing_dict = dict_v4 if key == 'ipv4' else dict_v6

                            if ip in routing_dict:
                                self._match_keys(dic=routing_dict[ip],
                                                 match={'interface': intf})

                            for protocol in self.ret_dict:
                                if 'tag' in self.ret_dict[protocol]:
                                    self.info[intf][key][ip]['route_tag'] = \
                                      self.ret_dict[protocol]['tag']
                                self.info[intf][key][ip]['origin'] = protocol

                            # Delete ret_dict
                            del self.ret_dict

            # delete the routing attribute which is only used 
            # for getting route_tag and origin
            for key in ['routing_v4', 'routing_v6']:
                if key in self.info:
                    del(self.info[key])

    def _match_keys(self, dic, match):
        '''find entry in the dic when values are same to match.
           will return the upper level dictionary contains those values
        '''
        if isinstance(dic, dict):
            for key, value in match.items():
                for dic_key in dic:
                    if key in dic[dic_key] and dic[dic_key][key] == value:
                        self.ret_dict.update(dic)
                        break
                    elif not isinstance(dic[dic_key], dict):
                        pass
                    else:
                        self._match_keys(dic=dic[dic_key], match=match)
        return(self.ret_dict)


