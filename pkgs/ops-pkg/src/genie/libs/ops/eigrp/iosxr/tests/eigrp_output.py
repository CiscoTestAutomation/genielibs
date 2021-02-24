'''
EIGRP Genie Ops Object Outputs for IOSXR
'''

class EigrpOutput(object):

    # 'show eigrp ipv4 neighbors detail'
	ShowEigrpIpv4NeighborsDetail = '''
#show eigrp ipv4 neighbors detail
Mon Apr 15 18:03:58.323 UTC

IPv4-EIGRP VR(test) Neighbors for AS(100) VRF default

H   Address                 Interface       Hold Uptime   SRTT   RTO  Q  Seq
                                    (sec)         (ms)       Cnt Num
1   10.23.90.3              Gi0/0/0/1.90      11 01:43:15   13   200  0  23
BFD disabled
Version 8.0/1.2, Retrans: 1, Retries: 0, Prefixes: 3
0   10.12.90.1              Gi0/0/0/0.90      14 02:56:28    1   200  0  17
BFD disabled
Version 23.0/2.0, Retrans: 1, Retries: 0, Prefixes: 3
'''

    # 'show eigrp ipv6 neighbors detail'
	ShowEigrpIpv6NeighborsDetail = '''
#show eigrp ipv6 neighbors detail
Mon Apr 15 18:05:00.348 UTC

IPv6-EIGRP VR(test) Neighbors for AS(100) VRF default

H   Address                 Interface       Hold Uptime   SRTT   RTO  Q  Seq
                                            (sec)         (ms)       Cnt Num
1   Link Local Address:     Gi0/0/0/1.90      13 01:37:57   11   200  0  28
    fe80::5c00:ff:fe02:7
    BFD disabled
    Version 8.0/1.2, Retrans: 1, Retries: 0, Prefixes: 5
0   Link Local Address:     Gi0/0/0/0.90      12 02:31:58    1   200  0  23
    fe80::f816:3eff:feb4:b131
    BFD disabled
    Version 23.0/2.0, Retrans: 1, Retries: 0, Prefixes: 6
'''

    # 'show eigrp ipv4 vrf all neighbors detail'
	ShowEigrpIpv4NeighborsDetailAllVrf = '''
#show eigrp ipv4 vrf all neighbors detail
Mon Apr 15 18:04:31.216 UTC

IPv4-EIGRP VR(test) Neighbors for AS(100) VRF VRF1

H   Address                 Interface       Hold Uptime   SRTT   RTO  Q  Seq
                                            (sec)         (ms)       Cnt Num
1   10.23.90.3              Gi0/0/0/1.390     14 01:41:47    4   200  0  15
    BFD disabled
    Version 8.0/1.2, Retrans: 1, Retries: 0, Prefixes: 3
0   10.12.90.1              Gi0/0/0/0.390     13 02:54:01  816  4896  0  8
    BFD disabled
    Version 23.0/2.0, Retrans: 0, Retries: 0, Prefixes: 3
'''

    # 'show eigrp ipv6 vrf all neighbors detail'
	ShowEigrpIpv6NeighborsDetailAllVrf = '''
#show eigrp ipv6 vrf all neighbors detail
Mon Apr 15 18:05:29.245 UTC

IPv6-EIGRP VR(test) Neighbors for AS(100) VRF VRF1

H   Address                 Interface       Hold Uptime   SRTT   RTO  Q  Seq
                                            (sec)         (ms)       Cnt Num
1   Link Local Address:     Gi0/0/0/1.390     11 01:42:44    9   200  0  14
    fe80::5c00:ff:fe02:7
    BFD disabled
    Version 8.0/1.2, Retrans: 1, Retries: 0, Prefixes: 5
0   Link Local Address:     Gi0/0/0/0.390     12 02:31:47    4   200  0  9
    fe80::f816:3eff:feb4:b131
    BFD disabled
    Version 23.0/2.0, Retrans: 1, Retries: 0, Prefixes: 6
'''

	EigrpInfo = {
    "eigrp_instance": {
        "100": {
            "vrf": {
                "default": {
                    "address_family": {
                        "ipv4": {
                            "name": "test",
                            "named_mode": True,
                            "eigrp_interface": {
                                "GigabitEthernet0/0/0/0.90": {
                                    "eigrp_nbr": {
                                        "10.12.90.1": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 17,
                                            "srtt": 0.001,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 0,
                                            "nbr_sw_ver": {
                                                "os_majorver": 23,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 2,
                                                "tlv_minorrev": 0,
                                            },
                                            "hold": 14,
                                            "uptime": "02:56:28",
                                            "prefixes": 3,
                                        }
                                    }
                                },
                                "GigabitEthernet0/0/0/1.90": {
                                    "eigrp_nbr": {
                                        "10.23.90.3": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 23,
                                            "srtt": 0.013,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 1,
                                            "nbr_sw_ver": {
                                                "os_majorver": 8,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 1,
                                                "tlv_minorrev": 2,
                                            },
                                            "hold": 11,
                                            "uptime": "01:43:15",
                                            "prefixes": 3,
                                        }
                                    }
                                },
                            },
                        },
                        "ipv6": {
                            "name": "test",
                            "named_mode": True,
                            "eigrp_interface": {
                                "GigabitEthernet0/0/0/0.90": {
                                    "eigrp_nbr": {
                                        "fe80::f816:3eff:feb4:b131": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 23,
                                            "srtt": 0.001,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 0,
                                            "nbr_sw_ver": {
                                                "os_majorver": 23,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 2,
                                                "tlv_minorrev": 0,
                                            },
                                            "hold": 12,
                                            "uptime": "02:31:58",
                                            "prefixes": 6,
                                        }
                                    }
                                },
                                "GigabitEthernet0/0/0/1.90": {
                                    "eigrp_nbr": {
                                        "fe80::5c00:ff:fe02:7": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 28,
                                            "srtt": 0.011,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 1,
                                            "nbr_sw_ver": {
                                                "os_majorver": 8,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 1,
                                                "tlv_minorrev": 2,
                                            },
                                            "hold": 13,
                                            "uptime": "01:37:57",
                                            "prefixes": 5,
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "VRF1": {
                    "address_family": {
                        "ipv4": {
                            "name": "test",
                            "named_mode": True,
                            "eigrp_interface": {
                                "GigabitEthernet0/0/0/0.390": {
                                    "eigrp_nbr": {
                                        "10.12.90.1": {
                                            "retransmit_count": 0,
                                            "retry_count": 0,
                                            "last_seq_number": 8,
                                            "srtt": 0.816,
                                            "rto": 4896,
                                            "q_cnt": 0,
                                            "peer_handle": 0,
                                            "nbr_sw_ver": {
                                                "os_majorver": 23,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 2,
                                                "tlv_minorrev": 0,
                                            },
                                            "hold": 13,
                                            "uptime": "02:54:01",
                                            "prefixes": 3,
                                        }
                                    }
                                },
                                "GigabitEthernet0/0/0/1.390": {
                                    "eigrp_nbr": {
                                        "10.23.90.3": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 15,
                                            "srtt": 0.004,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 1,
                                            "nbr_sw_ver": {
                                                "os_majorver": 8,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 1,
                                                "tlv_minorrev": 2,
                                            },
                                            "hold": 14,
                                            "uptime": "01:41:47",
                                            "prefixes": 3,
                                        }
                                    }
                                },
                            },
                        },
                        "ipv6": {
                            "name": "test",
                            "named_mode": True,
                            "eigrp_interface": {
                                "GigabitEthernet0/0/0/0.390": {
                                    "eigrp_nbr": {
                                        "fe80::f816:3eff:feb4:b131": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 9,
                                            "srtt": 0.004,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 0,
                                            "nbr_sw_ver": {
                                                "os_majorver": 23,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 2,
                                                "tlv_minorrev": 0,
                                            },
                                            "hold": 12,
                                            "uptime": "02:31:47",
                                            "prefixes": 6,
                                        }
                                    }
                                },
                                "GigabitEthernet0/0/0/1.390": {
                                    "eigrp_nbr": {
                                        "fe80::5c00:ff:fe02:7": {
                                            "retransmit_count": 1,
                                            "retry_count": 0,
                                            "last_seq_number": 14,
                                            "srtt": 0.009,
                                            "rto": 200,
                                            "q_cnt": 0,
                                            "peer_handle": 1,
                                            "nbr_sw_ver": {
                                                "os_majorver": 8,
                                                "os_minorver": 0,
                                                "tlv_majorrev": 1,
                                                "tlv_minorrev": 2,
                                            },
                                            "hold": 11,
                                            "uptime": "01:42:44",
                                            "prefixes": 5,
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
            }
        }
    }
}
