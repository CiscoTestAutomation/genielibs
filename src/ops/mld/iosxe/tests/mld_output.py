''' 
Mld Genie Ops Object Outputs for IOSXE.
'''


class MldOutput(object):

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

    ShowIpv6MldInterface_default = {
         "vrf": {
            "default": {
                 "interface": {
                      "Tunnel0": {
                           "oper_status": "up",
                           "interface_adress": "FE80::21E:BDFF:FEBA:D000/10",
                           "enable": False,
                           "interface_status": "up"
                      },
                      "VoIP-Null0": {
                           "oper_status": "up",
                           "interface_adress": "::/0",
                           "enable": False,
                           "interface_status": "up"
                      },
                      "LIIN0": {
                           "oper_status": "up",
                           "interface_adress": "::/0",
                           "enable": False,
                           "interface_status": "up"
                      },
                      "GigabitEthernet1": {
                           "oper_status": "up",
                           "querier_timeout": 740,
                           "active_groups": 0,
                           "group_policy": "test",
                           "query_interval": 366,
                           "version": 2,
                           "query_this_system": True,
                           "querier": "FE80::5054:FF:FE7C:DC70",
                           "interface_status": "up",
                           "last_member_query_interval": 1,
                           "counters": {
                                "leaves": 2,
                                "joins": 11
                           },
                           "max_groups": 6400,
                           "query_max_response_time": 16,
                           "enable": True,
                           "interface_adress": "FE80::5054:FF:FE7C:DC70/10"
                      },
                      "GigabitEthernet3": {
                           "oper_status": "down",
                           "interface_adress": "::/0",
                           "enable": False,
                           "interface_status": "administratively down"
                      },
                      "Null0": {
                           "oper_status": "up",
                           "interface_adress": "FE80::1/10",
                           "enable": False,
                           "interface_status": "up"
                      }
                 },
                 "max_groups": 64000,
                 "active_groups": 0
            }
        }
    }

    ShowIpv6MldInterface_VRF1 = '''\
        R4# show ipv6 mld vrf VRF1 interface

        Global State Limit : 0 active out of 64000 max
        GigabitEthernet2 is up, line protocol is up
          Internet address is FE80::5054:FF:FEDD:BB49/10
          MLD is enabled on interface
          Current MLD version is 2
          MLD query interval is 366 seconds
          MLD querier timeout is 740 seconds
          MLD max query response time is 16 seconds
          Last member query response interval is 1 seconds
          Interface State Limit : 0 active out of 6400 max
          MLD activity: 9 joins, 0 leaves
          MLD querying router is FE80::5054:FF:FEDD:BB49 (this system)
        Tunnel1 is up, line protocol is up
          Internet address is FE80::21E:BDFF:FEBA:D000/10
          MLD is disabled on interface
    '''

    ShowIpv6MldGroupsDetail_default = {
        "vrf": {
            "default": {
                 "interface": {
                      "GigabitEthernet1": {
                           "group": {
                                "FF15:1::1": {
                                     "up_time": "08:14:15",
                                     "source": {
                                          "2001:DB8:2:2::2": {
                                               "forward": True,
                                               "up_time": "08:13:22",
                                               "flags": "Remote Local 2D",
                                               "expire": "00:06:42"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "host_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                },
                                "FF25:2::1": {
                                     "up_time": "08:14:01",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70",
                                     "host_mode": "exclude",
                                     "expire": "never"
                                },
                                "FF35:1::1": {
                                     "up_time": "00:42:41",
                                     "source": {
                                          "2001:DB8:3:3::3": {
                                               "forward": True,
                                               "up_time": "00:42:41",
                                               "flags": "Remote Local E",
                                               "expire": "00:06:42"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "host_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                },
                                "FF45:1::1": {
                                     "up_time": "00:42:32",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70",
                                     "host_mode": "exclude",
                                     "expire": "never"
                                }
                           },
                           "join_group": {
                                "FF35:1::1 2001:DB8:3:3::3": {
                                     "group": "FF35:1::1",
                                     "source": "2001:DB8:3:3::3"
                                },
                                "FF15:1::1 2001:DB8:2:2::2": {
                                     "group": "FF15:1::1",
                                     "source": "2001:DB8:2:2::2"
                                }
                           },
                           "static_group": {
                                "FF35:1::1 2001:DB8:3:3::3": {
                                     "group": "FF35:1::1",
                                     "source": "2001:DB8:3:3::3"
                                }
                           }
                      }
                 }
            }
        }
    }

    ShowIpv6MldGroupsDetail_VRF1 = '''\
        R4# show ipv6 mld vrf VRF1 groups detail

        Interface:        GigabitEthernet2
        Group:                FF15:1::1
        Uptime:                08:14:20
        Router mode:        INCLUDE
        Host mode:        INCLUDE
        Last reporter:        FE80::5054:FF:FEDD:BB49
        Group source list:
        Source Address                          Uptime    Expires   Fwd  Flags
        2001:DB8:2:2::2                         08:13:56  00:12:23  Yes  Remote Local 2D
        Interface:        GigabitEthernet2
        Group:                FF25:2::1
        Uptime:                08:14:18
        Router mode:        EXCLUDE (Expires: never)
        Host mode:        EXCLUDE
        Last reporter:        FE80::5054:FF:FEDD:BB49
        Source list is empty
        Interface:        GigabitEthernet2
        Group:                FF35:1::1
        Uptime:                00:42:30
        Router mode:        INCLUDE
        Host mode:        INCLUDE
        Last reporter:        FE80::5054:FF:FEDD:BB49
        Group source list:
        Source Address                          Uptime    Expires   Fwd  Flags
        2001:DB8:3:3::3                         00:42:30  00:12:23  Yes  Remote Local E
        Interface:        GigabitEthernet2
        Group:                FF45:1::1
        Uptime:                00:42:30
        Router mode:        EXCLUDE (Expires: never)
        Host mode:        EXCLUDE
        Last reporter:        FE80::5054:FF:FEDD:BB49
        Source list is empty
    '''

    ShowIpv6MldSsmMap_default_1 = '''\
        R4# show ipv6 mld ssm-map FF15:1::1

        Group address  : FF35:1::1
        Group mode ssm : FALSE
        Database       : NONE

    '''


    ShowIpv6MldSsmMap_default_2 = '''\
        R4# show ipv6 mld ssm-map FF25:2::1

        Group address  : FF25:2::1
        Group mode ssm : FALSE
        Database       : NONE
    '''
    ShowIpv6MldSsmMap_default_3 = '''\
        R4# show ipv6 mld ssm-map FF35:1::1

        Group address  : FF35:1::1
        Group mode ssm : FALSE
        Database       : STATIC
        Source list    : 2001:DB8:1:1::1
    '''
    ShowIpv6MldSsmMap_default_4 = '''\
        R4# show ipv6 mld ssm-map FF45:1::1

        Group address  : FF45:1::1
        Group mode ssm : FALSE
        Database       : NONE
    '''

    ShowIpv6MldSsmMap_VRF1_1 = '''\
        R4# show ipv6 mld vrf VRF1 ssm-map FF15:1::1

        Group address  : FF15:1::1
        Group mode ssm : FALSE
        Database       : NONE
    '''
    ShowIpv6MldSsmMap_VRF1_2 = '''\
        R4# show ipv6 mld vrf VRF1 ssm-map FF25:2::1

        Group address  : FF25:2::1
        Group mode ssm : FALSE
        Database       : NONE
    '''
    ShowIpv6MldSsmMap_VRF1_3 = '''\
        R4# show ipv6 mld vrf VRF1 ssm-map FF35:1::1

        Group address  : FF35:1::1
        Group mode ssm : FALSE
        Database       : STATIC
        Source list    : 2001:DB8:1:1::1
    '''
    ShowIpv6MldSsmMap_VRF1_4 = '''\
        R4# show ipv6 mld vrf VRF1 ssm-map FF45:1::1

        Group address  : FF45:1::1
        Group mode ssm : FALSE
        Database       : NONE
    '''

    Mld_info = {
        "vrfs": {
            "VRF1": {
                 "ssm_map": {
                      "2001:DB8:1:1::1 FF35:1::1": {
                           "group_address": "FF35:1::1",
                           "source_addr": "2001:DB8:1:1::1"
                      }
                 },
                 "max_groups": 64000,
                 "interfaces": {
                      "Tunnel1": {
                           "enable": False,
                           "oper_status": "up"
                      },
                      "GigabitEthernet2": {
                           "oper_status": "up",
                           "querier": "FE80::5054:FF:FEDD:BB49",
                           "query_interval": 366,
                           "join_group": {
                                "FF15:1::1 2001:DB8:2:2::2": {
                                     "source": "2001:DB8:2:2::2",
                                     "group": "FF15:1::1"
                                }
                           },
                           "enable": True,
                           "static_group": {
                                "FF35:1::1 2001:DB8:3:3::3": {
                                     "source": "2001:DB8:3:3::3",
                                     "group": "FF35:1::1"
                                }
                           },
                           "group": {
                                "FF45:1::1": {
                                     "up_time": "00:42:30",
                                     "expire": "never",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FEDD:BB49"
                                },
                                "FF25:2::1": {
                                     "up_time": "08:14:18",
                                     "expire": "never",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FEDD:BB49"
                                },
                                "FF35:1::1": {
                                     "up_time": "00:42:30",
                                     "source": {
                                          "2001:DB8:3:3::3": {
                                               "up_time": "00:42:30",
                                               "expire": "00:12:23"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FEDD:BB49"
                                },
                                "FF15:1::1": {
                                     "up_time": "08:14:20",
                                     "source": {
                                          "2001:DB8:2:2::2": {
                                               "up_time": "08:13:56",
                                               "expire": "00:12:23"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FEDD:BB49"
                                }
                           },
                           "query_max_response_time": 16,
                           "max_groups": 6400,
                           "version": 2
                      }
                 }
            },
            "default": {
                 "ssm_map": {
                      "2001:DB8:1:1::1 FF35:1::1": {
                           "group_address": "FF35:1::1",
                           "source_addr": "2001:DB8:1:1::1"
                      }
                 },
                 "max_groups": 64000,
                 "interfaces": {
                      "GigabitEthernet3": {
                           "enable": False,
                           "oper_status": "down"
                      },
                      "GigabitEthernet1": {
                           "group_policy": "test",
                           "group": {
                                "FF45:1::1": {
                                     "up_time": "00:42:32",
                                     "expire": "never",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                },
                                "FF25:2::1": {
                                     "up_time": "08:14:01",
                                     "expire": "never",
                                     "filter_mode": "exclude",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                },
                                "FF35:1::1": {
                                     "up_time": "00:42:41",
                                     "source": {
                                          "2001:DB8:3:3::3": {
                                               "up_time": "00:42:41",
                                               "expire": "00:06:42"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                },
                                "FF15:1::1": {
                                     "up_time": "08:14:15",
                                     "source": {
                                          "2001:DB8:2:2::2": {
                                               "up_time": "08:13:22",
                                               "expire": "00:06:42"
                                          }
                                     },
                                     "filter_mode": "include",
                                     "last_reporter": "FE80::5054:FF:FE7C:DC70"
                                }
                           },
                           "enable": True,
                           "query_interval": 366,
                           "join_group": {
                                "FF15:1::1 2001:DB8:2:2::2": {
                                     "source": "2001:DB8:2:2::2",
                                     "group": "FF15:1::1"
                                },
                                "FF35:1::1 2001:DB8:3:3::3": {
                                     "source": "2001:DB8:3:3::3",
                                     "group": "FF35:1::1"
                                }
                           },
                           "oper_status": "up",
                           "querier": "FE80::5054:FF:FE7C:DC70",
                           "query_max_response_time": 16,
                           "static_group": {
                                "FF35:1::1 2001:DB8:3:3::3": {
                                     "source": "2001:DB8:3:3::3",
                                     "group": "FF35:1::1"
                                }
                           },
                           "max_groups": 6400,
                           "version": 2
                      },
                      "VoIP-Null0": {
                           "enable": False,
                           "oper_status": "up"
                      },
                      "Tunnel0": {
                           "enable": False,
                           "oper_status": "up"
                      },
                      "LIIN0": {
                           "enable": False,
                           "oper_status": "up"
                      },
                      "Null0": {
                           "enable": False,
                           "oper_status": "up"
                      }
                 }
            }
       }
    }
                                 