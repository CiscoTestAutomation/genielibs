''' 
Arp Genie Ops Object Outputs for IOSXR.
'''


class ArpOutput(object):

     ShowArpDetail = {
          'interfaces': {
               'GigabitEthernet0/0/0/0': {
                    'ipv4': {
                         'neighbors': {
                              '10.1.2.1': {
                                   'age': '02:55:43',
                                   'ip': '10.1.2.1',
                                   'link_layer_address': 'fa16.3e4c.b963',
                                   'origin': 'dynamic',
                                   'type': 'ARPA'},
                              '10.1.2.2': {
                                   'age': '-',
                                   'ip': '10.1.2.2',
                                   'link_layer_address': 'fa16.3ee4.1462',
                                   'origin': 'static',
                                   'type': 'ARPA'}
                         }
                    }
               },
               'GigabitEthernet0/0/0/1': {
                    'ipv4': {
                         'neighbors': {
                              '10.2.3.2': {
                                   'age': '-',
                                   'ip': '10.2.3.2',
                                   'link_layer_address': 'fa16.3e8f.3468',
                                   'origin': 'static',
                                   'type': 'ARPA'},
                              '10.2.3.3': {
                                   'age': '00:13:12',
                                   'ip': '10.2.3.3',
                                   'link_layer_address': '5e00.8002.0007',
                                   'origin': 'dynamic',
                                   'type': 'ARPA'}
                         }
                    }
               }
          }
     }

     ShowArpTrafficDetail = {
          '0/0/CPU0': {
               'cache': {
                    'alias': 0,
                    'dhcp': 0,
                    'dynamic': 2,
                    'interface': 2,
                    'ip_packet_drop_count': 0,
                    'standby': 0,
                    'static': 0,
                    'total_arp_entries': 4,
                    'total_arp_idb': 2},
               'statistics': {
                    'in_replies_pkts': 8,
                    'in_requests_pkts': 108,
                    'no_buffers_errors': 0,
                    'out_gratuitous_pkts': 2,
                    'out_local_proxy': 0,
                    'out_of_memory_errors': 0,
                    'out_of_subnet_errors': 0,
                    'out_proxy': 0,
                    'out_replies_pkts': 108,
                    'out_requests_pkts': 8,
                    'resolve_dropped_requests': 0,
                    'resolve_rcvd_requests': 0,
                    'subscriber_intf_gratuitous': 0,
                    'subscriber_intf_replies': 0,
                    'subscriber_intf_requests': 0}
          },
          '0/RP0/CPU0': {
               'cache': {
                    'alias': 0,
                    'dhcp': 0,
                    'dynamic': 0,
                    'interface': 0,
                    'ip_packet_drop_count': 0,
                    'standby': 0,
                    'static': 0,
                    'total_arp_entries': 0,
                    'total_arp_idb': 0},
               'statistics': {
                    'in_replies_pkts': 0,
                    'in_requests_pkts': 0,
                    'no_buffers_errors': 0,
                    'out_gratuitous_pkts': 0,
                    'out_local_proxy': 0,
                    'out_of_memory_errors': 0,
                    'out_of_subnet_errors': 0,
                    'out_proxy': 0,
                    'out_replies_pkts': 0,
                    'out_requests_pkts': 0,
                    'resolve_dropped_requests': 0,
                    'resolve_rcvd_requests': 0,
                    'subscriber_intf_gratuitous': 0,
                    'subscriber_intf_replies': 0,
                    'subscriber_intf_requests': 0}
          }
     }

     ShowIpv4VrfAllInterface = {
          'GigabitEthernet0/0/0/0': {
               'int_status': 'up',
               'ipv4': {
                    '10.1.3.1/24': {
                         'ip': '10.1.3.1',
                         'prefix_length': '24'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1514,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000000'},
               'multicast_groups': ['224.0.0.2',
                                    '224.0.0.1',
                                    '224.0.0.2',
                                    '224.0.0.5',
                                    '224.0.0.6'],
               'oper_status': 'up',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'GigabitEthernet0/0/0/1': {
               'int_status': 'up',
               'ipv4': {
                    '10.1.5.1/24': {
                         'ip': '10.1.5.1',
                         'prefix_length': '24',
                         'route_tag': 50},
                    '10.2.2.2/24': {
                         'ip': '10.2.2.2',
                         'prefix_length': '24',
                         'secondary': True},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1514,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000010'},
               'multicast_groups': ['224.0.0.2', '224.0.0.1'],
               'oper_status': 'up',
               'vrf': 'VRF1',
               'vrf_id': '0x60000001'},
          'GigabitEthernet0/0/0/2': {
               'int_status': 'up',
               'ipv4': {
                    '10.186.5.1/24': {
                         'ip': '10.186.5.1',
                         'prefix_length': '24'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1514,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000011'},
               'multicast_groups': ['224.0.0.2', '224.0.0.1'],
               'oper_status': 'up',
               'vrf': 'VRF2',
               'vrf_id': '0x60000002'},
          'GigabitEthernet0/0/0/3': {
               'int_status': 'up',
               'ipv4': {
                    '10.1.2.1/24': {
                         'ip': '10.1.2.1',
                         'prefix_length': '24'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1514,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000000'},
               'multicast_groups': ['224.0.0.2',
                                    '224.0.0.1',
                                    '224.0.0.2',
                                    '224.0.0.5',
                                    '224.0.0.6'],
               'oper_status': 'up',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'GigabitEthernet0/0/0/4': {
               'int_status': 'up',
               'ipv4': {
                    '10.69.111.111/32': {
                         'ip': '10.69.111.111',
                         'prefix_length': '32'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1514,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000000',
                    'unnumbered': {'unnumbered_intf_ref': 'Loopback11'}},
               'multicast_groups': ['224.0.0.2', '224.0.0.1'],
               'oper_status': 'up',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'GigabitEthernet0/0/0/5': {
               'int_status': 'shutdown',
               'oper_status': 'down',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'GigabitEthernet0/0/0/6': {
               'int_status': 'shutdown',
               'oper_status': 'down',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'Loopback0': {
               'int_status': 'up',
               'ipv4': {
                    '10.4.1.1/32': {
                         'ip': '10.4.1.1',
                         'prefix_length': '32'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1500,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000000'},
               'oper_status': 'up',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'Loopback11': {
               'int_status': 'up',
               'ipv4': {
                    '10.69.111.111/32': {
                         'ip': '10.69.111.111',
                         'prefix_length': '32'},
                    'broadcast_forwarding': 'disabled',
                    'icmp_redirects': 'never sent',
                    'icmp_replies': 'never sent',
                    'icmp_unreachables': 'always sent',
                    'mtu': 1500,
                    'mtu_available': 1500,
                    'proxy_arp': 'disabled',
                    'table_id': '0xe0000000'},
               'oper_status': 'up',
               'vrf': 'default',
               'vrf_id': '0x60000000'},
          'MgmtEth0/0/CPU0/0': {
               'int_status': 'shutdown',
               'oper_status': 'down',
               'vrf': 'default',
               'vrf_id': '0x60000000'}
     }

     Arp_info = {
          'interfaces': {
               'GigabitEthernet0/0/0/0': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False},
                    'ipv4': {
                         'neighbors': {
                              '10.1.2.1': {
                                   'ip': '10.1.2.1',
                                   'link_layer_address': 'fa16.3e4c.b963',
                                   'origin': 'dynamic'},
                              '10.1.2.2': {
                                   'ip': '10.1.2.2',
                                   'link_layer_address': 'fa16.3ee4.1462',
                                   'origin': 'static'}
                         }
                    }
               },
               'GigabitEthernet0/0/0/1': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False},
                    'ipv4': {
                         'neighbors': {
                              '10.2.3.2': {
                                   'ip': '10.2.3.2',
                                   'link_layer_address': 'fa16.3e8f.3468',
                                   'origin': 'static'},
                              '10.2.3.3': {
                                   'ip': '10.2.3.3',
                                   'link_layer_address': '5e00.8002.0007',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'GigabitEthernet0/0/0/2': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False}
               },
               'GigabitEthernet0/0/0/3': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False}
               },
               'GigabitEthernet0/0/0/4': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False}
               },
               'Loopback0': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False}
               },
               'Loopback11': {
                    'arp_dynamic_learning': {
                         'proxy_enable': False}
               }
          },
          'statistics': {
               'in_replies_pkts': 8,
               'in_requests_pkts': 108,
               'out_gratuitous_pkts': 2,
               'out_replies_pkts': 108,
               'out_requests_pkts': 8}
          }