'''
 Nd Genie Ops Object Outputs for NXOS.
'''

class NdOutput(object):

    showIpv6NeighborDetail = {
        'interfaces':{
            'Ethernet1/1':{
                'interface': 'Ethernet1/1',
                'neighbors': {
                    '2001:db8:c56d:4::2': {
                        'ip': '2001:db8:c56d:4::2',
                        'link_layer_address': 'fa16.3e82.6320',
                        'age': '00:09:27',
                        'preference': 50,
                        'origin': 'other',
                        'physical_interface': 'Ethernet1/1',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/2':{
                'interface': 'Ethernet1/2',
                'neighbors':{
                    '2001:db8:c8d1:4::33': {
                        'ip': '2001:db8:c8d1:4::33',
                        'link_layer_address': 'aaaa.bbbb.cccc',
                        'age': '2d15h',
                        'preference': 1,
                        'origin': 'static',
                        'physical_interface': 'Ethernet1/2',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
        },
    }
    showIpv6NdInterface = {
        "vrf": {
            "vrf1": {
                "interfaces": {
                    "Ethernet1/2": {
                        "router_advertisement": {
                            "default_router_preference": "medium",
                            "interval": 600,
                            "retrans_timer": 0,
                            "suppress_mtu": False,
                            "current_hop_limit": 64,
                            "reachable_time": 0,
                            "mtu": 1500,
                            "suppress": False,
                            "other_stateful_configuration": False,
                            "suppress_route_information": False,
                            "lifetime": 1800,
                            "managed_address_configuration": False
                        },
                        "oper_status": "up",
                        "neighbor_solicitation": {
                            "interval": 1000,
                            "retry_interval": 1000,
                            "retry_base": 1,
                            "retry_attempts": 3
                        },
                        "dad": {
                            "maximum_attempts": 1,
                            "current_attempt": 1
                        },
                        "local_address": "fe80::5c01:c0ff:fe02:7",
                        "error_message": {
                            "unreachables": False,
                            "redirects": True
                        },
                        "enable": True,
                        "link_status": "up",
                        "ip": "2001:db8:c8d1:4::3/64",
                        "mac_extract": "disabled",
                        "active_timers": {
                            "last_router_advertisement": "00:05:42",
                            "last_neighbor_advertisement": "00:01:07",
                            "last_neighbor_solicitation": "00:09:34",
                            "next_router_advertisement": "00:01:46"
                        },
                        "interface": "Ethernet1/2"
                    },
                }
            },
            "default": {
                "interfaces": {
                    "Ethernet1/1": {
                        "router_advertisement": {
                            "default_router_preference": "medium",
                            "interval": 201,
                            "retrans_timer": 0,
                            "suppress_mtu": False,
                            "current_hop_limit": 64,
                            "reachable_time": 0,
                            "mtu": 1500,
                            "suppress": True,
                            "other_stateful_configuration": False,
                            "suppress_route_information": False,
                            "lifetime": 1801,
                            "managed_address_configuration": False
                        },
                        "oper_status": "up",
                        "neighbor_solicitation": {
                            "interval": 1000,
                            "retry_interval": 1000,
                            "retry_base": 1,
                            "retry_attempts": 3
                        },
                        "dad": {
                            "maximum_attempts": 1,
                            "current_attempt": 1
                        },
                        "local_address": "fe80::5c01:c0ff:fe02:7",
                        "error_message": {
                            "unreachables": False,
                            "redirects": True
                        },
                        "enable": True,
                        "link_status": "up",
                        "ip": "2001:db8:c56d:4::3/64",
                        "mac_extract": "disabled",
                        "active_timers": {
                            "last_router_advertisement": "1d18h",
                            "last_neighbor_advertisement": "00:02:12",
                            "last_neighbor_solicitation": "00:06:16",
                            "next_router_advertisement": "0.000000"
                        },
                        "interface": "Ethernet1/1"
                    },
                }
            }
        }
    }
    showIpv6IcmpNeighborDetail = {
        "interfaces": {
            "Ethernet1/2": {
                "neighbors": {
                    "2001:db8:c8d1:4::33": {
                        "neighbor_state": "stale",
                        "age": "00:03:30",
                        "ip": "2001:db8:c8d1:4::33",
                        "link_layer_address": "fa16.3e8b.59c9",
                        "physical_interface": "Ethernet1/2"
                    },
                },
                "interface": "Ethernet1/2"
            },
            "Ethernet1/1": {
                "neighbors": {
                    "2001:db8:c56d:4::2": {
                        "neighbor_state": "stale",
                        "age": "00:15:02",
                        "ip": "2001:db8:c56d:4::2",
                        "link_layer_address": "fa16.3e82.6320",
                        "physical_interface": "Ethernet1/1"
                    }
                },
                "interface": "Ethernet1/1"
            },
        }
    }
    showIpv6Routers = {
        "interfaces": {
            "Ethernet1/1": {
                "neighbors": {
                    "2001:db8:c56d:4::2": {
                        "autonomous_flag": 1,
                        "homeagent_flag": 0,
                        "valid_lifetime": 2592000,
                        "is_router": True,
                        "addr_flag": 0,
                        "ip": "2001:db8:c56d:4::2",
                        "lifetime": 1800,
                        "onlink_flag": 1,
                        "current_hop_limit": 64,
                        "prefix": "2001:db8:c56d:4::/64",
                        "retransmission_time": 0,
                        "preferred_lifetime": 604800,
                        "last_update": "3.2",
                        "mtu": 1500,
                        "preference": "medium",
                        "other_flag": 0,
                        "reachable_time": 0
                    }
                },
                "interface": "Ethernet1/1"
            },
            "Ethernet1/2": {
                "neighbors": {
                    "2001:db8:c8d1:4::33": {
                        "autonomous_flag": 1,
                        "homeagent_flag": 0,
                        "valid_lifetime": 2592000,
                        "is_router": True,
                        "addr_flag": 0,
                        "ip": "2001:db8:c8d1:4::33",
                        "lifetime": 1800,
                        "onlink_flag": 1,
                        "current_hop_limit": 64,
                        "prefix": "2001:db8:c8d1:4::/64",
                        "retransmission_time": 0,
                        "preferred_lifetime": 604800,
                        "last_update": "1.5",
                        "mtu": 1500,
                        "preference": "medium",
                        "other_flag": 0,
                        "reachable_time": 0
                    }
                },
                "interface": "Ethernet1/2"
            }
        }
    }

    ndOpsOutput = {
        'interfaces':{
            'Ethernet1/1':{
                'interface': 'Ethernet1/1',
                "router_advertisement": {
                    "interval": 201,
                    "suppress": True,
                    "lifetime": 1801,
                },
                'neighbors': {
                    '2001:db8:c56d:4::2': {
                        'ip': '2001:db8:c56d:4::2',
                        'link_layer_address': 'fa16.3e82.6320',
                        'age': '00:09:27',
                        'origin': 'other',
                        "is_router": True,
                        "neighbor_state": "stale",
                    },
                },
            },
            'Ethernet1/2':{
                'interface': 'Ethernet1/2',
                "router_advertisement": {
                    "interval": 600,
                    "suppress": False,
                    "lifetime": 1800,
                },
                'neighbors':{
                    '2001:db8:c8d1:4::33': {
                        'ip': '2001:db8:c8d1:4::33',
                        'link_layer_address': 'aaaa.bbbb.cccc',
                        'age': '2d15h',
                        'origin': 'static',
                        "is_router": True,
                        "neighbor_state": "stale",
                    },
                },
            },
        },
    }

    showIpv6NeighborDetail_custom = {
        'adjacency_hit': {
            'INVALID': {
                'packet_count': 0,
                'byte_count': 0,
            },
            'GLOBAL DROP': {
                'packet_count': 0,
                'byte_count': 0,
            },
            'GLOBAL PUNT': {
                'packet_count': 0,
                'byte_count': 0,
            },
            'GLOBAL GLEAN': {
                'packet_count': 0,
                'byte_count': 0,
            },
            'GLEAN': {
                'packet_count': 0,
                'byte_count': 0,
            },
            'NORMAL': {
                'packet_count': 0,
                'byte_count': 0,
            },
        },
        'adjacency_statistics_last_updated_before': 'never',
        'total_number_of_entries': 5,
        'interfaces': {
            'Ethernet1/1.390': {
                'interface': 'Ethernet1/1.390',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'age': '00:08:47',
                        'link_layer_address': 'fa16.3e59.8f2e',
                        'origin': 'other',
                        'preference': 50,
                        'physical_interface': 'Ethernet1/1.390',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/1.410': {
                'interface': 'Ethernet1/1.410',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'age': '00:00:45',
                        'link_layer_address': 'fa16.3e59.8f2e',
                        'origin': 'other',
                        'preference': 50,
                        'physical_interface': 'Ethernet1/1.410',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/2.390': {
                'interface': 'Ethernet1/2.390',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'age': '3w0d',
                        'link_layer_address': 'fa16.3e5b.cf97',
                        'origin': 'other',
                        'preference': 50,
                        'physical_interface': 'Ethernet1/2.390',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/2.415': {
                'interface': 'Ethernet1/2.415',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'age': '3w0d',
                        'link_layer_address': 'fa16.3e5b.cf97',
                        'origin': 'other',
                        'preference': 50,
                        'physical_interface': 'Ethernet1/2.415',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/2.420': {
                'interface': 'Ethernet1/2.420',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'age': '02:30:05',
                        'link_layer_address': 'fa16.3e5b.cf97',
                        'origin': 'static',
                        'preference': 50,
                        'physical_interface': 'Ethernet1/2.420',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
        },
    }
    showIpv6NdInterface_custom = {
        'vrf': {
            'VRF1': {
                'interfaces': {
                    'Ethernet1/2.420': {
                        'interface': 'Ethernet1/2.420',
                        'oper_status': 'up',
                        'link_status': 'up',
                        'enable': True,
                        'ip': '2001:10:13:120::3/64',
                        'local_address': 'fe80::5c00:40ff:fe02:7',
                        'mac_extract': 'disabled',
                        'active_timers': {
                            'last_neighbor_solicitation': '00:12:56',
                            'last_neighbor_advertisement': '00:12:51',
                            'last_router_advertisement': '00:06:28',
                            'next_router_advertisement': '00:01:06',
                        },
                        'router_advertisement': {
                            'interval': 600,
                            'managed_address_configuration': False,
                            'other_stateful_configuration': False,
                            'default_router_preference': 'medium',
                            'current_hop_limit': 64,
                            'mtu': 1500,
                            'lifetime': 1800,
                            'reachable_time': 0,
                            'retrans_timer': 0,
                            'suppress': False,
                            'suppress_mtu': False,
                            'suppress_route_information': False,
                        },
                        'neighbor_solicitation': {
                            'interval': 1000,
                            'retry_base': 1,
                            'retry_interval': 1000,
                            'retry_attempts': 3,
                        },
                        'error_message': {
                            'redirects': True,
                            'unreachables': False,
                        },
                        'dad': {
                            'maximum_attempts': 1,
                            'current_attempt': 1,
                        },
                    },
                },
            },
        },
    }
    showIpv6IcmpNeighborDetail_custom = {
        'interfaces': {
            'Ethernet1/2.420': {
                'interface': 'Ethernet1/2.420',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'link_layer_address': 'fa16.3e5b.cf97',
                        'neighbor_state': 'stale',
                        'age': '00:14:18',
                        'physical_interface': 'Ethernet1/2.420',
                    },
                },
            },
        },
    }
    showIpv6Routers_custom = {
        'interfaces': {
            'Ethernet1/1.390': {
                'interface': 'Ethernet1/1.390',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'is_router': True,
                        'last_update': '2.2',
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:23:90::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/1.410': {
                'interface': 'Ethernet1/1.410',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'is_router': True,
                        'last_update': '0.6',
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:23:110::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/1.415': {
                'interface': 'Ethernet1/1.415',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'is_router': True,
                        'last_update': '1.3',
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:23:115::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/1.420': {
                'interface': 'Ethernet1/1.420',
                'neighbors': {
                    'fe80::f816:3eff:fe59:8f2e': {
                        'is_router': True,
                        'last_update': '0.9',
                        'ip': 'fe80::f816:3eff:fe59:8f2e',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:23:120::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/2.390': {
                'interface': 'Ethernet1/2.390',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'is_router': True,
                        'last_update': '0.6',
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:13:90::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/2.410': {
                'interface': 'Ethernet1/2.410',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'is_router': True,
                        'last_update': '1.4',
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:13:110::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/2.415': {
                'interface': 'Ethernet1/2.415',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'is_router': True,
                        'last_update': '0.5',
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:13:115::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
            'Ethernet1/2.420': {
                'interface': 'Ethernet1/2.420',
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'is_router': True,
                        'last_update': '2.5',
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'current_hop_limit': 64,
                        'lifetime': 1800,
                        'addr_flag': 0,
                        'other_flag': 0,
                        'mtu': 1500,
                        'homeagent_flag': 0,
                        'preference': 'medium',
                        'reachable_time': 0,
                        'retransmission_time': 0,
                        'prefix': {
                            '2001:10:13:120::/64': {
                                'onlink_flag': 1,
                                'autonomous_flag': 1,
                                'valid_lifetime': 2592000,
                                'preferred_lifetime': 604800,
                            },
                        },
                    },
                },
            },
        },
    }
    ndOpsOutput_custom = {
        'interfaces': {
            'Ethernet1/2.420': {
                'interface': 'Ethernet1/2.420',
                'router_advertisement': {
                    'interval': 600,
                    'lifetime': 1800,
                    'suppress': False,
                },
                'neighbors': {
                    'fe80::f816:3eff:fe5b:cf97': {
                        'ip': 'fe80::f816:3eff:fe5b:cf97',
                        'link_layer_address': 'fa16.3e5b.cf97',
                        'origin': 'static',
                        'age': '02:30:05',
                        'is_router': True,
                        'neighbor_state': 'stale',
                    },
                },
            },
        },
    }
