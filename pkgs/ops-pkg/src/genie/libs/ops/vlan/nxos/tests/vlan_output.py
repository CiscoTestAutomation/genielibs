'''
 Vlan Genie Ops Object Outputs for NXOS.
'''

class VlanOutput(object):
    # 'show vlan' output
    showVlan = {
        'vlans':{
            '1':{
                'vlan_id': '1',
                'name': 'default',
                'state': 'active',
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/2',
                               'Ethernet1/3', 'Ethernet1/4', 'Ethernet1/5',
                               'Ethernet1/6', 'Ethernet1/7', 'Ethernet1/8',
                               'Ethernet1/9', 'Ethernet1/10', 'Ethernet1/11',
                               'Ethernet1/12', 'Ethernet1/13', 'Ethernet1/14',
                               'Ethernet2/1','Ethernet2/2','Ethernet2/3','Ethernet2/4',
                               'Ethernet2/5','Ethernet2/6'],
                'mode': 'ce',
                'type': 'enet'
                },
            '2': {
                'vlan_id': '2',
                'name': 'VLAN0002',
                'state': 'active',
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/7',
                               'Ethernet1/8','Ethernet1/28'],
                'mode': 'ce',
                'type': 'enet'
                },

            '3': {
                'vlan_id': '3',
                'name': 'VLAN0003',
                'state': 'active',
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/7',
                               'Ethernet1/8', 'Ethernet1/28'],
                'mode': 'ce',
                'type': 'enet'
                },
        },
    }

    showFeature = {
        'feature':{
            'bash-shell':
                 {'instance':
                      {'1':
                           {'state': 'disabled', }}},
            'bgp':
                 {'instance':
                      {'1':
                           {'state': 'enabled', }}},
            'eigrp':
                 {'instance':
                      {'1':
                           {'state': 'enabled', },
                       '2':
                           {'state': 'enabled',
                            'running': 'no', },
                       '3':
                           {'state': 'enabled',
                            'running': 'no', },
                       '4':
                           {'state': 'enabled',
                            'running': 'no', }, }},
            'interface-vlan':{
                 'instance':{
                     '1':{
                          'state': 'enabled',
                        }
                    }
                },
            'vnseg_vlan': {
                 'instance':
                     {'1':
                          {'state': 'enabled', }
                      }
            },
        }
    }

    showVlanIdVnSegment = {
        'vlans': {
            '1': {
                'vlan_id': '1',
                'vn_segment_id': 5010,
            },
            '2': {
                'vlan_id': '2',
                'vn_segment_id': 5020,
            },
        },
    }

    showIgmp = \
        {
            'global_configuration': {
                'enabled': 'enabled',
                'v1v2_report_suppression': 'enabled',
                'v3_report_suppression': 'disabled',
                'link_local_groups_suppression': 'enabled',
                'vpc_multicast_optimization': 'disabled',
            },
            'vlans': {
                '1': {  # configuration_vlan_id
                    'ip_igmp_snooping': 'enabled',
                    'lookup_mode': 'ip',
                    'switch_querier': 'disabled',
                    'igmp_explicit_tracking': 'enabled',
                    'v2_fast_leave': 'disabled',
                    'router_ports_count': 1,
                    'groups_count': 0,
                    'vlan_vpc_function': 'enabled',
                    'active_ports': ['Po20', 'Po30'],
                    'report_flooding': 'disabled',
                    'report_flooding_interfaces': 'n/a',
                    'group_address_for_proxy_leaves': 'no',
                },
                '2': {  # configuration_vlan_id
                    'ip_igmp_snooping': 'enabled',
                    'lookup_mode': 'ip',
                    'igmp_querier': {
                        'address': '10.51.1.1',
                        'version': 2,
                        'interval': 125,
                        'last_member_query_interval': 1,
                        'robustness': 2,
                    },
                    'switch_querier': 'disabled',
                    'igmp_explicit_tracking': 'enabled',
                    'v2_fast_leave': 'disabled',
                    'router_ports_count': 2,
                    'groups_count': 0,
                    'vlan_vpc_function': 'enabled',
                    'active_ports': ['Po20', 'Po30'],
                    'report_flooding': 'disabled',
                    'report_flooding_interfaces': 'n/a',
                    'group_address_for_proxy_leaves': 'no',
                },
                '3': {  # configuration_vlan_id
                    'ip_igmp_snooping': 'enabled',
                    'lookup_mode': 'ip',
                    'switch_querier': 'disabled',
                    'igmp_explicit_tracking': 'enabled',
                    'v2_fast_leave': 'disabled',
                    'router_ports_count': 1,
                    'groups_count': 0,
                    'vlan_vpc_function': 'enabled',
                    'active_ports': ['Po20', 'Po30'],
                    'report_flooding': 'disabled',
                    'report_flooding_interfaces': 'n/a',
                    'group_address_for_proxy_leaves': 'no',
                },
            },
        }
    vlanOpsOutput = \
        {'vlans':{
            'interface_vlan_enabled': True,
            'vn_segment_vlan_based_enabled': True,
            '1':{
                'vlan_id': '1',
                'name': 'default',
                'state': 'active',
                'shutdown': False,
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/2',
                               'Ethernet1/3', 'Ethernet1/4', 'Ethernet1/5',
                               'Ethernet1/6', 'Ethernet1/7', 'Ethernet1/8',
                               'Ethernet1/9', 'Ethernet1/10', 'Ethernet1/11',
                               'Ethernet1/12', 'Ethernet1/13', 'Ethernet1/14',
                               'Ethernet2/1','Ethernet2/2','Ethernet2/3','Ethernet2/4',
                               'Ethernet2/5','Ethernet2/6'],
                'mode': 'ce',
                'vn_segment_id' : 5010,
            },
            '2': {
                'vlan_id': '2',
                'name': 'VLAN0002',
                'state': 'active',
                'shutdown': False,
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/7',
                               'Ethernet1/8','Ethernet1/28'],
                'mode': 'ce',
                'vn_segment_id': 5020,
            },
            '3': {
                'vlan_id': '3',
                'name': 'VLAN0003',
                'state': 'active',
                'shutdown': False,
                'interfaces': ['Port-channel4', 'Port-channel100', 'Ethernet1/7',
                               'Ethernet1/8', 'Ethernet1/28'],
                'mode': 'ce',

            },
            'configuration': {
                '1': {
                    'ip_igmp_snooping': 'enabled'
                },
                '2': {
                    'ip_igmp_snooping': 'enabled'
                },
                '3': {
                    'ip_igmp_snooping': 'enabled'
                },
             }
        },
    }


    showVlanOld = {'vlan_id':
                    {'108':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0108', 'ports': None, 'vlan_type': 'enet'},
                     '105':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0105', 'ports': None, 'vlan_type': 'enet'},
                     '110':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0110', 'ports': None, 'vlan_type': 'enet'},
                     '100':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0100', 'ports': None, 'vlan_type': 'enet'},
                     '101':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0101', 'ports': None, 'vlan_type': 'enet'},
                     '1':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'default', 'ports': 'Eth3/1, Eth3/2, Eth3/3, Eth3/4, Eth3/5, Eth3/6, Eth3/7, Eth3/8, Eth3/9, Eth3/10, Eth3/11, Eth3/12, Eth3/13, Eth3/14, Eth3/15, Eth3/16, Eth3/17, Eth3/18, Eth3/19, Eth3/20, Eth3/21, Eth3/22, Eth3/23, Eth3/24, Eth3/25, Eth3/26, Eth3/27, Eth3/28, Eth3/29, Eth3/30, Eth3/31, Eth3/32, Eth3/33, Eth3/34, Eth3/35, Eth3/36, Eth3/37, Eth3/38, Eth3/39, Eth3/40, Eth3/41, Eth3/42, Eth3/43, Eth3/44, Eth3/45, Eth3/46, Eth3/47, Eth3/48', 'vlan_type': 'enet'},
                     '103':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0103', 'ports': None, 'vlan_type': 'enet'},
                     '102':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0102', 'ports': None, 'vlan_type': 'enet'},
                     '23':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0023', 'ports': 'Eth6/24', 'vlan_type': 'enet'},
                     '109':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0109', 'ports': None, 'vlan_type': 'enet'},
                     '106':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0106', 'ports': None, 'vlan_type': 'enet'},
                     '104':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0104', 'ports': None, 'vlan_type': 'enet'},
                     '107':
                         {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0107', 'ports': None, 'vlan_type': 'enet'}
                     }
                }

    showVlanInternalInfo = {'vlan_id':
                                {'3':
                                     {'vlan_configuration': True},
                                 '8':
                                     {'vlan_configuration': True},
                                 '108':
                                     {'vlan_configuration': True},
                                 '5':
                                     {'vlan_configuration': True}
                                 }
                            }

    showVlanAccessMap = {'access_map_id':
                             {'map_id_tag':
                                  {'access_map_sequence':
                                       {'10':
                                            {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'foo', 'access_map_match_protocol': 'ip'}
                                        }
                                   }
                              }
                         }

    showVlanFilter = {'vlan_id':
                          {'100':
                               {'access_map_tag': 'map_id_tag'}
                           }
                      }

    showIpInterfaceBriefPipeVlan = {'interface':
                                        {'Vlan100':
                                             {'vlan_id':
                                                  {'100':
                                                       {'interface_status': 'protocol-down/link-down/admin-up', 'ip_address': '192.168.234.1'}
                                                   }
                                              },
                                         'Vlan101':
                                             {'vlan_id':
                                                  {'101':
                                                       {'interface_status': 'protocol-down/link-down/admin-up', 'ip_address': '192.168.151.1'}
                                                   }
                                              }
                                         }
                                    }

    # Case without using 'vlan_id' as the structure header
    # ----------------------------------------------------
    # When we call VlanOutput.vlan_all it automatically exclude the dictionary duplicate key's values.
    vlan_all = {
        "interface_vlan": {
            "Vlan100":{
                "vlan_id":{
                    "100": {
                        "ip_address": "192.168.234.1"
                    }
                }
            },
            "Vlan101":{
                "vlan_id":{
                    "101": {
                        "ip_address": "192.168.151.1"
                    }
                }
            }
        },
        '108':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0108', 'members': None, 'vlan_type': 'enet', 'vlan_configuration': True},
        '105':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0105', 'members': None, 'vlan_type': 'enet'},
        '110':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0110', 'members': None, 'vlan_type': 'enet'},
        '100':
            {'access_map_sequence':
                 {'10':
                      {'access_map_action_value': 'forward', 'access_map_match_protocol_value': 'foo', 'access_map_match_protocol': 'ip'}
                  }, 'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0100', 'members': None, 'vlan_type': 'enet'},
        '101':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0101', 'members': None, 'vlan_type': 'enet'},
        '1':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'default', 'members': 'Eth3/1, Eth3/2, Eth3/3, Eth3/4, Eth3/5, Eth3/6, Eth3/7, Eth3/8, Eth3/9, Eth3/10, Eth3/11, Eth3/12, Eth3/13, Eth3/14, Eth3/15, Eth3/16, Eth3/17, Eth3/18, Eth3/19, Eth3/20, Eth3/21, Eth3/22, Eth3/23, Eth3/24, Eth3/25, Eth3/26, Eth3/27, Eth3/28, Eth3/29, Eth3/30, Eth3/31, Eth3/32, Eth3/33, Eth3/34, Eth3/35, Eth3/36, Eth3/37, Eth3/38, Eth3/39, Eth3/40, Eth3/41, Eth3/42, Eth3/43, Eth3/44, Eth3/45, Eth3/46, Eth3/47, Eth3/48', 'vlan_type': 'enet'},
        '103':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0103', 'members': None, 'vlan_type': 'enet'},
        '102':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0102', 'members': None, 'vlan_type': 'enet'},
        '23':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0023', 'members': 'Eth6/24', 'vlan_type': 'enet'},
        '109':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0109', 'members': None, 'vlan_type': 'enet'},
        '106':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0106', 'members': None, 'vlan_type': 'enet'},
        '104':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0104', 'members': None, 'vlan_type': 'enet'},
        '107':
            {'vl_mode': 'CE', 'status': 'active', 'name': 'VLAN0107', 'members': None, 'vlan_type': 'enet'},
        '3':
            {'vlan_configuration': True},
        '8':
            {'vlan_configuration': True},
        '5':
            {'vlan_configuration': True}
    }

    vlan_all_empty_switchport = {'1': {'members': 'Eth3/1, Eth3/2, Eth3/3, Eth3/4, Eth3/5, Eth3/6, Eth3/7, '
                                                  'Eth3/8, Eth3/9, Eth3/10, Eth3/11, Eth3/12, Eth3/13, '
                                                  'Eth3/14, Eth3/15, Eth3/16, Eth3/17, Eth3/18, Eth3/19, '
                                                  'Eth3/20, Eth3/21, Eth3/22, Eth3/23, Eth3/24, Eth3/25, '
                                                  'Eth3/26, Eth3/27, Eth3/28, Eth3/29, Eth3/30, Eth3/31, '
                                                  'Eth3/32, Eth3/33, Eth3/34, Eth3/35, Eth3/36, Eth3/37, '
                                                  'Eth3/38, Eth3/39, Eth3/40, Eth3/41, Eth3/42, Eth3/43, '
                                                  'Eth3/44, Eth3/45, Eth3/46, Eth3/47, Eth3/48',
                                       'name': 'default',
                                       'status': 'active',
                                       'vl_mode': 'CE',
                                       'vlan_type': 'enet'},
                                 '100': {"vl_mode": "CE",
                                         "members": None,
                                         "access_map_sequence": {
                                             "10": {
                                                 "access_map_action_value": "forward",
                                                 "access_map_match_protocol_value": "foo",
                                                 "access_map_match_protocol": "ip"
                                             }
                                         },
                                         "status": "active",
                                         "name": "VLAN0100",
                                         "vlan_type": "enet"},
                                 '101': {'members': None,
                                         'name': 'VLAN0101',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '102': {'members': None,
                                         'name': 'VLAN0102',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '103': {'members': None,
                                         'name': 'VLAN0103',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '104': {'members': None,
                                         'name': 'VLAN0104',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '105': {'members': None,
                                         'name': 'VLAN0105',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '106': {'members': None,
                                         'name': 'VLAN0106',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '107': {'members': None,
                                         'name': 'VLAN0107',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '108': {'members': None,
                                         'name': 'VLAN0108',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_configuration': True,
                                         'vlan_type': 'enet'},
                                 '109': {'members': None,
                                         'name': 'VLAN0109',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '110': {'members': None,
                                         'name': 'VLAN0110',
                                         'status': 'active',
                                         'vl_mode': 'CE',
                                         'vlan_type': 'enet'},
                                 '23': {'members': 'Eth6/24',
                                        'name': 'VLAN0023',
                                        'status': 'active',
                                        'vl_mode': 'CE',
                                        'vlan_type': 'enet'},
                                 '3': {'vlan_configuration': True},
                                 '5': {'vlan_configuration': True},
                                 '8': {'vlan_configuration': True},
                                 "interface_vlan": {
                                     "Vlan100":{
                                         "vlan_id":{
                                             "100": {
                                                 "ip_address": "192.168.234.1"
                                             }
                                         }
                                     },
                                     "Vlan101":{
                                         "vlan_id":{
                                             "101": {
                                                 "ip_address": "192.168.151.1"
                                             }
                                         }
                                     }
                                 }
                                 }
