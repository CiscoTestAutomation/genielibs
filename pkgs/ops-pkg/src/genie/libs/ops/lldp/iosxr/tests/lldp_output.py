'''LLDP Genie Ops Object Outputs for IOSXR.'''


class LldpOutput(object):

    ShowLldp = {
        "hello_timer": 30,
        "enabled": True,
        "hold_timer": 120,
        "status": "active",
        "reinit_delay": 2
    }
    
    ShowLldpEntry = {
        'interfaces': {
            'GigabitEthernet0/0/0/0': {
                'port_id': {
                    'GigabitEthernet2': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'chassis_id': '001e.49f7.2c00',
                                'port_description': 'GigabitEthernet2',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'neighbor_id': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'time_remaining': 117,
                                'hold_time': 120,
                                'capabilities': {
                                    'bridge': {
                                        'system': True,
                                        },
                                    'router': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.1.2.1',
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet0/0/0/1': {
                'port_id': {
                    'Ethernet1/2': {
                        'neighbors': {
                            'R3_n9kv': {
                                'chassis_id': '5e00.8002.0009',
                                'port_description': 'Ethernet1/2',
                                'system_name': 'R3_n9kv',
                                'neighbor_id': 'R3_n9kv',
                                'system_description': 'Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(1)\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.\n',
                                'time_remaining': 103,
                                'hold_time': 120,
                                'capabilities': {
                                    'bridge': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        'total_entries': 2,
        }

    ShowLldpNeighborsDetail = {
        'interfaces': {
            'GigabitEthernet0/0/0/0': {
                'port_id': {
                    'GigabitEthernet2': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'chassis_id': '001e.49f7.2c00',
                                'port_description': 'GigabitEthernet2',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'neighbor_id': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'time_remaining': 90,
                                'hold_time': 120,
                                'capabilities': {
                                    'bridge': {
                                        'system': True,
                                        },
                                    'router': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.1.2.1',
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet0/0/0/1': {
                'port_id': {
                    'Ethernet1/2': {
                        'neighbors': {
                            'R3_n9kv': {
                                'chassis_id': '5e00.8002.0009',
                                'port_description': 'Ethernet1/2',
                                'system_name': 'R3_n9kv',
                                'neighbor_id': 'R3_n9kv',
                                'system_description': 'Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(1)\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.\n',
                                'time_remaining': 106,
                                'hold_time': 120,
                                'capabilities': {
                                    'bridge': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        'total_entries': 2,
        }

    ShowLldpTraffic = {
        "counters": {
            "frame_in": 399,
            "frame_out": 588,
            "frame_error_in": 0,
            "frame_discard": 0,
            "tlv_discard": 119,
            'tlv_unknown': 119,
            'entries_aged_out': 0
        }
    }

    ShowLldpInterface = {
        'interfaces': {
            'GigabitEthernet0/0/0/0': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet0/0/0/1': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
        }        
    }

    
    lldpOutput = {
        'enabled': True,
        'hello_timer': 30,
        'hold_timer': 120,
        'interfaces': {
            'GigabitEthernet0/0/0/1': {
                'port_id': {
                    'Ethernet1/2': {
                        'neighbors': {
                            'R3_n9kv': {
                                'neighbor_id': 'R3_n9kv',
                                'system_name': 'R3_n9kv',
                                'system_description': 'Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(1)\nTAC support: http://www.cisco.com/tac\nCopyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.\n',
                                'chassis_id': '5e00.8002.0009',
                                'port_description': 'Ethernet1/2',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        },
                                    'bridge': {
                                        'enabled': True,
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            'GigabitEthernet0/0/0/0': {
                'port_id': {
                    'GigabitEthernet2': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'neighbor_id': 'R1_csr1000v.openstacklocal',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'chassis_id': '001e.49f7.2c00',
                                'port_description': 'GigabitEthernet2',
                                'management_address': '10.1.2.1',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            },
        'counters': {
            'frame_in': 399,
            'frame_out': 588,
            'frame_error_in': 0,
            'frame_discard': 0,
            'tlv_discard': 119,
            'tlv_unknown': 119,
            'entries_aged_out': 0,
            },
        }

