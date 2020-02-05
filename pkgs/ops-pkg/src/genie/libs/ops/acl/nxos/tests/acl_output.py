"""ACL Genie Ops Object Outputs for NXOS."""

class AclOutput(object):
    ShowAccessLists = {
    'acl_name': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'ip',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                },
                'name': '10',
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
                                    'port': 'www',
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
                                    'port': '22',
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
                                    'port': '443',
                                },
                            },
                        },
                    },
                },
                'name': '30',
            },
        },
        'name': 'ipv4_acl',
        'type': 'ipv4-acl-type',
    },
    'ipv4_ext': {
        'name': 'ipv4_ext',
        'type': 'ipv4-acl-type',
    },
    'ipv6_acl': {
        'aces': {
            '10': {
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
                            'protocol': 'ipv6',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
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
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                '2001:1::2/128': {
                                    'destination_network': '2001:1::2/128',
                                },
                            },
                            'protocol': 'ipv6',
                            'source_network': {
                                '2001::1/128': {
                                    'source_network': '2001::1/128',
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
                },
                'matches': {
                    'l3': {
                        'ipv6': {
                            'destination_network': {
                                '2001:2::2/128': {
                                    'destination_network': '2001:2::2/128',
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
                            'source_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': '8443',
                                },
                            },
                        },
                    },
                },
                'name': '30',
            },
        },
        'name': 'ipv6_acl',
        'type': 'ipv6-acl-type',
    },
    'ipv6_acl2': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
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
                },
                'name': '10',
            },
        },
        'name': 'ipv6_acl2',
        'type': 'ipv6-acl-type',
    },
    'mac_acl': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'bbbb.cccc.dddd bbbb.cccc.dddd',
                            'ether_type': 'aarp',
                            'source_mac_address': 'aaaa.bbbb.cccc 0000.0000.0000',
                        },
                    },
                },
                'name': '10',
            },
            '20': {
                'actions': {
                    'forwarding': 'permit',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'any',
                            'source_mac_address': '0000.0000.0000 0000.0000.0000',
                        },
                    },
                },
                'name': '20',
            },
            '30': {
                'actions': {
                    'forwarding': 'deny',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'aaaa.bbbb.cccc 0000.0000.0000',
                            'source_mac_address': '0000.0000.0000 0000.0000.0000',
                            'mac_protocol_number': '0x8041',
                        },
                    },
                },
                'name': '30',
            },
            '40': {
                'actions': {
                    'forwarding': 'deny',
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
                'name': '40',
            },
            '50': {
                'actions': {
                    'forwarding': 'permit',
                },
                'matches': {
                    'l2': {
                        'eth': {
                            'destination_mac_address': 'any',
                            'ether_type': 'aarp',
                            'source_mac_address': 'aaaa.aaaa.aaaa ffff.ffff.0000',
                        },
                    },
                },
                'name': '50',
            },
        },
        'name': 'mac_acl',
        'type': 'eth-acl-type',
    },
    'test22': {
        'aces': {
            '10': {
                'actions': {
                    'forwarding': 'permit',
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                '10.4.1.1/32': {
                                    'destination_network': '10.4.1.1/32',
                                },
                            },
                            'protocol': 'tcp',
                            'source_network': {
                                '192.168.1.0 0.0.0.255': {
                                    'source_network': '192.168.1.0 0.0.0.255',
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
                                '10.16.2.2/32': {
                                    'source_network': '10.16.2.2/32',
                                },
                            },
                            'ttl': 255,
                        },
                    },
                    'l4': {
                        'tcp': {
                            'source_port': {
                                'operator': {
                                    'operator': 'eq',
                                    'port': 'www',
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
                },
                'matches': {
                    'l3': {
                        'ipv4': {
                            'destination_network': {
                                'any': {
                                    'destination_network': 'any',
                                },
                            },
                            'protocol': 'ip',
                            'source_network': {
                                'any': {
                                    'source_network': 'any',
                                },
                            },
                        },
                    },
                },
                'name': '30',
            },
        },
        'name': 'test22',
        'type': 'ipv4-acl-type',
    },
}
    ShowAccessListsSummary = {
    'acl': {
        'acl_name': {
            'total_aces_configured': 1,
        },
        'ipv4_ext': {
            'total_aces_configured': 0,
        },
    },
    'attachment_points': {
        'Ethernet1/1': {
            'egress': {
                'ipv4_acl': {
                    'total_aces_configured': 3,
                    'active': True,
                    'name': 'ipv4_acl',
                    'type': 'Router ACL',
                },
                'ipv6_acl2': {
                    'total_aces_configured': 1,
                    'active': True,
                    'name': 'ipv6_acl2',
                    'type': 'Router ACL',
                },
            },
            'ingress': {
                'ipv6_acl': {
                    'total_aces_configured': 3,
                    'active': True,
                    'name': 'ipv6_acl',
                    'type': 'Router ACL',
                },
                'mac_acl': {
                    'total_aces_configured': 5,
                    'active': True,
                    'name': 'mac_acl',
                    'type': 'Port ACL',
                },
                'test22': {
                    'total_aces_configured': 3,
                    'active': True,
                    'name': 'test22',
                    'type': 'Router ACL',
                },
            },
            'interface_id': 'Ethernet1/1',
        },
    },
}

    aclOutput = {
    'acls': {
        'acl_name': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'ip',
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
            },
            'name': 'acl_name',
            'type': 'ipv4-acl-type',
        },
        'ipv4_acl': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
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
                                        'port': 'www',
                                    },
                                },
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'accept',
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
                                        'port': '22',
                                    },
                                },
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'accept',
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
                                        'port': '443',
                                    },
                                },
                            },
                        },
                    },
                    'name': '30',
                },
            },
            'name': 'ipv4_acl',
            'type': 'ipv4-acl-type',
        },
        'ipv4_ext': {
            'name': 'ipv4_ext',
            'type': 'ipv4-acl-type',
        },
        'ipv6_acl': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
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
                                'protocol': 'ipv6',
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                    },
                                },
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    '2001:1::2/128': {
                                        'destination_ipv6_network': '2001:1::2/128',
                                    },
                                },
                                'protocol': 'ipv6',
                                'source_ipv6_network': {
                                    '2001::1/128': {
                                        'source_ipv6_network': '2001::1/128',
                                    },
                                },
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'destination_ipv6_network': {
                                    '2001:2::2/128': {
                                        'destination_ipv6_network': '2001:2::2/128',
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
                    },
                    'name': '30',
                },
            },
            'name': 'ipv6_acl',
            'type': 'ipv6-acl-type',
        },
        'ipv6_acl2': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
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
                    },
                    'name': '10',
                },
            },
            'name': 'ipv6_acl2',
            'type': 'ipv6-acl-type',
        },
        'mac_acl': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'bbbb.cccc.dddd bbbb.cccc.dddd',
                                'ether_type': 'aarp',
                                'source_mac_address': 'aaaa.bbbb.cccc 0000.0000.0000',
                            },
                        },
                    },
                    'name': '10',
                },
                '20': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'source_mac_address': '0000.0000.0000 0000.0000.0000',
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'drop',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'aaaa.bbbb.cccc 0000.0000.0000',
                                'source_mac_address': '0000.0000.0000 0000.0000.0000',
                            },
                        },
                    },
                    'name': '30',
                },
                '40': {
                    'actions': {
                        'forwarding': 'drop',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'source_mac_address': 'any',
                            },
                        },
                    },
                    'name': '40',
                },
                '50': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'ether_type': 'aarp',
                                'source_mac_address': 'aaaa.aaaa.aaaa ffff.ffff.0000',
                            },
                        },
                    },
                    'name': '50',
                },
            },
            'name': 'mac_acl',
            'type': 'eth-acl-type',
        },
        'test22': {
            'aces': {
                '10': {
                    'actions': {
                        'forwarding': 'accept',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    '10.4.1.1/32': {
                                        'destination_ipv4_network': '10.4.1.1/32',
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
                        'forwarding': 'accept',
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
                                    '10.16.2.2/32': {
                                        'source_ipv4_network': '10.16.2.2/32',
                                    },
                                },
                                'ttl': 255,
                            },
                        },
                    },
                    'name': '20',
                },
                '30': {
                    'actions': {
                        'forwarding': 'drop',
                    },
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                    },
                                },
                                'protocol': 'ip',
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
            },
            'name': 'test22',
            'type': 'ipv4-acl-type',
        },
    },
    'attachment_points': {
        'Ethernet1/1': {
            'egress': {
                'acl_sets': {
                    'ipv4_acl': {
                        'name': 'ipv4_acl',
                    },
                    'ipv6_acl2': {
                        'name': 'ipv6_acl2',
                    },
                },
            },
            'ingress': {
                'acl_sets': {
                    'ipv6_acl': {
                        'name': 'ipv6_acl',
                    },
                    'mac_acl': {
                        'name': 'mac_acl',
                    },
                    'test22': {
                        'name': 'test22',
                    },
                },
            },
            'interface_id': 'Ethernet1/1',
        },
    },
}