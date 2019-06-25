'''
 StaticRoute Genie Ops Object Outputs for IOSXR.
'''

class StaticRouteOutput(object):
    # 'show static topology detail' output

    showStaticRouteTopologyDetail = {
        'vrf': {
            'VRF1': {
                'address_family': {
                    'ipv6': {
                        'table_id': '0xe0800010',
                        'safi': 'unicast',
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'active': True,
                                            'outgoing_interface': 'Null0',
                                            'install_date': 'Dec  7 21:51:47.424',
                                            'metrics': 1234,
                                            'preference': 99,
                                            'path_version': 1,
                                            'path_status': '0x21',
                                            'tag': 0,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'active': True,
                                            'outgoing_interface': 'Null0',
                                            'install_date': 'Dec  7 21:51:47.424',
                                            'metrics': 3456,
                                            'preference': 101,
                                            'path_version': 1,
                                            'path_status': '0x21',
                                            'tag': 0,
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
                        'table_id': '0xe0800000',
                        'safi': 'unicast',
                        'routes': {
                            '2001:1:1:1::1/128': {
                                'route': '2001:1:1:1::1/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '2001:10:1:2::1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/3',
                                            'install_date': 'Dec  7 21:52:00.843',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0xa1',
                                            'tag': 0,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '2001:20:1:2::1',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0',
                                            'install_date': 'Dec  7 21:52:00.733',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0xa1',
                                            'tag': 0,
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '2001:20:2:3::3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/2',
                                            'install_date': 'Dec  7 21:52:00.763',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0xa1',
                                            'tag': 0,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '2001:10:2:3::3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1',
                                            'install_date': 'Dec  7 21:52:00.753',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0xa1',
                                            'tag': 0,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '2001:20:2:3::3',
                                            'configure_date': 'Dec  7 21:47:43.624',
                                            'metrics': 1,
                                            'preference': 3,
                                            'path_version': 0,
                                            'path_status': '0x0',
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'ipv4': {
                        'table_id': '0xe0000000',
                        'safi': 'unicast',
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/3': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/0/0/3',
                                            'install_date': 'Dec  7 21:52:00.853',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0x21',
                                            'tag': 0,
                                        },
                                        'GigabitEthernet0/0/0/0': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0',
                                            'install_date': 'Dec  7 21:52:00.733',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0x21',
                                            'tag': 0,
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.229.3.3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/2',
                                            'install_date': 'Dec  7 21:52:00.843',
                                            'metrics': 1,
                                            'preference': 1,
                                            'path_version': 1,
                                            'path_status': '0xa1',
                                            'tag': 0,

                                        },
                                        2: {
                                            'index': 2,
                                            'active': False,
                                            'next_hop': '10.229.3.3',
                                            'configure_date': 'Dec  7 21:47:43.624',
                                            'metrics': 1,
                                            'preference': 3,
                                            'path_version': 0,
                                            'path_status': '0x0',

                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '10.2.3.3',
                                            'outgoing_interface': 'GigabitEthernet0/0/0/1',
                                            'configure_date': 'Dec  7 21:47:43.624',
                                            'metrics': 1,
                                            'preference': 17,
                                            'path_version': 0,
                                            'track': 1,
                                            'path_status': '0x80',

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

    staticRouteOpsOutput = {
        'vrf': {
            'default': {
                'address_family': {
                    'ipv4': {
                        'routes': {
                            '10.4.1.1/32': {
                                'route': '10.4.1.1/32',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'GigabitEthernet0/0/0/3': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/0/0/3',
                                            'preference': 1,
                                        },
                                        'GigabitEthernet0/0/0/0': {
                                            'active': True,
                                            'outgoing_interface': 'GigabitEthernet0/0/0/0',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '10.36.3.3/32': {
                                'route': '10.36.3.3/32',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '10.229.3.3',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': False,
                                            'next_hop': '10.229.3.3',
                                            'preference': 3,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '10.2.3.3',
                                            'preference': 17,
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
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '2001:10:1:2::1',
                                            'preference': 1,

                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '2001:20:1:2::1',
                                            'preference': 1,
                                        },
                                    },
                                },
                            },
                            '2001:3:3:3::3/128': {
                                'route': '2001:3:3:3::3/128',
                                'next_hop': {
                                    'next_hop_list': {
                                        1: {
                                            'index': 1,
                                            'active': True,
                                            'next_hop': '2001:20:2:3::3',
                                            'preference': 1,
                                        },
                                        2: {
                                            'index': 2,
                                            'active': True,
                                            'next_hop': '2001:10:2:3::3',
                                            'preference': 1,
                                        },
                                        3: {
                                            'index': 3,
                                            'active': False,
                                            'next_hop': '2001:20:2:3::3',
                                            'preference': 3,
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
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'active': True,
                                            'outgoing_interface': 'Null0',
                                            'preference': 99,
                                        },
                                    },
                                },
                            },
                            '2001:2:2:2::2/128': {
                                'route': '2001:2:2:2::2/128',
                                'next_hop': {
                                    'outgoing_interface': {
                                        'Null0': {
                                            'active': True,
                                            'outgoing_interface': 'Null0',
                                            'preference': 101,

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
