'''LLDP Genie Ops Object Outputs for IOSXE.'''


class LldpOutput(object):

    ShowLldp = {
        "hello_timer": 30,
        "enabled": True,
        "hold_timer": 120,
        "status": "active",
        "reinit_timer": 2

    }
    
    ShowLldpEntry = {
        'interfaces': {
            'GigabitEthernet2/0/15': {
                'if_name': 'GigabitEthernet2/0/15',
                'port_id': {
                    'GigabitEthernet1/0/4': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/4',
                                'port_description': 'GigabitEthernet1/0/4',
                                'system_name': 'R5',
                                'time_remaining': 112,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/16': {
                'if_name': 'GigabitEthernet1/0/16',
                'port_id': {
                    'GigabitEthernet1/0/2': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/2',
                                'port_description': 'GigabitEthernet1/0/2',
                                'system_name': 'R5',
                                'time_remaining': 111,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/17': {
                'if_name': 'GigabitEthernet1/0/17',
                'port_id': {
                    'GigabitEthernet1/0/3': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/3',
                                'port_description': 'GigabitEthernet1/0/3',
                                'system_name': 'R5',
                                'time_remaining': 108,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/15': {
                'if_name': 'GigabitEthernet1/0/15',
                'port_id': {
                    'GigabitEthernet1/0/1': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/1',
                                'port_description': 'GigabitEthernet1/0/1',
                                'system_name': 'R5',
                                'time_remaining': 108,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            },
        'total_entries': 4,
        }

    ShowLldpNeighborsDetail = {
        'interfaces': {
            'GigabitEthernet2/0/15': {
                'if_name': 'GigabitEthernet2/0/15',
                'port_id': {
                    'GigabitEthernet1/0/4': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/4',
                                'port_description': 'GigabitEthernet1/0/4',
                                'system_name': 'R5',
                                'time_remaining': 101,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/16': {
                'if_name': 'GigabitEthernet1/0/16',
                'port_id': {
                    'GigabitEthernet1/0/2': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/2',
                                'port_description': 'GigabitEthernet1/0/2',
                                'system_name': 'R5',
                                'time_remaining': 99,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/17': {
                'if_name': 'GigabitEthernet1/0/17',
                'port_id': {
                    'GigabitEthernet1/0/3': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/3',
                                'port_description': 'GigabitEthernet1/0/3',
                                'system_name': 'R5',
                                'time_remaining': 94,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            'GigabitEthernet1/0/15': {
                'if_name': 'GigabitEthernet1/0/15',
                'port_id': {
                    'GigabitEthernet1/0/1': {
                        'neighbors': {
                            'R5': {
                                'neighbor_id': 'R5',
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/1',
                                'port_description': 'GigabitEthernet1/0/1',
                                'system_name': 'R5',
                                'time_remaining': 98,
                                'capabilities': {
                                    'mac_bridge': {
                                        'name': 'mac_bridge',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True,
                                        },
                                    },
                                'management_address': '10.9.1.1',
                                'auto_negotiation': 'supported, enabled',
                                'physical_media_capabilities': ['1000baseT(FD)', '100base-TX(FD)', '100base-TX(HD)', '10base-T(FD)', '10base-T(HD)'],
                                'unit_type': 30,
                                'vlan_id': 1,
                                },
                            },
                        },
                    },
                },
            },
        'total_entries': 4,
        }

    ShowLldpTraffic = {
        "frame_in": 13315,
        "frame_out": 20372,
        "frame_error_in": 0,
        "frame_discard": 14,
        "tlv_discard": 0,
        'tlv_unknown': 0,
        'entries_aged_out': 34
    }

    ShowLldpInterface = {
        'interfaces': {
            'GigabitEthernet1/0/15': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet1/0/16': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet1/0/17': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
            'GigabitEthernet2/0/15': {
                'tx': 'enabled',
                'rx': 'enabled',
                'tx_state': 'idle',
                'rx_state': 'wait for frame',
            },
        }        
    }

    Lldp_info = {
        'enabled': True,
        'hello_timer': 30,
        'hold_timer': 120,
        'counters': {
            'frame_in': 13315,
            'frame_out': 20372,
            'frame_error_in': 0,
            'frame_discard': 14,
            'tlv_discard': 0,
            'tlv_unknown': 0,
            'entries_aged_out': 34,
            },
        'interfaces': {
            'GigabitEthernet1/0/15': {
                'if_name': 'GigabitEthernet1/0/15',
                'port_id': {
                    'GigabitEthernet1/0/1': {
                        'neighbors': {
                            'R5': {
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/1',
                                'neighbor_id': 'R5',
                                'system_name': 'R5',
                                'port_description': 'GigabitEthernet1/0/1',
                                'management_address': '10.9.1.1',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        'name': 'router',
                                        },
                                    'mac_bridge': {
                                        'enabled': True,
                                        'name': 'mac_bridge',
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            'GigabitEthernet1/0/17': {
                'if_name': 'GigabitEthernet1/0/17',
                'port_id': {
                    'GigabitEthernet1/0/3': {
                        'neighbors': {
                            'R5': {
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/3',
                                'neighbor_id': 'R5',
                                'system_name': 'R5',
                                'port_description': 'GigabitEthernet1/0/3',
                                'management_address': '10.9.1.1',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        'name': 'router',
                                        },
                                    'mac_bridge': {
                                        'enabled': True,
                                        'name': 'mac_bridge',
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            'GigabitEthernet1/0/16': {
                'if_name': 'GigabitEthernet1/0/16',
                'port_id': {
                    'GigabitEthernet1/0/2': {
                        'neighbors': {
                            'R5': {
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/2',
                                'neighbor_id': 'R5',
                                'system_name': 'R5',
                                'port_description': 'GigabitEthernet1/0/2',
                                'management_address': '10.9.1.1',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        'name': 'router',
                                        },
                                    'mac_bridge': {
                                        'enabled': True,
                                        'name': 'mac_bridge',
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            'GigabitEthernet2/0/15': {
                'if_name': 'GigabitEthernet2/0/15',
                'port_id': {
                    'GigabitEthernet1/0/4': {
                        'neighbors': {
                            'R5': {
                                'chassis_id': '843d.c638.b980',
                                'port_id': 'GigabitEthernet1/0/4',
                                'neighbor_id': 'R5',
                                'system_name': 'R5',
                                'port_description': 'GigabitEthernet1/0/4',
                                'management_address': '10.9.1.1',
                                'capabilities': {
                                    'router': {
                                        'enabled': True,
                                        'name': 'router',
                                        },
                                    'mac_bridge': {
                                        'enabled': True,
                                        'name': 'mac_bridge',
                                        },
                                    },
                                },
                            },
                        },
                    },
                'enabled': True,
                },
            },
        }
