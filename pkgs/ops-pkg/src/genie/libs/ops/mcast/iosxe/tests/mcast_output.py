''' 
Mcast Genie Ops Object Outputs for IOSXE.
'''


class McastOutput(object):

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
                                  "enable_alert_percent": {
                                       "alert_percent_value": 10000
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
                                       "alert_percent_value": 7000
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

    # Set output for 'vrf default' as input to parser
    ShowIpMroute_default_output = '''\
        IP Multicast Routing Table
        Flags: D - Dense, S - Sparse, B - Bidir Group, s - SSM Group, C - Connected,
               L - Local, P - Pruned, R - RP-bit set, F - Register flag,
               T - SPT-bit set, J - Join SPT, M - MSDP created entry, E - Extranet,
               X - Proxy Join Timer Running, A - Candidate for MSDP Advertisement,
               U - URD, I - Received Source Specific Host Report, 
               Z - Multicast Tunnel, z - MDT-data group sender, 
               Y - Joined MDT-data group, y - Sending to MDT-data group, 
               G - Received BGP C-Mroute, g - Sent BGP C-Mroute, 
               N - Received BGP Shared-Tree Prune, n - BGP C-Mroute suppressed, 
               Q - Received BGP S-A Route, q - Sent BGP S-A Route, 
               V - RD & Vector, v - Vector, p - PIM Joins on route, 
               x - VxLAN group
        Outgoing interface flags: H - Hardware switched, A - Assert winner, p - PIM Join
         Timers: Uptime/Expires
         Interface state: Interface, Next-Hop or VCD, State/Mode

        (*, 239.1.1.1), 00:00:03/stopped, RP 10.4.1.1, flags: SPF
          Incoming interface: Null, RPF nbr 0.0.0.0
          Outgoing interface list: Null

        (10.4.1.1, 239.1.1.1), 00:00:03/00:02:57, flags: PFT
          Incoming interface: Loopback0, RPF nbr 0.0.0.0, Registering
          Outgoing interface list: Null

        (10.1.3.1, 239.1.1.1), 00:00:03/00:02:57, flags: PFT
          Incoming interface: GigabitEthernet2, RPF nbr 0.0.0.0, Registering
          Outgoing interface list: Null

        (*, 224.0.1.40), 2d09h/00:02:56, RP 10.16.2.2, flags: SCL
          Incoming interface: Null, RPF nbr 0.0.0.0
          Outgoing interface list:
            Loopback0, Forward/Sparse, 2d09h/00:02:56

        (*, 224.1.1.1), 00:03:57/00:02:54, RP 172.16.0.0, flags: SJ
          Incoming interface: Null, RPF nbr 224.0.0.0224.0.0.0
          Outgoing interface list:
            ATM0/0, VCD 14, Forward/Sparse, 00:03:57/00:02:53
    '''

    ShowIpv6Mroute_default_output = '''\
        Multicast Routing Table
        Flags:D - Dense, S - Sparse, B - Bidir Group, s - SSM Group, 
               C - Connected, L - Local, I - Received Source Specific Host Report,
               P - Pruned, R - RP-bit set, F - Register flag, T - SPT-bit set,
               J - Join SPT 
        Timers:Uptime/Expires
        Interface state:Interface, State
        (*, FF07::1), 00:04:45/00:02:47, RP 2001:DB8:6::6, flags:S
          Incoming interface:Tunnel5
          RPF nbr:2001:db8:90:24::6
          Outgoing interface list:
            POS4/0, Forward, 00:04:45/00:02:47
        (2001:DB8:999::99, FF07::1), 00:02:06/00:01:23, flags:SFT
          Incoming interface:POS1/0
          RPF nbr:2001:DB8:999::99
          Outgoing interface list:
            POS4/0, Forward, 00:02:06/00:03:27
    '''

    ShowIpMrouteStatic_default_output = '''\
        Mroute: 172.16.0.0/16, RPF neighbor: 172.30.10.13, distance: 1
        Mroute: 172.16.1.0/24, RPF neighbor: 172.30.10.13, distance: 1
    '''

    ShowIpMulticast_default_output = '''\
        Multicast Routing: enabled
        Multicast Multipath: enabled
        Multicast Route limit: No limit
        Multicast Fallback group mode: Sparse
        Number of multicast boundaries configured with filter-autorp option: 0
        MoFRR: Disabled
    '''

    ShowIpv6Rpf_default_output = '''\
        RPF information for 2001:99:99::99
          RPF interface: GigabitEthernet1
          RPF neighbor: 2001:99:99::99
          RPF route/mask: 2001:99:99::99/128
          RPF type: Mroute
          RPF recursion count: 0
          Metric preference: 128
          Metric: 0
    '''

    ShowIpv6PimInterface_default_output = '''\
        Interface          PIM   Nbr   Hello  DR
                                 Count Intvl  Prior

        GigabitEthernet1   on    1     30     1     
            Address: FE80::5054:FF:FE2C:6CDF
            DR     : FE80::5054:FF:FEAC:64B3
        GigabitEthernet2   on    0     30     1     
            Address: FE80::5054:FF:FEBE:8787
            DR     : this system
        Tunnel2            off    0     30     1     
            Address: ::
            DR     : not elected
        Tunnel1            off    0     30     1     
            Address: FE80::21E:F6FF:FEAC:A600
            DR     : not elected
        Null0              off    0     30     1     
            Address: FE80::1
            DR     : not elected
        Tunnel3            off    0     30     1     
            Address: ::
            DR     : not elected
        Tunnel4            off    0     30     1     
            Address: ::
            DR     : not elected
        Loopback0          on    0     30     1     
            Address: FE80::21E:F6FF:FEAC:A600
            DR     : this system
        Tunnel0            off    0     30     1     
            Address: FE80::21E:F6FF:FEAC:A600
            DR     : not elected
    '''

    # Set output for 'show bgp vrf VRF1 all neighbors' as input to parser
    ShowIpMroute_vrf1_output = '''\
        IP Multicast Routing Table
        Flags: D - Dense, S - Sparse, B - Bidir Group, s - SSM Group, C - Connected,
               L - Local, P - Pruned, R - RP-bit set, F - Register flag,
               T - SPT-bit set, J - Join SPT, M - MSDP created entry, E - Extranet,
               X - Proxy Join Timer Running, A - Candidate for MSDP Advertisement,
               U - URD, I - Received Source Specific Host Report, 
               Z - Multicast Tunnel, z - MDT-data group sender, 
               Y - Joined MDT-data group, y - Sending to MDT-data group, 
               G - Received BGP C-Mroute, g - Sent BGP C-Mroute, 
               N - Received BGP Shared-Tree Prune, n - BGP C-Mroute suppressed, 
               Q - Received BGP S-A Route, q - Sent BGP S-A Route, 
               V - RD & Vector, v - Vector, p - PIM Joins on route, 
               x - VxLAN group
        Outgoing interface flags: H - Hardware switched, A - Assert winner, p - PIM Join
         Timers: Uptime/Expires
         Interface state: Interface, Next-Hop or VCD, State/Mode

        (*, 239.1.1.1), 00:00:04/stopped, RP 10.229.11.11, flags: SPF
          Incoming interface: Null, RPF nbr 0.0.0.0
          Outgoing interface list: Null

        (10.229.11.11, 239.1.1.1), 00:00:04/00:02:55, flags: PFT
          Incoming interface: Loopback1, RPF nbr 0.0.0.0, Registering
          Outgoing interface list: Null

        (*, 224.0.1.40), 00:08:58/00:02:52, RP 10.229.11.11, flags: SJCL
          Incoming interface: Null, RPF nbr 0.0.0.0
          Outgoing interface list:
            Loopback1, Forward/Sparse, 00:08:58/00:02:52
    '''

    ShowIpv6Mroute_vrf1_output = '''\
        Multicast Routing Table
        Flags:D - Dense, S - Sparse, B - Bidir Group, s - SSM Group, 
               C - Connected, L - Local, I - Received Source Specific Host Report,
               P - Pruned, R - RP-bit set, F - Register flag, T - SPT-bit set,
               J - Join SPT 
        Timers:Uptime/Expires
        Interface state:Interface, State
        (*, FF07::1), 00:04:45/00:02:47, RP 2001:DB8:6::6, flags:S
          Incoming interface:Tunnel5
          RPF nbr:2001:db8:90:24::6
          Outgoing interface list:
            POS4/0, Forward, 00:04:45/00:02:47
        (2001:DB8:999::99, FF07::1), 00:02:06/00:01:23, flags:SFT
          Incoming interface:POS1/0
          RPF nbr:2001:DB8:999::99
          Outgoing interface list:
            POS4/0, Forward, 00:02:06/00:03:27
    '''

    ShowIpMrouteStatic_vrf1_output = '''\
        Mroute: 10.1.77.77/32, RPF neighbor: 10.12.12.13, distance: 1
    '''

    ShowIpMulticast_vrf1_output = '''\
        Multicast Routing: enabled
        Multicast Multipath: disabled
        Multicast Route limit: No limit
        Multicast Fallback group mode: Sparse
        Number of multicast boundaries configured with filter-autorp option: 0
        MoFRR: Disabled
    '''

    ShowIpv6Rpf_vrf1_output = '''\
        RPF information for 2001:99:99::99
          RPF interface: GigabitEthernet3
          RPF neighbor: 2001:99:99::99
          RPF route/mask: 2001:99:99::99/128
          RPF type: Mroute
          RPF recursion count: 0
          Metric preference: 128
          Metric: 0
    '''

    ShowIpv6PimInterface_vrf1_output = '''\
        Interface          PIM   Nbr   Hello  DR
                                 Count Intvl  Prior

        GigabitEthernet3   on    0     30     1     
            Address: FE80::5054:FF:FE84:F097
            DR     : this system
        Tunnel5            off    0     30     1     
            Address: FE80::21E:F6FF:FEAC:A600
            DR     : not elected
        Tunnel6            off    0     30     1     
            Address: ::
            DR     : not elected
        Tunnel7            off    0     30     1     
            Address: ::
            DR     : not elected
        Loopback1          on    0     30     1     
            Address: FE80::21E:F6FF:FEAC:A600
            DR     : this system
    '''

    McastInfo = {
        "vrf": {
          "VRF1": {
               "address_family": {
                    "ipv4": {
                         "enable": True,
                         "multipath": False,
                         "mroute": {
                              "10.1.77.77/32": {
                                   "path": {
                                        "10.12.12.13 1": {
                                             "admin_distance": "1",
                                             "neighbor_address": "10.12.12.13"
                                        }
                                   }
                              }
                         }
                    },
                    "ipv6": {
                         "enable": True,
                         "mroute": {
                              "FF07::1": {
                                   "path": {
                                        "2001:99:99::99 GigabitEthernet3 128": {
                                             "admin_distance": "128",
                                             "neighbor_address": "2001:99:99::99",
                                             "interface_name": "GigabitEthernet3"
                                        }
                                   }
                              }
                         }
                    }
               }
          },
          "default": {
               "address_family": {
                    "ipv6": {
                         "enable": True,
                         "mroute": {
                              "FF07::1": {
                                   "path": {
                                        "2001:99:99::99 GigabitEthernet1 128": {
                                             "admin_distance": "128",
                                             "neighbor_address": "2001:99:99::99",
                                             "interface_name": "GigabitEthernet1"
                                        }
                                   }
                              }
                         }
                    },
                    "ipv4": {
                         "enable": True,
                         "multipath": True,
                         "mroute": {
                              "172.16.0.0/16": {
                                   "path": {
                                        "172.30.10.13 1": {
                                             "admin_distance": "1",
                                             "neighbor_address": "172.30.10.13"
                                        }
                                   }
                              },
                              "172.16.1.0/24": {
                                   "path": {
                                        "172.30.10.13 1": {
                                             "admin_distance": "1",
                                             "neighbor_address": "172.30.10.13"
                                        }
                                   }
                              }
                         }
                    }
               }
          }
     }
    }

    McastTable = {
        "vrf": {
          "VRF1": {
               "address_family": {
                    "ipv6": {
                         "multicast_group": {
                              "FF07::1": {
                                   "source_address": {
                                        "2001:DB8:999::99": {
                                             "expire": "00:01:23",
                                             "uptime": "00:02:06",
                                             "flags": "SFT",
                                             "rpf_nbr": "2001:DB8:999::99",
                                             "outgoing_interface_list": {
                                                  "POS4/0": {
                                                       "expire": "00:03:27",
                                                       "uptime": "00:02:06",
                                                       "state_mode": "forward"
                                                  }
                                             },
                                             "incoming_interface_list": {
                                                  "POS1/0": {
                                                       "rpf_nbr": "2001:DB8:999::99"
                                                  }
                                             }
                                        },
                                        "*": {
                                             "rp": "2001:DB8:6::6",
                                             "uptime": "00:04:45",
                                             "outgoing_interface_list": {
                                                  "POS4/0": {
                                                       "expire": "00:02:47",
                                                       "uptime": "00:04:45",
                                                       "state_mode": "forward"
                                                  }
                                             },
                                             "expire": "00:02:47",
                                             "flags": "S",
                                             "rpf_nbr": "2001:db8:90:24::6",
                                             "incoming_interface_list": {
                                                  "Tunnel5": {
                                                       "rpf_nbr": "2001:db8:90:24::6"
                                                  }
                                             }
                                        }
                                   }
                              }
                         }
                    },
                    "ipv4": {
                         "multicast_group": {
                              "224.0.1.40": {
                                   "source_address": {
                                        "*": {
                                             "rp": "10.229.11.11",
                                             "uptime": "00:08:58",
                                             "outgoing_interface_list": {
                                                  "Loopback1": {
                                                       "expire": "00:02:52",
                                                       "uptime": "00:08:58",
                                                       "state_mode": "forward/sparse"
                                                  }
                                             },
                                             "expire": "00:02:52",
                                             "flags": "SJCL",
                                             "rpf_nbr": "0.0.0.0",
                                        }
                                   }
                              },
                              "239.1.1.1": {
                                   "source_address": {
                                        "*": {
                                             "rp": "10.229.11.11",
                                             "expire": "stopped",
                                             "uptime": "00:00:04",
                                             "flags": "SPF",
                                             "rpf_nbr": "0.0.0.0",
                                        },
                                        "10.229.11.11": {
                                             "expire": "00:02:55",
                                             "uptime": "00:00:04",
                                             "flags": "PFT",
                                             "rpf_nbr": "0.0.0.0",
                                             "incoming_interface_list": {
                                                  "Loopback1": {
                                                       "rpf_nbr": "0.0.0.0",
                                                       "rpf_info": "registering"
                                                  }
                                             }
                                        }
                                   }
                              }
                         }
                    }
               }
          },
          "default": {
               "address_family": {
                    "ipv6": {
                         "multicast_group": {
                              "FF07::1": {
                                   "source_address": {
                                        "2001:DB8:999::99": {
                                             "expire": "00:01:23",
                                             "uptime": "00:02:06",
                                             "flags": "SFT",
                                             "rpf_nbr": "2001:DB8:999::99",
                                             "outgoing_interface_list": {
                                                  "POS4/0": {
                                                       "expire": "00:03:27",
                                                       "uptime": "00:02:06",
                                                       "state_mode": "forward"
                                                  }
                                             },
                                             "incoming_interface_list": {
                                                  "POS1/0": {
                                                       "rpf_nbr": "2001:DB8:999::99"
                                                  }
                                             }
                                        },
                                        "*": {
                                             "rp": "2001:DB8:6::6",
                                             "uptime": "00:04:45",
                                             "outgoing_interface_list": {
                                                  "POS4/0": {
                                                       "expire": "00:02:47",
                                                       "uptime": "00:04:45",
                                                       "state_mode": "forward"
                                                  }
                                             },
                                             "expire": "00:02:47",
                                             "flags": "S",
                                             "rpf_nbr": "2001:db8:90:24::6",
                                             "incoming_interface_list": {
                                                  "Tunnel5": {
                                                       "rpf_nbr": "2001:db8:90:24::6"
                                                  }
                                             }
                                        }
                                   }
                              }
                         }
                    },
                    "ipv4": {
                         "multicast_group": {
                              "224.0.1.40": {
                                   "source_address": {
                                        "*": {
                                             "rp": "10.16.2.2",
                                             "uptime": "2d09h",
                                             "outgoing_interface_list": {
                                                  "Loopback0": {
                                                       "expire": "00:02:56",
                                                       "uptime": "2d09h",
                                                       "state_mode": "forward/sparse"
                                                  }
                                             },
                                             "expire": "00:02:56",
                                             "flags": "SCL",
                                             "rpf_nbr": "0.0.0.0",
                                        }
                                   }
                              },
                              "239.1.1.1": {
                                   "source_address": {
                                        "*": {
                                             "rp": "10.4.1.1",
                                             "expire": "stopped",
                                             "uptime": "00:00:03",
                                             "flags": "SPF",
                                             "rpf_nbr": "0.0.0.0",
                                        },
                                        "10.1.3.1": {
                                             "expire": "00:02:57",
                                             "uptime": "00:00:03",
                                             "flags": "PFT",
                                             "rpf_nbr": "0.0.0.0",
                                             "incoming_interface_list": {
                                                  "GigabitEthernet2": {
                                                       "rpf_nbr": "0.0.0.0",
                                                       "rpf_info": "registering"
                                                  }
                                             }
                                        },
                                        "10.4.1.1": {
                                             "expire": "00:02:57",
                                             "uptime": "00:00:03",
                                             "flags": "PFT",
                                             "rpf_nbr": "0.0.0.0",
                                             "incoming_interface_list": {
                                                  "Loopback0": {
                                                       "rpf_nbr": "0.0.0.0",
                                                       "rpf_info": "registering"
                                                  }
                                             }
                                        }
                                   }
                              },
                              "224.1.1.1": {
                                   "source_address": {
                                        "*": {
                                             "rp": "172.16.0.0",
                                             "uptime": "00:03:57",
                                             "outgoing_interface_list": {
                                                  "ATM0/0": {
                                                       "expire": "00:02:53",
                                                       "uptime": "00:03:57",
                                                       "vcd": "14",
                                                       "state_mode": "forward/sparse"
                                                  }
                                             },
                                             "expire": "00:02:54",
                                             "flags": "SJ",
                                             "rpf_nbr": "224.0.0.0224.0.0.0",
                                        }
                                   }
                              }
                         }
                    }
               }
          }
     }
    }
