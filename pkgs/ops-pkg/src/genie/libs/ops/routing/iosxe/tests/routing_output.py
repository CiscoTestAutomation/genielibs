'''
 Route Genie Ops Object Outputs for IOSXE.
'''

class RouteOutput(object):
    """show ip route output """

    ShowVrfDetail = {
        "Mgmt-vrf": {
              "vrf_id": 1,
              "interfaces": [
                   "GigabitEthernet0/0"
              ],
              "address_family": {
                   "ipv4 unicast": {
                        "table_id": "0x1",
                        "flags": "0x0",
                        "vrf_label": {
                            'allocation_mode': 'per-prefix'
                        }
                   },
                   "ipv6 unicast": {
                        "table_id": "0x1E000001",
                        "flags": "0x0",
                        "vrf_label": {
                            'allocation_mode': 'per-prefix'
                        }
                   }
              },
              "flags": "0x1808"
         },
        "VRF1": {
              "interfaces": [
                   "GigabitEthernet0/0"
              ],
              "address_family": {
                   "ipv4 unicast": {
                        "export_to_global": {
                             "export_to_global_map": "export_to_global_map",
                             "prefix_limit": 1000
                        },
                        "import_from_global": {
                             "prefix_limit": 1000,
                             "import_from_global_map": "import_from_global_map"
                        },
                        "table_id": "0x1",
                        "routing_table_limit": {
                             "routing_table_limit_action": {
                                  "enable_alert_limit_number": {
                                       "alert_limit_number": 10000
                                  }
                             }
                        },
                        "route_targets": {
                             "200:1": {
                                  "rt_type": "both",
                                  "route_target": "200:1"
                             },
                             "100:1": {
                                  "rt_type": "both",
                                  "route_target": "100:1"
                             }
                        },
                        "flags": "0x2100",
                        "vrf_label": {
                            'allocation_mode': 'per-prefix'
                        }
                   },
                   "ipv6 unicast": {
                        "export_to_global": {
                             "export_to_global_map": "export_to_global_map",
                             "prefix_limit": 1000
                        },
                        "table_id": "0x1E000001",
                        "routing_table_limit": {
                             "routing_table_limit_action": {
                                  "enable_alert_percent": {
                                       "alert_percent_value": 70
                                  },
                                  "enable_alert_limit_number": {
                                       "alert_limit_number": 7000
                                  }
                             },
                             "routing_table_limit_number": 10000
                        },
                        "route_targets": {
                             "200:1": {
                                  "rt_type": "import",
                                  "route_target": "200:1"
                             },
                             "400:1": {
                                  "rt_type": "import",
                                  "route_target": "400:1"
                             },
                             "300:1": {
                                  "rt_type": "export",
                                  "route_target": "300:1"
                             },
                             "100:1": {
                                  "rt_type": "export",
                                  "route_target": "100:1"
                             }
                        },
                        "flags": "0x100",
                        "vrf_label": {
                            'allocation_mode': 'per-prefix'
                        }
                   }
              },
              "flags": "0x180C",
              "route_distinguisher": "100:1",
              "vrf_id": 1
         }
    }

    showIpRoute_default = '''\
        genie_Router#show ip route
          Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override, p - overrides from PfR

          Gateway of last resort is not set

               10.1.0.0/32 is subnetted, 1 subnets
          C        10.4.1.1 is directly connected, Loopback0
               10.4.0.0/32 is subnetted, 1 subnets
          D        10.16.2.2 [90/10752] via 10.12.90.2, 4d19h, GigabitEthernet2.90
               10.9.0.0/32 is subnetted, 1 subnets
          D        10.36.3.3 [90/2570240] via 10.13.90.3, 4d19h, GigabitEthernet3.90
               10.0.0.0/8 is variably subnetted, 20 subnets, 2 masks
          C        10.12.90.0/24 is directly connected, GigabitEthernet2.90
          L        10.12.90.1/32 is directly connected, GigabitEthernet2.90
          C        10.12.110.0/24 is directly connected, GigabitEthernet2.110
          L        10.12.110.1/32 is directly connected, GigabitEthernet2.110
          C        10.12.115.0/24 is directly connected, GigabitEthernet2.115
          L        10.12.115.1/32 is directly connected, GigabitEthernet2.115
          C        10.12.120.0/24 is directly connected, GigabitEthernet2.120
          L        10.12.120.1/32 is directly connected, GigabitEthernet2.120
          C        10.13.90.0/24 is directly connected, GigabitEthernet3.90
          L        10.13.90.1/32 is directly connected, GigabitEthernet3.90
          C        10.13.110.0/24 is directly connected, GigabitEthernet3.110
          L        10.13.110.1/32 is directly connected, GigabitEthernet3.110
          C        10.13.115.0/24 is directly connected, GigabitEthernet3.115
          L        10.13.115.1/32 is directly connected, GigabitEthernet3.115
          C        10.13.120.0/24 is directly connected, GigabitEthernet3.120
          L        10.13.120.1/32 is directly connected, GigabitEthernet3.120
          D        10.23.90.0/24 [90/15360] via 10.13.90.3, 4d19h, GigabitEthernet3.90
                              [90/15360] via 10.12.90.2, 4d19h, GigabitEthernet2.90
          O        10.23.110.0/24 [110/2] via 10.12.110.2, 4d19h, GigabitEthernet2.110
          i L1     10.23.115.0/24 [115/20] via 10.12.115.2, 4d19h, GigabitEthernet2.115
          R        10.23.120.0/24
                    [120/1] via 10.13.120.3, 00:00:08, GigabitEthernet3.120
                    [120/1] via 10.12.120.2, 00:00:02, GigabitEthernet2.120
    '''

    showIpRoute_VRF1 = '''\
        genie_Router#show ip route vrf VRF1

          Routing Table: VRF1
          Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override, p - overrides from PfR

          Gateway of last resort is not set

               10.1.0.0/32 is subnetted, 1 subnets
          C        10.4.1.1 is directly connected, Loopback300
               10.4.0.0/32 is subnetted, 1 subnets
          D        10.16.2.2 [90/10752] via 10.12.90.2, 4d19h, GigabitEthernet2.390
               10.9.0.0/32 is subnetted, 1 subnets
          D        10.36.3.3 [90/2570240] via 10.13.90.3, 4d19h, GigabitEthernet3.390
               10.0.0.0/8 is variably subnetted, 20 subnets, 2 masks
          C        10.12.90.0/24 is directly connected, GigabitEthernet2.390
          L        10.12.90.1/32 is directly connected, GigabitEthernet2.390
          C        10.12.110.0/24 is directly connected, GigabitEthernet2.410
          L        10.12.110.1/32 is directly connected, GigabitEthernet2.410
          C        10.12.115.0/24 is directly connected, GigabitEthernet2.415
          L        10.12.115.1/32 is directly connected, GigabitEthernet2.415
          C        10.12.120.0/24 is directly connected, GigabitEthernet2.420
          L        10.12.120.1/32 is directly connected, GigabitEthernet2.420
          C        10.13.90.0/24 is directly connected, GigabitEthernet3.390
          L        10.13.90.1/32 is directly connected, GigabitEthernet3.390
          C        10.13.110.0/24 is directly connected, GigabitEthernet3.410
          L        10.13.110.1/32 is directly connected, GigabitEthernet3.410
          C        10.13.115.0/24 is directly connected, GigabitEthernet3.415
          L        10.13.115.1/32 is directly connected, GigabitEthernet3.415
          C        10.13.120.0/24 is directly connected, GigabitEthernet3.420
          L        10.13.120.1/32 is directly connected, GigabitEthernet3.420
          D        10.23.90.0/24 [90/15360] via 10.13.90.3, 4d19h, GigabitEthernet3.390
                              [90/15360] via 10.12.90.2, 4d19h, GigabitEthernet2.390
          O        10.23.110.0/24 [110/2] via 10.12.110.2, 4d19h, GigabitEthernet2.410
          i L1     10.23.115.0/24 [115/50] via 10.13.115.3, 4d19h, GigabitEthernet3.415
          R        10.23.120.0/24
                    [120/1] via 10.13.120.3, 00:00:20, GigabitEthernet3.420
                    [120/1] via 10.12.120.2, 00:00:17, GigabitEthernet2.420
    '''

    showIpv6RouteUpdated_default = '''\
        genie_Router#show ipv6 route
          IPv6 Routing Table - default - 24 entries
          Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
               B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
               I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
               EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
               NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
               OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
               ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
               ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
               a - Application
          LC  2001:1:1:1::1/128 [0/0]
               via Loopback0, receive
          D   2001:2:2:2::2/128 [90/10752]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.90
          D   2001:3:3:3::3/128 [90/2570240]
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.90
          C   2001:10:12:90::/64 [0/0]
               via GigabitEthernet2.90, directly connected
          L   2001:10:12:90::1/128 [0/0]
               via GigabitEthernet2.90, receive
          C   2001:10:12:110::/64 [0/0]
               via GigabitEthernet2.110, directly connected
          L   2001:10:12:110::1/128 [0/0]
               via GigabitEthernet2.110, receive
          C   2001:10:12:115::/64 [0/0]
               via GigabitEthernet2.115, directly connected
          L   2001:10:12:115::1/128 [0/0]
               via GigabitEthernet2.115, receive
          C   2001:10:12:120::/64 [0/0]
               via GigabitEthernet2.120, directly connected
          L   2001:10:12:120::1/128 [0/0]
               via GigabitEthernet2.120, receive
          C   2001:10:13:90::/64 [0/0]
               via GigabitEthernet3.90, directly connected
          L   2001:10:13:90::1/128 [0/0]
               via GigabitEthernet3.90, receive
          C   2001:10:13:110::/64 [0/0]
               via GigabitEthernet3.110, directly connected
          L   2001:10:13:110::1/128 [0/0]
               via GigabitEthernet3.110, receive
          C   2001:10:13:115::/64 [0/0]
               via GigabitEthernet3.115, directly connected
          L   2001:10:13:115::1/128 [0/0]
               via GigabitEthernet3.115, receive
          C   2001:10:13:120::/64 [0/0]
               via GigabitEthernet3.120, directly connected
          L   2001:10:13:120::1/128 [0/0]
               via GigabitEthernet3.120, receive
          D   2001:10:23:90::/64 [90/15360]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.90
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.90
          O   2001:10:23:110::/64 [110/2]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.110
          I1  2001:10:23:115::/64 [115/20]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.115
          R   2001:10:23:120::/64 [120/2]
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.120
          L   FF00::/8 [0/0]
               via Null0, receive
    '''

    showIpv6RouteUpdated_VRF1 = '''\
        genie_Router#show ipv6 route vrf VRF1
          IPv6 Routing Table - VRF1 - 23 entries
          Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
               B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
               I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
               EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
               NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
               OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
               ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
               ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
               a - Application
          LC  2001:1:1:1::1/128 [0/0]
               via Loopback300, receive
          D   2001:2:2:2::2/128 [90/10752]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.390
          D   2001:3:3:3::3/128 [90/2570240]
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.390
          C   2001:10:12:90::/64 [0/0]
               via GigabitEthernet2.390, directly connected
          L   2001:10:12:90::1/128 [0/0]
               via GigabitEthernet2.390, receive
          C   2001:10:12:110::/64 [0/0]
               via GigabitEthernet2.410, directly connected
          L   2001:10:12:110::1/128 [0/0]
               via GigabitEthernet2.410, receive
          C   2001:10:12:115::/64 [0/0]
               via GigabitEthernet2.415, directly connected
          L   2001:10:12:115::1/128 [0/0]
               via GigabitEthernet2.415, receive
          C   2001:10:12:120::/64 [0/0]
               via GigabitEthernet2.420, directly connected
          L   2001:10:12:120::1/128 [0/0]
               via GigabitEthernet2.420, receive
          C   2001:10:13:90::/64 [0/0]
               via GigabitEthernet3.390, directly connected
          L   2001:10:13:90::1/128 [0/0]
               via GigabitEthernet3.390, receive
          C   2001:10:13:110::/64 [0/0]
               via GigabitEthernet3.410, directly connected
          L   2001:10:13:110::1/128 [0/0]
               via GigabitEthernet3.410, receive
          C   2001:10:13:115::/64 [0/0]
               via GigabitEthernet3.415, directly connected
          L   2001:10:13:115::1/128 [0/0]
               via GigabitEthernet3.415, receive
          C   2001:10:13:120::/64 [0/0]
               via GigabitEthernet3.420, directly connected
          L   2001:10:13:120::1/128 [0/0]
               via GigabitEthernet3.420, receive
          D   2001:10:23:90::/64 [90/15360]
               via FE80::F816:3EFF:FE21:73F6, GigabitEthernet2.390
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.390
          I1  2001:10:23:115::/64 [115/50]
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.415
          R   2001:10:23:120::/64 [120/2]
               via FE80::5C00:80FF:FE02:7, GigabitEthernet3.420
          L   FF00::/8 [0/0]
               via Null0, receive
    '''

    routeOpsOutput_vrf1 = {
        "vrf": {
            "VRF1": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "10.23.120.0/24": {
                                "route": "10.23.120.0/24",
                                "active": True,
                                "route_preference": 120,
                                "metric": 1,
                                "source_protocol": "rip",
                                "source_protocol_codes": "R",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.120.2",
                                            "outgoing_interface": "GigabitEthernet2.420",
                                            "updated": "00:00:17",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.120.3",
                                            "outgoing_interface": "GigabitEthernet3.420",
                                            "updated": "00:00:20",
                                        },
                                    }
                                },
                            },
                            "10.23.115.0/24": {
                                "route": "10.23.115.0/24",
                                "active": True,
                                "route_preference": 115,
                                "metric": 50,
                                "source_protocol": "isis",
                                "source_protocol_codes": "i L1",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.115.3",
                                            "outgoing_interface": "GigabitEthernet3.415",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.110.0/24": {
                                "route": "10.23.110.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 2,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.110.2",
                                            "outgoing_interface": "GigabitEthernet2.410",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.90.0/24": {
                                "route": "10.23.90.0/24",
                                "active": True,
                                "route_preference": 90,
                                "metric": 15360,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.390",
                                            "updated": "4d19h",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.390",
                                            "updated": "4d19h",
                                        },
                                    }
                                },
                            },
                            "10.13.120.1/32": {
                                "route": "10.13.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                },
                            },
                            "10.13.120.0/24": {
                                "route": "10.13.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                },
                            },
                            "10.13.115.1/32": {
                                "route": "10.13.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                },
                            },
                            "10.13.115.0/24": {
                                "route": "10.13.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                },
                            },
                            "10.13.110.1/32": {
                                "route": "10.13.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                },
                            },
                            "10.13.110.0/24": {
                                "route": "10.13.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                },
                            },
                            "10.13.90.1/32": {
                                "route": "10.13.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                },
                            },
                            "10.13.90.0/24": {
                                "route": "10.13.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                },
                            },
                            "10.12.120.1/32": {
                                "route": "10.12.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                },
                            },
                            "10.12.120.0/24": {
                                "route": "10.12.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                },
                            },
                            "10.12.115.1/32": {
                                "route": "10.12.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                },
                            },
                            "10.12.115.0/24": {
                                "route": "10.12.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                },
                            },
                            "10.12.110.1/32": {
                                "route": "10.12.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                },
                            },
                            "10.12.110.0/24": {
                                "route": "10.12.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                },
                            },
                            "10.12.90.1/32": {
                                "route": "10.12.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                },
                            },
                            "10.12.90.0/24": {
                                "route": "10.12.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                },
                            },
                            "10.36.3.3/32": {
                                "route": "10.36.3.3/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 2570240,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.390",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.16.2.2/32": {
                                "route": "10.16.2.2/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 10752,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.390",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.4.1.1/32": {
                                "route": "10.4.1.1/32",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback300": {"outgoing_interface": "Loopback300"}
                                    }
                                },
                            },
                        }
                    },
                    "ipv6": {
                        "routes": {
                            "2001:1:1:1::1/128": {
                                "route": "2001:1:1:1::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "LC",
                                "source_protocol": "local_connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback300": {
                                            "outgoing_interface": "Loopback300"
                                        }
                                    }
                                }
                            },
                            "2001:2:2:2::2/128": {
                                "route": "2001:2:2:2::2/128",
                                "active": True,
                                "metric": 10752,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                }
                            },
                            "2001:3:3:3::3/128": {
                                "route": "2001:3:3:3::3/128",
                                "active": True,
                                "metric": 2570240,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:90::/64": {
                                "route": "2001:10:12:90::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:90::1/128": {
                                "route": "2001:10:12:90::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:110::/64": {
                                "route": "2001:10:12:110::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:110::1/128": {
                                "route": "2001:10:12:110::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:115::/64": {
                                "route": "2001:10:12:115::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:115::1/128": {
                                "route": "2001:10:12:115::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:120::/64": {
                                "route": "2001:10:12:120::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:120::1/128": {
                                "route": "2001:10:12:120::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:90::/64": {
                                "route": "2001:10:13:90::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:90::1/128": {
                                "route": "2001:10:13:90::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:110::/64": {
                                "route": "2001:10:13:110::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:110::1/128": {
                                "route": "2001:10:13:110::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:115::/64": {
                                "route": "2001:10:13:115::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:115::1/128": {
                                "route": "2001:10:13:115::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:120::/64": {
                                "route": "2001:10:13:120::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:120::1/128": {
                                "route": "2001:10:13:120::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:90::/64": {
                                "route": "2001:10:23:90::/64",
                                "active": True,
                                "metric": 15360,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:115::/64": {
                                "route": "2001:10:23:115::/64",
                                "active": True,
                                "metric": 50,
                                "route_preference": 115,
                                "source_protocol_codes": "I1",
                                "source_protocol": "isis",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:120::/64": {
                                "route": "2001:10:23:120::/64",
                                "active": True,
                                "metric": 2,
                                "route_preference": 120,
                                "source_protocol_codes": "R",
                                "source_protocol": "rip",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                }
                            },
                            "FF00::/8": {
                                "route": "FF00::/8",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Null0": {
                                            "outgoing_interface": "Null0"
                                        }
                                    }
                                }
                            },
                        }
                    },
                }
            }
        }
    }

    routeOpsOutput = {
        "vrf": {
            "VRF1": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "10.23.120.0/24": {
                                "route": "10.23.120.0/24",
                                "active": True,
                                "route_preference": 120,
                                "metric": 1,
                                "source_protocol": "rip",
                                "source_protocol_codes": "R",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.120.2",
                                            "outgoing_interface": "GigabitEthernet2.420",
                                            "updated": "00:00:17",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.120.3",
                                            "outgoing_interface": "GigabitEthernet3.420",
                                            "updated": "00:00:20",
                                        },
                                    }
                                },
                            },
                            "10.23.115.0/24": {
                                "route": "10.23.115.0/24",
                                "active": True,
                                "route_preference": 115,
                                "metric": 50,
                                "source_protocol": "isis",
                                "source_protocol_codes": "i L1",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.115.3",
                                            "outgoing_interface": "GigabitEthernet3.415",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.110.0/24": {
                                "route": "10.23.110.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 2,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.110.2",
                                            "outgoing_interface": "GigabitEthernet2.410",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.90.0/24": {
                                "route": "10.23.90.0/24",
                                "active": True,
                                "route_preference": 90,
                                "metric": 15360,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.390",
                                            "updated": "4d19h",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.390",
                                            "updated": "4d19h",
                                        },
                                    }
                                },
                            },
                            "10.13.120.1/32": {
                                "route": "10.13.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                },
                            },
                            "10.13.120.0/24": {
                                "route": "10.13.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.420": {
                                            "outgoing_interface": "GigabitEthernet3.420"
                                        }
                                    }
                                },
                            },
                            "10.13.115.1/32": {
                                "route": "10.13.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                },
                            },
                            "10.13.115.0/24": {
                                "route": "10.13.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.415": {
                                            "outgoing_interface": "GigabitEthernet3.415"
                                        }
                                    }
                                },
                            },
                            "10.13.110.1/32": {
                                "route": "10.13.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                },
                            },
                            "10.13.110.0/24": {
                                "route": "10.13.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.410": {
                                            "outgoing_interface": "GigabitEthernet3.410"
                                        }
                                    }
                                },
                            },
                            "10.13.90.1/32": {
                                "route": "10.13.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                },
                            },
                            "10.13.90.0/24": {
                                "route": "10.13.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.390": {
                                            "outgoing_interface": "GigabitEthernet3.390"
                                        }
                                    }
                                },
                            },
                            "10.12.120.1/32": {
                                "route": "10.12.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                },
                            },
                            "10.12.120.0/24": {
                                "route": "10.12.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.420": {
                                            "outgoing_interface": "GigabitEthernet2.420"
                                        }
                                    }
                                },
                            },
                            "10.12.115.1/32": {
                                "route": "10.12.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                },
                            },
                            "10.12.115.0/24": {
                                "route": "10.12.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.415": {
                                            "outgoing_interface": "GigabitEthernet2.415"
                                        }
                                    }
                                },
                            },
                            "10.12.110.1/32": {
                                "route": "10.12.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                },
                            },
                            "10.12.110.0/24": {
                                "route": "10.12.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.410": {
                                            "outgoing_interface": "GigabitEthernet2.410"
                                        }
                                    }
                                },
                            },
                            "10.12.90.1/32": {
                                "route": "10.12.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                },
                            },
                            "10.12.90.0/24": {
                                "route": "10.12.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.390": {
                                            "outgoing_interface": "GigabitEthernet2.390"
                                        }
                                    }
                                },
                            },
                            "10.36.3.3/32": {
                                "route": "10.36.3.3/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 2570240,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.390",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.16.2.2/32": {
                                "route": "10.16.2.2/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 10752,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.390",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.4.1.1/32": {
                                "route": "10.4.1.1/32",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback300": {"outgoing_interface": "Loopback300"}
                                    }
                                },
                            },
                        }
                    }
                }
            },
            "default": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "10.23.120.0/24": {
                                "route": "10.23.120.0/24",
                                "active": True,
                                "route_preference": 120,
                                "metric": 1,
                                "source_protocol": "rip",
                                "source_protocol_codes": "R",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.120.2",
                                            "outgoing_interface": "GigabitEthernet2.120",
                                            "updated": "00:00:02",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.120.3",
                                            "outgoing_interface": "GigabitEthernet3.120",
                                            "updated": "00:00:08",
                                        },
                                    }
                                },
                            },
                            "10.23.115.0/24": {
                                "route": "10.23.115.0/24",
                                "active": True,
                                "route_preference": 115,
                                "metric": 20,
                                "source_protocol": "isis",
                                "source_protocol_codes": "i L1",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.115.2",
                                            "outgoing_interface": "GigabitEthernet2.115",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.110.0/24": {
                                "route": "10.23.110.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 2,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.110.2",
                                            "outgoing_interface": "GigabitEthernet2.110",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.23.90.0/24": {
                                "route": "10.23.90.0/24",
                                "active": True,
                                "route_preference": 90,
                                "metric": 15360,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.90",
                                            "updated": "4d19h",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.90",
                                            "updated": "4d19h",
                                        },
                                    }
                                },
                            },
                            "10.13.120.1/32": {
                                "route": "10.13.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.120": {
                                            "outgoing_interface": "GigabitEthernet3.120"
                                        }
                                    }
                                },
                            },
                            "10.13.120.0/24": {
                                "route": "10.13.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.120": {
                                            "outgoing_interface": "GigabitEthernet3.120"
                                        }
                                    }
                                },
                            },
                            "10.13.115.1/32": {
                                "route": "10.13.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.115": {
                                            "outgoing_interface": "GigabitEthernet3.115"
                                        }
                                    }
                                },
                            },
                            "10.13.115.0/24": {
                                "route": "10.13.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.115": {
                                            "outgoing_interface": "GigabitEthernet3.115"
                                        }
                                    }
                                },
                            },
                            "10.13.110.1/32": {
                                "route": "10.13.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.110": {
                                            "outgoing_interface": "GigabitEthernet3.110"
                                        }
                                    }
                                },
                            },
                            "10.13.110.0/24": {
                                "route": "10.13.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.110": {
                                            "outgoing_interface": "GigabitEthernet3.110"
                                        }
                                    }
                                },
                            },
                            "10.13.90.1/32": {
                                "route": "10.13.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.90": {
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                },
                            },
                            "10.13.90.0/24": {
                                "route": "10.13.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.90": {
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                },
                            },
                            "10.12.120.1/32": {
                                "route": "10.12.120.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.120": {
                                            "outgoing_interface": "GigabitEthernet2.120"
                                        }
                                    }
                                },
                            },
                            "10.12.120.0/24": {
                                "route": "10.12.120.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.120": {
                                            "outgoing_interface": "GigabitEthernet2.120"
                                        }
                                    }
                                },
                            },
                            "10.12.115.1/32": {
                                "route": "10.12.115.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.115": {
                                            "outgoing_interface": "GigabitEthernet2.115"
                                        }
                                    }
                                },
                            },
                            "10.12.115.0/24": {
                                "route": "10.12.115.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.115": {
                                            "outgoing_interface": "GigabitEthernet2.115"
                                        }
                                    }
                                },
                            },
                            "10.12.110.1/32": {
                                "route": "10.12.110.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.110": {
                                            "outgoing_interface": "GigabitEthernet2.110"
                                        }
                                    }
                                },
                            },
                            "10.12.110.0/24": {
                                "route": "10.12.110.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.110": {
                                            "outgoing_interface": "GigabitEthernet2.110"
                                        }
                                    }
                                },
                            },
                            "10.12.90.1/32": {
                                "route": "10.12.90.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.90": {
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        }
                                    }
                                },
                            },
                            "10.12.90.0/24": {
                                "route": "10.12.90.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.90": {
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        }
                                    }
                                },
                            },
                            "10.36.3.3/32": {
                                "route": "10.36.3.3/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 2570240,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.13.90.3",
                                            "outgoing_interface": "GigabitEthernet3.90",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.16.2.2/32": {
                                "route": "10.16.2.2/32",
                                "active": True,
                                "route_preference": 90,
                                "metric": 10752,
                                "source_protocol": "eigrp",
                                "source_protocol_codes": "D",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.12.90.2",
                                            "outgoing_interface": "GigabitEthernet2.90",
                                            "updated": "4d19h",
                                        }
                                    }
                                },
                            },
                            "10.4.1.1/32": {
                                "route": "10.4.1.1/32",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {"outgoing_interface": "Loopback0"}
                                    }
                                },
                            },
                        }
                    },
                    "ipv6": {
                        "routes": {
                            "2001:1:1:1::1/128": {
                                "route": "2001:1:1:1::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "LC",
                                "source_protocol": "local_connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {
                                            "outgoing_interface": "Loopback0"
                                        }
                                    }
                                }
                            },
                            "2001:2:2:2::2/128": {
                                "route": "2001:2:2:2::2/128",
                                "active": True,
                                "metric": 10752,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        }
                                    }
                                }
                            },
                            "2001:3:3:3::3/128": {
                                "route": "2001:3:3:3::3/128",
                                "active": True,
                                "metric": 2570240,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:90::/64": {
                                "route": "2001:10:12:90::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.90": {
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:90::1/128": {
                                "route": "2001:10:12:90::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.90": {
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:110::/64": {
                                "route": "2001:10:12:110::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.110": {
                                            "outgoing_interface": "GigabitEthernet2.110"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:110::1/128": {
                                "route": "2001:10:12:110::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.110": {
                                            "outgoing_interface": "GigabitEthernet2.110"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:115::/64": {
                                "route": "2001:10:12:115::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.115": {
                                            "outgoing_interface": "GigabitEthernet2.115"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:115::1/128": {
                                "route": "2001:10:12:115::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.115": {
                                            "outgoing_interface": "GigabitEthernet2.115"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:120::/64": {
                                "route": "2001:10:12:120::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.120": {
                                            "outgoing_interface": "GigabitEthernet2.120"
                                        }
                                    }
                                }
                            },
                            "2001:10:12:120::1/128": {
                                "route": "2001:10:12:120::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet2.120": {
                                            "outgoing_interface": "GigabitEthernet2.120"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:90::/64": {
                                "route": "2001:10:13:90::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.90": {
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:90::1/128": {
                                "route": "2001:10:13:90::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.90": {
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:110::/64": {
                                "route": "2001:10:13:110::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.110": {
                                            "outgoing_interface": "GigabitEthernet3.110"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:110::1/128": {
                                "route": "2001:10:13:110::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.110": {
                                            "outgoing_interface": "GigabitEthernet3.110"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:115::/64": {
                                "route": "2001:10:13:115::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.115": {
                                            "outgoing_interface": "GigabitEthernet3.115"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:115::1/128": {
                                "route": "2001:10:13:115::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.115": {
                                            "outgoing_interface": "GigabitEthernet3.115"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:120::/64": {
                                "route": "2001:10:13:120::/64",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.120": {
                                            "outgoing_interface": "GigabitEthernet3.120"
                                        }
                                    }
                                }
                            },
                            "2001:10:13:120::1/128": {
                                "route": "2001:10:13:120::1/128",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet3.120": {
                                            "outgoing_interface": "GigabitEthernet3.120"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:90::/64": {
                                "route": "2001:10:23:90::/64",
                                "active": True,
                                "metric": 15360,
                                "route_preference": 90,
                                "source_protocol_codes": "D",
                                "source_protocol": "eigrp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.90"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.90"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:110::/64": {
                                "route": "2001:10:23:110::/64",
                                "active": True,
                                "metric": 2,
                                "route_preference": 110,
                                "source_protocol_codes": "O",
                                "source_protocol": "ospf",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.110"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:115::/64": {
                                "route": "2001:10:23:115::/64",
                                "active": True,
                                "metric": 20,
                                "route_preference": 115,
                                "source_protocol_codes": "I1",
                                "source_protocol": "isis",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::F816:3EFF:FE21:73F6",
                                            "outgoing_interface": "GigabitEthernet2.115"
                                        }
                                    }
                                }
                            },
                            "2001:10:23:120::/64": {
                                "route": "2001:10:23:120::/64",
                                "active": True,
                                "metric": 2,
                                "route_preference": 120,
                                "source_protocol_codes": "R",
                                "source_protocol": "rip",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "FE80::5C00:80FF:FE02:7",
                                            "outgoing_interface": "GigabitEthernet3.120"
                                        }
                                    }
                                }
                            },
                            "FF00::/8": {
                                "route": "FF00::/8",
                                "active": True,
                                "metric": 0,
                                "route_preference": 0,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Null0": {
                                            "outgoing_interface": "Null0"
                                        }
                                    }
                                }
                            },
                        }
                    },
                }
            },
        }
    }
