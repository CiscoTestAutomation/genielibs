'''
 Vlan Genie Ops Object Outputs for IOSXE.
'''

class VlanOutput(object):
    # 'show vlan' output


    showVlan = {
        'vlans': {
            '1': {
                'vlan_id': '1',
                'name': 'default',
                'state': 'active',
                'shutdown': False,
                'interfaces': ['GigabitEthernet1/0/1', 'GigabitEthernet1/0/2', 'GigabitEthernet1/0/3',
                               'GigabitEthernet1/0/5', 'GigabitEthernet1/0/6', 'GigabitEthernet1/0/12',
                               'GigabitEthernet1/0/13', 'GigabitEthernet1/0/14', 'GigabitEthernet1/0/15',
                               'GigabitEthernet1/0/16', 'GigabitEthernet1/0/17', 'GigabitEthernet1/0/18',
                               'GigabitEthernet1/0/19', 'GigabitEthernet1/0/20', 'GigabitEthernet1/0/21',
                               'GigabitEthernet1/0/22']
            },
            '2': {
                'vlan_id': '2',
                'name': 'VLAN0002',
                'state': 'shutdown',
                'shutdown': True,
            },
            '20': {
                'vlan_id': '20',
                'name': 'VLAN0020',
                'state': 'active',
                'shutdown': False,
            },
            '100': {
                'vlan_id': '100',
                'name': 'V100',
                'state': 'suspended',
                'shutdown': False,
            },
            '101': {
                'vlan_id': '101',
                'name': 'VLAN0101',
                'state': 'active',
                'shutdown': False,
            },
            '102': {
                'vlan_id': '102',
                'name': 'VLAN0102',
                'state': 'active',
                'shutdown': False,
            },
            '103': {
                'vlan_id': '103',
                'name': 'VLAN0103',
                'state': 'active',
                'shutdown': False,
            },
        },
    }

    vlanOpsOutput = \
        {
            'vlans': {
                '1': {
                    'interfaces': ['GigabitEthernet1/0/1',
                                   'GigabitEthernet1/0/2',
                                   'GigabitEthernet1/0/3',
                                   'GigabitEthernet1/0/5',
                                   'GigabitEthernet1/0/6',
                                   'GigabitEthernet1/0/12',
                                   'GigabitEthernet1/0/13',
                                   'GigabitEthernet1/0/14',
                                   'GigabitEthernet1/0/15',
                                   'GigabitEthernet1/0/16',
                                   'GigabitEthernet1/0/17',
                                   'GigabitEthernet1/0/18',
                                   'GigabitEthernet1/0/19',
                                   'GigabitEthernet1/0/20',
                                   'GigabitEthernet1/0/21',
                                   'GigabitEthernet1/0/22'],
                    'vlan_id': '1',
                    'name': 'default',
                    'state': 'active',
                    'shutdown': False,
                },
                '2': {
                    'vlan_id': '2',
                    'name': 'VLAN0002',
                    'state': 'shutdown',
                    'shutdown': True,
                },
                '20': {
                    'vlan_id': '20',
                    'name': 'VLAN0020',
                    'state': 'active',
                    'shutdown': False,
                },
                '100': {
                    'vlan_id': '100',
                    'name': 'V100',
                    'state': 'suspended',
                    'shutdown': False,
                },
                '101': {
                    'vlan_id': '101',
                    'name': 'VLAN0101',
                    'state': 'active',
                    'shutdown': False,
                },
                '102': {
                    'vlan_id': '102',
                    'name': 'VLAN0102',
                    'state': 'active',
                    'shutdown': False,
                },
                '103': {
                    'vlan_id': '103',
                    'name': 'VLAN0103',
                    'state': 'active',
                    'shutdown': False,
                },
            },
        }

    showVlanMtuempty = {}

    showVlanMtu = {'vlan_id':
                       {'2':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '1005':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '1003':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '300':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '1002':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '1004':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                        '100':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': '1500'},
                        '1':
                            {'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': '1500'}
                        }
                   }


    showVlanRemoteSpan = {'vlan_id':
                              {'400':
                                   {'vlan_is_remote_span': True},
                               '500':
                                   {'vlan_is_remote_span': True},
                               '100':
                                   {'vlan_is_remote_span': True}
                               }
                          }

    showVlanAccessMap = {'access_map_id':
                             {'map1':
                                  {'access_map_sequence':
                                       {'20':
                                            {'access_map_action_value': 'forward'},
                                        '10':
                                            {'access_map_action_value': 'forward'},
                                        '90':
                                            {'access_map_action_value': 'forward'},
                                        '70':
                                            {'access_map_action_value': 'forward'},
                                        '30':
                                            {'access_map_action_value': 'forward'},
                                        '50':
                                            {'access_map_action_value': 'forward'},
                                        '60':
                                            {'access_map_action_value': 'forward'},
                                        '40':
                                            {'access_map_action_value': 'forward'},
                                        '80':
                                            {'access_map_action_value': 'forward'}}},
                              'map2':
                                  {'access_map_sequence':
                                       {'20':
                                            {'access_map_action_value': 'forward', 'access_map_match_protocol_value': '2', 'access_map_match_protocol': 'ip'},
                                        '10':
                                            {'access_map_action_value': 'forward'},
                                        '30':
                                            {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'la', 'access_map_match_protocol': 'ipv6'},
                                        '50':
                                            {'access_map_action_value': 'forward', 'access_map_match_protocol_value': '1301 feq', 'access_map_match_protocol': 'ip'},
                                        '60':
                                            {'access_map_action_value': 'drop', 'access_map_match_protocol_value': 'laila suzam', 'access_map_match_protocol': 'ipv6'},
                                        '40':
                                            {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'fa', 'access_map_match_protocol': 'mac'}
                                        }
                                   }
                              }
                         }

    showIpInterfaceBriefPipeVlan = {'interface':
                                        {'Vlan100':
                                             {'vlan_id':
                                                  {'100':
                                                       {'status': 'up', 'protocol': 'down', 'interface_is_ok': 'YES', 'ip_address': '192.168.234.1', 'method': 'manual'}}},
                                         'Vlan1':
                                             {'vlan_id':
                                                  {'1':
                                                       {'status': 'administratively down', 'protocol': 'down', 'interface_is_ok': 'YES', 'ip_address': 'unassigned', 'method': 'unset'}}
                                              }
                                         }
                                    }

    showVlanFilter = {'vlan_id':
                          {'100':
                               {'access_map_tag': 'map2'},
                           '200':
                               {'access_map_tag': 'map1'},
                           '300':
                               {'access_map_tag': 'map1'}
                           }
                      }

    showInterfacesSwitchport = {'interface':
                                    {'Gi1/0/1':
                                         {'switchport_mode': {'trunk': {'vlan_id': {'16': {'admin_trunking_encapsulation': 'dot1q'}}}}},
                                     'Gi1/0/3':
                                         {'switchport_mode': {'trunk': {'vlan_id': {'1': {'admin_trunking_encapsulation': 'dot1q'},
                                                                                    '300': {}}}}},
                                     'Gi1/0/4': {},
                                     'Gi1/0/5':
                                         {'switchport_mode': {'trunk': {'vlan_id': {'1': {'admin_trunking_encapsulation': 'dot1q'}}}}},
                                     'Gi2/0/15':
                                         {'switchport_mode': {'static access': {'vlan_id': {'1': {'admin_trunking_encapsulation': 'dot1q'}}}}}
                                     }
                                }

    # Case without using 'vlan_id' as the structure header
    # ----------------------------------------------------
    # When we call VlanOutput.vlan_all it automatically exclude the dictionary duplicate key's values.
    vlan_all = {'1003':
                    {'status': 'act/unsup', 'name': 'token-ring-default', 'vlan_mtu': None},
                '500':
                    {'status': 'active', 'name': 'VLAN0500', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100500', 'RingNo': None, 'Trans2': '0', 'remote_span_vlan': True, 'mtu': '1500', 'BridgeNo': None, 'remote_span_vlan': True},
                '1005':
                    {'status': 'act/unsup', 'members': None, 'name': 'trnet-default', 'stp': 'ibm', 'type': 'trnet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '101005', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                '1004':
                    {'status': 'act/unsup', 'members': None, 'name': 'fddinet-default', 'stp': 'ieee', 'type': 'fdnet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '101004', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                '100':
                    {'access_map_sequence':
                         {'10': {'access_map_action_value': 'forward'},
                          '20': {'access_map_action_value': 'forward', 'access_map_match_protocol_value': '2', 'access_map_match_protocol': 'ip'},
                          '30': {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'la', 'access_map_match_protocol': 'ipv6'},
                          '40': {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'fa', 'access_map_match_protocol': 'mac'},
                          '50': {'access_map_action_value': 'forward', 'access_map_match_protocol_value': '1301 feq', 'access_map_match_protocol': 'ip'},
                          '60': {'access_map_action_value': 'drop', 'access_map_match_protocol_value': 'laila suzam', 'access_map_match_protocol': 'ipv6'}}, 'ip_address': '192.168.234.1', 'status': 'active', 'members': None, 'name': 'VLAN0100', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100100', 'RingNo': None, 'Trans2': '0', 'remote_span_vlan': True, 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': '1500', 'remote_span_vlan': True},
                '200':
                    {'access_map_sequence':
                         {'10': {'access_map_action_value': 'forward'},
                          '20': {'access_map_action_value': 'forward'},
                          '30': {'access_map_action_value': 'forward'},
                          '40': {'access_map_action_value': 'forward'},
                          '50': {'access_map_action_value': 'forward'},
                          '60': {'access_map_action_value': 'forward'},
                          '70': {'access_map_action_value': 'forward'},
                          '80': {'access_map_action_value': 'forward'},
                          '90': {'access_map_action_value': 'forward'}}, 'private_secondary_vlan': 'none', 'status': 'active', 'members': None, 'name': 'VLAN0200', 'private_vlan_type': 'primary', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100200', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                '400':
                    {'status': 'active', 'members': None, 'name': 'VLAN0400', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100400', 'RingNo': None, 'Trans2': '0', 'remote_span_vlan': True, 'mtu': '1500', 'BridgeNo': None, 'remote_span_vlan': True},
                '16': {'switchport_interfaces': {'Gi1/0/1': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}}}},
                '300':
                    {'access_map_sequence':
                         {'10': {'access_map_action_value': 'forward'},
                          '20': {'access_map_action_value': 'forward'},
                          '30': {'access_map_action_value': 'forward'},
                          '40': {'access_map_action_value': 'forward'},
                          '50': {'access_map_action_value': 'forward'},
                          '60': {'access_map_action_value': 'forward'},
                          '70': {'access_map_action_value': 'forward'},
                          '80': {'access_map_action_value': 'forward'},
                          '90': {'access_map_action_value': 'forward'}}, 'switchport_interfaces': {'Gi1/0/3': {'switchport_mode': {'trunk': None}}}, 'private_secondary_vlan': 'none', 'status': 'act/unsup', 'members': None, 'name': 'VLAN0300', 'private_vlan_type': 'primary', 'stp': None, 'type': 'fddi', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100300', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None},
                '270':
                    {'private_secondary_vlan': '500', 'status': 'active', 'members': None, 'name': 'VLAN0270', 'private_vlan_type': 'non-operational', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100270', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None},
                '1':
                    {'switchport_interfaces': {'Gi1/0/3': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}},
                                               'Gi1/0/5': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}},
                                               'Gi2/0/15': {'switchport_mode': {'static access': {'admin_trunking_encapsulation': 'dot1q'}}}},
                     'ip_address': 'unassigned', 'status': 'active', 'members': 'Gi1/0/5, Gi1/0/6, Gi1/0/10, Gi1/0/11, Gi1/0/12, Gi1/0/13, Gi1/0/14, Gi1/0/15, Gi1/0/16, Gi1/0/17, Gi1/0/18, Gi1/0/19, Gi1/0/20, Gi1/0/21, Gi1/0/22, Gi1/0/23, Gi1/0/24, Gi2/0/1, Gi2/0/2, Gi2/0/3, Gi2/0/4, Gi2/0/5, Gi2/0/6, Gi2/0/7, Gi2/0/8, Gi2/0/9, Gi2/0/10, Gi2/0/11, Gi2/0/12, Gi2/0/13, Gi2/0/14, Gi2/0/15, Gi2/0/16, Gi2/0/17, Gi2/0/18, Gi2/0/19, Gi2/0/20, Gi2/0/21, Gi2/0/22, Gi2/0/23, Gi2/0/24, Gi3/0/1, Gi3/0/2, Gi3/0/3, Gi3/0/4, Gi3/0/5, Gi3/0/6, Gi3/0/7, Gi3/0/8, Gi3/0/9, Gi3/0/10, Gi3/0/11, Gi3/0/12, Gi3/0/13, Gi3/0/14, Gi3/0/15, Gi3/0/16, Gi3/0/17, Gi3/0/18, Gi3/0/19, Gi3/0/20, Gi3/0/21, Gi3/0/22, Gi3/0/23, Gi3/0/24, Gi4/0/1, Gi4/0/2, Gi4/0/3, Gi4/0/4, Gi4/0/5, Gi4/0/6, Gi4/0/7, Gi4/0/8, Gi4/0/9, Gi4/0/10, Gi4/0/11, Gi4/0/12, Gi4/0/13, Gi4/0/14, Gi4/0/15, Gi4/0/16, Gi4/0/17, Gi4/0/18, Gi4/0/19, Gi4/0/20, Gi4/0/21, Gi4/0/22, Gi4/0/23, Gi4/0/24, Gi5/0/1, Gi5/0/2, Gi5/0/3, Gi5/0/4, Gi5/0/5, Gi5/0/6, Gi5/0/7, Gi5/0/8, Gi5/0/9, Gi5/0/10, Gi5/0/11, Gi5/0/12, Gi5/0/13, Gi5/0/14, Gi5/0/15, Gi5/0/16, Gi5/0/17, Gi5/0/18, Gi5/0/19, Gi5/0/20, Gi5/0/21, Gi5/0/22, Gi5/0/23, Gi5/0/24', 'name': 'default', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100001', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': '1500'},
                '280':
                    {'status': 'active', 'members': None, 'name': 'VLAN0280', 'stp': None, 'type': 'enet', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '100280', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None},
                '1002':
                    {'status': 'act/unsup', 'members': None, 'name': 'fddi-default', 'stp': None, 'type': 'fddi', 'parent': None, 'Trans1': '0', 'BrdgMode': None, 'said': '101002', 'RingNo': None, 'Trans2': '0', 'mtu': '1500', 'BridgeNo': None, 'vlan_min_mtu': '1500', 'vlan_max_mtu': '1500', 'mtu_mismatch': 'No', 'vlan_mtu': None}}

    # Case when show vlan mtu returns empty output
    # --------------------------------------------
    vlan_all_empty_mtu = {'1': {'BrdgMode': None,
                                'BridgeNo': None,
                                'RingNo': None,
                                'Trans1': '0',
                                'Trans2': '0',
                                'ip_address': 'unassigned',
                                'members': 'Gi1/0/5, Gi1/0/6, Gi1/0/10, Gi1/0/11, Gi1/0/12, '
                                           'Gi1/0/13, Gi1/0/14, Gi1/0/15, Gi1/0/16, Gi1/0/17, '
                                           'Gi1/0/18, Gi1/0/19, Gi1/0/20, Gi1/0/21, Gi1/0/22, '
                                           'Gi1/0/23, Gi1/0/24, Gi2/0/1, Gi2/0/2, Gi2/0/3, Gi2/0/4, '
                                           'Gi2/0/5, Gi2/0/6, Gi2/0/7, Gi2/0/8, Gi2/0/9, Gi2/0/10, '
                                           'Gi2/0/11, Gi2/0/12, Gi2/0/13, Gi2/0/14, Gi2/0/15, '
                                           'Gi2/0/16, Gi2/0/17, Gi2/0/18, Gi2/0/19, Gi2/0/20, '
                                           'Gi2/0/21, Gi2/0/22, Gi2/0/23, Gi2/0/24, Gi3/0/1, '
                                           'Gi3/0/2, Gi3/0/3, Gi3/0/4, Gi3/0/5, Gi3/0/6, Gi3/0/7, '
                                           'Gi3/0/8, Gi3/0/9, Gi3/0/10, Gi3/0/11, Gi3/0/12, '
                                           'Gi3/0/13, Gi3/0/14, Gi3/0/15, Gi3/0/16, Gi3/0/17, '
                                           'Gi3/0/18, Gi3/0/19, Gi3/0/20, Gi3/0/21, Gi3/0/22, '
                                           'Gi3/0/23, Gi3/0/24, Gi4/0/1, Gi4/0/2, Gi4/0/3, Gi4/0/4, '
                                           'Gi4/0/5, Gi4/0/6, Gi4/0/7, Gi4/0/8, Gi4/0/9, Gi4/0/10, '
                                           'Gi4/0/11, Gi4/0/12, Gi4/0/13, Gi4/0/14, Gi4/0/15, '
                                           'Gi4/0/16, Gi4/0/17, Gi4/0/18, Gi4/0/19, Gi4/0/20, '
                                           'Gi4/0/21, Gi4/0/22, Gi4/0/23, Gi4/0/24, Gi5/0/1, '
                                           'Gi5/0/2, Gi5/0/3, Gi5/0/4, Gi5/0/5, Gi5/0/6, Gi5/0/7, '
                                           'Gi5/0/8, Gi5/0/9, Gi5/0/10, Gi5/0/11, Gi5/0/12, '
                                           'Gi5/0/13, Gi5/0/14, Gi5/0/15, Gi5/0/16, Gi5/0/17, '
                                           'Gi5/0/18, Gi5/0/19, Gi5/0/20, Gi5/0/21, Gi5/0/22, '
                                           'Gi5/0/23, Gi5/0/24',
                                'mtu': '1500',
                                'name': 'default',
                                'parent': None,
                                'said': '100001',
                                'status': 'active',
                                'stp': None,
                                'switchport_interfaces': {'Gi1/0/3': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}},
                                                          'Gi1/0/5': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}},
                                                          'Gi2/0/15': {'switchport_mode': {'static access': {'admin_trunking_encapsulation': 'dot1q'}}}},
                                'type': 'enet'},
                          '100': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'access_map_sequence': {'10': {'access_map_action_value': 'forward'},
                                                          '20': {'access_map_action_value': 'forward',
                                                                 'access_map_match_protocol': 'ip',
                                                                 'access_map_match_protocol_value': '2'},
                                                          '30': {'access_map_action_value': 'forward',
                                                                 'access_map_match_protocol': 'ipv6',
                                                                 'access_map_match_protocol_value': 'la'},
                                                          '40': {'access_map_action_value': 'forward',
                                                                 'access_map_match_protocol': 'mac',
                                                                 'access_map_match_protocol_value': 'fa'},
                                                          '50': {'access_map_action_value': 'forward',
                                                                 'access_map_match_protocol': 'ip',
                                                                 'access_map_match_protocol_value': '1301 '
                                                                                                    'feq'},
                                                          '60': {'access_map_action_value': 'drop',
                                                                 'access_map_match_protocol': 'ipv6',
                                                                 'access_map_match_protocol_value': 'laila '
                                                                                                    'suzam'}},
                                  'ip_address': '192.168.234.1',
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0100',
                                  'parent': None,
                                  'remote_span_vlan': True,
                                  'said': '100100',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'},
                          '1002': {'BrdgMode': None,
                                   'BridgeNo': None,
                                   'RingNo': None,
                                   'Trans1': '0',
                                   'Trans2': '0',
                                   'members': None,
                                   'mtu': '1500',
                                   'name': 'fddi-default',
                                   'parent': None,
                                   'said': '101002',
                                   'status': 'act/unsup',
                                   'stp': None,
                                   'type': 'fddi'},
                          '1003': {'BrdgMode': None,
                                   'BridgeNo': None,
                                   'RingNo': None,
                                   'Trans1': '0',
                                   'Trans2': '0',
                                   'members': None,
                                   'mtu': '1500',
                                   'name': 'token-ring-default',
                                   'parent': None,
                                   'said': '101003',
                                   'status': 'act/unsup',
                                   'stp': None,
                                   'type': 'tr'},
                          '1004': {'BrdgMode': None,
                                   'BridgeNo': None,
                                   'RingNo': None,
                                   'Trans1': '0',
                                   'Trans2': '0',
                                   'members': None,
                                   'mtu': '1500',
                                   'name': 'fddinet-default',
                                   'parent': None,
                                   'said': '101004',
                                   'status': 'act/unsup',
                                   'stp': 'ieee',
                                   'type': 'fdnet'},
                          '1005': {'BrdgMode': None,
                                   'BridgeNo': None,
                                   'RingNo': None,
                                   'Trans1': '0',
                                   'Trans2': '0',
                                   'members': None,
                                   'mtu': '1500',
                                   'name': 'trnet-default',
                                   'parent': None,
                                   'said': '101005',
                                   'status': 'act/unsup',
                                   'stp': 'ibm',
                                   'type': 'trnet'},
                          '16': {'switchport_interfaces': {'Gi1/0/1': {'switchport_mode': {'trunk': {'admin_trunking_encapsulation': 'dot1q'}}}}},
                          '200': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'access_map_sequence': {'10': {'access_map_action_value': 'forward'},
                                                          '20': {'access_map_action_value': 'forward'},
                                                          '30': {'access_map_action_value': 'forward'},
                                                          '40': {'access_map_action_value': 'forward'},
                                                          '50': {'access_map_action_value': 'forward'},
                                                          '60': {'access_map_action_value': 'forward'},
                                                          '70': {'access_map_action_value': 'forward'},
                                                          '80': {'access_map_action_value': 'forward'},
                                                          '90': {'access_map_action_value': 'forward'}},
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0200',
                                  'parent': None,
                                  'private_secondary_vlan': 'none',
                                  'private_vlan_type': 'primary',
                                  'said': '100200',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'},
                          '270': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0270',
                                  'parent': None,
                                  'private_secondary_vlan': '500',
                                  'private_vlan_type': 'non-operational',
                                  'said': '100270',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'},
                          '280': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0280',
                                  'parent': None,
                                  'said': '100280',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'},
                          '300': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'access_map_sequence': {'10': {'access_map_action_value': 'forward'},
                                                          '20': {'access_map_action_value': 'forward'},
                                                          '30': {'access_map_action_value': 'forward'},
                                                          '40': {'access_map_action_value': 'forward'},
                                                          '50': {'access_map_action_value': 'forward'},
                                                          '60': {'access_map_action_value': 'forward'},
                                                          '70': {'access_map_action_value': 'forward'},
                                                          '80': {'access_map_action_value': 'forward'},
                                                          '90': {'access_map_action_value': 'forward'}},
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0300',
                                  'parent': None,
                                  'private_secondary_vlan': 'none',
                                  'private_vlan_type': 'primary',
                                  'said': '100300',
                                  'status': 'act/unsup',
                                  'stp': None,
                                  'switchport_interfaces': {'Gi1/0/3': {'switchport_mode': {'trunk': None}}},
                                  'type': 'fddi'},
                          '400': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0400',
                                  'parent': None,
                                  'remote_span_vlan': True,
                                  'said': '100400',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'},
                          '500': {'BrdgMode': None,
                                  'BridgeNo': None,
                                  'RingNo': None,
                                  'Trans1': '0',
                                  'Trans2': '0',
                                  'members': None,
                                  'mtu': '1500',
                                  'name': 'VLAN0500',
                                  'parent': None,
                                  'remote_span_vlan': True,
                                  'said': '100500',
                                  'status': 'active',
                                  'stp': None,
                                  'type': 'enet'}}