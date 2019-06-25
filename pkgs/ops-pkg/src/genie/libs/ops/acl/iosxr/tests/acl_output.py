'''ACL Genie Ops Object Outputs for IOSXR.'''


class AclOutput(object):

    ShowAclEthernetServices = {
        'eth_acl': {
            'name': 'eth_acl',
            'type': 'eth-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'any',
                                'source_mac_address': 'any',
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        },
                    },
                },
            },
        'mac_acl': {
            'name': 'mac_acl',
            'type': 'eth-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'host 0000.0000.0000',
                                'source_mac_address': 'host 0000.0000.0000',
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        },
                    },
                20: {
                    'name': '20',
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'host 0000.0000.0000',
                                'source_mac_address': 'host 0000.0000.0000',
                                'ether_type': '8041',
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'deny',
                        },
                    },
                30: {
                    'name': '30',
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'host 0000.0000.0000',
                                'source_mac_address': 'host 0000.0000.0000',
                                'vlan': 10,
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'deny',
                        },
                    },
                40: {
                    'name': '40',
                    'matches': {
                        'l2': {
                            'eth': {
                                'destination_mac_address': 'host bbbb.bbbb.bbbb',
                                'source_mac_address': 'host aaaa.aaaa.aaaa',
                                'ether_type': '80f3',
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        },
                    },
                },
            },
        }
        
    ShowAclAfiAll = {
        'acl_name': {
            'name': 'acl_name',
            'type': 'ipv4-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                },
            },
        'ipv4_acl': {
            'name': 'ipv4_acl',
            'type': 'ipv4-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
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
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                20: {
                    'name': '20',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                        },
                                    },
                                },
                            },
                        'l4': {
                            'tcp': {
                                'destination_port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 'ssh',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                30: {
                    'name': '30',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
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
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                },
            },
        'test22': {
            'name': 'test22',
            'type': 'ipv4-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    '192.168.1.0 0.0.0.255': {
                                        'source_ipv4_network': '192.168.1.0 0.0.0.255',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    '192.168.1.0 0.0.0.255': {
                                        'destination_ipv4_network': 'host 10.4.1.1',
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
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                        },
                    },
                20: {
                    'name': '20',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'host 10.16.2.2': {
                                        'source_ipv4_network': 'host 10.16.2.2',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'host 10.16.2.2': {
                                        'destination_ipv4_network': 'any',
                                        },
                                    },
                                'precedence': 'network',
                                'ttl': 255,
                                'ttl_operator': 'eq',
                                },
                            },
                        'l4': {
                            'tcp': {
                                'source-port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': 'www',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                30: {
                    'name': '30',
                    'matches': {
                        'l3': {
                            'ipv4': {
                                'source_ipv4_network': {
                                    'any': {
                                        'source_ipv4_network': 'any',
                                        },
                                    },
                                'destination_ipv4_network': {
                                    'any': {
                                        'destination_ipv4_network': 'any',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'deny',
                        'logging': 'log-none',
                        },
                    },
                },
            },
        'ipv6_acl': {
            'name': 'ipv6_acl',
            'type': 'ipv6-acl-type',
            'aces': {
                10: {
                    'name': '10',
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                        },
                                    },
                                'destination_ipv6_network': {
                                    'any': {
                                        'destination_ipv6_network': 'any',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-syslog',
                        },
                    },
                20: {
                    'name': '20',
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'source_ipv6_network': {
                                    'host 2001::1': {
                                        'source_ipv6_network': 'host 2001::1',
                                        },
                                    },
                                'destination_ipv6_network': {
                                    'host 2001::1': {
                                        'destination_ipv6_network': 'host 2001:1::2',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                30: {
                    'name': '30',
                    'matches': {
                        'l3': {
                            'ipv6': {
                                'source_ipv6_network': {
                                    'any': {
                                        'source_ipv6_network': 'any',
                                        },
                                    },
                                'destination_ipv6_network': {
                                    'any': {
                                        'destination_ipv6_network': 'host 2001:2::2',
                                        },
                                    },
                                },
                            },
                        'l4': {
                            'tcp': {
                                'source-port': {
                                    'operator': {
                                        'operator': 'eq',
                                        'port': '8443',
                                        },
                                    },
                                },
                            },
                        },
                    'actions': {
                        'forwarding': 'permit',
                        'logging': 'log-none',
                        },
                    },
                },
            },
        }
        
    aclOutput = {
        'acls': {
            'ipv6_acl': {
                'name': 'ipv6_acl',
                'type': 'ipv6-acl-type',
                'aces': {
                    30: {
                        'name': '30',
                        'actions': {
                            'logging': 'log-none',
                            'forwarding': 'accept',
                            },
                        'matches': {
                            'l3': {
                                'ipv6': {
                                    'destination_ipv6_network': {
                                        'any': {
                                            'destination_ipv6_network': 'host 2001:2::2',
                                            },
                                        },
                                    'source_ipv6_network': {
                                        'any': {
                                            'source_ipv6_network': 'any',
                                            },
                                        },
                                    },
                                },
                            'l4': {
                                'tcp': {
                                    'source-port': {
                                        'operator': {
                                            'operator': 'eq',
                                            'port': '8443',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    20: {
                        'name': '20',
                        'actions': {
                            'logging': 'log-none',
                            'forwarding': 'accept',
                            },
                        'matches': {
                            'l3': {
                                'ipv6': {
                                    'destination_ipv6_network': {
                                        'host 2001::1': {
                                            'destination_ipv6_network': 'host 2001:1::2',
                                            },
                                        },
                                    'source_ipv6_network': {
                                        'host 2001::1': {
                                            'source_ipv6_network': 'host 2001::1',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    10: {
                        'name': '10',
                        'actions': {
                            'logging': 'log-syslog',
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
                                    'source_ipv6_network': {
                                        'any': {
                                            'source_ipv6_network': 'any',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            'test22': {
                'name': 'test22',
                'type': 'ipv4-acl-type',
                'aces': {
                    30: {
                        'name': '30',
                        'actions': {
                            'logging': 'log-none',
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
                                    'source_ipv4_network': {
                                        'any': {
                                            'source_ipv4_network': 'any',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    20: {
                        'name': '20',
                        'actions': {
                            'logging': 'log-none',
                            'forwarding': 'accept',
                            },
                        'matches': {
                            'l3': {
                                'ipv4': {
                                    'ttl': 255,
                                    'ttl_operator': 'eq',
                                    'precedence': 'network',
                                    'destination_ipv4_network': {
                                        'host 10.16.2.2': {
                                            'destination_ipv4_network': 'any',
                                            },
                                        },
                                    'source_ipv4_network': {
                                        'host 10.16.2.2': {
                                            'source_ipv4_network': 'host 10.16.2.2',
                                            },
                                        },
                                    },
                                },
                            'l4': {
                                'tcp': {
                                    'source-port': {
                                        'operator': {
                                            'operator': 'eq',
                                            'port': 'www',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    10: {
                        'name': '10',
                        'actions': {
                            'logging': 'log-syslog',
                            'forwarding': 'accept',
                            },
                        'matches': {
                            'l3': {
                                'ipv4': {
                                    'destination_ipv4_network': {
                                        '192.168.1.0 0.0.0.255': {
                                            'destination_ipv4_network': 'host 10.4.1.1',
                                            },
                                        },
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
                        },
                    },
                },
            'ipv4_acl': {
                'name': 'ipv4_acl',
                'type': 'ipv4-acl-type',
                'aces': {
                    30: {
                        'name': '30',
                        'actions': {
                            'logging': 'log-none',
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
                        },
                    20: {
                        'name': '20',
                        'actions': {
                            'logging': 'log-none',
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
                                            'port': 'ssh',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    10: {
                        'name': '10',
                        'actions': {
                            'logging': 'log-none',
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
                        },
                    },
                },
            'acl_name': {
                'name': 'acl_name',
                'type': 'ipv4-acl-type',
                'aces': {
                    10: {
                        'name': '10',
                        'actions': {
                            'logging': 'log-none',
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
                                    'source_ipv4_network': {
                                        'any': {
                                            'source_ipv4_network': 'any',
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            'mac_acl': {
                'name': 'mac_acl',
                'type': 'eth-acl-type',
                'aces': {
                    40: {
                        'name': '40',
                        'matches': {
                            'l2': {
                                'eth': {
                                    'destination_mac_address': 'host bbbb.bbbb.bbbb',
                                    'source_mac_address': 'host aaaa.aaaa.aaaa',
                                    'ether_type': 'aarp',
                                    },
                                },
                            },
                        'actions': {
                            'forwarding': 'accept',
                            },
                        },
                    30: {
                        'name': '30',
                        'matches': {
                            'l2': {
                                'eth': {
                                    'destination_mac_address': 'host 0000.0000.0000',
                                    'source_mac_address': 'host 0000.0000.0000',
                                    },
                                },
                            },
                        'actions': {
                            'forwarding': 'drop',
                            },
                        },
                    20: {
                        'name': '20',
                        'matches': {
                            'l2': {
                                'eth': {
                                    'destination_mac_address': 'host 0000.0000.0000',
                                    'source_mac_address': 'host 0000.0000.0000',
                                    'ether_type': '8041',
                                    },
                                },
                            },
                        'actions': {
                            'forwarding': 'drop',
                            },
                        },
                    10: {
                        'name': '10',
                        'matches': {
                            'l2': {
                                'eth': {
                                    'destination_mac_address': 'host 0000.0000.0000',
                                    'source_mac_address': 'host 0000.0000.0000',
                                    },
                                },
                            },
                        'actions': {
                            'forwarding': 'accept',
                            },
                        },
                    },
                },
            'eth_acl': {
                'name': 'eth_acl',
                'type': 'eth-acl-type',
                'aces': {
                    10: {
                        'name': '10',
                        'matches': {
                            'l2': {
                                'eth': {
                                    'destination_mac_address': 'any',
                                    'source_mac_address': 'any',
                                    },
                                },
                            },
                        'actions': {
                            'forwarding': 'accept',
                            },
                        },
                    },
                },
            },
        }