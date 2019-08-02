'''LLDP Genie Ops Object Outputs for NXOS.'''


class LldpOutput(object):
    ShowLldpTimers = {
        'hold_timer': 120,
        'reinit_timer': 2,
        'hello_timer': 30
    }

    ShowLldpAll = {
        'interfaces': {
            'Ethernet1/1':
                {'enabled': True,
                 'tx': True,
                 'rx': True,
                 'dcbx': True
                 },
            'Ethernet1/2':
                {'enabled': True,
                 'tx': True,
                 'rx': True,
                 'dcbx': False
                 }
        }
    }

    ShowLldpTlvSelect = {
        'suppress_tlv_advertisement': {
            'port_description': False,
            'system_name': False,
            'system_description': False,
            'system_capabilities': False,
            'management_address_v4': False,
            'management_address_v6': False,
            'power_management': False,
            'port_vlan': False,
            'dcbxp': False
        }
    }

    ShowLldpNeighborsDetail = {
        'total_entries': 2,
        'interfaces': {
            'Ethernet1/1': {
                'port_id': {
                    'GigabitEthernet3': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'chassis_id': '001e.49f7.2c00',
                                'port_description': 'GigabitEthernet3',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], '
                                                      'Virtual XE Software ('
                                                      'X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'time_remaining': 114,
                                'capabilities': {
                                    'bridge': {
                                        'name': 'bridge',
                                        'system': True,
                                    },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address_v4': '10.1.3.1',
                                'management_address_v6': 'not advertised',
                                'vlan_id': 'not advertised'
                            }
                        }
                    }
                }
            },
            'Ethernet1/2': {
                'port_id': {
                    'GigabitEthernet0/0/0/1': {
                        'neighbors': {
                            'R2_xrv9000': {
                                'chassis_id': '000d.bd09.46fa',
                                'system_name': 'R2_xrv9000',
                                'system_description': '6.2.2, IOS-XRv 9000',
                                'time_remaining': 95,
                                'capabilities': {
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address_v4': '10.2.3.2',
                                'management_address_v6': 'not advertised',
                                'vlan_id': 'not advertised'
                            }
                        }
                    }
                }
            }
        }
    }

    ShowLldpTraffic = {
        'counters': {
            "total_frames_received": 209,
            "total_frames_transmitted": 349,
            "total_frames_received_in_error": 0,
            "total_frames_discarded": 0,
            'total_unrecognized_tlvs': 0,
            'total_entries_aged': 0
        }
    }

    Lldp_info = {
        'hello_timer': 30,
        'hold_timer': 120,
        'suppress_tlv_advertisement': {
            'port_description': False,
            'system_name': False,
            'system_description': False,
            'system_capabilities': False,
            'management_address': False,
        },
        'counters': {
            'frame_in': 209,
            'frame_out': 349,
            'frame_error_in': 0,
            'frame_discard': 0,
            'tlv_unknown': 0,
            'entries_aged_out': 0,
        },
        'interfaces': {
            'Ethernet1/1': {
                'enabled': True,
                'if_name': 'Ethernet1/1',
                'port_id': {
                    'GigabitEthernet3': {
                        'neighbors': {
                            'R1_csr1000v.openstacklocal': {
                                'chassis_id': '001e.49f7.2c00',
                                'port_id': 'GigabitEthernet3',
                                'port_description': 'GigabitEthernet3',
                                'system_name': 'R1_csr1000v.openstacklocal',
                                'system_description': 'Cisco IOS Software [Everest], '
                                                      'Virtual XE Software ('
                                                      'X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by',
                                'capabilities': {
                                    'bridge': {
                                        'name': 'bridge',
                                        'system': True,
                                    },
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address': '10.1.3.1',
                                'management_address_type': 'ipv4',
                            },
                        },
                    },
                },
            },
            'Ethernet1/2': {
                'if_name': 'Ethernet1/2',
                'enabled': True,
                'port_id': {
                    'GigabitEthernet0/0/0/1': {
                        'neighbors': {
                            'R2_xrv9000': {
                                'chassis_id': '000d.bd09.46fa',
                                'port_id': 'GigabitEthernet0/0/0/1',
                                'system_name': 'R2_xrv9000',
                                'system_description': '6.2.2, IOS-XRv 9000',
                                'capabilities': {
                                    'router': {
                                        'name': 'router',
                                        'system': True,
                                        'enabled': True
                                    }
                                },
                                'management_address': '10.2.3.2',
                                'management_address_type': 'ipv4',
                            },
                        },
                    },
                },
            },

        }
    }
