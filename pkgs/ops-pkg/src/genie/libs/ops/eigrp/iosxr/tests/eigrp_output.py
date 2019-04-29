'''
EIGRP Genie Ops Object Outputs for IOSXR
'''

class EigrpOutput(object):

    # 'show eigrp ipv4 neighbors detail'
	ShowEigrpIpv4NeighborsDetail = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'VRF1': {
                        'address_family': {
                            'ipv4': {
                                'name': 'test',
                                'named_mode': True,
                                'eigrp_interface': {
                                    'GigabitEthernet0/0/0/1.390': {
                                        'eigrp_nbr': {
                                            '10.23.90.3': {
                                                'peer_handle': 1,
                                                'hold': 14,
                                                'uptime': '01:41:47',
                                                'srtt': 0.004,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'last_seq_number': 15,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 8,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 1,
                                                    'tlv_minorrev': 2
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd': 'disabled',
                                                'prefixes': 3
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/0.390': {
                                        'eigrp_nbr': {
                                            '10.12.90.1': {
                                                'peer_handle': 0,
                                                'hold': 13,
                                                'uptime': '02:54:01',
                                                'srtt': 0.816,
                                                'rto': 4896,
                                                'q_cnt': 0,
                                                'last_seq_number': 8,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 0,
                                                'retry_count': 0,
                                                'bfd': 'disabled',
                                                'prefixes': 3
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # 'show eigrp ipv6 neighbors detail'
	ShowEigrpIpv6NeighborsDetail = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'VRF1': {
                        'address_family': {
                            'ipv6': {
                                'name': 'test',
                                'named_mode': True,
                                'eigrp_interface': {
                                    'GigabitEthernet0/0/0/1.390': {
                                        'eigrp_nbr': {
                                            'fe80::5c00:ff:fe02:7': {
                                                'peer_handle': 1,
                                                'hold': 11,
                                                'uptime': '01:42:44',
                                                'srtt': 0.009,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'last_seq_number': 14,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 8,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 1,
                                                    'tlv_minorrev': 2
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd': 'disabled',
                                                'prefixes': 5
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/0.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:feb4:b131': {
                                                'peer_handle': 0,
                                                'hold': 12,
                                                'uptime': '02:31:47',
                                                'srtt': 0.004,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'last_seq_number': 9,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd': 'disabled',
                                                'prefixes': 6
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

	EigrpInfo = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'VRF1': {
                        'address_family': {
                            'ipv4': {
                                'name': 'test',
                                'named_mode': True,
                                'eigrp_interface': {
                                    'GigabitEthernet0/0/0/0.390': {
                                        'eigrp_nbr': {
                                            '10.12.90.1': {
                                                'retransmit_count': 0,
                                                'retry_count': 0,
                                                'last_seq_number': 8,
                                                'srtt': 0.816,
                                                'rto': 4896,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 13,
                                                'uptime': '02:54:01',
                                                'prefixes': 3
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/1.390': {
                                        'eigrp_nbr': {
                                            '10.23.90.3': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 15,
                                                'srtt': 0.004,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 8,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 1,
                                                    'tlv_minorrev': 2
                                                },
                                                'hold': 14,
                                                'uptime': '01:41:47',
                                                'prefixes': 3
                                            }
                                        }
                                    }
                                }
                            },
                            'ipv6': {
                                'name': 'test',
                                'named_mode': True,
                                'eigrp_interface': {
                                    'GigabitEthernet0/0/0/0.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:feb4:b131': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 9,
                                                'srtt': 0.004,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 12,
                                                'uptime': '02:31:47',
                                                'prefixes': 6
                                            }
                                        }
                                    },
                                    'GigabitEthernet0/0/0/1.390': {
                                        'eigrp_nbr': {
                                            'fe80::5c00:ff:fe02:7': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 14,
                                                'srtt': 0.009,
                                                'rto': 200,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 8,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 1,
                                                    'tlv_minorrev': 2
                                                },
                                                'hold': 11,
                                                'uptime': '01:42:44',
                                                'prefixes': 5
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
