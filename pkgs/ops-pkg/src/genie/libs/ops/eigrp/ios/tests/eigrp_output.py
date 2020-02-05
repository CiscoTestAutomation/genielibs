"""
EIGRP Genie Ops Object Outputs for IOS

"""


class EigrpOutput(object):

    # 'show ip eigrp neighbors detail'
    ShowIpEigrpNeighborsDetail = {
        "eigrp_instance": {
            "100": {
                "vrf": {
                    "default": {
                        "address_family": {
                            "ipv4": {
                                "name": "test",
                                "named_mode": True,
                                "eigrp_interface": {
                                    "GigabitEthernet2.90": {
                                        "eigrp_nbr": {
                                            "10.12.90.2": {
                                                "peer_handle": 1,
                                                "hold": 12,
                                                "uptime": "2d10h",
                                                "srtt": 1283.0,
                                                "rto": 5000,
                                                "q_cnt": 0,
                                                "last_seq_number": 5,
                                                "topology_advert_to_peer": "base",
                                                "nbr_sw_ver": {
                                                    "os_majorver": 3,
                                                    "os_minorver": 3,
                                                    "tlv_majorrev": 2,
                                                    "tlv_minorrev": 0,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "prefixes": 3,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                    "GigabitEthernet3.90": {
                                        "eigrp_nbr": {
                                            "10.13.90.3": {
                                                "peer_handle": 0,
                                                "hold": 10,
                                                "uptime": "2d10h",
                                                "srtt": 6.0,
                                                "rto": 100,
                                                "q_cnt": 0,
                                                "last_seq_number": 9,
                                                "topology_advert_to_peer": "base",
                                                "nbr_sw_ver": {
                                                    "os_majorver": 8,
                                                    "os_minorver": 0,
                                                    "tlv_majorrev": 1,
                                                    "tlv_minorrev": 2,
                                                },
                                                "retransmit_count": 1,
                                                "retry_count": 0,
                                                "prefixes": 3,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                },
                            }
                        }
                    }
                }
            }
        }
    }

    ShowIpEigrpNeighborsDetail_golden = """
        EIGRP-IPv4 VR(test) Address-Family Neighbors for AS(100)
            H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                               (sec)         (ms)       Cnt Num
            1   10.12.90.2              Gi2.90                   12 2d10h    1283  5000  0  5
               Version 3.3/2.0, Retrans: 0, Retries: 0, Prefixes: 3
               Topology-ids from peer - 0
               Topologies advertised to peer:   base

            0   10.13.90.3              Gi3.90                   10 2d10h       6   100  0  9
               Version 8.0/1.2, Retrans: 1, Retries: 0, Prefixes: 3
               Topology-ids from peer - 0
               Topologies advertised to peer:   base

            Max Nbrs: 0, Current Nbrs: 0               10 01:37:17   13   100  0  9
    """

    # 'show ipv6 eigrp neighbors detail '
    ShowIpv6EigrpNeighborsDetail = {
        "eigrp_instance": {
            "100": {
                "vrf": {
                    "default": {
                        "address_family": {
                            "ipv6": {
                                "name": "test",
                                "named_mode": True,
                                "eigrp_interface": {
                                    "GigabitEthernet0/2.90": {
                                        "eigrp_nbr": {
                                            "FE80::F816:3EFF:FE39:94CB": {
                                                "peer_handle": 1,
                                                "hold": 11,
                                                "uptime": "01:42:01",
                                                "srtt": 0.739,
                                                "rto": 4434,
                                                "q_cnt": 0,
                                                "last_seq_number": 7,
                                                "topology_advert_to_peer": "base",
                                                "nbr_sw_ver": {
                                                    "os_majorver": 3,
                                                    "os_minorver": 3,
                                                    "tlv_majorrev": 2,
                                                    "tlv_minorrev": 0,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "prefixes": 4,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                    "GigabitEthernet0/3.90": {
                                        "eigrp_nbr": {
                                            "FE80::5C00:80FF:FE01:7": {
                                                "peer_handle": 0,
                                                "hold": 11,
                                                "uptime": "01:44:53",
                                                "srtt": 0.993,
                                                "rto": 5000,
                                                "q_cnt": 0,
                                                "last_seq_number": 11,
                                                "topology_advert_to_peer": "base",
                                                "nbr_sw_ver": {
                                                    "os_majorver": 8,
                                                    "os_minorver": 0,
                                                    "tlv_majorrev": 1,
                                                    "tlv_minorrev": 2,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "prefixes": 4,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                },
                            }
                        }
                    }
                }
            }
        }
    }

    ShowIpv6EigrpNeighborsDetail_golden = """
        EIGRP-IPv6 VR(test) Address-Family Neighbors for AS(100)
            H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                               (sec)         (ms)       Cnt Num
            1   Link-local address:     Gi0/2.90                 11 01:42:01  739  4434  0  7
                FE80::F816:3EFF:FE39:94CB
               Version 3.3/2.0, Retrans: 0, Retries: 0, Prefixes: 4
               Topology-ids from peer - 0
               Topologies advertised to peer:   base

            0   Link-local address:     Gi0/3.90                 11 01:44:53  993  5000  0  11
                FE80::5C00:80FF:FE01:7
               Version 8.0/1.2, Retrans: 0, Retries: 0, Prefixes: 4
               Topology-ids from peer - 0
               Topologies advertised to peer:   base

            Max Nbrs: 0, Current Nbrs: 0
    """

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
                                    "GigabitEthernet3.90": {
                                        "eigrp_nbr": {
                                            "10.13.90.3": {
                                                "nbr_sw_ver": {
                                                    "os_majorver": 8,
                                                    "os_minorver": 0,
                                                    "tlv_majorrev": 1,
                                                    "tlv_minorrev": 2,
                                                },
                                                "retransmit_count": 1,
                                                "retry_count": 0,
                                                "last_seq_number": 9,
                                                "srtt": 6.0,
                                                "rto": 100,
                                                "q_cnt": 0,
                                                "hold": 10,
                                                "uptime": "2d10h",
                                                "peer_handle": 0,
                                                "prefixes": 3,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                    "GigabitEthernet2.90": {
                                        "eigrp_nbr": {
                                            "10.12.90.2": {
                                                "nbr_sw_ver": {
                                                    "os_majorver": 3,
                                                    "os_minorver": 3,
                                                    "tlv_majorrev": 2,
                                                    "tlv_minorrev": 0,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "last_seq_number": 5,
                                                "srtt": 1283.0,
                                                "rto": 5000,
                                                "q_cnt": 0,
                                                "hold": 12,
                                                "uptime": "2d10h",
                                                "peer_handle": 1,
                                                "prefixes": 3,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                },
                            },
                            "ipv6": {
                                "name": "test",
                                "named_mode": True,
                                "eigrp_interface": {
                                    "GigabitEthernet0/3.90": {
                                        "eigrp_nbr": {
                                            "FE80::5C00:80FF:FE01:7": {
                                                "nbr_sw_ver": {
                                                    "os_majorver": 8,
                                                    "os_minorver": 0,
                                                    "tlv_majorrev": 1,
                                                    "tlv_minorrev": 2,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "last_seq_number": 11,
                                                "srtt": 0.993,
                                                "rto": 5000,
                                                "q_cnt": 0,
                                                "hold": 11,
                                                "uptime": "01:44:53",
                                                "peer_handle": 0,
                                                "prefixes": 4,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                    "GigabitEthernet0/2.90": {
                                        "eigrp_nbr": {
                                            "FE80::F816:3EFF:FE39:94CB": {
                                                "nbr_sw_ver": {
                                                    "os_majorver": 3,
                                                    "os_minorver": 3,
                                                    "tlv_majorrev": 2,
                                                    "tlv_minorrev": 0,
                                                },
                                                "retransmit_count": 0,
                                                "retry_count": 0,
                                                "last_seq_number": 7,
                                                "srtt": 0.739,
                                                "rto": 4434,
                                                "q_cnt": 0,
                                                "hold": 11,
                                                "uptime": "01:42:01",
                                                "peer_handle": 1,
                                                "prefixes": 4,
                                                "topology_ids_from_peer": 0,
                                            }
                                        }
                                    },
                                },
                            },
                        }
                    }
                }
            }
        }
    }
