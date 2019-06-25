'''
 Vxlan Genie Ops Object Outputs for NXOS.
'''

class VxlanOutput(object):
    # 'vxlan' Ops output

    showFeature = {
    'feature':
        {'nve':
             {'instance':
                  {'1':
                       {'state': 'enabled'}}},
         'vnseg_vlan':
             {'instance':
                  {'1':
                       {'state': 'enabled'}}}}}
    showRunningConfigNvOverlay = {
        'evpn_multisite_border_gateway' : 111111
    }
    showNveMultisiteDciLinks = {
        'multisite': {
            'dci_links': {
                'Ethernet1/50': {
                    'if_name': 'Ethernet1/50',
                    'if_state': 'up'
                },
                'Ethernet1/52': {
                    'if_name': 'Ethernet1/52',
                    'if_state': 'up'
                },
            },
        },
    }
    showNveMultisiteFabricLinks = {
        'multisite': {
            'fabric_links':{
                'Ethernet1/53':{
                    'if_name': 'Ethernet1/53',
                    'if_state': 'up'
                },
                'Ethernet1/54': {
                    'if_name': 'Ethernet1/54',
                    'if_state': 'down'
                },
            },
        },
    }
    showNveVni = {
        'nve1': {
            'vni': {
                5001:{
                    'vni': 5001,
                    'mcast': "234.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1001]",
                    'flags':'',
                },
                5002: {
                    'vni': 5002,
                    'mcast': "234.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1002]",
                    'flags': '',
                },
                5003: {
                    'vni': 5003,
                    'mcast': "234.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1003]",
                    'flags': '',
                },
                5004: {
                    'vni': 5004,
                    'mcast': "234.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1004]",
                    'flags': '',
                },
                6004: {
                    'vni': 6004,
                    'mcast': "231.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1014]",
                    'flags': '',
                },
                6005: {
                    'vni': 6005,
                    'mcast': "231.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1015]",
                    'flags': '',
                },
                7001: {
                    'vni': 7001,
                    'mcast': "235.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1103]",
                    'flags': '',
                },
                7002: {
                    'vni': 7002,
                    'mcast': "235.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1104]",
                    'flags': '',
                },
                7003: {
                    'vni': 7003,
                    'mcast': "235.1.1.1",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L2 [1105]",
                    'flags': '',
                },
                10001: {
                    'vni': 10001,
                    'mcast': "n/a",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L3 [vni_10001]",
                    'flags': '',
                },
                10002: {
                    'vni': 10002,
                    'mcast': "n/a",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L3 [vni_10002]",
                    'flags': '',
                },
                10005: {
                    'vni': 10005,
                    'mcast': "n/a",
                    'vni_state': "up",
                    'mode': "CP",
                    'type': "L3 [vni_10005]",
                    'flags': '',
                },
            },
        },
     }
    showNveEthernetSegment = {
        'nve': {
            'nve1': {
                'ethernet_segment': {
                    'esi': {
                        '0300.0000.0001.2c00.0309': {
                            'esi': '0300.0000.0001.2c00.0309',
                            'if_name': 'nve1',
                            'es_state': 'up',
                            'po_state': 'n/a',
                            'nve_if_name': 'nve1',
                            'nve_state': 'up',
                            'host_reach_mode': 'control-plane',
                            'active_vlans': '1,101-105,1001-1100,2001-2100,3001-3005',
                            'df_vlans': '102,104,1002,1004,1006,1008,1010,1012,1014,1016,1018,1020,1022,1024' \
                                        ',1026,1028,1030,1032,1034,1036,1038,1040,1042,1044,1046,1048,1050,1052,1054,1056' \
                                        ',1058,1060,1062,1064,1066,1068,1070,1072,1074,1076,1078,1080,1082,1084,1086,1088' \
                                        ',1090,1092,1094,1096,1098,1100,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020' \
                                        ',2022,2024,2026,2028,2030,2032,2034,2036,2038,2040,2042,2044,2046,2048,2050,2052' \
                                        ',2054,2056,2058,2060,2062,2064,2066,2068,2070,2072,2074,2076,2078,2080,2082,2084' \
                                        ',2086,2088,2090,2092,2094,2096,2098,2100,3002,3004',
                            'active_vnis': '501001-501100,502001-502100,503001-503005,600101-600105',
                            'cc_failed_vlans': '',
                            'cc_timer_left': '0',
                            'num_es_mem': 2,
                            'local_ordinal': 0,
                            'df_timer_st': '00:00:00',
                            'config_status': 'n/a',
                            'df_list': '192.168.111.55 192.168.111.66',
                            'es_rt_added': True,
                            'ead_rt_added': False,
                            'ead_evi_rt_timer_age': 'not running',
                        },
                    },
                },
            },
        },
    }
    showNvePeers = {
        'nve1':{
            'peer_ip': {
                '192.168.16.1':{
                    'peer_state': 'up',
                    'learn_type': 'CP',
                    'uptime': '01:15:09',
                    'router_mac': 'n/a',
                },
                '192.168.106.1': {
                    'peer_state': 'up',
                    'learn_type': 'CP',
                    'uptime': '00:03:05',
                    'router_mac': '5e00.0002.0007',
                }
            },
        },}
    showNveInterfaceDetail = {
        'nve1': {
            'nve_name': 'nve1',
            'if_state': "down",
            'encap_type': "vxlan",
            'vpc_capability': "vpc-vip-only [notified]",
            'local_rmac': "6cb2.ae24.3f17",
            'host_reach_mode': "control-plane",
            'source_if': "loopback1",
            'primary_ip': "192.168.111.11",
            'secondary_ip': "192.168.196.22",
            'src_if_state': "up",
            'ir_cap_mode': "no",
            'adv_vmac': True,
            'nve_flags': "",
            'nve_if_handle': 1224736769,
            'src_if_holddown_tm': 180,
            'src_if_holdup_tm': 30,
            'src_if_holddown_left': 0,
            'vip_rmac': "0200.c90c.0b16",
            'vip_rmac_ro': "0200.6565.6565",
            'sm_state': "nve-intf-init",
            'multisite_bgw_if': "loopback2",
            'multisite_bgw_if_ip': '10.4.101.101',
            'multisite_bgw_if_admin_state': "down",
            'multisite_bgw_if_oper_state': "down",
            'multisite_bgw_if_oper_state_down_reason': "NVE not up."

        }, }
    showNveVniSummary = {
        'vni': {
            'summary': {
                'cp_vni_count': 21,
                'cp_vni_up': 21,
                'cp_vni_down': 0,
                'dp_vni_count': 0,
                'dp_vni_up': 0,
                'dp_vni_down': 0,
            },
        },
    }
    showNveVniIngressReplication = {
        'nve1': {
            'vni': {
                10001: {
                    'vni': 10001,
                    'repl_ip': {
                        "10.196.7.7": {
                        'repl_ip': "10.196.7.7",
                        'up_time': "1d02h",
                        'source': "bgp-imet",
                        }
                    },
                },
                10002: {
                    'vni': 10002,
                    'repl_ip': {
                        "10.196.7.7": {
                        'repl_ip': "10.196.7.7",
                        'up_time': "1d02h",
                        'source': "bgp-imet",
                        }
                    },
                },
                10005: {
                    'vni': 10005,
                    'repl_ip': {
                        "10.196.7.7": {
                        'repl_ip': "10.196.7.7",
                        'up_time': "1d02h",
                        'source': "bgp-imet",
                        }
                    },
                },
            },
        },
    } 

    #################################################
    #  Vxlan vni
    #################################################
    vxlanVniOpsOutput = {
        'enabled_nv_overlay': True,
        'enabled_vn_segment_vlan_based': True,
        'enabled_nv_overlay_evpn': True,
        'evpn_multisite_border_gateway': 111111,
        'vni': {
            'summary': {
                'cp_vni_count': 21,
                'cp_vni_up': 21,
                'cp_vni_down': 0,
                'dp_vni_count': 0,
                'dp_vni_up': 0,
                'dp_vni_down': 0,
            },
        },
        'nve1': {
            'nve_name': 'nve1',
            'if_state': "down",
            'encap_type': "vxlan",
            'vpc_capability': "vpc-vip-only [notified]",
            'local_rmac': "6cb2.ae24.3f17",
            'host_reach_mode': "control-plane",
            'source_if': "Loopback1",
            'primary_ip': "192.168.111.11",
            'secondary_ip': "192.168.196.22",
            'src_if_state': "up",
            'ir_cap_mode': "no",
            'adv_vmac': True,
            'nve_flags': "",
            'nve_if_handle': 1224736769,
            'src_if_holddown_tm': 180,
            'src_if_holdup_tm': 30,
            'src_if_holddown_left': 0,
            'vip_rmac': "0200.c90c.0b16",
            'vip_rmac_ro': "0200.6565.6565",
            'sm_state': "nve-intf-init",
            'multisite_bgw_if': "Loopback2",
            'multisite_bgw_if_ip': '10.4.101.101',
            'multisite_bgw_if_admin_state': "down",
            'multisite_bgw_if_oper_state': "down",
            'multisite_bgw_if_oper_state_down_reason': "NVE not up.",
            'peer_ip': {
                '192.168.16.1': {
                  'peer_state': 'up',
                  'learn_type': 'CP',
                  'uptime': '01:15:09',
                  'router_mac': 'n/a',
                },
                '192.168.106.1': {
                  'peer_state': 'up',
                  'learn_type': 'CP',
                  'uptime': '00:03:05',
                  'router_mac': '5e00.0002.0007',
                },
            },
            'ethernet_segment': {
                'esi': {
                    '0300.0000.0001.2c00.0309': {
                       'esi': '0300.0000.0001.2c00.0309',
                       'if_name': 'nve1',
                       'es_state': 'up',
                       'po_state': 'n/a',
                       'nve_if_name': 'nve1',
                       'nve_state': 'up',
                       'host_reach_mode': 'control-plane',
                       'active_vlans': '1,101-105,1001-1100,2001-2100,3001-3005',
                       'df_vlans': '102,104,1002,1004,1006,1008,1010,1012,1014,1016,1018,1020,1022,1024' \
                                   ',1026,1028,1030,1032,1034,1036,1038,1040,1042,1044,1046,1048,1050,1052,1054,1056' \
                                   ',1058,1060,1062,1064,1066,1068,1070,1072,1074,1076,1078,1080,1082,1084,1086,1088' \
                                   ',1090,1092,1094,1096,1098,1100,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020' \
                                   ',2022,2024,2026,2028,2030,2032,2034,2036,2038,2040,2042,2044,2046,2048,2050,2052' \
                                   ',2054,2056,2058,2060,2062,2064,2066,2068,2070,2072,2074,2076,2078,2080,2082,2084' \
                                   ',2086,2088,2090,2092,2094,2096,2098,2100,3002,3004',
                       'active_vnis': '501001-501100,502001-502100,503001-503005,600101-600105',
                       'cc_failed_vlans': '',
                       'cc_timer_left': '0',
                       'num_es_mem': 2,
                       'local_ordinal': 0,
                       'df_timer_st': '00:00:00',
                       'config_status': 'n/a',
                       'df_list': '192.168.111.55 192.168.111.66',
                       'es_rt_added': True,
                       'ead_rt_added': False,
                       'ead_evi_rt_timer_age': 'not running',
                    },
                },
            },
            'vni': {
               5001: {
                   'vni': 5001,
                   'mcast': "234.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1001]",
                   'flags': '',
               },
               5002: {
                   'vni': 5002,
                   'mcast': "234.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1002]",
                   'flags': '',
               },
               5003: {
                   'vni': 5003,
                   'mcast': "234.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1003]",
                   'flags': '',
               },
               5004: {
                   'vni': 5004,
                   'mcast': "234.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1004]",
                   'flags': '',
               },
               6004: {
                   'vni': 6004,
                   'mcast': "231.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1014]",
                   'flags': '',
               },
               6005: {
                   'vni': 6005,
                   'mcast': "231.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1015]",
                   'flags': '',
               },
               7001: {
                   'vni': 7001,
                   'mcast': "235.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1103]",
                   'flags': '',
               },
               7002: {
                   'vni': 7002,
                   'mcast': "235.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1104]",
                   'flags': '',
               },
               7003: {
                   'vni': 7003,
                   'mcast': "235.1.1.1",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L2 [1105]",
                   'flags': '',
               },
               10001: {
                   'vni': 10001,
                   'mcast': "n/a",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L3 [vni_10001]",
                   'flags': '',
                   'repl_ip': {
                       "10.196.7.7": {
                           'repl_ip': "10.196.7.7",
                           'up_time': "1d02h",
                           'source': "bgp-imet",
                       }
                   },
               },
               10002: {
                   'vni': 10002,
                   'mcast': "n/a",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L3 [vni_10002]",
                   'flags': '',
                   'repl_ip': {
                       "10.196.7.7": {
                           'repl_ip': "10.196.7.7",
                           'up_time': "1d02h",
                           'source': "bgp-imet",
                       }
                   },
               },
               10005: {
                   'vni': 10005,
                   'mcast': "n/a",
                   'vni_state': "up",
                   'mode': "CP",
                   'type': "L3 [vni_10005]",
                   'flags': '',
                   'repl_ip': {
                       "10.196.7.7": {
                           'repl_ip': "10.196.7.7",
                           'up_time': "1d02h",
                           'source': "bgp-imet",
                       }
                   },
               },
           },
        },
        'multisite': {
            'dci_links': {
                'Ethernet1/50': {
                    'if_name': 'Ethernet1/50',
                    'if_state': 'up'
                },
                'Ethernet1/52': {
                    'if_name': 'Ethernet1/52',
                    'if_state': 'up'
                },
            },
            'fabric_links': {
                'Ethernet1/53': {
                    'if_name': 'Ethernet1/53',
                    'if_state': 'up'
                },
                'Ethernet1/54': {
                    'if_name': 'Ethernet1/54',
                    'if_state': 'down'
                },
            },
        },
    }


    ########################################################
    #  vxlan l2route
    #######################################################
    showL2routeFlAll = {
        'topology': {
            'topo_id': {
                101: {
                    'num_of_peer_id': 3,
                    'peer_id': {
                        8: {
                            'topo_id': 101,
                            'peer_id': 8,
                            'flood_list': '192.168.169.44',
                            'is_service_node': 'no',
                        },
                        2: {
                            'topo_id': 101,
                            'peer_id': 2,
                            'flood_list': '192.168.111.55',
                            'is_service_node': 'no',
                        },
                        1: {
                            'topo_id': 101,
                            'peer_id': 1,
                            'flood_list': '192.168.111.66',
                            'is_service_node': 'no',
                        },
                    },
                },
            }
        }
    }
    showL2routeEvpnEternetSegmentAll = {
        'evpn': {
            'ethernet_segment': {
                1: {
                    'ethernet_segment': '0300.0000.0001.2c00.0309',
                    'originating_rtr': '192.168.111.55',
                    'prod_name': 'vxlan',
                    'int_ifhdl': 'nve1',
                    'client_nfn': 64,
                },
                2: {
                    'ethernet_segment': '0300.0000.0001.2c00.0309',
                    'originating_rtr': '192.168.111.66',
                    'prod_name': 'bgp',
                    'int_ifhdl': 'n/a',
                    'client_nfn': 32,
                },
            },
        },
    }
    showL2routeTopologyDetail = {
        'topology': {
            'topo_id': {
                101: {
                    'topo_name': {
                        'Vxlan-10001': {
                            'topo_name': 'Vxlan-10001',
                            'topo_type': 'vni',
                            'vni': 10001,
                            'encap_type': 0,
                            'iod': 0,
                            'if_hdl': 1224736769,
                            'vtep_ip': '192.168.4.11',
                            'emulated_ip': '192.168.196.22',
                            'emulated_ro_ip': '192.168.196.22',
                            'tx_id': 20,
                            'rcvd_flag': 0,
                            'rmac': '5e00.0005.0007',
                            'vrf_id': 3,
                            'vmac': '0200.c90c.0b16',
                            'flags': 'L3cp',
                            'sub_flags': '--',
                            'prev_flags': '-',
                        },
                    },
                },
            },
        },
    }

    showL2routeMacAllDetail = {
        'topology': {
            'topo_id': {
                101: {
                    'mac': {
                        '5e00.0002.0007': {
                            'mac_addr': '5e00.0002.0007',
                            'prod_type': 'vxlan',
                            'flags': 'rmac',
                            'seq_num': 0,
                            'next_hop1': '192.168.106.1',
                            'rte_res': 'regular',
                            'fwd_state': 'Resolved',
                            'peer_id': 2,
                        },
                    },
                },
            }
        }
    }
    showL2routeMacIpAllDetail = {
        'topology': {
            'topo_id': {
                101: {
                    'mac_ip': {
                        'fa16.3ec2.34fe': {
                            'mac_addr': 'fa16.3ec2.34fe',
                            'mac_ip_prod_type': 'bgp',
                            'mac_ip_flags': '--',
                            'seq_num': 0,
                            'next_hop1': '192.168.106.1',
                            'host_ip': '10.36.10.11',
                        },
                        'fa16.3ea3.fb66': {
                            'mac_addr': 'fa16.3ea3.fb66',
                            'mac_ip_prod_type': 'hmm',
                            'mac_ip_flags': '--',
                            'seq_num': 0,
                            'next_hop1': 'local',
                            'host_ip': '10.36.10.55',
                            'sent_to': 'bgp',
                            'soo': 774975538,
                            'l3_info': 10001,
                        },
                    },
                },
            }
        }
    }
    showL2routeSummary = {
        'summary': {
            'total_memory': 6967,
            'numof_converged_tables': 47,
            'table_name': {
                'Topology': {
                    'producer_name': {
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 21,
                            'memory': 5927,
                        },
                        'total_obj': 21,
                        'total_mem': 5927,
                    },
                },
                'MAC': {
                    'producer_name': {
                        'local': {
                            'producer_name': 'local',
                            'id': 3,
                            'objects': 1,
                            'memory': 152,
                        },
                        'bgp': {
                            'producer_name': 'bgp',
                            'id': 5,
                            'objects': 1,
                            'memory': 152,
                        },
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 1,
                            'memory': 152,
                        },
                        'total_obj': 3,
                        'total_mem': 456,
                    }
                },
                'PEERID': {
                    'producer_name': {
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 2,
                            'memory': 312,
                        },
                        'total_obj': 2,
                        'total_mem': 312,
                    }
                },
                'MAC-IP': {
                    'producer_name': {
                        'bgp': {
                            'producer_name': 'bgp',
                            'id': 5,
                            'objects': 1,
                            'memory': 136,
                        },
                        'hmm': {
                            'producer_name': 'hmm',
                            'id': 12,
                            'objects': 1,
                            'memory': 136,
                        },
                        'total_obj': 2,
                        'total_mem': 272,
                    }
                },
            }
        }
    }

    vxlanL2routeOpsOutput={
        'evpn': {
            'ethernet_segment': {
                1: {
                    'ethernet_segment': '0300.0000.0001.2c00.0309',
                    'originating_rtr': '192.168.111.55',
                    'prod_name': 'vxlan',
                    'int_ifhdl': 'nve1',
                    'client_nfn': 64,
                },
                2: {
                    'ethernet_segment': '0300.0000.0001.2c00.0309',
                    'originating_rtr': '192.168.111.66',
                    'prod_name': 'bgp',
                    'int_ifhdl': 'n/a',
                    'client_nfn': 32,
                },
            },
        },
        'topology': {
            'topo_id': {
                101: {
                    'num_of_peer_id': 3,
                    'peer_id': {
                        8: {
                            'topo_id': 101,
                            'peer_id': 8,
                            'flood_list': '192.168.169.44',
                            'is_service_node': 'no',
                        },
                        2: {
                            'topo_id': 101,
                            'peer_id': 2,
                            'flood_list': '192.168.111.55',
                            'is_service_node': 'no',
                        },
                        1: {
                            'topo_id': 101,
                            'peer_id': 1,
                            'flood_list': '192.168.111.66',
                            'is_service_node': 'no',
                        },
                    },
                    'topo_name': {
                        'Vxlan-10001': {
                            'topo_name': 'Vxlan-10001',
                            'topo_type': 'vni',
                            'vni': 10001,
                            'encap_type': 0,
                            'iod': 0,
                            'if_hdl': 1224736769,
                            'vtep_ip': '192.168.4.11',
                            'emulated_ip': '192.168.196.22',
                            'emulated_ro_ip': '192.168.196.22',
                            'tx_id': 20,
                            'rcvd_flag': 0,
                            'rmac': '5e00.0005.0007',
                            'vrf_id': 3,
                            'vmac': '0200.c90c.0b16',
                            'flags': 'L3cp',
                            'sub_flags': '--',
                            'prev_flags': '-',
                        },
                    },
                    'mac': {
                        '5e00.0002.0007': {
                            'mac_addr': '5e00.0002.0007',
                            'prod_type': 'vxlan',
                            'flags': 'rmac',
                            'seq_num': 0,
                            'next_hop1': '192.168.106.1',
                            'rte_res': 'regular',
                            'fwd_state': 'Resolved',
                            'peer_id': 2,
                        },
                    },
                    'mac_ip': {
                        'fa16.3ec2.34fe': {
                            'mac_addr': 'fa16.3ec2.34fe',
                            'mac_ip_prod_type': 'bgp',
                            'mac_ip_flags': '--',
                            'seq_num': 0,
                            'next_hop1': '192.168.106.1',
                            'host_ip': '10.36.10.11',
                        },
                        'fa16.3ea3.fb66': {
                            'mac_addr': 'fa16.3ea3.fb66',
                            'mac_ip_prod_type': 'hmm',
                            'mac_ip_flags': '--',
                            'seq_num': 0,
                            'next_hop1': 'local',
                            'host_ip': '10.36.10.55',
                            'sent_to': 'bgp',
                            'soo': 774975538,
                            'l3_info': 10001,
                        },
                    },
                },
            },
        },
        'summary': {
            'total_memory': 6967,
            'numof_converged_tables': 47,
            'table_name': {
                'Topology': {
                    'producer_name': {
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 21,
                            'memory': 5927,
                        },
                        'total_obj': 21,
                        'total_mem': 5927,
                    },
                },
                'MAC': {
                    'producer_name': {
                        'local': {
                            'producer_name': 'local',
                            'id': 3,
                            'objects': 1,
                            'memory': 152,
                        },
                        'bgp': {
                            'producer_name': 'bgp',
                            'id': 5,
                            'objects': 1,
                            'memory': 152,
                        },
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 1,
                            'memory': 152,
                        },
                        'total_obj': 3,
                        'total_mem': 456,
                    }
                },
                'PEERID': {
                    'producer_name': {
                        'vxlan': {
                            'producer_name': 'vxlan',
                            'id': 11,
                            'objects': 2,
                            'memory': 312,
                        },
                        'total_obj': 2,
                        'total_mem': 312,
                    }
                },
                'MAC-IP': {
                    'producer_name': {
                        'bgp': {
                            'producer_name': 'bgp',
                            'id': 5,
                            'objects': 1,
                            'memory': 136,
                        },
                        'hmm': {
                            'producer_name': 'hmm',
                            'id': 12,
                            'objects': 1,
                            'memory': 136,
                        },
                        'total_obj': 2,
                        'total_mem': 272,
                    }
                },
            }
        }
    }

    ##############################################################
    #        vxlan l2vpn evpn
    ###############################################################
    showBgpL2vpnEvpnSummary = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'vrf_router_id': '192.168.4.11',
                        'vrf_local_as': 100,
                        'address_family': {
                            'l2vpn evpn': {
                                'tableversion': 155,
                                'configuredpeers': 2,
                                'capablepeers': 2,
                                'totalnetworks': 32,
                                'totalpaths': 32,
                                'memoryused': 5708,
                                'numberattrs': 20,
                                'bytesattrs': 3200,
                                'numberpaths': 0,
                                'bytespaths': 0,
                                'numbercommunities': 1,
                                'bytescommunities': 32,
                                'numberclusterlist': 3,
                                'bytesclusterlist': 12,
                                'dampening': 'disabled',
                                'neighbor': {
                                    '172.16.205.8': {
                                        'neighbor': '172.16.205.8',
                                        'version': 4,
                                        'msgrecvd': 130,
                                        'msgsent': 139,
                                        'neighbortableversion': 155,
                                        'inq': 0,
                                        'outq': 0,
                                        'remoteas': 200,
                                        'time': '02:05:01',
                                        'state': 'established',
                                        'prefixreceived': 0,
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    showBgpL2vpnEvpnNeighbors = {
        'instance': {
            'default': {
                'vrf': {
                    'default': { 
                        'address_family': {
                            'l2vpn evpn': { 
                                'neighbor': {
                                    '172.16.205.8': {
                                        'neighbor': '172.16.205.8',
                                        'remoteas': 200,
                                        'link': 'ebgp',
                                        'index': 3,
                                        'version': 4,
                                        'remote_id':'192.168.144.33',
                                        'state': 'established',
                                        'up': True,
                                        'elapsedtime': '02:11:53',
                                        'connectedif': 'ethernet1/6',
                                        'bfd': True,
                                        'lastread': '00:00:51',
                                        'holdtime': 180,
                                        'keepalivetime': 60,
                                        'lastwrite': '00:00:21',
                                        'keepalive': '00:00:38',
                                        'msgrecvd': 137,
                                        'notificationsrcvd': 0,
                                        'recvbufbytes': 0,
                                        'msgsent': 146,
                                        'notificationssent': 0,
                                        'sentbytesoutstanding': 0,
                                        'totalbytessent':0,
                                        'connsestablished': 1,
                                        'connsdropped': 0,
                                        'resettime': 'never',
                                        'resetreason': 'no error',
                                        'peerresettime': 'never',
                                        'peerresetreason': 'no error',
                                        'capmpadvertised': True,
                                        'caprefreshadvertised': True,
                                        'capgrdynamicadvertised': True,
                                        'capmprecvd': True,
                                        'caprefreshrecvd': True,
                                        'capgrdynamicrecvd': True,
                                        'capolddynamicadvertised': True,
                                        'capolddynamicrecvd': True,
                                        'caprradvertised': True,
                                        'caprrrecvd': True,
                                        'capoldrradvertised': True,
                                        'capoldrrrecvd': True,
                                        'capas4advertised': True,
                                        'capas4recvd': True,
                                        'af': {
                                            'l2vpn evpn': { 
                                                'af_advertised': True,
                                                'af_recvd': True,
                                                'af_name': 'l2vpn evpn', 
                                            }
                                        },
                                        'capgradvertised': True,
                                        'capgrrecvd': True,
                                        'graf': {
                                            'l2vpn evpn': { 
                                                'gr_af_name': 'l2vpn evpn', 
                                                'gr_adv': True,
                                                'gr_recv': True,
                                                'gr_fwd': True,
                                            }
                                        },
                                        'grrestarttime': 120,
                                        'grstaletiem': 300,
                                        'grrecvdrestarttime': 120,
                                        'capextendednhadvertised': True,
                                        'capextendednhrecvd': True,
                                        'capextendednhaf': {
                                            'ipv4 unicast': {
                                                'capextendednh_af_name': 'ipv4 unicast',
                                            },
                                        },
                                        'openssent': 1,
                                        'opensrecvd':1,
                                        'updatessent': 70,
                                        'updatesrecvd': 1,
                                        'keepalivesent': 129,
                                        'keepaliverecvd': 133,
                                        'rtrefreshsent': 0,
                                        'rtrefreshrecvd': 0,
                                        'capabilitiessent': 2,
                                        'capabilitiesrecvd': 2,
                                        'bytessent': 10398,
                                        'bytesrecvd': 2595,
                                        'peraf': {
                                            'l2vpn evpn': { 
                                                'per_af_name': 'l2vpn evpn', 
                                                'tableversion': 191,
                                                'neighbortableversion': 191,
                                                'pfxrecvd': 0,
                                                'pfxbytes': 0,
                                                'sendcommunity': True,
                                                'sendextcommunity': True,
                                                }
                                        },
                                        'localaddr': '172.16.205.6',
                                        'localport': 179,
                                        'remoteaddr': '172.16.205.8',
                                        'remoteport': 52715,
                                        'fd': 84,
                                    },
                                },
                            },
                        }
                    }
                }
            }
        }
     }

    showBgpL2vpnEvpnRouteType_4 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'l2vpn evpn': {
                                'rd': {
                                    '10.121.0.55:27001': {
                                        'rd': '10.121.0.55:27001',
                                        'prefix': {
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.55]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.55]/136',
                                                'prefixversion': 13144,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.55',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.121.0.55',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'advertisedto': ['10.121.0.11', '10.121.0.22', '10.121.0.33',
                                                                         '10.121.0.44', '10.196.0.11'],
                                                    },
                                                }
                                            },
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136',
                                                'prefixversion': 13146,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.66',
                                                        'nexthopmetric': 3,
                                                        'neighbor': '10.196.0.11',
                                                        'neighborid': '10.196.0.11',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'originatorid': '10.121.0.66',
                                                        'clusterlist': ['10.196.0.11'],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                    '10.121.0.66:27001': {
                                        'rd': '10.121.0.66:27001',
                                        'prefix': {
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136',
                                                'prefixversion': 13145,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.66',
                                                        'nexthopmetric': 3,
                                                        'neighbor': '10.196.0.11',
                                                        'neighborid': '10.196.0.11',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'advertisedto': ['10.121.0.11', '10.121.0.22', '10.121.0.33',
                                                                         '10.121.0.44'],
                                                        'originatorid': '10.121.0.66',
                                                        'clusterlist': ['10.196.0.11'],
                                                    },
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    showBgpL2vpnEvpnRouteType_1 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'l2vpn evpn': {
                                'rd': {
                                    '192.168.9.1:33767': {
                                        'rd': '192.168.9.1:33767',
                                        'rd_vrf': 'l2',
                                        'rd_vniid': 25000,
                                        'prefix': {
                                            '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152',
                                                'prefixversion': 4904,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            },
                                            '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152',
                                                'prefixversion': 4074,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            },
                                            '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152',
                                                'prefixversion': 4487,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                    '192.168.9.1:33768': {
                                        'rd': '192.168.9.1:33768',
                                        'rd_vrf': 'l2',
                                        'rd_vniid': 25001,
                                        'prefix': {
                                            '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152',
                                                'prefixversion': 4905,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            },
                                            '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152',
                                                'prefixversion': 4075,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            },
                                            '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152',
                                                'prefixversion': 4488,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    showBgpL2vpnEvpnRouteType_2 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'l2vpn evpn': {
                                'rd': {
                                    '192.168.154.1:3': {
                                        'rd': '192.168.154.1:3',
                                        'prefix': {
                                            '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216': {
                                                'nonipprefix': '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216',
                                                'prefixversion': 116,
                                                'on_xmitlist': True,
                                                'mpath': 'ibgp',
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': False,
                                                        'ipnexthop': '192.168.16.1',
                                                        'nexthopmetric': 81,
                                                        'neighbor': '192.168.234.1',
                                                        'neighborid': '192.168.234.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        "extcommunity": [
                                                            "RT:100:10001",
                                                            "ENCAP:8"
                                                        ],
                                                        'inlabel': 10001,
                                                        'originatorid': '192.168.154.1',
                                                        'clusterlist': ['192.168.234.1'],
                                                        'advertisedto': ['172.16.205.8'],
                                                    },
                                                }
                                            },
                                        },
                                    },
                                    '192.168.154.1:4': {
                                        'rd': '192.168.154.1:4',
                                        'prefix': {
                                            '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216': {
                                                'nonipprefix': '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216',
                                                'prefixversion': 117,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'mpath': 'ibgp',
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': False,
                                                        'ipnexthop': '192.168.16.1',
                                                        'nexthopmetric': 81,
                                                        'neighbor': '192.168.234.1',
                                                        'neighborid': '192.168.234.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'inlabel': 10002,
                                                        'advertisedto': ['172.16.205.8'],
                                                        'originatorid': '192.168.154.1',
                                                        'clusterlist': ['192.168.234.1'],
                                                    },
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    showBgpL2vpnEvpnRouteType_3 = {
        "instance": {
            "default": {
                "vrf": {
                    "default": {
                        "address_family": {
                            "l2vpn evpn": {
                                "rd": {
                                    "10.196.7.7:32969": {
                                        "rd": "10.196.7.7:32969",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5387,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32968": {
                                        "rd": "10.196.7.7:32968",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5386,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32868": {
                                        "rd": "10.196.7.7:32868",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5384,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32868": {
                                        "rd": "10.144.6.6:32868",
                                        "rd_vniid": 10101,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5809,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5759,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32969": {
                                        "rd": "10.144.6.6:32969",
                                        "rd_vniid": 10202,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5813,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5761,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32968": {
                                        "rd": "10.144.6.6:32968",
                                        "rd_vniid": 10201,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5811,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5760,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32869": {
                                        "rd": "10.196.7.7:32869",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10102",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10102",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5385,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    vxlanBgpL2vpnEvpnOpsOutput = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'vrf_router_id': '192.168.4.11',
                        'vrf_local_as': 100,
                        'address_family': {
                            'l2vpn evpn': {
                                'tableversion': 155,
                                'configuredpeers': 2,
                                'capablepeers': 2,
                                'totalnetworks': 32,
                                'totalpaths': 32,
                                'memoryused': 5708,
                                'numberattrs': 20,
                                'bytesattrs': 3200,
                                'numberpaths': 0,
                                'bytespaths': 0,
                                'numbercommunities': 1,
                                'bytescommunities': 32,
                                'numberclusterlist': 3,
                                'bytesclusterlist': 12,
                                'dampening': 'disabled',
                                'neighbor': {
                                    '172.16.205.8': {
                                        'neighbor': '172.16.205.8',
                                        'version': 4,
                                        'msgrecvd': 130,
                                        'msgsent': 139,
                                        'neighbortableversion': 155,
                                        'inq': 0,
                                        'outq': 0,
                                        'remoteas': 200,
                                        'state': 'established',
                                        'prefixreceived': 0,
                                        'elapsedtime': '02:11:53',
                                        'link': 'ebgp',
                                        'index': 3,
                                        'remote_id': '192.168.144.33',
                                        'up': True,
                                        'connectedif': 'ethernet1/6',
                                        'bfd': True,
                                        'lastread': '00:00:51',
                                        'holdtime': 180,
                                        'keepalivetime': 60,
                                        'lastwrite': '00:00:21',
                                        'keepalive': '00:00:38',
                                        'notificationsrcvd': 0,
                                        'recvbufbytes': 0,
                                        'notificationssent': 0,
                                        'sentbytesoutstanding': 0,
                                        'connsestablished': 1,
                                        'connsdropped': 0,
                                        'resettime': 'never',
                                        'resetreason': 'no error',
                                        'peerresettime': 'never',
                                        'peerresetreason': 'no error',
                                        'capmpadvertised': True,
                                        'caprefreshadvertised': True,
                                        'capgrdynamicadvertised': True,
                                        'capmprecvd': True,
                                        'caprefreshrecvd': True,
                                        'capgrdynamicrecvd': True,
                                        'capolddynamicadvertised': True,
                                        'capolddynamicrecvd': True,
                                        'caprradvertised': True,
                                        'caprrrecvd': True,
                                        'capoldrradvertised': True,
                                        'capoldrrrecvd': True,
                                        'capas4advertised': True,
                                        'capas4recvd': True,
                                        'af': {
                                            'l2vpn evpn': {
                                                'af_advertised': True,
                                                'af_recvd': True,
                                                'af_name': 'l2vpn evpn',
                                            }
                                        },
                                        'capgradvertised': True,
                                        'capgrrecvd': True,
                                        'graf': {
                                            'l2vpn evpn': {
                                                'gr_af_name': 'l2vpn evpn',
                                                'gr_adv': True,
                                                'gr_recv': True,
                                                'gr_fwd': True,
                                            }
                                        },
                                        'grrestarttime': 120,
                                        'grstaletiem': 300,
                                        'grrecvdrestarttime': 120,
                                        'capextendednhadvertised': True,
                                        'capextendednhrecvd': True,
                                        'capextendednhaf': {
                                            'ipv4 unicast': {
                                                'capextendednh_af_name': 'ipv4 unicast',
                                            },
                                        },
                                        'openssent': 1,
                                        'opensrecvd': 1,
                                        'updatessent': 70,
                                        'updatesrecvd': 1,
                                        'keepalivesent': 129,
                                        'keepaliverecvd': 133,
                                        'rtrefreshsent': 0,
                                        'rtrefreshrecvd': 0,
                                        'capabilitiessent': 2,
                                        'capabilitiesrecvd': 2,
                                        'bytessent': 10398,
                                        'bytesrecvd': 2595,
                                        'peraf': {
                                            'l2vpn evpn': {
                                                'per_af_name': 'l2vpn evpn',
                                                'tableversion': 191,
                                                'neighbortableversion': 191,
                                                'pfxrecvd': 0,
                                                'pfxbytes': 0,
                                                'sendcommunity': True,
                                                'sendextcommunity': True,
                                            }
                                        },
                                        'localaddr': '172.16.205.6',
                                        'localport': 179,
                                        'remoteaddr': '172.16.205.8',
                                        'remoteport': 52715,
                                        'fd': 84,
                                   },
                                },
                                'rd': {
                                    '192.168.9.1:33767': {
                                        'rd': '192.168.9.1:33767',
                                        'rd_vrf': 'l2',
                                        'rd_vniid': 25000,
                                        'prefix': {
                                            '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152',
                                                'prefixversion': 4904,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            },
                                            '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152',
                                                'prefixversion': 4074,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            },
                                            '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152',
                                                'prefixversion': 4487,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25000,
                                                        'extcommunity': ['RT:200:25000', 'ENCAP:8'],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                    '192.168.9.1:33768': {  # Ops Str '10.121.0.55:27001'
                                        'rd': '192.168.9.1:33768',
                                        'rd_vrf': 'l2',
                                        'rd_vniid': 25001,
                                        'prefix': {
                                            '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03bb.bbbb.bbbb.bb00.0016]:[0x0]/152',
                                                'prefixversion': 4905,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            },
                                            '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03cc.cc11.1122.2200.0021]:[0x0]/152',
                                                'prefixversion': 4075,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            },
                                            '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152': {
                                                'nonipprefix': '[1]:[03dd.dd11.1122.2200.002c]:[0x0]/152',
                                                'prefixversion': 4488,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.9.1',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '192.168.9.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'inlabel': 25001,
                                                        "extcommunity": [
                                                            "RT:200:25001",
                                                            "RT:1234:5678",
                                                            "ENCAP:8"
                                                        ],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                    '192.168.154.1:3': {
                                        'rd': '192.168.154.1:3',
                                        'prefix': {
                                            '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216': {
                                                'nonipprefix': '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216',
                                                'prefixversion': 116,
                                                'on_xmitlist': True,
                                                'mpath': 'ibgp',
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': False,
                                                        'ipnexthop': '192.168.16.1',
                                                        'nexthopmetric': 81,
                                                        'neighbor': '192.168.234.1',
                                                        'neighborid': '192.168.234.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        "extcommunity": [
                                                            "RT:100:10001",
                                                            "ENCAP:8"
                                                        ],
                                                        'inlabel': 10001,
                                                        'originatorid': '192.168.154.1',
                                                        'clusterlist': ['192.168.234.1'],
                                                        'advertisedto': ['172.16.205.8'],
                                                    },
                                                }
                                            },
                                        },
                                    },
                                    '192.168.154.1:4': {
                                        'rd': '192.168.154.1:4',
                                        'prefix': {
                                            '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216': {
                                                'nonipprefix': '[2]:[0]:[0]:[48]:[5e00.0003.0007]:[0]:[0.0.0.0]/216',
                                                'prefixversion': 117,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'mpath': 'ibgp',
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': False,
                                                        'ipnexthop': '192.168.16.1',
                                                        'nexthopmetric': 81,
                                                        'neighbor': '192.168.234.1',
                                                        'neighborid': '192.168.234.1',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'inlabel': 10002,
                                                        'advertisedto': ['172.16.205.8'],
                                                        'originatorid': '192.168.154.1',
                                                        'clusterlist': ['192.168.234.1'],
                                                    },
                                                }
                                            },
                                        }
                                    },
                                    '10.121.0.55:27001': {
                                        'rd': '10.121.0.55:27001',
                                        'prefix': {
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.55]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.55]/136',
                                                'prefixversion': 13144,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.55',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.121.0.55',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'advertisedto': ['10.121.0.11', '10.121.0.22', '10.121.0.33',
                                                                         '10.121.0.44', '10.196.0.11'],
                                                    },
                                                }
                                            },
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136',
                                                'prefixversion': 13146,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.66',
                                                        'nexthopmetric': 3,
                                                        'neighbor': '10.196.0.11',
                                                        'neighborid': '10.196.0.11',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'originatorid': '10.121.0.66',
                                                        'clusterlist': ['10.196.0.11'],
                                                    },
                                                }
                                            }
                                        }
                                    },
                                    '10.121.0.66:27001': {
                                        'rd': '10.121.0.66:27001',
                                        'prefix': {
                                            '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136': {
                                                'nonipprefix': '[4]:[0300.0000.0001.2c00.0309]:[32]:[192.168.111.66]/136',
                                                'prefixversion': 13145,
                                                'on_xmitlist': True,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'path': {
                                                    1: {
                                                        'pathnr': 1,
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '192.168.111.66',
                                                        'nexthopmetric': 3,
                                                        'neighbor': '10.196.0.11',
                                                        'neighborid': '10.196.0.11',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 0,
                                                        'extcommunity': ['ENCAP:8', 'RT:0000.0000.012c'],
                                                        'advertisedto': ['10.121.0.11', '10.121.0.22', '10.121.0.33',
                                                                         '10.121.0.44'],
                                                        'originatorid': '10.121.0.66',
                                                        'clusterlist': ['10.196.0.11'],
                                                    },
                                                }
                                            },
                                        }
                                    },
                                    "10.196.7.7:32969": {
                                        "rd": "10.196.7.7:32969",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5387,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32968": {
                                        "rd": "10.196.7.7:32968",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5386,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32868": {
                                        "rd": "10.196.7.7:32868",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5384,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32868": {
                                        "rd": "10.144.6.6:32868",
                                        "rd_vniid": 10101,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5809,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10101",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10101",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5759,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32969": {
                                        "rd": "10.144.6.6:32969",
                                        "rd_vniid": 10202,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5813,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10202",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10202",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5761,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.144.6.6:32968": {
                                        "rd": "10.144.6.6:32968",
                                        "rd_vniid": 10201,
                                        "rd_vrf": "l2",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5811,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                            "[3]:[0]:[32]:[10.144.6.6]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "ipnexthop": "10.144.6.6",
                                                        "neighbor": "0.0.0.0",
                                                        "localpref": 100,
                                                        "neighborid": "10.144.6.6",
                                                        "pathbest": True,
                                                        "nexthopmetric": 0,
                                                        "pathvalid": True,
                                                        "advertisedto": [
                                                            "10.166.7.7"
                                                        ],
                                                        "extcommunity": [
                                                            "RT:100:10201",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10201",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.144.6.6",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 32768
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.144.6.6]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5760,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            }
                                        }
                                    },
                                    "10.196.7.7:32869": {
                                        "rd": "10.196.7.7:32869",
                                        "prefix": {
                                            "[3]:[0]:[32]:[10.196.7.7]/88": {
                                                "bestpathnr": 1,
                                                "path": {
                                                    1: {
                                                        "pathnr": 0,
                                                        "pathnolabeledrnh": True,
                                                        "neighbor": "10.166.7.7",
                                                        "localpref": 100,
                                                        "neighborid": "10.196.7.7",
                                                        "pathbest": True,
                                                        "nexthopmetric": 20,
                                                        "pathvalid": True,
                                                        "ipnexthop": "10.196.7.7",
                                                        "extcommunity": [
                                                            "RT:100:10102",
                                                            "ENCAP:8"
                                                        ],
                                                        "origin": "igp",
                                                        "pmsi_tunnel_attribute": {
                                                            "label": "10102",
                                                            "flags": "0x00",
                                                            "tunnel_id": "10.196.7.7",
                                                            "tunnel_type": "Ingress Replication"
                                                        },
                                                        "weight": 0
                                                    }
                                                },
                                                "nonipprefix": "[3]:[0]:[32]:[10.196.7.7]/88",
                                                "mpath": "ibgp",
                                                "prefixversion": 5385,
                                                "totalpaths": 1,
                                                "on_xmitlist": True
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }

    }

    ##################################################################
    #         TRM  - Fabric                                          #
    ##################################################################
    showFabricMulticastGlobals ={
        "multicast": {
            "globals": {
                "pruning": "segment-based",
                "switch_role": "",
                "fabric_control_seg": "Null",
                "peer_fabric_ctrl_addr": "0.0.0.0",
                "advertise_vpc_rpf_routes": "disabled",
                "created_vni_list": "-",
                "fwd_encap": "(null)",
                "overlay_distributed_dr": False,
                "overlay_spt_only": True,
            },
        },
    }

    showFabricMulticastIpSaAdRoute = {
        "multicast": {
            "vrf": {
                "default": {
                    "vnid": '0',
                },
                "vni_10100": {
                    "vnid": "10100",
                    "address_family": {
                        "ipv4": {
                            "sa_ad_routes": {
                                "gaddr": {
                                    "238.8.4.101/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "10.111.1.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:01:01",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:01:01",
                                                    }
                                                }
                                            },
                                            "10.111.1.4/32": {
                                                "src_len": 32,
                                                "uptime": "00:01:01",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:01:01",
                                                    }
                                                }
                                            },
                                            "10.111.6.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "10.111.6.4/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "10.111.7.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:02:38",
                                                "interested_fabric_nodes": {
                                                    "10.196.7.7": {
                                                        "uptime": "00:02:38",
                                                    }
                                                }
                                            },
                                            "10.111.8.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.1.8.8": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                        }
                                    },
                                    "238.8.4.102/32": {
                                        "grp_len": 32,
                                        'saddr': {
                                            "10.4.1.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:00:10",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:00:10",
                                                    }
                                                }
                                            },
                                            "10.4.2.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:47:51",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:47:51",
                                                    }
                                                }
                                            },
                                            "10.4.6.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    }
                },
                "vni_10200": {
                    "vnid": "10200",
                    "address_family": {
                        "ipv4": {
                            "sa_ad_routes": {
                                "gaddr": {
                                    "238.8.4.201/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "192.168.189.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:03:24",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:03:24",
                                                    }
                                                }
                                            },
                                            "192.168.229.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:07:48",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:07:48",
                                                    }
                                                }
                                            },
                                            "192.168.154.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },

                                        }
                                    },
                                    "238.8.4.202/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "192.168.229.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:02:10",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:02:10",
                                                    }
                                                }
                                            },
                                            "192.168.16.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "192.168.204.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },

                                        }
                                    },
                                }
                            }
                        }
                    }
                },
                "vpc-keepalive": {
                    "vnid": '0',
                },
            }
        }
    }

    showFabricMulticastIpL2Mroute = {
        "multicast": {
            "l2_mroute": {
                "vni": {
                    "10101":{
                        "vnid": "10101",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "231.1.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node":{
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "231.1.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node":{
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "232.2.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "232.2.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "233.3.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "233.3.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "236.6.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.144.6.6": {
                                                    "node": "10.144.6.6"
                                                }
                                            },
                                        },
                                    }
                                },
                                "236.6.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.144.6.6":{
                                                    "node": "10.144.6.6"
                                                }
                                            },
                                        },
                                    }
                                },
                                "237.7.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                }
                                            },
                                        },
                                    }
                                },
                            }
                        },
                    },
                    "10102": {
                        "vnid": "10102",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.102/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                },
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "10201": {
                        "vnid": "10201",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.201/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                    }
                                                },
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    "10202": {
                        "vnid": "10202",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.202/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                }
                                            },
                                        },
                                    }
                                },
                            }
                        },
                    }
                }
            }
        }
    }

    fabricOpsOutput = {
        "multicast": {
            "globals": {
                "pruning": "segment-based",
                "switch_role": "",
                "fabric_control_seg": "Null",
                "peer_fabric_ctrl_addr": "0.0.0.0",
                "advertise_vpc_rpf_routes": "disabled",
                "created_vni_list": "-",
                "fwd_encap": "(null)",
                "overlay_distributed_dr": False,
                "overlay_spt_only": True,
            },
            "vrf": {
                "default": {
                    "vnid": '0',
                },
                "vni_10100": {
                    "vnid": "10100",
                    "address_family": {
                        "ipv4": {
                            "sa_ad_routes": {
                                "gaddr": {
                                    "238.8.4.101/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "10.111.1.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:01:01",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:01:01",
                                                    }
                                                }
                                            },
                                            "10.111.1.4/32": {
                                                "src_len": 32,
                                                "uptime": "00:01:01",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:01:01",
                                                    }
                                                }
                                            },
                                            "10.111.6.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "10.111.6.4/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "10.111.7.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:02:38",
                                                "interested_fabric_nodes": {
                                                    "10.196.7.7": {
                                                        "uptime": "00:02:38",
                                                    }
                                                }
                                            },
                                            "10.111.8.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.1.8.8": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                        }
                                    },
                                    "238.8.4.102/32": {
                                        "grp_len": 32,
                                        'saddr': {
                                            "10.4.1.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:00:10",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:00:10",
                                                    }
                                                }
                                            },
                                            "10.4.2.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:47:51",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:47:51",
                                                    }
                                                }
                                            },
                                            "10.4.6.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    }
                },
                "vni_10200": {
                    "vnid": "10200",
                    "address_family": {
                        "ipv4": {
                            "sa_ad_routes": {
                                "gaddr": {
                                    "238.8.4.201/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "192.168.189.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:03:24",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:03:24",
                                                    }
                                                }
                                            },
                                            "192.168.229.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:07:48",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:07:48",
                                                    }
                                                }
                                            },
                                            "192.168.154.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },

                                        }
                                    },
                                    "238.8.4.202/32": {
                                        "grp_len": 32,
                                        "saddr": {
                                            "192.168.229.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:02:10",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:02:10",
                                                    }
                                                }
                                            },
                                            "192.168.16.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "This node": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                            "192.168.204.3/32": {
                                                "src_len": 32,
                                                "uptime": "00:49:39",
                                                "interested_fabric_nodes": {
                                                    "10.144.6.6": {
                                                        "uptime": "00:49:39",
                                                    }
                                                }
                                            },
                                        }
                                    },
                                }
                            }
                        }
                    }
                },
                "vpc-keepalive": {
                    "vnid": '0',
                },
            },
            "l2_mroute": {
                "vni": {
                    "10101": {
                        "vnid": "10101",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "231.1.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "231.1.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "232.2.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "232.2.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "233.3.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "233.3.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "This node": {
                                                    "node": "This node"
                                                }
                                            },
                                        },
                                    }
                                },
                                "236.6.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.144.6.6": {
                                                    "node": "10.144.6.6"
                                                }
                                            },
                                        },
                                    }
                                },
                                "236.6.4.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.144.6.6": {
                                                    "node": "10.144.6.6"
                                                }
                                            },
                                        },
                                    }
                                },
                                "237.7.3.101/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                }
                                            },
                                        },
                                    }
                                },
                            }
                        },
                    },
                    "10102": {
                        "vnid": "10102",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.102/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                },
                                            },
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "10201": {
                        "vnid": "10201",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.201/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                }
                                            },
                                        },
                                    }
                                },
                            }
                        }
                    },
                    "10202": {
                        "vnid": "10202",
                        'fabric_l2_mroutes': {
                            "gaddr": {
                                "238.8.4.202/32": {
                                    "saddr": {
                                        "*": {
                                            "interested_fabric_nodes": {
                                                "10.1.8.8": {
                                                    "node": "10.1.8.8"
                                                }
                                            },
                                        },
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }
    }

    #################################################################
    #        TRM - Forwarding
    #################################################################

    showForwardingDistributionMulticastRoute = {
        "distribution": {
            "multicast": {
                "route": {
                    "vrf": {
                        'default': {
                            "address_family": {
                                "ipv4": {
                                    "num_groups": 5,
                                    "gaddr": {
                                        '224.0.0.0/4': {
                                            "grp_len": 4,
                                             "saddr": {
                                                  '*': {
                                                    "rpf_ifname": 'NULL',
                                                    "flags": 'D',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 0
                                                    }
                                                  }
                                             },
                                        '224.0.0.0/24': {
                                            "grp_len": 24,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'NULL',
                                                    "flags": 'CP',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 0
                                                }
                                            }
                                        },
                                        '231.100.1.1/32': {
                                            "grp_len": 32,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'Ethernet1/2',
                                                    "flags": 'GLd',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 30,
                                                        'nve1': {
                                                            'oif': 'nve1',
                                                        },
                                                    },
                                                },
                                                '10.76.23.23/32': {
                                                    "src_len": 32,
                                                    "rpf_ifname": "loopback1",
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 29,
                                                        'Ethernet1/2': {
                                                            'oif': 'Ethernet1/2',
                                                        },
                                                    },
                                                }
                                            }
                                        },
                                        '231.1.3.101/32': {
                                            "grp_len": 32,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'loopback100',
                                                    "flags": 'GL',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 104,
                                                        "Vlan101": {
                                                            "oif": "Vlan101",
                                                            "mem_l2_ports": "port-channel1 nve1",
                                                            "l2_oiflist_index": 44,
                                                        },
                                                    },
                                                },
                                            }
                                        },
                                        "238.8.4.101/32": {
                                            "grp_len": 32,
                                            "saddr": {
                                                "10.111.1.3/32": {
                                                    "src_len": 32,
                                                    "rpf_ifname": 'Vlan101',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 2,
                                                    "oifs": {
                                                        "oif_index": 54,
                                                        'Vlan100': {
                                                            "oif": "Vlan100",
                                                            "encap": 'vxlan',
                                                            "mem_l2_ports": "nve1",
                                                            "l2_oiflist_index": 19,
                                                        },
                                                        'Vlan101': {
                                                            "oif": 'Vlan101',
                                                            "mem_l2_ports": "nve1",
                                                            "l2_oiflist_index": 19,
                                                        },
                                                    },
                                                },
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    forwardingOpsOutput = {
        "distribution": {
            "multicast": {
                "route": {
                    "vrf": {
                        'default': {
                            "address_family": {
                                "ipv4": {
                                    "num_groups": 5,
                                    "gaddr": {
                                        '224.0.0.0/4': {
                                            "grp_len": 4,
                                             "saddr": {
                                                  '*': {
                                                    "rpf_ifname": 'NULL',
                                                    "flags": 'D',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 0
                                                    }
                                                  }
                                             },
                                        '224.0.0.0/24': {
                                            "grp_len": 24,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'NULL',
                                                    "flags": 'CP',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 0
                                                }
                                            }
                                        },
                                        '231.100.1.1/32': {
                                            "grp_len": 32,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'Ethernet1/2',
                                                    "flags": 'GLd',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 30,
                                                        'nve1': {
                                                            'oif': 'nve1',
                                                        },
                                                    },
                                                },
                                                '10.76.23.23/32': {
                                                    "src_len": 32,
                                                    "rpf_ifname": "loopback1",
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 29,
                                                        'Ethernet1/2': {
                                                            'oif': 'Ethernet1/2',
                                                        },
                                                    },
                                                }
                                            }
                                        },
                                        '231.1.3.101/32': {
                                            "grp_len": 32,
                                            "saddr": {
                                                '*': {
                                                    "rpf_ifname": 'loopback100',
                                                    "flags": 'GL',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 1,
                                                    "oifs": {
                                                        "oif_index": 104,
                                                        "Vlan101": {
                                                            "oif": "Vlan101",
                                                            "mem_l2_ports": "port-channel1 nve1",
                                                            "l2_oiflist_index": 44,
                                                        },
                                                    },
                                                },
                                            }
                                        },
                                        "238.8.4.101/32": {
                                            "grp_len": 32,
                                            "saddr": {
                                                "10.111.1.3/32": {
                                                    "src_len": 32,
                                                    "rpf_ifname": 'Vlan101',
                                                    "rcv_packets": 0,
                                                    "rcv_bytes": 0,
                                                    "num_of_oifs": 2,
                                                    "oifs": {
                                                        "oif_index": 54,
                                                        'Vlan100': {
                                                            "oif": "Vlan100",
                                                            "encap": 'vxlan',
                                                            "mem_l2_ports": "nve1",
                                                            "l2_oiflist_index": 19,
                                                        },
                                                        'Vlan101': {
                                                            "oif": 'Vlan101',
                                                            "mem_l2_ports": "nve1",
                                                            "l2_oiflist_index": 19,
                                                        },
                                                    },
                                                },
                                            }
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }}

    #################################################################
    #        TRM - bgp_mvpn
    #################################################################

    showBgpIpMvpnRouteType_1 ={
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[1][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[1][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    showBgpIpMvpnRouteType_2 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[2][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[2][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    showBgpIpMvpnRouteType_3 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[3][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[3][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    showBgpIpMvpnRouteType_4 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[4][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[4][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    showBgpIpMvpnRouteType_5 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[5][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[5][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    }
    showBgpIpMvpnRouteType_6 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[6][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[6][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    }
    showBgpIpMvpnRouteType_7 = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[7][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[7][10.111.1.3][238.8.4.101]/64',
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'ipnexthop': '0.0.0.0',
                                                        'weight': 32768,
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                    }
                                                }
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    }
    showBgpIpMvpnSaadDetail = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[1][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[1][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[2][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[2][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[3][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[3][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[4][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[4][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[5][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[5][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[6][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[6][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[7][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[7][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'i',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                        }
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    bgpMvpnOpsOutput = {
        'instance': {
            'default': {
                'vrf': {
                    'default': {
                        'vrf_name_out': 'default',
                        'address_family': {
                            'ipv4 mvpn': {
                                'af_name': 'ipv4 mvpn',
                                'table_version': '390',
                                'router_id': '10.16.2.2',
                                'rd': {
                                    '10.16.2.2:3': {
                                        'rd_val': '10.16.2.2:3',
                                        'rd_vrf': '10100',
                                        'prefix': {
                                            '[1][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[1][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[2][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[2][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[3][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[3][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[4][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[4][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[5][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[5][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[6][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[6][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                            '[7][10.111.1.3][238.8.4.101]/64': {
                                                'nonipprefix': '[7][10.111.1.3][238.8.4.101]/64',
                                                'prefixversion': 7,
                                                'totalpaths': 1,
                                                'bestpathnr': 1,
                                                'on_xmitlist': True,
                                                'path': {
                                                    1: {
                                                        'pathnr': 0,
                                                        'statuscode': '*',
                                                        'bestcode': '>',
                                                        'typecode': 'l',
                                                        'pathtype': 'local',
                                                        'pathvalid': True,
                                                        'pathbest': True,
                                                        'pathnolabeledrnh': True,
                                                        'ipnexthop': '0.0.0.0',
                                                        'nexthopmetric': 0,
                                                        'neighbor': '0.0.0.0',
                                                        'neighborid': '10.16.2.2',
                                                        'origin': 'igp',
                                                        'localpref': 100,
                                                        'weight': 32768,
                                                        'extcommunity': [
                                                            'RT:100:10100'
                                                        ],
                                                        'advertisedto': [
                                                            '10.64.4.4',
                                                            '10.100.5.5'
                                                        ],
                                                    }
                                                },
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


