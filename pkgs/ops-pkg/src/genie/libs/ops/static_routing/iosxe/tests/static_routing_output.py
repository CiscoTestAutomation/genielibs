'''
 StaticRoute Genie Ops Object Outputs for IOSXE.
'''

class StaticRouteOutput(object):
    # 'show ipv4 static route' output
    ShowVrfDetail = {
        "Mgmt-vrf": {
            "vrf_id": 1,
            "interfaces": [
                "GigabitEthernet0/0"
            ],
            "address_family": {
                "ipv4 unicast": {
                    "table_id": "0x1",
                    "flags": "0x0",
                    "vrf_label": {
                        'allocation_mode': 'per-prefix'
                    }
                },
                "ipv6 unicast": {
                    "table_id": "0x1E000001",
                    "flags": "0x0",
                    "vrf_label": {
                        'allocation_mode': 'per-prefix'
                    }
                }
            },
            "flags": "0x1808"
        },
        "VRF1": {
            "interfaces": [
                "GigabitEthernet0/0"
            ],
            "address_family": {
                "ipv4 unicast": {
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map",
                        "prefix_limit": 1000
                    },
                    "import_from_global": {
                        "prefix_limit": 1000,
                        "import_from_global_map": "import_from_global_map"
                    },
                    "table_id": "0x1",
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_limit_number": {
                                "alert_limit_number": 10000
                            }
                        }
                    },
                    "route_targets": {
                        "200:1": {
                            "rt_type": "both",
                            "route_target": "200:1"
                        },
                        "100:1": {
                            "rt_type": "both",
                            "route_target": "100:1"
                        }
                    },
                    "flags": "0x2100",
                    "vrf_label": {
                        'allocation_mode': 'per-prefix'
                    }
                },
                "ipv6 unicast": {
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map",
                        "prefix_limit": 1000
                    },
                    "table_id": "0x1E000001",
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_percent": {
                                "alert_percent_value": 70
                            },
                            "enable_alert_limit_number": {
                                "alert_limit_number": 7000
                            }
                        },
                        "routing_table_limit_number": 10000
                    },
                    "route_targets": {
                        "200:1": {
                            "rt_type": "import",
                            "route_target": "200:1"
                        },
                        "400:1": {
                            "rt_type": "import",
                            "route_target": "400:1"
                        },
                        "300:1": {
                            "rt_type": "export",
                            "route_target": "300:1"
                        },
                        "100:1": {
                            "rt_type": "export",
                            "route_target": "100:1"
                        }
                    },
                    "flags": "0x100",
                    "vrf_label": {
                        'allocation_mode': 'per-prefix'
                    }
                }
            },
            "flags": "0x180C",
            "route_distinguisher": "100:1",
            "vrf_id": 1
        }
    }
    showIpv4StaticRoute = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.1.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': False,
                                            'next_hop': '10.186.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                            'preference': 2,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '10.186.2.2',
                                            'preference': 3,
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/2': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                            'preference': 1,
                                        },
                                        'GigabitEthernet0/3': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
    showIpv6StaticRoute = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': False,
                                            'next_hop': '2001:10:1:2::2',
                                            'resolved_outgoing_interface': 'GigabitEthernet0/0',
                                            'resolved_paths_number': 1,
                                            'max_depth': 1,
                                            'preference': 3,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:20:1:2::2',
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                            'preference': 1,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '2001:10:1:2::2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                            'rejected_by': 'routing table',
                                            'preference': 11,
                                            'tag': 100,
                                            'track': 1,
                                            'track_state': 'up',
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/3': {
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                            'active': True,
                                            'preference': 1,
                                        },
                                        'GigabitEthernet0/2': {
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                            'active': True,
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    showIpv4StaticRoute_default ='''\
    R1#show ip static route

    '''
    showIpv4StaticRoute_vrf1 = '''\
    R1#show ip static route vrf VRF1
    Codes: M - Manual static, A - AAA download, N - IP NAT, D - DHCP,
       G - GPRS, V - Crypto VPN, C - CASA, P - Channel interface processor,
       B - BootP, S - Service selection gateway
       DN - Default Network, T - Tracking object
       L - TL1, E - OER, I - iEdge
       D1 - Dot1x Vlan Network, K - MWAM Route
       PP - PPP default route, MR - MRIPv6, SS - SSLVPN
       H - IPe Host, ID - IPe Domain Broadcast
       U - User GPRS, TE - MPLS Traffic-eng, LI - LIIN
       IR - ICMP Redirect
    Codes in []: A - active, N - non-active, B - BFD-tracked, D - Not Tracked, P - permanent
    Static local RIB for VRF1
    M  10.16.2.2/32 [1/0] via GigabitEthernet0/0 10.1.2.2 [A]
    M             [2/0] via GigabitEthernet0/1 10.186.2.2 [N]
    M             [3/0] via 10.186.2.2 [N]
    M  10.36.3.3/32 [1/0] via GigabitEthernet0/2 [A]
    M             [1/0] via GigabitEthernet0/3 [A]
    '''
    showIpv6StaticRoute_default = '''\
R1#show ipv6 static detail
IPv6 Static routes Table - default
Codes: * - installed in RIB, u/m - Unicast/Multicast only
       U - Per-user Static route
       N - ND Static route
       M - MIP Static route
       P - DHCP-PD Static route
       R - RHI Static route
    2001:2:2:2::2/128 via 2001:10:1:2::2, distance 3
     Resolves to 1 paths (max depth 1)
     via GigabitEthernet0/0
*   2001:2:2:2::2/128 via 2001:20:1:2::2, GigabitEthernet0/1, distance 1
    2001:2:2:2::2/128 via 2001:10:1:2::2, GigabitEthernet0/0, distance 11, tag 100
     Rejected by routing table
     Tracked object 1 is Up
*   2001:3:3:3::3/128 via GigabitEthernet0/3, distance 1
*   2001:3:3:3::3/128 via GigabitEthernet0/2, distance 1
    '''
    showIpv6StaticRoute_vrf1 = '''\
R1#show ipv6 static vrf VRF1 detail

    '''
    staticRouteOpsOutput = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.1.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': False,
                                            'next_hop': '10.186.2.2',
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                            'preference': 2,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '10.186.2.2',
                                            'preference': 3,
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/2': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                            'preference': 1,
                                        },
                                        'GigabitEthernet0/3': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },

                },
            },
            'default': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': False,
                                            'next_hop': '2001:10:1:2::2',
                                            'preference': 3,
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:20:1:2::2',
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/1',
                                            'preference': 1,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '2001:10:1:2::2',
                                            'outgoing_interface': 'GigabitEthernet0/0',
                                            'preference': 11,
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/3': {
                                            'outgoing_interface': 'GigabitEthernet0/3',
                                            'active': True,
                                            'preference': 1,
                                        },
                                        'GigabitEthernet0/2': {
                                            'outgoing_interface': 'GigabitEthernet0/2',
                                            'active': True,
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
