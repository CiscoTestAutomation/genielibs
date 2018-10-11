''' 
Interface Genie Ops Object Outputs for IOSXR.
'''


class InterfaceOutput(object):

    ShowInterfacesDetail = {
        'GigabitEthernet0/0/0/0': {
              'auto_negotiate': True,
              'bandwidth': 768,
              'counters': {'carrier_transitions': 0,
                           'drops': 0,
                           'in_abort': 0,
                           'in_broadcast_pkts': 0,
                           'in_crc_errors': 0,
                           'in_discards': 0,
                           'in_errors': 0,
                           'in_frame': 0,
                           'in_giants': 0,
                           'in_ignored': 0,
                           'in_multicast_pkts': 0,
                           'in_octets': 0,
                           'in_overrun': 0,
                           'in_parity': 0,
                           'in_pkts': 0,
                           'in_runts': 0,
                           'in_throttles': 0,
                           'last_clear': 'never',
                           'out_applique': 0,
                           'out_broadcast_pkts': 0,
                           'out_buffer_failures': 0,
                           'out_buffer_swapped_out': 0,
                           'out_discards': 0,
                           'out_errors': 0,
                           'out_multicast_pkts': 0,
                           'out_octets': 0,
                           'out_pkts': 0,
                           'out_resets': 0,
                           'out_underruns': 0,
                           'rate': {'in_rate': 0,
                                    'in_rate_pkts': 0,
                                    'load_interval': 30,
                                    'out_rate': 0,
                                    'out_rate_pkts': 0}},
              'description': 'desc',
              'duplex_mode': 'full',
              'enabled': False,
              'encapsulations': {'encapsulation': 'ARPA'},
              'flow_control': {'flow_control_receive': False,
                               'flow_control_send': False},
              'interface_state': 0,
              'ipv4': {'10.1.1.1/24': {'ip': '10.1.1.1',
                                       'prefix_length': '24'}},
              'last_input': 'never',
              'last_output': 'never',
              'line_protocol': 'administratively down',
              'location': 'unknown',
              'loopback_status': 'not set',
              'mac_address': 'aaaa.bbbb.cccc',
              'mtu': 1600,
              'phys_address': '5254.0077.9407',
              'port_speed': '1000Mb/s',
              'reliability': '255/255',
              'rxload': '0/255',
              'txload': '0/255',
              'types': 'GigabitEthernet'},
         'GigabitEthernet0/0/0/0.10': {
              'bandwidth': 768,
               'counters': {'drops': 0,
                            'in_broadcast_pkts': 0,
                            'in_discards': 0,
                            'in_multicast_pkts': 0,
                            'in_octets': 0,
                            'in_pkts': 0,
                            'last_clear': 'never',
                            'out_broadcast_pkts': 0,
                            'out_discards': 0,
                            'out_multicast_pkts': 0,
                            'out_octets': 0,
                            'out_pkts': 0,
                            'rate': {'in_rate': 0,
                                     'in_rate_pkts': 0,
                                     'load_interval': 5,
                                     'out_rate': 0,
                                     'out_rate_pkts': 0}},
               'enabled': False,
               'encapsulations': {'encapsulation': '802.1Q '
                                                   'Virtual '
                                                   'LAN',
                                  'first_dot1q': '10',
                                  'second_dot1q': '10'},
               'interface_state': 0,
               'last_input': 'never',
               'last_output': 'never',
               'line_protocol': 'administratively down',
               'loopback_status': 'not set',
               'mtu': 1608,
               'reliability': '255/255',
               'rxload': '0/255',
               'txload': '0/255'},
         'GigabitEthernet0/0/0/0.20': {
              'bandwidth': 768,
               'counters': {'drops': 0,
                            'in_broadcast_pkts': 0,
                            'in_discards': 0,
                            'in_multicast_pkts': 0,
                            'in_octets': 0,
                            'in_pkts': 0,
                            'last_clear': 'never',
                            'out_broadcast_pkts': 0,
                            'out_discards': 0,
                            'out_multicast_pkts': 0,
                            'out_octets': 0,
                            'out_pkts': 0,
                            'rate': {'in_rate': 0,
                                     'in_rate_pkts': 0,
                                     'load_interval': 5,
                                     'out_rate': 0,
                                     'out_rate_pkts': 0}},
               'enabled': False,
               'encapsulations': {'encapsulation': '802.1Q '
                                                   'Virtual '
                                                   'LAN',
                                  'first_dot1q': '20'},
               'interface_state': 0,
               'last_input': 'never',
               'last_output': 'never',
               'line_protocol': 'administratively down',
               'loopback_status': 'not set',
               'mtu': 1604,
               'reliability': '255/255',
               'rxload': '0/255',
               'txload': '0/255'},
         'MgmtEth0/0/CPU0/0': {
              'auto_negotiate': True,
               'bandwidth': 0,
               'counters': {'carrier_transitions': 0,
                            'drops': 0,
                            'in_abort': 0,
                            'in_broadcast_pkts': 0,
                            'in_crc_errors': 0,
                            'in_discards': 0,
                            'in_errors': 0,
                            'in_frame': 0,
                            'in_giants': 0,
                            'in_ignored': 0,
                            'in_multicast_pkts': 0,
                            'in_octets': 0,
                            'in_overrun': 0,
                            'in_parity': 0,
                            'in_pkts': 0,
                            'in_runts': 0,
                            'in_throttles': 0,
                            'last_clear': 'never',
                            'out_applique': 0,
                            'out_broadcast_pkts': 0,
                            'out_buffer_failures': 0,
                            'out_buffer_swapped_out': 0,
                            'out_discards': 0,
                            'out_errors': 0,
                            'out_multicast_pkts': 0,
                            'out_octets': 0,
                            'out_pkts': 0,
                            'out_resets': 0,
                            'out_underruns': 0,
                            'rate': {'in_rate': 0,
                                     'in_rate_pkts': 0,
                                     'load_interval': 5,
                                     'out_rate': 0,
                                     'out_rate_pkts': 0}},
               'duplex_mode': 'duplex unknown',
               'enabled': False,
               'encapsulations': {'encapsulation': 'ARPA'},
               'flow_control': {'flow_control_receive': False,
                                'flow_control_send': False},
               'interface_state': 0,
               'last_input': 'never',
               'last_output': 'never',
               'line_protocol': 'administratively down',
               'location': 'unknown',
               'loopback_status': 'not set',
               'mac_address': '5254.00c3.6c43',
               'mtu': 1514,
               'phys_address': '5254.00c3.6c43',
               'port_speed': '0Kb/s',
               'reliability': '255/255',
               'rxload': 'Unknown',
               'txload': 'Unknown',
               'types': 'Management Ethernet'},
         'Null0': {
            'bandwidth': 0,
             'counters': {'drops': 0,
                          'in_broadcast_pkts': 0,
                          'in_discards': 0,
                          'in_multicast_pkts': 0,
                          'in_octets': 0,
                          'in_pkts': 0,
                          'last_clear': 'never',
                          'out_broadcast_pkts': 0,
                          'out_discards': 0,
                          'out_multicast_pkts': 0,
                          'out_octets': 0,
                          'out_pkts': 0,
                          'rate': {'in_rate': 0,
                                   'in_rate_pkts': 0,
                                   'load_interval': 5,
                                   'out_rate': 0,
                                   'out_rate_pkts': 0}},
             'enabled': True,
             'encapsulations': {'encapsulation': 'Null'},
             'last_input': 'never',
             'last_output': 'never',
             'line_protocol': 'up',
             'loopback_status': 'not set',
             'mtu': 1500,
             'reliability': '255/255',
             'rxload': 'Unknown',
             'txload': 'Unknown',
             'types': 'Null'}

    }

    ShowEthernetTags = {        
        "GigabitEthernet0/0/0/0.10": {
              "rewrite_num_of_tags_push": 0,
              "status": "up",
              "rewrite_num_of_tags_pop": 1,
              "mtu": 1518,
              "outer_vlan": ".1Q:10",
              "vlan_id": "10"
         },
         "GigabitEthernet0/0/0/0.20": {
              "rewrite_num_of_tags_push": 0,
              "status": "up",
              "rewrite_num_of_tags_pop": 1,
              "mtu": 1518,
              "outer_vlan": ".1Q:20",
              "vlan_id": "20"
         }
    }

    ShowIpv6VrfAllInterface = {
        'GigabitEthernet0/0/0/0': {
            'enabled': True,
            'int_status': 'shutdown',
            'ipv6': {'2001:db8:1:1::1/64': {'ipv6': '2001:db8:1:1::1',
                                            'ipv6_prefix_length': '64',
                                            'ipv6_status': 'tentative',
                                            'ipv6_subnet': '2001:db8:1:1::'},
                     '2001:db8:2:2::2/64': {'ipv6': '2001:db8:2:2::2',
                                            'ipv6_prefix_length': '64',
                                            'ipv6_status': 'tentative',
                                            'ipv6_subnet': '2001:db8:2:2::'},
                     '2001:db8:3:3:a8aa:bbff:febb:cccc/64': {'ipv6': '2001:db8:3:3:a8aa:bbff:febb:cccc',
                                                             'ipv6_eui64': True,
                                                             'ipv6_prefix_length': '64',
                                                             'ipv6_status': 'tentative',
                                                             'ipv6_subnet': '2001:db8:3:3::'},
                     '2001:db8:4:4::4/64': {'ipv6': '2001:db8:4:4::4',
                                            'ipv6_prefix_length': '64',
                                            'ipv6_route_tag': '10',
                                            'ipv6_status': 'tentative',
                                            'ipv6_subnet': '2001:db8:4:4::'},
                     'auto_config_state': 'stateless',
                     'complete_glean_adj': '0',
                     'complete_protocol_adj': '0',
                     'dropped_glean_req': '0',
                     'dropped_protocol_req': '0',
                     'icmp_redirects': 'disabled',
                     'icmp_unreachables': 'enabled',
                     'in_access_list': 'not set',
                     'incomplete_glean_adj': '0',
                     'incomplete_protocol_adj': '0',
                     'ipv6_link_local': 'fe80::a8aa:bbff:febb:cccc',
                     'ipv6_link_local_state': 'tentative',
                     'ipv6_mtu': '1600',
                     'ipv6_mtu_available': '1586',
                     'nd_adv_retrans_int': '0',
                     'nd_cache_limit': '1000000000',
                     'nd_reachable_time': '0',
                     'out_access_list': 'not set',
                     'table_id': '0xe0800011'},
            'ipv6_enabled': False,
            'oper_status': 'down',
            'vrf': 'VRF1',
            'vrf_id': '0x60000002'},
       'GigabitEthernet0/0/0/0.10': {'enabled': False,
                                     'int_status': 'shutdown',
                                     'ipv6_enabled': False,
                                     'oper_status': 'down',
                                     'vrf': 'default',
                                     'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/0.20': {'enabled': False,
                                     'int_status': 'shutdown',
                                     'ipv6_enabled': False,
                                     'oper_status': 'down',
                                     'vrf': 'default',
                                     'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/1': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'VRF2',
                                  'vrf_id': '0x60000003'},
       'GigabitEthernet0/0/0/2': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/3': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/4': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/5': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/6': {'enabled': False,
                                  'int_status': 'shutdown',
                                  'ipv6_enabled': False,
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'MgmtEth0/0/CPU0/0': {'enabled': False,
                             'int_status': 'shutdown',
                             'ipv6_enabled': False,
                             'oper_status': 'down',
                             'vrf': 'default',
                             'vrf_id': '0x60000000'}
    }

    ShowIpv4VrfAllInterface = {
        'GigabitEthernet0/0/0/0': {
            'int_status': 'shutdown',
            'ipv4': {'10.1.1.1/24': {'ip': '10.1.1.1',
                                     'prefix_length': '24',
                                     'route_tag': 50},
                     '10.2.2.2/24': {'arp': 'disabled',
                                     'broadcast_forwarding': 'disabled',
                                     'helper_address': 'not '
                                                       'set',
                                     'icmp_redirects': 'never '
                                                       'sent',
                                     'icmp_replies': 'never '
                                                     'sent',
                                     'icmp_unreachables': 'always '
                                                          'sent',
                                     'in_access_list': 'not '
                                                       'set',
                                     'ip': '10.2.2.2',
                                     'mtu': 1600,
                                     'mtu_available': 1586,
                                     'out_access_list': 'not '
                                                        'set',
                                     'prefix_length': '24',
                                     'secondary': True,
                                     'table_id': '0xe0000011'},
                     'unnumbered': {'unnumbered_int': '111.111.111.111/32',
                                    'unnumbered_intf_ref': 'Loopback11'}},
            'oper_status': 'down',
            'vrf': 'VRF1',
            'vrf_id': '0x60000002'},
       'GigabitEthernet0/0/0/0.10': {'int_status': 'shutdown',
                                     'oper_status': 'down',
                                     'vrf': 'default',
                                     'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/0.20': {'int_status': 'shutdown',
                                     'oper_status': 'down',
                                     'vrf': 'default',
                                     'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/1': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'VRF2',
                                  'vrf_id': '0x60000003'},
       'GigabitEthernet0/0/0/2': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/3': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/4': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/5': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'GigabitEthernet0/0/0/6': {'int_status': 'shutdown',
                                  'oper_status': 'down',
                                  'vrf': 'default',
                                  'vrf_id': '0x60000000'},
       'MgmtEth0/0/CPU0/0': {'int_status': 'shutdown',
                             'oper_status': 'down',
                             'vrf': 'default',
                             'vrf_id': '0x60000000'}
    }

    ShowVrfAllDetail = {
        "VRF1": {
            "description": "not set",
            "vrf_mode": "Regular",
            "address_family": {
                 "ipv6 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"
                           },
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"
                           },
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"
                           },
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"
                           }
                      }
                 },
                 "ipv4 unicast": {
                      "route_target": {
                           "400:1": {
                                "rt_type": "import",
                                "route_target": "400:1"
                           },
                           "300:1": {
                                "rt_type": "import",
                                "route_target": "300:1"
                           },
                           "200:1": {
                                "rt_type": "both",
                                "route_target": "200:1"
                           },
                           "200:2": {
                                "rt_type": "import",
                                "route_target": "200:2"
                           }
                      }
                 }
            },
            "route_distinguisher": "200:1",
            "interfaces": [
                 "GigabitEthernet0/0/0/1"
            ]
            },
            "VRF2": {
            "description": "not set",
            "vrf_mode": "Regular",
            "address_family": {
                 "ipv6 unicast": {
                      "route_target": {
                           "200:2": {
                                "rt_type": "both",
                                "route_target": "200:2"
                           }
                      }
                 },
                 "ipv4 unicast": {
                      "route_target": {
                           "200:2": {
                                "rt_type": "both",
                                "route_target": "200:2"
                           }
                      }
                 }
            },
            "route_distinguisher": "200:2",
            "interfaces": [
                 "GigabitEthernet0/0/0/2"
            ]}
    }

    ShowInterfacesAccounting = \
        {
          "GigabitEthernet0/0/0/0": {
            "accounting": {
              "arp": {
                "chars_in": 378,
                "chars_out": 378,
                "pkts_in": 9,
                "pkts_out": 9
              },
              "ipv4_multicast": {
                "chars_in": 0,
                "chars_out": 843700,
                "pkts_in": 0,
                "pkts_out": 10514
              },
              "ipv4_unicast": {
                "chars_in": 1226852,
                "chars_out": 887519,
                "pkts_in": 19254,
                "pkts_out": 13117
              }
            }
          },
          "GigabitEthernet0/0/0/1": {
            "accounting": {
              "arp": {
                "chars_in": 378,
                "chars_out": 378,
                "pkts_in": 9,
                "pkts_out": 9
              },
              "ipv4_multicast": {
                "chars_in": 0,
                "chars_out": 844816,
                "pkts_in": 0,
                "pkts_out": 10530
              },
              "ipv4_unicast": {
                "chars_in": 843784,
                "chars_out": 1764,
                "pkts_in": 10539,
                "pkts_out": 26
              }
            }
          }
        }

    InterfaceOpsOutput_info = {
        "Null0": {
          "mtu": 1500,
          "type": "Null",
          "enabled": True,
          "bandwidth": 0,
          "counters": {
               "in_octets": 0,
               "out_broadcast_pkts": 0,
               "out_pkts": 0,
               "in_discards": 0,
               "in_pkts": 0,
               "in_multicast_pkts": 0,
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate": 0,
                    "out_rate_pkts": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 5,
                    "in_rate": 0
               },
               "last_clear": "never",
               "out_multicast_pkts": 0,
               "out_octets": 0
          },
          "encapsulation": {
               "encapsulation": "Null"
          },
      },
      "MgmtEth0/0/CPU0/0": {
          "mtu": 1514,
          "mac_address": "5254.00c3.6c43",
          "flow_control": {
               "flow_control_receive": False,
               "flow_control_send": False
          },
          "type": "Management Ethernet",
          "enabled": False,
          "encapsulation": {
               "encapsulation": "ARPA"
          },
          "auto_negotiate": True,
          "bandwidth": 0,
          "counters": {
               "out_broadcast_pkts": 0,
               "in_multicast_pkts": 0,
               "in_crc_errors": 0,
               "in_pkts": 0,
               "in_errors": 0,
               "in_broadcast_pkts": 0,
               "out_multicast_pkts": 0,
               "out_errors": 0,
               "in_octets": 0,
               "rate": {
                    "out_rate": 0,
                    "out_rate_pkts": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 5,
                    "in_rate": 0
               },
               "out_pkts": 0,
               "in_discards": 0,
               "last_clear": "never",
               "out_octets": 0
          },
          "duplex_mode": "duplex unknown",
          "port_speed": "0Kb/s",
          "phys_address": "5254.00c3.6c43",
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/5": {
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/4": {
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/0": {
          "mtu": 1600,
          "mac_address": "aaaa.bbbb.cccc",
          "description": "desc",
          "duplex_mode": "full",
          "type": "GigabitEthernet",
          "enabled": False,
          "encapsulation": {
               "encapsulation": "ARPA"
          },
          "auto_negotiate": True,
          "ipv4": {
               "10.1.1.1/24": {
                    "ip": "10.1.1.1",
                    "prefix_length": "24",
                    "route_tag": 50},
               "10.2.2.2/24": {
                     "ip": '10.2.2.2',
                     'prefix_length': '24',
                     'secondary': True},
               "unnumbered": {
                    "unnumbered_intf_ref": "Loopback11"
               }
          },
          "bandwidth": 768,
          "accounting": {
               "arp": {
                    "chars_in": 378,
                    "chars_out": 378,
                    "pkts_in": 9,
                    "pkts_out": 9
               },
               "ipv4_multicast": {
                    "chars_in": 0,
                    "chars_out": 843700,
                    "pkts_in": 0,
                    "pkts_out": 10514
               },
               "ipv4_unicast": {
                    "chars_in": 1226852,
                    "chars_out": 887519,
                    "pkts_in": 19254,
                    "pkts_out": 13117
               }
          },
          "counters": {
               "out_broadcast_pkts": 0,
               "in_multicast_pkts": 0,
               "in_crc_errors": 0,
               "in_pkts": 0,
               "in_errors": 0,
               "in_broadcast_pkts": 0,
               "out_multicast_pkts": 0,
               "out_errors": 0,
               "in_octets": 0,
               "rate": {
                    "out_rate": 0,
                    "out_rate_pkts": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 30,
                    "in_rate": 0
               },
               "out_pkts": 0,
               "in_discards": 0,
               "last_clear": "never",
               "out_octets": 0
          },
          "flow_control": {
               "flow_control_receive": False,
               "flow_control_send": False
          },
          "port_speed": "1000Mb/s",
          "phys_address": "5254.0077.9407",
          "ipv6": {
               "2001:db8:2:2::2/64": {
                    "status": "tentative",
                    "ip": "2001:db8:2:2::2",
                    "prefix_length": "64"
               },
               "2001:db8:1:1::1/64": {
                    "status": "tentative",
                    "ip": "2001:db8:1:1::1",
                    "prefix_length": "64"
               },
               "enabled": False,
               "2001:db8:4:4::4/64": {
                    "status": "tentative",
                    "route_tag": "10",
                    "ip": "2001:db8:4:4::4",
                    "prefix_length": "64"
               },
               "2001:db8:3:3:a8aa:bbff:febb:cccc/64": {
                    "status": "tentative",
                    "ip": "2001:db8:3:3:a8aa:bbff:febb:cccc",
                    "prefix_length": "64",
                    "eui64": True
               }
          }
      },
      "GigabitEthernet0/0/0/1": {
          "vrf": "VRF1",
          "ipv6": {
               "enabled": False
          },
          "accounting": {
               "arp": {
                    "chars_in": 378,
                    "chars_out": 378,
                    "pkts_in": 9,
                    "pkts_out": 9
               },
               "ipv4_multicast": {
                    "chars_in": 0,
                    "chars_out": 844816,
                    "pkts_in": 0,
                    "pkts_out": 10530
               },
               "ipv4_unicast": {
                    "chars_in": 843784,
                    "chars_out": 1764,
                    "pkts_in": 10539,
                    "pkts_out": 26
               }
          }
      },
      "GigabitEthernet0/0/0/6": {
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/0.20": {
          "mtu": 1604,
          "counters": {
               "in_octets": 0,
               "out_broadcast_pkts": 0,
               "out_pkts": 0,
               "in_discards": 0,
               "in_pkts": 0,
               "in_multicast_pkts": 0,
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate": 0,
                    "out_rate_pkts": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 5,
                    "in_rate": 0
               },
               "last_clear": "never",
               "out_multicast_pkts": 0,
               "out_octets": 0
          },
          "enabled": False,
          "bandwidth": 768,
          "vlan_id": '20',
          "encapsulation": {
               "encapsulation": "802.1Q Virtual LAN",
               "first_dot1q": "20"
          },
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/2": {
          "vrf": "VRF2",
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/3": {
          "ipv6": {
               "enabled": False
          }
      },
      "GigabitEthernet0/0/0/0.10": {
          "mtu": 1608,
          "counters": {
               "in_octets": 0,
               "out_broadcast_pkts": 0,
               "out_pkts": 0,
               "in_discards": 0,
               "in_pkts": 0,
               "in_multicast_pkts": 0,
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate": 0,
                    "out_rate_pkts": 0,
                    "in_rate_pkts": 0,
                    "load_interval": 5,
                    "in_rate": 0
               },
               "last_clear": "never",
               "out_multicast_pkts": 0,
               "out_octets": 0
          },
          "enabled": False,
          "bandwidth": 768,
          "vlan_id": '10',
          "encapsulation": {
               "encapsulation": "802.1Q Virtual LAN",
               "first_dot1q": "10",
               "second_dot1q": "10"
          },
          "ipv6": {
               "enabled": False
          }
      }
    }
