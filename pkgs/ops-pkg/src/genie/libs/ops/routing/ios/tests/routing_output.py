'''
 Route Genie Ops Object Outputs for IOS
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
        R1_iosv#show ip route
        Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
               D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
               N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
               E1 - OSPF external type 1, E2 - OSPF external type 2
               i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
               ia - IS-IS inter area, * - candidate default, U - per-user static route
               o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
               a - application route
               + - replicated route, % - next hop override

        Gateway of last resort is not set

              10.1.0.0/32 is subnetted, 1 subnets
        C        10.4.1.1 is directly connected, Loopback0
              10.4.0.0/32 is subnetted, 1 subnets
        S        10.16.2.2 [1/0] via 10.186.2.2, GigabitEthernet0/1
                         [1/0] via 10.1.2.2, GigabitEthernet0/0
              10.9.0.0/32 is subnetted, 1 subnets
        S        10.36.3.3 is directly connected, GigabitEthernet0/3
                         is directly connected, GigabitEthernet0/2
              10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
        C        10.1.2.0/24 is directly connected, GigabitEthernet0/0
        L        10.1.2.1/32 is directly connected, GigabitEthernet0/0
        C        10.1.3.0/24 is directly connected, GigabitEthernet0/2
        L        10.1.3.1/32 is directly connected, GigabitEthernet0/2
        O        10.2.3.0/24 [110/2] via 10.186.2.2, 06:46:59, GigabitEthernet0/1
                             [110/2] via 10.1.2.2, 06:46:59, GigabitEthernet0/0
               10.229.0.0/32 is subnetted, 1 subnets
        i L1     10.151.22.22 [115/20] via 10.186.2.2, 06:47:04, GigabitEthernet0/1
                         [115/20] via 10.1.2.2, 06:47:04, GigabitEthernet0/0
              10.4.0.0/32 is subnetted, 1 subnets
        B        10.16.32.32 [200/0] via 10.66.12.12, 1d00h
    '''
    showIpRoute_VRF1 = '''\
        PE1#sh ip route vrf VRF1
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

              10.0.0.0/24 is subnetted, 50 subnets
        O        10.0.0.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
        O        10.0.1.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
        O        10.0.2.0 [110/1] via 10.81.1.2, 01:02:20, GigabitEthernet0/0/2.100
              10.145.0.0/24 is subnetted, 50 subnets
        B        10.145.0.0 [200/1] via 192.168.51.1, 01:01:10
        B        10.145.1.0 [200/1] via 192.168.51.1, 01:01:10
        B        10.145.2.0 [200/1] via 192.168.51.1, 01:01:10
              10.81.0.0/8 is variably subnetted, 2 subnets, 2 masks
        C        10.81.1.0/24 is directly connected, GigabitEthernet0/0/2.100
        L        10.81.1.1/32 is directly connected, GigabitEthernet0/0/2.100
        B     192.168.4.0/24 [200/0] via 192.168.51.1, 01:01:10

    '''
    showIpv6RouteUpdated_default = '''\
        R1_iosv#show ipv6 route updated
        IPv6 Routing Table - default - 23 entries
        Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
               B - BGP, HA - Home Agent, MR - Mobile Router, R - RIP
               H - NHRP, I1 - ISIS L1, I2 - ISIS L2, IA - ISIS interarea
               IS - ISIS summary, D - EIGRP, EX - EIGRP external, NM - NEMO
               ND - ND Default, NDp - ND Prefix, DCE - Destination, NDr - Redirect
               O - OSPF Intra, OI - OSPF Inter, OE1 - OSPF ext 1, OE2 - OSPF ext 2
               ON1 - OSPF NSSA ext 1, ON2 - OSPF NSSA ext 2, la - LISP alt
               lr - LISP site-registrations, ld - LISP dyn-eid, a - Application
        LC  2001:1:1:1::1/128 [0/0]
             via Loopback0, receive
              Last updated 22:55:51 04 December 2017
        S   2001:2:2:2::2/128 [1/0]
             via 2001:10:1:2::2, GigabitEthernet0/0
              Last updated 22:57:07 04 December 2017
             via 2001:20:1:2::2, GigabitEthernet0/1
              Last updated 22:57:23 04 December 2017
        S   2001:3:3:3::3/128 [1/0]
             via GigabitEthernet0/2, directly connected
              Last updated 22:57:34 04 December 2017
             via GigabitEthernet0/3, directly connected
              Last updated 22:57:43 04 December 2017
        B   2001:db8:400:1::/64 [200/1]
            via 192.168.51.1%default, indirectly connected
            Last updated 09:43:27 06 December 2017
    '''

    showIpv6RouteUpdated_VRF1 = '''\
        IPv6 Routing Table - VRF1 - 104 entries
        Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
               B - BGP, R - RIP, H - NHRP, I1 - ISIS L1
               I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
               EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
               NDr - Redirect, O - OSPF Intra, OI - OSPF Inter, OE1 - OSPF ext 1
               OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1, ON2 - OSPF NSSA ext 2
               la - LISP alt, lr - LISP site-registrations, ld - LISP dyn-eid
               a - Application
        O   2001:db8:100::/64 [110/1]
             via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
              Last updated 09:42:39 06 December 2017
        O   2001:db8:100:1::/64 [110/1]
             via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
              Last updated 09:42:39 06 December 2017
        O   2001:db8:100:4::/64 [110/1]
             via FE80::211:1FF:FE00:1, GigabitEthernet0/0/2.100
              Last updated 09:42:39 06 December 2017
       '''


    routeOpsOutput = {
        "vrf": {
            "VRF1": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "192.168.4.0/24": {
                                "route": "192.168.4.0/24",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "192.168.51.1",
                                            "updated": "01:01:10",
                                        }
                                    }
                                },
                            },
                            "10.81.1.1/32": {
                                "route": "10.81.1.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/2.100": {
                                            "outgoing_interface": "GigabitEthernet0/0/2.100"
                                        }
                                    }
                                },
                            },
                            "10.81.1.0/24": {
                                "route": "10.81.1.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/2.100": {
                                            "outgoing_interface": "GigabitEthernet0/0/2.100"
                                        }
                                    }
                                },
                            },
                            "10.145.2.0/24": {
                                "route": "10.145.2.0/24",
                                "active": True,
                                "route_preference": 200,
                                "metric": 1,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "192.168.51.1",
                                            "updated": "01:01:10",
                                        }
                                    }
                                },
                            },
                            "10.145.1.0/24": {
                                "route": "10.145.1.0/24",
                                "active": True,
                                "route_preference": 200,
                                "metric": 1,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "192.168.51.1",
                                            "updated": "01:01:10",
                                        }
                                    }
                                },
                            },
                            "10.145.0.0/24": {
                                "route": "10.145.0.0/24",
                                "active": True,
                                "route_preference": 200,
                                "metric": 1,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "192.168.51.1",
                                            "updated": "01:01:10",
                                        }
                                    }
                                },
                            },
                            "10.0.2.0/24": {
                                "route": "10.0.2.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 1,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.81.1.2",
                                            "outgoing_interface": "GigabitEthernet0/0/2.100",
                                            "updated": "01:02:20",
                                        }
                                    }
                                },
                            },
                            "10.0.1.0/24": {
                                "route": "10.0.1.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 1,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.81.1.2",
                                            "outgoing_interface": "GigabitEthernet0/0/2.100",
                                            "updated": "01:02:20",
                                        }
                                    }
                                },
                            },
                            "10.0.0.0/24": {
                                "route": "10.0.0.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 1,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.81.1.2",
                                            "outgoing_interface": "GigabitEthernet0/0/2.100",
                                            "updated": "01:02:20",
                                        }
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
                            "10.16.32.32/32": {
                                "route": "10.16.32.32/32",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.66.12.12",
                                            "updated": "1d00h",
                                        }
                                    }
                                },
                            },
                            "10.151.22.22/32": {
                                "route": "10.151.22.22/32",
                                "active": True,
                                "route_preference": 115,
                                "metric": 20,
                                "source_protocol": "isis",
                                "source_protocol_codes": "i L1",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.1.2.2",
                                            "outgoing_interface": "GigabitEthernet0/0",
                                            "updated": "06:47:04",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.186.2.2",
                                            "outgoing_interface": "GigabitEthernet0/1",
                                            "updated": "06:47:04",
                                        },
                                    }
                                },
                            },
                            "10.2.3.0/24": {
                                "route": "10.2.3.0/24",
                                "active": True,
                                "route_preference": 110,
                                "metric": 2,
                                "source_protocol": "ospf",
                                "source_protocol_codes": "O",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.1.2.2",
                                            "outgoing_interface": "GigabitEthernet0/0",
                                            "updated": "06:46:59",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.186.2.2",
                                            "outgoing_interface": "GigabitEthernet0/1",
                                            "updated": "06:46:59",
                                        },
                                    }
                                },
                            },
                            "10.1.3.1/32": {
                                "route": "10.1.3.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/2": {
                                            "outgoing_interface": "GigabitEthernet0/2"
                                        }
                                    }
                                },
                            },
                            "10.1.3.0/24": {
                                "route": "10.1.3.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/2": {
                                            "outgoing_interface": "GigabitEthernet0/2"
                                        }
                                    }
                                },
                            },
                            "10.1.2.1/32": {
                                "route": "10.1.2.1/32",
                                "active": True,
                                "source_protocol": "local",
                                "source_protocol_codes": "L",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0": {
                                            "outgoing_interface": "GigabitEthernet0/0"
                                        }
                                    }
                                },
                            },
                            "10.1.2.0/24": {
                                "route": "10.1.2.0/24",
                                "active": True,
                                "source_protocol": "connected",
                                "source_protocol_codes": "C",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0": {
                                            "outgoing_interface": "GigabitEthernet0/0"
                                        }
                                    }
                                },
                            },
                            "10.36.3.3/32": {
                                "route": "10.36.3.3/32",
                                "active": True,
                                "source_protocol": "static",
                                "source_protocol_codes": "S",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/2": {
                                            "outgoing_interface": "GigabitEthernet0/2"
                                        },
                                        "GigabitEthernet0/3": {
                                            "outgoing_interface": "GigabitEthernet0/3"
                                        },
                                    }
                                },
                            },
                            "10.16.2.2/32": {
                                "route": "10.16.2.2/32",
                                "active": True,
                                "route_preference": 1,
                                "metric": 0,
                                "source_protocol": "static",
                                "source_protocol_codes": "S",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.1.2.2",
                                            "outgoing_interface": "GigabitEthernet0/0",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.186.2.2",
                                            "outgoing_interface": "GigabitEthernet0/1",
                                        },
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
                            "2001:db8:400:1::/64": {
                                "route": "2001:db8:400:1::/64",
                                "active": True,
                                "route_preference": 200,
                                "metric": 1,
                                "source_protocol": "bgp",
                                "source_protocol_codes": "B",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {"index": 1, "next_hop": "192.168.51.1"}
                                    }
                                },
                            },
                            "2001:3:3:3::3/128": {
                                "route": "2001:3:3:3::3/128",
                                "active": True,
                                "route_preference": 1,
                                "metric": 0,
                                "source_protocol": "static",
                                "source_protocol_codes": "S",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/3": {
                                            "outgoing_interface": "GigabitEthernet0/3"
                                        },
                                        "GigabitEthernet0/2": {
                                            "outgoing_interface": "GigabitEthernet0/2"
                                        },
                                    }
                                },
                            },
                            "2001:2:2:2::2/128": {
                                "route": "2001:2:2:2::2/128",
                                "active": True,
                                "route_preference": 1,
                                "metric": 0,
                                "source_protocol": "static",
                                "source_protocol_codes": "S",
                                "next_hop": {
                                    "next_hop_list": {
                                        2: {
                                            "index": 2,
                                            "next_hop": "2001:20:1:2::2",
                                            "outgoing_interface": "GigabitEthernet0/1",
                                        },
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:10:1:2::2",
                                            "outgoing_interface": "GigabitEthernet0/0",
                                        },
                                    }
                                },
                            },
                            "2001:1:1:1::1/128": {
                                "route": "2001:1:1:1::1/128",
                                "active": True,
                                "route_preference": 0,
                                "metric": 0,
                                "source_protocol": "local_connected",
                                "source_protocol_codes": "LC",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {"outgoing_interface": "Loopback0"}
                                    }
                                },
                            },
                        }
                    },
                }
            },
        }
    }