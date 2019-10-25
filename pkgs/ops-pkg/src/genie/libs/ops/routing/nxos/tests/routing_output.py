'''
 StaticRoute Genie Ops Object Outputs for NXOS.
'''

class RouteOutput(object):
    """ output for:
        show ip route
        show ipv6 route"""

    showIpRoute = {
        'vrf':{
            'default':{
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'ubest':2,
                                'mbest':0,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol':'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.1.3.1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.186.3.1',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:30',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'active': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.2.3.2',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.229.3.2',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:29',
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'active': True,
                                'attached': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.36.3.3',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Loopback0',
                                            'updated': '01:01:31',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.36.3.3',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Loopback0',
                                            'updated': '01:01:31',
                                        },
                                    },
                                },
                            },
                            '10.1.2.0/24': {
                                'route': '10.1.2.0/24',
                                'active': True,
                                'ubest': 4,
                                'mbest': 0,
                                'route_preference': 110,
                                'source_protocol': 'ospf',
                                'process_id': 1,
                                'source_protocol_status': 'intra',
                                'metric': 41,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.1.3.1',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:01:18',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.2.3.2',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:18',
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop': '10.186.3.1',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:18',
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop': '10.229.3.2',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:18',
                                        },

                                    },
                                },
                            },
                            '10.21.33.33/32': {
                                'route': '10.21.33.33/32',
                                'active': True,
                                'attached': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.21.33.33',
                                            'outgoing_interface': 'Loopback3',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.21.33.33',
                                            'outgoing_interface': 'Loopback3',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:30',
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'attached': True,
                                'active': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 0,
                                'metric': 0,
                                'source_protocol': 'local',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.4.1.1',
                                            'outgoing_interface': 'Loopback4',
                                            'best_ucast_nexthop': True,
                                            'updated': '00:00:10',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.4.1.1',
                                            'outgoing_interface': 'Loopback4',
                                            'best_ucast_nexthop': True,
                                            'updated': '00:00:10',
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

    showIpv6Route = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:10:1:3::1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:02:00',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:20:1:3::1',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:02:00',
                                        },
                                    },
                                },
                            },
                            '2001:10:1:2::/64': {
                                'route': '2001:10:1:2::/64',
                                'active': True,
                                'ubest': 4,
                                'mbest': 0,
                                'route_preference': 110,
                                'metric': 41,
                                'source_protocol': 'ospfv3',
                                'process_id': 1,
                                'source_protocol_status': 'intra',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::5054:ff:fe64:bd2e',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:10',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': 'fe80::5054:ff:fea5:6e95',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:01:10',
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop': 'fe80::5054:ff:fea7:1341',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:10',
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop': 'fe80::5054:ff:feb3:b312',
                                            'best_ucast_nexthop': True,
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:10',
                                        },
                                    },
                                },
                            },
                            '2001:31:31:31::31/128': {
                                'route': '2001:31:31:31::31/128',
                                'active': True,
                                'ubest': 1,
                                'mbest': 0,
                                'route_preference': 200,
                                'source_protocol': 'bgp',
                                'source_protocol_status': 'internal',
                                'process_id': 100,
                                'tag': 100,
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '::ffff:10.229.11.11',
                                            'next_hop_vrf': 'default',
                                            'next_hop_af': 'ipv4',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:43',
                                        },

                                    },
                                },
                            },
                            '2001:32:32:32::32/128': {
                                'route': '2001:32:32:32::32/128',
                                'active': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 200,
                                'source_protocol': 'bgp',
                                'source_protocol_status': 'internal',
                                'process_id': 100,
                                'tag': 100,
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::5054:ff:fea7:1341',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:24',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': 'fe80::5054:ff:feb3:b312',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:01:24',
                                        },
                                    },
                                },
                            },
                            '2001:33:33:33::33/128': {
                                'route': '2001:33:33:33::33/128',
                                'active': True,
                                'attached': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:33:33:33::33',
                                            'outgoing_interface': 'Loopback3',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:02:01',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:33:33:33::33',
                                            'outgoing_interface': 'Loopback3',
                                            'best_ucast_nexthop': True,
                                            'updated': '01:02:01',
                                        },
                                    },
                                },
                            },

                        },
                    },
                },
            },
            'VRF1': {
                'address_family': {
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'attached': True,
                                'active': True,
                                'ubest': 2,
                                'mbest': 0,
                                'route_preference': 0,
                                'metric': 0,
                                'source_protocol': 'local',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:1:1:1::1',
                                            'outgoing_interface': 'Loopback4',
                                            'best_ucast_nexthop': True,
                                            'updated': '00:00:35',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:1:1:1::1',
                                            'outgoing_interface': 'Loopback4',
                                            'best_ucast_nexthop': True,
                                            'updated': '00:00:35',
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

    routeOpsOutput = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.1.3.1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.186.3.1',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:30',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.2.3.2',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.229.3.2',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:29',
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'active': True,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.36.3.3',
                                            'outgoing_interface': 'Loopback0',
                                            'updated': '01:01:31',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.36.3.3',
                                            'outgoing_interface': 'Loopback0',
                                            'updated': '01:01:31',
                                        },
                                    },
                                },
                            },
                            '10.1.2.0/24': {
                                'route': '10.1.2.0/24',
                                'active': True,
                                'route_preference': 110,
                                'source_protocol': 'ospf',
                                'metric': 41,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.1.3.1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:01:18',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.2.3.2',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:18',
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop': '10.186.3.1',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:18',
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop': '10.229.3.2',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:18',
                                        },

                                    },
                                },
                            },
                            '10.21.33.33/32': {
                                'route': '10.21.33.33/32',
                                'active': True,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.21.33.33',
                                            'outgoing_interface': 'Loopback3',
                                            'updated': '01:01:30',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.21.33.33',
                                            'outgoing_interface': 'Loopback3',
                                            'updated': '01:01:30',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'route_preference': 1,
                                'metric': 0,
                                'source_protocol': 'static',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:10:1:3::1',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:02:00',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:20:1:3::1',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:02:00',
                                        },
                                    },
                                },
                            },
                            '2001:10:1:2::/64': {
                                'route': '2001:10:1:2::/64',
                                'active': True,
                                'route_preference': 110,
                                'metric': 41,
                                'source_protocol': 'ospfv3',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::5054:ff:fe64:bd2e',
                                            'outgoing_interface': 'Ethernet1/3',
                                            'updated': '01:01:10',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': 'fe80::5054:ff:fea5:6e95',
                                            'outgoing_interface': 'Ethernet1/2',
                                            'updated': '01:01:10',
                                        },
                                        3: {
                                            'index': 3,
                                            'next_hop': 'fe80::5054:ff:fea7:1341',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:10',
                                        },
                                        4: {
                                            'index': 4,
                                            'next_hop': 'fe80::5054:ff:feb3:b312',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:10',
                                        },
                                    },
                                },
                            },
                            '2001:31:31:31::31/128': {
                                'route': '2001:31:31:31::31/128',
                                'active': True,
                                'route_preference': 200,
                                'source_protocol': 'bgp',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '::ffff:10.229.11.11',
                                            'updated': '01:01:43',
                                        },

                                    },
                                },
                            },
                            '2001:32:32:32::32/128': {
                                'route': '2001:32:32:32::32/128',
                                'active': True,
                                'route_preference': 200,
                                'source_protocol': 'bgp',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::5054:ff:fea7:1341',
                                            'outgoing_interface': 'Ethernet1/4',
                                            'updated': '01:01:24',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': 'fe80::5054:ff:feb3:b312',
                                            'outgoing_interface': 'Ethernet1/1',
                                            'updated': '01:01:24',
                                        },
                                    },
                                },
                            },
                            '2001:33:33:33::33/128': {
                                'route': '2001:33:33:33::33/128',
                                'active': True,
                                'route_preference': 0,
                                'source_protocol': 'local',
                                'metric': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:33:33:33::33',
                                            'outgoing_interface': 'Loopback3',
                                            'updated': '01:02:01',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:33:33:33::33',
                                            'outgoing_interface': 'Loopback3',
                                            'updated': '01:02:01',
                                        },
                                    },
                                },
                            },

                        },
                    },
                },
            },

            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'route_preference': 0,
                                'metric': 0,
                                'source_protocol': 'local',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.4.1.1',
                                            'outgoing_interface': 'Loopback4',
                                            'updated': '00:00:10',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.4.1.1',
                                            'outgoing_interface': 'Loopback4',
                                            'updated': '00:00:10',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'route_preference': 0,
                                'metric': 0,
                                'source_protocol': 'local',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:1:1:1::1',
                                            'outgoing_interface': 'Loopback4',
                                            'updated': '00:00:35',
                                        },
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:1:1:1::1',
                                            'outgoing_interface': 'Loopback4',
                                            'updated': '00:00:35',
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
    routeOpsOutput_custom = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'source_protocol': 'local',
                                'metric': 0,
                                'route_preference': 0,
                                'next_hop': {
                                    'next_hop_list': {
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.4.1.1',
                                            'updated': '00:00:10',
                                            'outgoing_interface': 'Loopback4',
                                        },
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.4.1.1',
                                            'updated': '00:00:10',
                                            'outgoing_interface': 'Loopback4',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv6': {
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'route_preference': 0,
                                'metric': 0,
                                'source_protocol': 'local',
                                'next_hop': {
                                    'next_hop_list': {
                                        2: {
                                            'index': 2,
                                            'next_hop': '2001:1:1:1::1',
                                            'updated': '00:00:35',
                                            'outgoing_interface': 'Loopback4',
                                        },
                                        1: {
                                            'index': 1,
                                            'next_hop': '2001:1:1:1::1',
                                            'updated': '00:00:35',
                                            'outgoing_interface': 'Loopback4',
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
