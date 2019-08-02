
class EigrpOutput(object):

    ShowIpv4EigrpNeighborsDetail = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'ipv4': {
                                'eigrp_interface': {
                                    'Ethernet1/2.90': {
                                        'eigrp_nbr': {
                                            '10.13.90.1': {
                                                'peer_handle': 1,
                                                'hold': 14,
                                                'uptime': '01:58:11',
                                                'srtt': 0.001,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'last_seq_number': 16,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 3, }, }, },
                                    'Ethernet1/1.90': {
                                        'eigrp_nbr': {
                                            '10.23.90.2': {
                                                'peer_handle': 0,
                                                'hold': 13,
                                                'uptime': '01:47:34',
                                                'srtt': 0.015,
                                                'rto': 90,
                                                'q_cnt': 0,
                                                'last_seq_number': 22,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 3}}}}}}},
                    'VRF1': {
                        'address_family': {
                            'ipv4': {
                                'eigrp_interface': {
                                    'Ethernet1/2.390': {
                                        'eigrp_nbr': {
                                            '10.13.90.1': {
                                                'peer_handle': 1,
                                                'hold': 14,
                                                'uptime': '01:44:45',
                                                'srtt': 0.001,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'last_seq_number': 7,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 3}, }, },
                                    'Ethernet1/1.390': {
                                        'eigrp_nbr': {
                                            '10.23.90.2': {
                                                'peer_handle': 0,
                                                'hold': 14,
                                                'uptime': '01:45:34',
                                                'srtt': 0.01,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'last_seq_number': 9,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 3}}}}}}}}}}}

    ShowIpv6EigrpNeighborsDetail = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'default': {
                        'address_family': {
                            'ipv6': {
                                'eigrp_interface': {
                                    'Ethernet1/1.90': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fecf:5a5b': {
                                                'peer_handle': 0,
                                                'hold': 12,
                                                'uptime': '01:41:31',
                                                'srtt': 0.010,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'last_seq_number': 30,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 0
                                            }
                                        }
                                    },
                                    'Ethernet1/2.90': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fe62:65af': {
                                                'peer_handle': 1,
                                                'hold': 12,
                                                'uptime': '01:41:30',
                                                'srtt': 0.004,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'last_seq_number': 22,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 0,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 0}}}}}}},
                    'VRF1': {
                        'address_family': {
                            'ipv6': {
                                'eigrp_interface': {
                                    'Ethernet1/1.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fecf:5a5b': {
                                                'peer_handle': 0,
                                                'hold': 11,
                                                'uptime': '01:45:50',
                                                'srtt': 0.010,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'last_seq_number': 10,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 2,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 0
                                            }
                                        }
                                    },
                                    'Ethernet1/2.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fe62:65af': {
                                                'peer_handle': 1,
                                                'hold': 14,
                                                'uptime': '01:45:01',
                                                'srtt': 0.004,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'last_seq_number': 8,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'bfd_state': 'N/A',
                                                'prefixes': 0}}}}}}}}}}}

    EigrpInfo = {
        'eigrp_instance': {
            '100': {
                'vrf': {
                    'VRF1': {
                        'address_family': {
                            'ipv4': {
                                'eigrp_interface': {
                                    'Ethernet1/1.390': {
                                        'eigrp_nbr': {
                                            '10.23.90.2': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 9,
                                                'srtt': 0.01,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 14,
                                                'uptime': '01:45:34',
                                                'prefixes': 3
                                            }
                                        }
                                    },
                                    'Ethernet1/2.390': {
                                        'eigrp_nbr': {
                                            '10.13.90.1': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 7,
                                                'srtt': 0.001,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 14,
                                                'uptime': '01:44:45',
                                                'prefixes': 3
                                            }
                                        }
                                    }
                                }
                            },
                            'ipv6': {
                                'eigrp_interface': {
                                    'Ethernet1/2.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fe62:65af': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 8,
                                                'srtt': 0.004,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 14,
                                                'uptime': '01:45:01',
                                                'prefixes': 0
                                            }
                                        }
                                    },
                                    'Ethernet1/1.390': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fecf:5a5b': {
                                                'retransmit_count': 2,
                                                'retry_count': 0,
                                                'last_seq_number': 10,
                                                'srtt': 0.01,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 11,
                                                'uptime': '01:45:50',
                                                'prefixes': 0
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
                                'eigrp_interface': {
                                    'Ethernet1/1.90': {
                                        'eigrp_nbr': {
                                            '10.23.90.2': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 22,
                                                'srtt': 0.015,
                                                'rto': 90,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 13,
                                                'uptime': '01:47:34',
                                                'prefixes': 3
                                            }
                                        }
                                    },
                                    'Ethernet1/2.90': {
                                        'eigrp_nbr': {
                                            '10.13.90.1': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 16,
                                                'srtt': 0.001,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 14,
                                                'uptime': '01:58:11',
                                                'prefixes': 3
                                            }
                                        }
                                    }
                                }
                            },
                            'ipv6': {
                                'eigrp_interface': {
                                    'Ethernet1/2.90': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fe62:65af': {
                                                'retransmit_count': 0,
                                                'retry_count': 0,
                                                'last_seq_number': 22,
                                                'srtt': 0.004,
                                                'rto': 50,
                                                'q_cnt': 0,
                                                'peer_handle': 1,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 23,
                                                    'os_minorver': 0,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 12,
                                                'uptime': '01:41:30',
                                                'prefixes': 0
                                            }
                                        }
                                    },
                                    'Ethernet1/1.90': {
                                        'eigrp_nbr': {
                                            'fe80::f816:3eff:fecf:5a5b': {
                                                'retransmit_count': 1,
                                                'retry_count': 0,
                                                'last_seq_number': 30,
                                                'srtt': 0.01,
                                                'rto': 60,
                                                'q_cnt': 0,
                                                'peer_handle': 0,
                                                'nbr_sw_ver': {
                                                    'os_majorver': 3,
                                                    'os_minorver': 3,
                                                    'tlv_majorrev': 2,
                                                    'tlv_minorrev': 0
                                                },
                                                'hold': 12,
                                                'uptime': '01:41:31',
                                                'prefixes': 0
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
