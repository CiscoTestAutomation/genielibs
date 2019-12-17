'''ACL Genie Ops Object Outputs for IOSXE.'''


class AclOutput(object):

    ShowAccessLists = {
    'acl_name': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'ipv4',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'ipv4': {
                            'established': False,
                        },
                    },
                },
                'name': '10',
                'statistics': {
                    'matched_packets': 10031,
                },
            },
        },
        'name': 'acl_name',
        'type': 'ipv4-acl-type',
    },
    'ipv4_acl': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'tcp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'tcp': {
                            'destination_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 80,
                                },
                            },
                            'established': False,
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'tcp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'tcp': {
                            'destination_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 22,
                                },
                            },
                            'established': False,
                        },
                    },
                },
                'name': '20',
            },
        },
        'name': 'ipv4_acl',
        'type': 'ipv4-acl-type',
    },
    'test1': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-syslog',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'dscp': 'default',
                            'protocol': 'pim',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'pim': {
                            'established': False,
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'source_network': {
                                '0.1.1.1 255.0.0.0': {
                                    'source_network': '0.1.1.1 255.0.0.0',
                                },
                            },
                            'protocol': 'icmp',
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'icmp': {
                            'code': 66,
                            'established': False,
                            'type': 10,
                        },
                    },
                },
                'name': '20',
            },
        },
        'name': 'test1',
        'type': 'ipv4-acl-type',
    },
    'test22': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-syslog',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'source_network': {
                                '192.168.1.0 0.0.0.255': {
                                    'source_network': '192.168.1.0 0.0.0.255',
                                },
                            },
                            'protocol': 'tcp',
                            'destination_network': {
                                '10.4.1.1': {
                                    'destination_network': '10.4.1.1',
                                },
                            },
                        },
                    },
                    'l4': {
                        'tcp': {
                            'established': True,
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'precedence': 'network',
                            'protocol': 'tcp',
                            'source_network': {
                                '10.16.2.2': {
                                    'source_network': '10.16.2.2',
                                },
                            },
                            'ttl': 255,
                            'ttl_operator': 'eq',
                        },
                    },
                    'l4': {
                        'tcp': {
                            'established': False,
                            'source_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 'www telnet 443',
                                },
                            },
                        },
                    },
                },
                'name': '20',
            },
            '30': {
                'actions': {
                    'forwarding': 'deny',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'ipv4',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'ipv4': {
                            'established': False,
                        },
                    },
                },
                'name': '30',
            },
            '40': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'tcp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'tcp': {
                            'established': False,
                            'source_port': {
                                'range': {
                                    'lower_port': 20,
                                    'upper_port': 179,
                                },
                            },
                        },
                    },
                },
                'name': '40',
            },
        },
        'name': 'test22',
        'type': 'ipv4-acl-type',
    },
    'ipv6_acl': {
        'aces': {
            '20': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                '2001:1::2': {
                                    'destination_network': '2001:1::2',
                                },
                            },
                            'protocol': 'ipv6',
                            'source_network': {
                                '2001::1': {
                                    'source_network': '2001::1',
                                },
                            },
                        },
                    },
                    'l4': {
                        'ipv6': {
                            'established': False,
                        },
                    },
                },
                'name': '20',
            },
            '30': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                '2001:2::2': {
                                    'destination_network': '2001:2::2',
                                },
                            },
                            'protocol': 'tcp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'tcp': {
                            'established': False,
                            'source_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 'www 8443',
                                },
                            },
                        },
                    },
                },
                'name': '30',
            },
            '80': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-syslog',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                '2001:db8:1:1::1 2001:db8:24:24::6': {
                                    'destination_network': '2001:db8:1:1::1 2001:db8:24:24::6',
                                },
                            },
                            'protocol': 'ipv6',
                            'source_network': {
                                '2001:db8:9:9::3 2001:db8:10:10::4': {
                                    'source_network': '2001:db8:9:9::3 2001:db8:10:10::4',
                                },
                            },
                        },
                    },
                    'l4': {
                        'ipv6': {
                            'established': False,
                        },
                    },
                },
                'name': '80',
            },
        },
        'name': 'ipv6_acl',
        'type': 'ipv6-acl-type',
    },
    'preauth_v6': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'udp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'udp': {
                            'destination_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 53,
                                },
                            },
                            'established': False,
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-syslog',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'dscp': 'cs7',
                            'protocol': 'esp',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'esp': {
                            'established': False,
                        },
                    },
                },
                'name': '20',
            },
            '30': {
                'actions': {
                    'forwarding': 'deny',
                    'logging': 'log-none',
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'ipv6',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                    'l4': {
                        'ipv6': {
                            'established': False,
                        },
                    },
                },
                'name': '30',
            },
        },
        'name': 'preauth_v6',
        'per_user': True,
        'type': 'ipv6-acl-type',
    },
    'mac_acl': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'any',
                            'source_mac_address': 'any',
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'deny',
                    'logging': 'log-none',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'any',
                            'ether_type': 'msdos',
                            'source_mac_address': 'any',
                        },
                    },
                },
                'name': '20',
            },
            '30': {
                'actions': {
                    'forwarding': 'deny',
                    'logging': 'log-none',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'any',
                            'source_mac_address': 'any',
                            'vlan': 10,
                        },
                    },
                },
                'name': '30',
            },
            '40': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': '0003.0003.0003',
                            'lsap': '0x1 0xD8FE',
                            'source_mac_address': '0001.0002.0033',
                        },
                    },
                },
                'name': '40',
            },
            '50': {
                'actions': {
                    'forwarding': 'permit',
                    'logging': 'log-none',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'cos': 4,
                            'destination_mac_address': 'any',
                            'ether_type': 'aarp',
                            'source_mac_address': 'any',
                            'vlan': 20,
                        },
                    },
                },
                'name': '50',
            },
        },
        'name': 'mac_acl',
        'type': 'eth-acl-type',
    },
}

    Acl_info = {
    'acls': {
        'acl_name': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'ipv4',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '10',
                    'statistics': {
                        'matched_packets': 10031,
                    },
                },
            },
            'name': 'acl_name',
            'type': 'ipv4-acl-type',
        },
        'ipv4_acl': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'tcp',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'tcp': {
                                'destination_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 80,
                                    },
                                },
                                'established': False,
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'tcp',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'tcp': {
                                'destination_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 22,
                                    },
                                },
                                'established': False,
                            },
                        },
                    },
                    'name': '20',
                },
            },
            'name': 'ipv4_acl',
            'type': 'ipv4-acl-type',
        },
        'ipv6_acl': {
            'aces': {
                '20': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    '2001:1::2': {
                                        'destination_ipv6_network': '2001:1::2',
                                    },
                                },
                                'protocol': 'ipv6',
                                'source_ipv6_network': {
                                    '2001::1': {
                                        'source_ipv6_network': '2001::1',
                                    },
                                },
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    '2001:2::2': {
                                        'destination_ipv6_network': '2001:2::2',
                                    },
                                },
                                'protocol': 'tcp',
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'tcp': {
                                'established': False,
                                'source_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 'www 8443',
                                    },
                                },
                            },
                        },
                    },
                    'name': '30',
                },
                '80': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    '2001:db8:1:1::1 2001:db8:24:24::6': {
                                        'destination_ipv6_network': '2001:db8:1:1::1 2001:db8:24:24::6',
                                    },
                                },
                                'protocol': 'ipv6',
                                'source_ipv6_network': {
                                    '2001:db8:9:9::3 2001:db8:10:10::4': {
                                        'source_ipv6_network': '2001:db8:9:9::3 2001:db8:10:10::4',
                                    },
                                },
                            },
                        },
                    },
                    'name': '80',
                },
            },
            'name': 'ipv6_acl',
            'type': 'ipv6-acl-type',
        },
        'mac_acl': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'source_mac_address': 'any',
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'deny',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'ether_type': 'msdos',
                                'source_mac_address': 'any',
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'deny',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'source_mac_address': 'any',
                            },
                        },
                    },
                    'name': '30',
                },
                '40': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': '0003.0003.0003',
                                'source_mac_address': '0001.0002.0033',
                            },
                        },
                    },
                    'name': '40',
                },
                '50': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'ether_type': 'aarp',
                                'source_mac_address': 'any',
                            },
                        },
                    },
                    'name': '50',
                },
            },
            'name': 'mac_acl',
            'type': 'eth-acl-type',
        },
        'preauth_v6': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    'any': {
                                        'destination_ipv6_network': 'any',
                                    },
                                },
                                'protocol': 'udp',
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'udp': {
                                'destination_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 53,
                                    },
                                },
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    'any': {
                                        'destination_ipv6_network': 'any',
                                    },
                                },
                                'dscp': 'cs7',
                                'protocol': 'esp',
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'deny',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    'any': {
                                        'destination_ipv6_network': 'any',
                                    },
                                },
                                'protocol': 'ipv6',
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '30',
                },
            },
            'name': 'preauth_v6',
            'type': 'ipv6-acl-type',
        },
        'test1': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'dscp': 'default',
                                'protocol': 'pim',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'icmp',
                                'source_ipv4_network': {
                                    '0.1.1.1 255.0.0.0': {
                                        'source_ipv4_network': '0.1.1.1 255.0.0.0',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'icmp': {
                                'code': 66,
                                'type': 10,
                            },
                        },
                    },
                    'name': '20',
                },
            },
            'name': 'test1',
            'type': 'ipv4-acl-type',
        },
        'test22': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    '10.4.1.1': {
                                        'destination_ipv4_network': '10.4.1.1',
                                    },
                                },
                                'protocol': 'tcp',
                                'source_ipv4_network': {
                                    '192.168.1.0 0.0.0.255': {
                                        'source_ipv4_network': '192.168.1.0 0.0.0.255',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'tcp': {
                                'established': True,
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'precedence': 'network',
                                'protocol': 'tcp',
                                'source_ipv4_network': {
                                    '10.16.2.2': {
                                        'source_ipv4_network': '10.16.2.2',
                                    },
                                },
                                'ttl': 255,
                                'ttl_operator': 'eq',
                            },
                        },
                        'l4': {
                            'tcp': {
                                'established': False,
                                'source_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 'www telnet 443',
                                    },
                                },
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'deny',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'ipv4',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '30',
                },
                '40': {
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'tcp',
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                    },
                                },
                            },
                        },
                        'l4': {
                            'tcp': {
                                'established': False,
                                'source_port': {
                                    'range': {
                                        'lower_port': 20,
                                        'upper_port': 179,
                                    },
                                },
                            },
                        },
                    },
                    'name': '40',
                },
            },
            'name': 'test22',
            'type': 'ipv4-acl-type',
        },
    },
}