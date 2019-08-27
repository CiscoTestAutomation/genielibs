''' 
Rip Genie Ops Object Outputs for IOS
'''


class RipOutput(object):

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

    showIpProtocols_default = '''\
    R1#show ip protocols | sec rip
Routing Protocol is "rip"
  Output delay 50 milliseconds between packets
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Incoming routes will have 10 added to metric if on list 21
  Sending updates every 10 seconds, next due in 8 seconds
  Invalid after 21 seconds, hold down 22, flushed after 23
  Default redistribution metric is 3
  Redistributing: connected, static, rip
  Neighbor(s):
    10.1.2.2
  Default version control: send version 2, receive version 2
    Interface                           Send  Recv  Triggered RIP  Key-chain
    GigabitEthernet3.100                2     2          No        1
  Automatic network summarization is not in effect
  Address Summarization:
    172.16.0.0/17 for GigabitEthernet3.100
  Maximum path: 4
  Routing for Networks:
    10.0.0.0
  Passive Interface(s):
    GigabitEthernet2.100
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.1.3.3             120      00:00:00
    10.1.2.2             120      00:00:04
  Distance: (default is 120)
        '''
    showIpProtocols_vrf1 = '''\
R1#show ip protocols vrf VRF1 | sec rip
Routing Protocol is "rip"
  Output delay 50 milliseconds between packets
  Outgoing update filter list for all interfaces is not set
  Incoming update filter list for all interfaces is not set
  Sending updates every 30 seconds, next due in 2 seconds
  Invalid after 180 seconds, hold down 180, flushed after 240
  Redistributing: connected, static, rip
  Default version control: send version 2, receive version 2
    Interface                           Send  Recv  Triggered RIP  Key-chain
    GigabitEthernet2.200                2     2          No        none
    GigabitEthernet3.200                2     2          No        none
  Maximum path: 4
  Routing for Networks:
     10.0.0.0
    10.0.0.0
  Routing Information Sources:
    Gateway         Distance      Last Update
    10.1.3.3             120      20:33:00
    10.1.2.2             120      00:00:21
  Distance: (default is 120)
        '''

    showIpRipDatabase_default = '''\
    R1#show ip rip database
0.0.0.0/0    auto-summary
0.0.0.0/0    redistributed
    [3] via 172.16.1.254, from 0.0.0.0,
    [3] via 172.16.1.254, from 0.0.0.0,
10.0.0.0/8    auto-summary
10.1.2.0/24    directly connected, GigabitEthernet2.100
10.1.3.0/24    directly connected, GigabitEthernet3.100
10.2.3.0/24
    [1] via 10.1.3.3, 00:00:05, GigabitEthernet3.100
    [1] via 10.1.2.2, 00:00:21, GigabitEthernet2.100
172.16.0.0/16    auto-summary
172.16.0.0/17    int-summary
172.16.0.0/17
    [4] via 10.1.2.2, 00:00:00, GigabitEthernet2.100

    '''
    showIpRipDatabase_vrf1 = '''\
    R1#show ip rip database vrf VRF1
10.0.0.0/8    auto-summary
10.1.2.0/24    directly connected, GigabitEthernet2.200
10.1.3.0/24    directly connected, GigabitEthernet3.200
10.2.3.0/24
    [1] via 10.1.2.2, 00:00:08, GigabitEthernet2.200
172.16.0.0/16    auto-summary
172.16.11.0/24    redistributed
    [15] via 0.0.0.0,
172.16.22.0/24
    [15] via 10.1.2.2, 00:00:08, GigabitEthernet2.200
192.168.1.0/24    auto-summary
192.168.1.1/32    redistributed
     [1] via 0.0.0.0,
        '''

    showIpv6Protocols_default = '''\
        R1#show ipv6 protocols | sec rip
    IPv6 Routing Protocol is "rip ripng"
      Interfaces:
        GigabitEthernet3.100
        GigabitEthernet2.100
      Redistribution:
        Redistributing protocol static with metric 3
            '''
    showIpv6Protocols_vrf1 = '''\
        R1#show ipv6 protocols vrf VRF1 | sec rip
    IPv6 Routing Protocol is "rip ripng"
      Interfaces:
        GigabitEthernet3.200
        GigabitEthernet2.200
      Redistribution:
        Redistributing protocol connected with transparent metric
        Redistributing protocol static with transparent metric route-map static-to-rip
               '''

    showIpv6RipDatabase_default =  '''\
    R1#show ipv6 rip database
    RIP VRF "Default VRF", local RIB
     2001:DB8:1:3::/64, metric 2
         GigabitEthernet3.100/FE80::F816:3EFF:FEFF:1E3D, expires in 179 secs
     2001:DB8:2:3::/64, metric 2, installed
         GigabitEthernet3.100/FE80::F816:3EFF:FEFF:1E3D, expires in 179 secs
     2001:DB8:2222:2222::/64, metric 7, installed
         GigabitEthernet3.100/FE80::F816:3EFF:FEFF:1E3D, expires in 179 secs
     2001:DB8:2223:2223::/64, metric 6, installed
         GigabitEthernet2.100/FE80::F816:3EFF:FE7B:437, expires in 173 secs
        '''

    showIpv6RipDatabase_vrf1 = '''\
    R1#show ipv6 rip vrf VRF1 database
RIP VRF "VRF1", local RIB
 2001:DB8:1:2::/64, metric 2
     GigabitEthernet2.200/FE80::F816:3EFF:FE7B:437, expires in 166 secs
 2001:DB8:1:3::/64, metric 2
     GigabitEthernet3.200/FE80::F816:3EFF:FEFF:1E3D, expires in 169 secs
 2001:DB8:2:3::/64, metric 2, installed
     GigabitEthernet3.200/FE80::F816:3EFF:FEFF:1E3D, expires in 169 secs
     GigabitEthernet2.200/FE80::F816:3EFF:FE7B:437, expires in 166 secs
    '''

    showIpv6Rip_default = '''\
        R1#show ipv6 rip
        RIP VRF "Default VRF", port 521, multicast-group FF02::9, pid 635
         Administrative distance is 120. Maximum paths is 16
         Updates every 30 seconds, expire after 180
         Holddown lasts 0 seconds, garbage collect after 120
         Split horizon is on; poison reverse is off
         Default routes are not generated
         Periodic updates 399, trigger updates 8
         Full Advertisement 0, Delayed Events 0
        Interfaces:
            GigabitEthernet3.100
            GigabitEthernet2.100
        Redistribution:
            Redistributing protocol static with metric 3
        '''

    showIpv6Rip_vrf1= '''\
    R1#show ipv6 rip vrf VRF1
    RIP VRF "VRF1", port 521, multicast-group FF02::9, pid 635
     Administrative distance is 120. Maximum paths is 16
     Updates every 30 seconds, expire after 180
     Holddown lasts 0 seconds, garbage collect after 120
     Split horizon is on; poison reverse is off
     Default routes are generated
     Periodic updates 390, trigger updates 3
     Full Advertisement 0, Delayed Events 0
    Interfaces:
       GigabitEthernet3.200
       GigabitEthernet2.200
    Redistribution:
       Redistributing protocol connected with transparent metric
       Redistributing protocol static with transparent metric route-map static-to-rip
'''
    ripOpsOutput={
    "vrf": {
        "default": {
            "address_family": {
                "ipv6": {
                    "instance": {
                        "rip ripng": {
                            "redistribute": {
                                "static": {
                                    "metric": 3
                                }
                            },
                            "timers": {
                                "holddown_interval": 0,
                                "flush_interval": 120,
                                "update_interval": 30
                            },
                            "maximum_paths": 16,
                            "split_horizon": True,
                            "routes": {
                                "2001:DB8:2223:2223::/64": {
                                    "index": {
                                        1: {
                                            "metric": 6,
                                            "expire_time": "173",
                                            "interface": "GigabitEthernet2.100",
                                            "next_hop": "FE80::F816:3EFF:FE7B:437"
                                        }
                                    }
                                },
                                "2001:DB8:2:3::/64": {
                                    "index": {
                                        1: {
                                            "metric": 2,
                                            "expire_time": "179",
                                            "interface": "GigabitEthernet3.100",
                                            "next_hop": "FE80::F816:3EFF:FEFF:1E3D"
                                        }
                                    }
                                },
                                "2001:DB8:1:3::/64": {
                                    "index": {
                                        1: {
                                            "metric": 2,
                                            "expire_time": "179",
                                            "interface": "GigabitEthernet3.100",
                                            "next_hop": "FE80::F816:3EFF:FEFF:1E3D"
                                        }
                                    }
                                },
                                "2001:DB8:2222:2222::/64": {
                                    "index": {
                                        1: {
                                            "metric": 7,
                                            "expire_time": "179",
                                            "interface": "GigabitEthernet3.100",
                                            "next_hop": "FE80::F816:3EFF:FEFF:1E3D"
                                        }
                                    }
                                }
                            },
                            "originate_default_route": {
                                "enabled": False
                            },
                            "distance": 120,
                            "poison_reverse": False,
                            "interfaces": {
                                "GigabitEthernet3.100": {},
                                "GigabitEthernet2.100": {}
                            }
                        }
                    }
                },
                "ipv4": {
                    "instance": {
                        "rip": {
                            "distance": 120,
                            "output_delay": 50,
                            "maximum_paths": 4,
                            "default_metric": 3,
                            "routes": {
                                "10.2.3.0/24": {
                                    "index": {
                                        1: {
                                            "metric": 1,
                                            "next_hop": "10.1.3.3",
                                            "interface": "GigabitEthernet3.100"
                                        },
                                        2: {
                                            "metric": 1,
                                            "next_hop": "10.1.2.2",
                                            "interface": "GigabitEthernet2.100"
                                        }
                                    }
                                },
                                "10.0.0.0/8": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        }
                                    }
                                },
                                "172.16.0.0/17": {
                                    "index": {
                                        1: {
                                            "summary_type": "int-summary"
                                        },
                                        2: {
                                            "metric": 4,
                                            "next_hop": "10.1.2.2",
                                            "interface": "GigabitEthernet2.100"
                                        }
                                    }
                                },
                                "0.0.0.0/0": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        },
                                        2: {
                                            "metric": 3,
                                            "next_hop": "172.16.1.254",
                                            "redistributed": True
                                        },
                                        3: {
                                            "metric": 3,
                                            "next_hop": "172.16.1.254",
                                            "redistributed": True
                                        }
                                    }
                                },
                                "172.16.0.0/16": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        }
                                    }
                                },
                                "10.1.2.0/24": {
                                    "index": {
                                        1: {
                                            "route_type": "connected",
                                            "interface": "GigabitEthernet2.100"
                                        }
                                    }
                                },
                                "10.1.3.0/24": {
                                    "index": {
                                        1: {
                                            "route_type": "connected",
                                            "interface": "GigabitEthernet3.100"
                                        }
                                    }
                                }
                            },
                            "interfaces": {
                                "GigabitEthernet3.100": {
                                    "passive": True,
                                    "summary_address": {
                                        "172.16.0.0/17": {}
                                    }
                                }
                            },
                            "redistribute": {
                                "static": {},
                                "rip": {},
                                "connected": {}
                            }
                        }
                    }
                }
            }
        },
        "VRF1": {
            "address_family": {
                "ipv6": {
                    "instance": {
                        "rip ripng": {
                            "redistribute": {
                                "static": {
                                    "route_policy": "static-to-rip"
                                },
                                "connected": {}
                            },
                            "timers": {
                                "update_interval": 30,
                                "flush_interval": 120,
                                "holddown_interval": 0
                            },
                            "maximum_paths": 16,
                            "split_horizon": True,
                            "routes": {
                                "2001:DB8:2:3::/64": {
                                    "index": {
                                        1: {
                                            "metric": 2,
                                            "expire_time": "169",
                                            "interface": "GigabitEthernet3.200",
                                            "next_hop": "FE80::F816:3EFF:FEFF:1E3D"
                                        },
                                        2: {
                                            "metric": 2,
                                            "expire_time": "166",
                                            "interface": "GigabitEthernet2.200",
                                            "next_hop": "FE80::F816:3EFF:FE7B:437"
                                        }
                                    }
                                },
                                "2001:DB8:1:3::/64": {
                                    "index": {
                                        1: {
                                            "metric": 2,
                                            "expire_time": "169",
                                            "interface": "GigabitEthernet3.200",
                                            "next_hop": "FE80::F816:3EFF:FEFF:1E3D"
                                        }
                                    }
                                },
                                "2001:DB8:1:2::/64": {
                                    "index": {
                                        1: {
                                            "metric": 2,
                                            "expire_time": "166",
                                            "interface": "GigabitEthernet2.200",
                                            "next_hop": "FE80::F816:3EFF:FE7B:437"
                                        }
                                    }
                                }
                            },
                            "originate_default_route": {
                                "enabled": True
                            },
                            "distance": 120,
                            "poison_reverse": False,
                            "interfaces": {
                                "GigabitEthernet2.200": {},
                                "GigabitEthernet3.200": {}
                            }
                        }
                    }
                },
                "ipv4": {
                    "instance": {
                        "rip": {
                            "distance": 120,
                            "output_delay": 50,
                            "routes": {
                                "192.168.1.1/32": {
                                    "index": {
                                        1: {
                                            "metric": 1,
                                            "next_hop": "0.0.0.0",
                                            "redistributed": True
                                        }
                                    }
                                },
                                "192.168.1.0/24": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        }
                                    }
                                },
                                "172.16.22.0/24": {
                                    "index": {
                                        1: {
                                            "metric": 15,
                                            "next_hop": "10.1.2.2",
                                            "interface": "GigabitEthernet2.200"
                                        }
                                    }
                                },
                                "10.0.0.0/8": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        }
                                    }
                                },
                                "10.1.2.0/24": {
                                    "index": {
                                        1: {
                                            "route_type": "connected",
                                            "interface": "GigabitEthernet2.200"
                                        }
                                    }
                                },
                                "172.16.0.0/16": {
                                    "index": {
                                        1: {
                                            "summary_type": "auto-summary"
                                        }
                                    }
                                },
                                "172.16.11.0/24": {
                                    "index": {
                                        1: {
                                            "metric": 15,
                                            "next_hop": "0.0.0.0",
                                            "redistributed": True
                                        }
                                    }
                                },
                                "10.2.3.0/24": {
                                    "index": {
                                        1: {
                                            "metric": 1,
                                            "next_hop": "10.1.2.2",
                                            "interface": "GigabitEthernet2.200"
                                        }
                                    }
                                },
                                "10.1.3.0/24": {
                                    "index": {
                                        1: {
                                            "route_type": "connected",
                                            "interface": "GigabitEthernet3.200"
                                        }
                                    }
                                }
                            },
                            "redistribute": {
                                "static": {},
                                "rip": {},
                                "connected": {}
                            },
                            "maximum_paths": 4
                        }
                    }
                }
            }
        }
    }
}
