"""
 Routing Genie Ops Object Outputs for IOSXR.
"""

class RoutingOutput(object):
    """ show route ops output """

    showRouteIpv4 = '''\
       genie_Router#show route ipv4
        Tue Oct 29 14:23:27.507 UTC

        Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
            D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
            N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
            E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
            i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
            ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
            U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
            A - access/subscriber, a - Application route
            M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

        Gateway of last resort is not set

        R    10.1.0.0/8 [120/1] via 10.12.120.1, 5d16h, GigabitEthernet0/0/0/0.120
        D    10.4.1.1/32 [90/10880] via 10.12.90.1, 5d16h, GigabitEthernet0/0/0/0.90
        L    10.16.2.2/32 is directly connected, 3w3d, Loopback0
        D    10.36.3.3/32 [90/2570240] via 10.23.90.3, 3w3d, GigabitEthernet0/0/0/1.90
        C    10.12.90.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/0.90
        L    10.12.90.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/0.90
        C    10.12.110.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/0.110
        L    10.12.110.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/0.110
        C    10.12.115.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/0.115
        L    10.12.115.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/0.115
        C    10.12.120.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/0.120
        L    10.12.120.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/0.120
        D    10.13.90.0/24 [90/15360] via 10.12.90.1, 5d16h, GigabitEthernet0/0/0/0.90
                        [90/15360] via 10.23.90.3, 5d16h, GigabitEthernet0/0/0/1.90
        O    10.13.110.0/24 [110/2] via 10.12.110.1, 5d16h, GigabitEthernet0/0/0/0.110
        i L1 10.13.115.0/24 [115/20] via 10.12.115.1, 5d16h, GigabitEthernet0/0/0/0.115
        R    10.13.120.0/24 [120/1] via 10.12.120.1, 5d16h, GigabitEthernet0/0/0/0.120
                            [120/1] via 10.23.120.3, 5d16h, GigabitEthernet0/0/0/1.120
        C    10.23.90.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/1.90
        L    10.23.90.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/1.90
        C    10.23.110.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/1.110
        L    10.23.110.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/1.110
        C    10.23.115.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/1.115
        L    10.23.115.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/1.115
        C    10.23.120.0/24 is directly connected, 3w3d, GigabitEthernet0/0/0/1.120
        L    10.23.120.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/11.120 
    '''
    showRouteVrfAllIpv4 = '''\
       genie_Router#show route vrf all ipv4
        Tue Oct 29 14:23:27.507 UTC

        VRF: VRF1

        Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
            D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
            N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
            E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
            i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
            ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
            U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
            A - access/subscriber, a - Application route
            M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

        Gateway of last resort is not set

        L    10.23.120.2/32 is directly connected, 3w3d, GigabitEthernet0/0/0/11.120 
    '''
    showRouteIpv4_route = '''\
        genie_Router#show route ipv4 10.23.90.0
        Tue Oct 29 15:00:22.242 UTC

        Routing entry for 10.23.90.0/24
        Known via "connected", distance 0, metric 0 (connected)
        Installed Oct  4 15:47:45.390 for 3w3d
        Routing Descriptor Blocks
            directly connected, via GigabitEthernet0/0/0/1.90
            Route metric is 0
        Redist Advertisers:
            eigrp/100 (protoid=5, clientid=22)
    '''
    showRouteVrfAllIpv4_route = '''\
        genie_Router#show route vrf all ipv4 10.23.90.0
        Tue Oct 29 15:00:22.242 UTC

        VRF: VRF1

        Routing entry for 10.23.90.0/24
        Known via "connected", distance 0, metric 0 (connected)
        Installed Oct  4 15:47:45.390 for 3w3d
        Routing Descriptor Blocks
            directly connected, via GigabitEthernet0/0/0/1.90
            Route metric is 0
        Redist Advertisers:
            eigrp/100 (protoid=5, clientid=22)
    '''
    showRouteIpv6 = '''\
    genie_Router#show route ipv6
        Tue Oct 29 14:24:32.669 UTC

        Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
            D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
            N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
            E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
            i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
            ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
            U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
            A - access/subscriber, a - Application route
            M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

        Gateway of last resort is not set

        D    2001:1:1:1::1/128
            [90/10880] via fe80::f816:3eff:fe76:b56d, 5d16h, GigabitEthernet0/0/0/0.90
        L    2001:2:2:2::2/128 is directly connected,
            3w3d, Loopback0
        D    2001:3:3:3::3/128
            [90/2570240] via fe80::5c00:80ff:fe02:7, 3w3d, GigabitEthernet0/0/0/1.90
        C    2001:10:12:90::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.90
        L    2001:10:12:90::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.90
        C    2001:10:12:110::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.110
        L    2001:10:12:110::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.110
        C    2001:10:12:115::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.115
        L    2001:10:12:115::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.115
        C    2001:10:12:120::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.120
        L    2001:10:12:120::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/0.120
        D    2001:10:13:90::/64
            [90/15360] via fe80::f816:3eff:fe76:b56d, 5d16h, GigabitEthernet0/0/0/0.90
        D    2001:10:13:110::/64
            [90/15360] via fe80::f816:3eff:fe76:b56d, 5d16h, GigabitEthernet0/0/0/0.90
        D    2001:10:13:115::/64
            [90/15360] via fe80::f816:3eff:fe76:b56d, 5d16h, GigabitEthernet0/0/0/0.90
        D    2001:10:13:120::/64
            [90/15360] via fe80::f816:3eff:fe76:b56d, 5d16h, GigabitEthernet0/0/0/0.90
        C    2001:10:23:90::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.90
        L    2001:10:23:90::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.90
        C    2001:10:23:110::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.110
        L    2001:10:23:110::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.110
        C    2001:10:23:115::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.115
        L    2001:10:23:115::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.115
        C    2001:10:23:120::/64 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.120
        L    2001:10:23:120::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.120
    '''
    showRouteVrfAllIpv6 = '''\
    genie_Router#show route vrf all ipv6
        Tue Oct 29 14:24:32.669 UTC

        VRF: VRF1

        Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
            D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
            N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
            E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
            i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
            ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
            U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
            A - access/subscriber, a - Application route
            M - mobile route, r - RPL, t - Traffic Engineering, (!) - FRR Backup path

        Gateway of last resort is not set

        L    2001:10:23:120::2/128 is directly connected,
            3w3d, GigabitEthernet0/0/0/1.120
    '''

    showRouteOpsOutput = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.23.120.2/32': {
                                'route': '10.23.120.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/11.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/11.120',
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'ipv6': {
                        'routes': {
                            '2001:10:23:120::2/128': {
                                'route': '2001:10:23:120::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.120',
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.23.120.2/32': {
                                'route': '10.23.120.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/11.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/11.120',
                                        },
                                    },
                                },
                            },
                            '10.23.120.0/24': {
                                'route': '10.23.120.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.120',
                                        },
                                    },
                                },
                            },
                            '10.23.115.2/32': {
                                'route': '10.23.115.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.115',
                                        },
                                    },
                                },
                            },
                            '10.23.115.0/24': {
                                'route': '10.23.115.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.115',
                                        },
                                    },
                                },
                            },
                            '10.23.110.2/32': {
                                'route': '10.23.110.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.110',
                                        },
                                    },
                                },
                            },
                            '10.23.110.0/24': {
                                'route': '10.23.110.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.110',
                                        },
                                    },
                                },
                            },
                            '10.23.90.2/32': {
                                'route': '10.23.90.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                            },
                            '10.23.90.0/24': {
                                'route': '10.23.90.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                            },
                            '10.13.120.0/24': {
                                'route': '10.13.120.0/24',
                                'active': True,
                                'route_preference': 120,
                                'metric': 1,
                                'source_protocol': 'rip',
                                'source_protocol_codes': 'R',
                                'next_hop': {
                                    'next_hop_list': {
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.23.120.3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.120',
                                            'updated': '5d16h',
                                        },
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.120.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                            '10.13.115.0/24': {
                                'route': '10.13.115.0/24',
                                'active': True,
                                'route_preference': 115,
                                'metric': 20,
                                'source_protocol': 'isis',
                                'source_protocol_codes': 'i L1',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.115.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.115',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                            '10.13.110.0/24': {
                                'route': '10.13.110.0/24',
                                'active': True,
                                'route_preference': 110,
                                'metric': 2,
                                'source_protocol': 'ospf',
                                'source_protocol_codes': 'O',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.110.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.110',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                            '10.13.90.0/24': {
                                'route': '10.13.90.0/24',
                                'active': True,
                                'route_preference': 90,
                                'metric': 15360,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        2: {
                                            'index': 2,
                                            'next_hop': '10.23.90.3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                            'updated': '5d16h',
                                        },
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.90.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                            '10.12.120.2/32': {
                                'route': '10.12.120.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                        },
                                    },
                                },
                            },
                            '10.12.120.0/24': {
                                'route': '10.12.120.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                        },
                                    },
                                },
                            },
                            '10.12.115.2/32': {
                                'route': '10.12.115.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.115',
                                        },
                                    },
                                },
                            },
                            '10.12.115.0/24': {
                                'route': '10.12.115.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.115',
                                        },
                                    },
                                },
                            },
                            '10.12.110.2/32': {
                                'route': '10.12.110.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.110',
                                        },
                                    },
                                },
                            },
                            '10.12.110.0/24': {
                                'route': '10.12.110.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.110',
                                        },
                                    },
                                },
                            },
                            '10.12.90.2/32': {
                                'route': '10.12.90.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '10.12.90.0/24': {
                                'route': '10.12.90.0/24',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'active': True,
                                'route_preference': 90,
                                'metric': 2570240,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.23.90.3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                            'updated': '3w3d',
                                        },
                                    },
                                },
                            },
                            '10.16.2.2/32': {
                                'route': '10.16.2.2/32',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Loopback0': {
                                            'outgoing_interface': 'Loopback0',
                                        },
                                    },
                                },
                            },
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'active': True,
                                'route_preference': 90,
                                'metric': 10880,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.90.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                            '10.1.0.0/8': {
                                'route': '10.1.0.0/8',
                                'active': True,
                                'route_preference': 120,
                                'metric': 1,
                                'source_protocol': 'rip',
                                'source_protocol_codes': 'R',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': '10.12.120.1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                            'updated': '5d16h',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv6': {
                        'routes': {
                            '2001:10:23:120::2/128': {
                                'route': '2001:10:23:120::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.120',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:120::/64': {
                                'route': '2001:10:23:120::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.120',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:115::2/128': {
                                'route': '2001:10:23:115::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.115',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:115::/64': {
                                'route': '2001:10:23:115::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.115',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:110::2/128': {
                                'route': '2001:10:23:110::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.110',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:110::/64': {
                                'route': '2001:10:23:110::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.110',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:90::2/128': {
                                'route': '2001:10:23:90::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:23:90::/64': {
                                'route': '2001:10:23:90::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:13:120::/64': {
                                'route': '2001:10:13:120::/64',
                                'active': True,
                                'route_preference': 90,
                                'metric': 15360,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::f816:3eff:fe76:b56d',
                                            'updated': '5d16h',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:13:115::/64': {
                                'route': '2001:10:13:115::/64',
                                'active': True,
                                'route_preference': 90,
                                'metric': 15360,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::f816:3eff:fe76:b56d',
                                            'updated': '5d16h',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:13:110::/64': {
                                'route': '2001:10:13:110::/64',
                                'active': True,
                                'route_preference': 90,
                                'metric': 15360,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::f816:3eff:fe76:b56d',
                                            'updated': '5d16h',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:13:90::/64': {
                                'route': '2001:10:13:90::/64',
                                'active': True,
                                'route_preference': 90,
                                'metric': 15360,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::f816:3eff:fe76:b56d',
                                            'updated': '5d16h',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:120::2/128': {
                                'route': '2001:10:12:120::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:120::/64': {
                                'route': '2001:10:12:120::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.120': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.120',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:115::2/128': {
                                'route': '2001:10:12:115::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.115',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:115::/64': {
                                'route': '2001:10:12:115::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.115': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.115',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:110::2/128': {
                                'route': '2001:10:12:110::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.110',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:110::/64': {
                                'route': '2001:10:12:110::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.110': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.110',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:90::2/128': {
                                'route': '2001:10:12:90::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:10:12:90::/64': {
                                'route': '2001:10:12:90::/64',
                                'active': True,
                                'source_protocol': 'connected',
                                'source_protocol_codes': 'C',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/0.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'active': True,
                                'route_preference': 90,
                                'metric': 2570240,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::5c00:80ff:fe02:7',
                                            'updated': '3w3d',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'active': True,
                                'source_protocol': 'local',
                                'source_protocol_codes': 'L',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Loopback0': {
                                            'outgoing_interface': 'Loopback0',
                                        },
                                    },
                                },
                            },
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'active': True,
                                'route_preference': 90,
                                'metric': 10880,
                                'source_protocol': 'eigrp',
                                'source_protocol_codes': 'D',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'next_hop': 'fe80::f816:3eff:fe76:b56d',
                                            'updated': '5d16h',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0.90',
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


    showRouteOpsOutput_custom = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.23.90.0/24': {
                                'active': True,
                                'metric': 0,
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        }
                                    }
                                },
                                'route': '10.23.90.0/24',
                            }
                        }
                    }
                }
            },
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.23.90.0/24': {
                                'active': True,
                                'metric': 0,
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/1.90': {
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1.90',
                                        },
                                    },
                                },
                                'route': '10.23.90.0/24',
                            },
                        },
                    },
                },
            },
        },
    }
