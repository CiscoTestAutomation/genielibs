''' 
Igmp Genie Ops Object Outputs for IOSXE.
'''


class IgmpOutput(object):

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

     ShowIpIgmpInterface_default = '''\
        R4# show ip igmp interface

        Global IGMP State Limit : 1 active out of 20 max
        GigabitEthernet1 is up, line protocol is up
          Internet address is 10.1.2.1/24
          IGMP is enabled on interface
          Current IGMP host version is 3
          Current IGMP router version is 3
          IGMP query interval is 133 seconds
          IGMP configured query interval is 133 seconds
          IGMP querier timeout is 266 seconds
          IGMP configured querier timeout is 266 seconds
          IGMP max query response time is 10 seconds
          Last member query count is 2
          Last member query response interval is 100 ms
          Inbound IGMP access group is test2
          IGMP activity: 13 joins, 3 leaves
          Interface IGMP State Limit : 1 active out of 10 max
          Multicast routing is enabled on interface
          Multicast TTL threshold is 0
          Multicast designated router (DR) is 10.1.2.1 (this system)
          IGMP querying router is 10.1.2.1 (this system)
          Multicast groups joined by this system (number of users):
              224.0.1.40(1)  239.4.4.4(1)  239.3.3.3(1)
              239.2.2.2(1)  239.1.1.1(1)
     '''

     ShowIpIgmpInterface_VRF1 = '''\
        R4# show ip igmp vrf VRF1 interface

        Global IGMP State Limit : 0 active out of 20 max
        GigabitEthernet2 is up, line protocol is up
          Internet address is 10.186.2.1/24
          IGMP is enabled on interface
          Multicast Routing table VRF1
          Current IGMP host version is 3
          Current IGMP router version is 3
          IGMP query interval is 133 seconds
          IGMP configured query interval is 133 seconds
          IGMP querier timeout is 266 seconds
          IGMP configured querier timeout is 266 seconds
          IGMP max query response time is 10 seconds
          Last member query count is 2
          Last member query response interval is 100 ms
          Inbound IGMP access group is test2
          IGMP activity: 9 joins, 0 leaves
          Interface IGMP State Limit : 0 active out of 10 max
          Multicast routing is enabled on interface
          Multicast TTL threshold is 0
          Multicast designated router (DR) is 10.186.2.1 (this system)
          IGMP querying router is 10.186.2.1 (this system)
          Multicast groups joined by this system (number of users):
              224.0.1.40(1)  239.1.1.1(1)  239.2.2.2(1)
              239.3.3.3(1)  239.4.4.4(1)
     '''

     ShowIpIgmpGroupsDetail_default = '''\
        R4# show ip igmp groups detail

        Flags: L - Local, U - User, SG - Static Group, VG - Virtual Group,
               SS - Static Source, VS - Virtual Source,
               Ac - Group accounted towards access control limit

        Interface:        GigabitEthernet1
        Group:                239.1.1.1
        Flags:                L U 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.3.3.3
        Flags:                L 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.4.1.1          00:05:06  stopped   stopped   Yes  L

        Interface:        GigabitEthernet1
        Group:                239.2.2.2
        Flags:                L U 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.5.5.5
        Flags:                SG 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.4.4.4
        Flags:                L 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.4.1.2          00:05:06  stopped   stopped   Yes  L

        Interface:        GigabitEthernet1
        Group:                239.7.7.7
        Flags:                SS 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.16.2.1          00:05:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet1
        Group:                239.6.6.6
        Flags:                SG 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.9.9.9
        Flags:                Ac 
        Uptime:                00:23:15
        Group mode:        EXCLUDE (Expires: 00:06:06)
        Last reporter:        10.1.2.2
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.8.8.8
        Flags:                SS 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.16.2.1          00:05:06  stopped   stopped   Yes  S
          10.16.2.2          00:05:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet1
        Group:                224.0.1.40
        Flags:                L U 
        Uptime:                00:25:33
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty
     '''

     ShowIpIgmpGroupsDetail_VRF1 = '''\
        R4# show ip igmp vrf VRF1 groups detail

        Flags: L - Local, U - User, SG - Static Group, VG - Virtual Group,
               SS - Static Source, VS - Virtual Source,
               Ac - Group accounted towards access control limit

        Interface:        GigabitEthernet2
        Group:                239.1.1.1
        Flags:                L U 
        Uptime:                00:06:24
        Group mode:        EXCLUDE (Expires: never)
        Last reporter:        10.186.2.1
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.3.3.3
        Flags:                L 
        Uptime:                00:06:24
        Group mode:        INCLUDE
        Last reporter:        10.186.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.4.1.1          00:06:24  stopped   stopped   Yes  L

        Interface:        GigabitEthernet2
        Group:                239.2.2.2
        Flags:                L U 
        Uptime:                00:06:24
        Group mode:        EXCLUDE (Expires: never)
        Last reporter:        10.186.2.1
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.5.5.5
        Flags:                SG 
        Uptime:                00:06:17
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.4.4.4
        Flags:                L 
        Uptime:                00:06:23
        Group mode:        INCLUDE
        Last reporter:        10.186.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.4.1.2          00:06:23  stopped   stopped   Yes  L

        Interface:        GigabitEthernet2
        Group:                239.7.7.7
        Flags:                SS 
        Uptime:                00:06:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.16.2.1          00:06:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet2
        Group:                239.6.6.6
        Flags:                SG 
        Uptime:                00:06:14
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.8.8.8
        Flags:                SS 
        Uptime:                00:05:59
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          10.16.2.1          00:03:56  stopped   stopped   Yes  S
          10.16.2.2          00:05:57  stopped   stopped   Yes  S

        Interface:        GigabitEthernet2
        Group:                224.0.1.40
        Flags:                L U 
        Uptime:                00:25:55
        Group mode:        INCLUDE
        Last reporter:        10.186.2.1
        Source list is empty
     '''

     ShowIpIgmpSsmMapping_default_1 = '''\
        R4# show ip igmp ssm-mapping 239.1.1.1

        Group address: 239.1.1.1
        Database     : Static
        Source list  : 10.4.1.1
                       10.16.2.2
     '''


     ShowIpIgmpSsmMapping_default_2 = '''\
        R4# show ip igmp ssm-mapping 239.2.2.2

        Can't resolve 239.2.2.2 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_3 = '''\
        R4# show ip igmp ssm-mapping 239.3.3.3

        Can't resolve 239.3.3.3 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_4 = '''\
        R4# show ip igmp ssm-mapping 239.4.4.4

        Can't resolve 239.4.4.4 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_5 = '''\
        R4# show ip igmp ssm-mapping 239.5.5.5

        Can't resolve 239.5.5.5 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_6 = '''\
        R4# show ip igmp ssm-mapping 239.6.6.6

        Can't resolve 239.6.6.6 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_7 = '''\
        R4# show ip igmp ssm-mapping 239.7.7.7

        Can't resolve 239.7.7.7 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_8 = '''\
        R4# show ip igmp ssm-mapping 239.8.8.8

        Can't resolve 239.8.8.8 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_9 = '''\
        R4# show ip igmp ssm-mapping 239.9.9.9

        Can't resolve 239.9.9.9 to source mapping
     '''
     ShowIpIgmpSsmMapping_default_10 = '''\
        R4# show ip igmp ssm-mapping 224.0.1.40

        Can't resolve 224.0.1.40 to source mapping
     '''

     ShowIpIgmpSsmMapping_VRF1_1 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.1.1.1

        Group address: 239.1.1.1
        Database     : Static
        Source list  : 10.4.1.1
                       10.16.2.2
     '''
     ShowIpIgmpSsmMapping_VRF1_2 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.2.2.2

        Can't resolve 239.2.2.2 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_3 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.3.3.3

        Can't resolve 239.3.3.3 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_4 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.4.4.4

        Can't resolve 239.4.4.4 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_5 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.5.5.5

        Can't resolve 239.5.5.5 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_6 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.6.6.6

        Can't resolve 239.6.6.6 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_7 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.7.7.7

        Can't resolve 239.7.7.7 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_8 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 239.8.8.8

        Can't resolve 239.8.8.8 to source mapping
     '''
     ShowIpIgmpSsmMapping_VRF1_10 = '''\
        R4# show ip igmp vrf VRF1 ssm-mapping 224.0.1.40

        Can't resolve 224.0.1.40 to source mapping
     '''

     Igmp_info = {
          "vrfs": {
               "VRF1": {
                    "max_groups": 20,
                    "ssm_map": {
                         "10.4.1.1 239.1.1.1": {
                              "source_addr": "10.4.1.1",
                              "group_address": "239.1.1.1"
                         },
                         "10.16.2.2 239.1.1.1": {
                              "source_addr": "10.16.2.2",
                              "group_address": "239.1.1.1"
                         }
                    },
                    "interfaces": {
                         "GigabitEthernet2": {
                              "querier": "10.186.2.1",
                              "group": {
                                   "224.0.1.40": {
                                        "last_reporter": "10.186.2.1",
                                        "up_time": "00:25:55"
                                   },
                                   "239.6.6.6": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:06:14"
                                   },
                                   "239.8.8.8": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:05:59",
                                        "source": {
                                             "10.16.2.2": {
                                                  "up_time": "00:05:57"
                                             },
                                             "10.16.2.1": {
                                                  "up_time": "00:03:56"
                                             }
                                        }
                                   },
                                   "239.3.3.3": {
                                        "last_reporter": "10.186.2.1",
                                        "up_time": "00:06:24",
                                        "source": {
                                             "10.4.1.1": {
                                                  "up_time": "00:06:24"
                                             }
                                        }
                                   },
                                   "239.5.5.5": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:06:17"
                                   },
                                   "239.2.2.2": {
                                        "expire": "never",
                                        "up_time": "00:06:24",
                                        "last_reporter": "10.186.2.1"
                                   },
                                   "239.4.4.4": {
                                        "last_reporter": "10.186.2.1",
                                        "up_time": "00:06:23",
                                        "source": {
                                             "10.4.1.2": {
                                                  "up_time": "00:06:23"
                                             }
                                        }
                                   },
                                   "239.7.7.7": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:06:06",
                                        "source": {
                                             "10.16.2.1": {
                                                  "up_time": "00:06:06"
                                             }
                                        }
                                   },
                                   "239.1.1.1": {
                                        "expire": "never",
                                        "up_time": "00:06:24",
                                        "last_reporter": "10.186.2.1"
                                   }
                              },
                              "oper_status": "up",
                              "query_max_response_time": 10,
                              "static_group": {
                                   "239.5.5.5 *": {
                                        "source": "*",
                                        "group": "239.5.5.5"
                                   },
                                   "239.6.6.6 *": {
                                        "source": "*",
                                        "group": "239.6.6.6"
                                   }
                              },
                              "group_policy": "test2",
                              "join_group": {
                                   "239.8.8.8 10.16.2.2": {
                                        "source": "10.16.2.2",
                                        "group": "239.8.8.8"
                                   },
                                   "239.4.4.4 10.4.1.2": {
                                        "source": "10.4.1.2",
                                        "group": "239.4.4.4"
                                   },
                                   "224.0.1.40 *": {
                                        "source": "*",
                                        "group": "224.0.1.40"
                                   },
                                   "239.7.7.7 10.16.2.1": {
                                        "source": "10.16.2.1",
                                        "group": "239.7.7.7"
                                   },
                                   "239.2.2.2 *": {
                                        "source": "*",
                                        "group": "239.2.2.2"
                                   },
                                   "239.1.1.1 *": {
                                        "source": "*",
                                        "group": "239.1.1.1"
                                   },
                                   "239.3.3.3 10.4.1.1": {
                                        "source": "10.4.1.1",
                                        "group": "239.3.3.3"
                                   },
                                   "239.8.8.8 10.16.2.1": {
                                        "source": "10.16.2.1",
                                        "group": "239.8.8.8"
                                   }
                              },
                              "max_groups": 10,
                              "last_member_query_interval": 100,
                              "version": 3,
                              "enable": True,
                              "joined_group": [
                                   "224.0.1.40",
                                   "239.1.1.1",
                                   "239.2.2.2",
                                   "239.3.3.3",
                                   "239.4.4.4"
                              ],
                              "query_interval": 133
                         }
                    }
               },
               "default": {
                    "max_groups": 20,
                    "ssm_map": {
                         "10.4.1.1 239.1.1.1": {
                              "source_addr": "10.4.1.1",
                              "group_address": "239.1.1.1"
                         },
                         "10.16.2.2 239.1.1.1": {
                              "source_addr": "10.16.2.2",
                              "group_address": "239.1.1.1"
                         }
                    },
                    "interfaces": {
                         "GigabitEthernet1": {
                              "querier": "10.1.2.1",
                              "oper_status": "up",
                              "group": {
                                   "224.0.1.40": {
                                        "last_reporter": "10.1.2.1",
                                        "up_time": "00:25:33"
                                   },
                                   "239.9.9.9": {
                                        "expire": "00:06:06",
                                        "up_time": "00:23:15",
                                        "last_reporter": "10.1.2.2"
                                   },
                                   "239.8.8.8": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:05:06",
                                        "source": {
                                             "10.16.2.2": {
                                                  "up_time": "00:05:06"
                                             },
                                             "10.16.2.1": {
                                                  "up_time": "00:05:06"
                                             }
                                        }
                                   },
                                   "239.3.3.3": {
                                        "last_reporter": "10.1.2.1",
                                        "up_time": "00:05:06",
                                        "source": {
                                             "10.4.1.1": {
                                                  "up_time": "00:05:06"
                                             }
                                        }
                                   },
                                   "239.5.5.5": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:05:06"
                                   },
                                   "239.6.6.6": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:05:06"
                                   },
                                   "239.2.2.2": {
                                        "last_reporter": "10.1.2.1",
                                        "up_time": "00:05:06"
                                   },
                                   "239.7.7.7": {
                                        "last_reporter": "0.0.0.0",
                                        "up_time": "00:05:06",
                                        "source": {
                                             "10.16.2.1": {
                                                  "up_time": "00:05:06"
                                             }
                                        }
                                   },
                                   "239.4.4.4": {
                                        "last_reporter": "10.1.2.1",
                                        "up_time": "00:05:06",
                                        "source": {
                                             "10.4.1.2": {
                                                  "up_time": "00:05:06"
                                             }
                                        }
                                   },
                                   "239.1.1.1": {
                                        "last_reporter": "10.1.2.1",
                                        "up_time": "00:05:06"
                                   }
                              },
                              "max_groups": 10,
                              "static_group": {
                                   "239.5.5.5 *": {
                                        "source": "*",
                                        "group": "239.5.5.5"
                                   },
                                   "239.6.6.6 *": {
                                        "source": "*",
                                        "group": "239.6.6.6"
                                   }
                              },
                              "group_policy": "test2",
                              "join_group": {
                                   "239.8.8.8 10.16.2.2": {
                                        "source": "10.16.2.2",
                                        "group": "239.8.8.8"
                                   },
                                   "239.9.9.9 *": {
                                        "source": "*",
                                        "group": "239.9.9.9"
                                   },
                                   "224.0.1.40 *": {
                                        "source": "*",
                                        "group": "224.0.1.40"
                                   },
                                   "239.7.7.7 10.16.2.1": {
                                        "source": "10.16.2.1",
                                        "group": "239.7.7.7"
                                   },
                                   "239.1.1.1 *": {
                                        "source": "*",
                                        "group": "239.1.1.1"
                                   },
                                   "239.2.2.2 *": {
                                        "source": "*",
                                        "group": "239.2.2.2"
                                   },
                                   "239.4.4.4 10.4.1.2": {
                                        "source": "10.4.1.2",
                                        "group": "239.4.4.4"
                                   },
                                   "239.3.3.3 10.4.1.1": {
                                        "source": "10.4.1.1",
                                        "group": "239.3.3.3"
                                   },
                                   "239.8.8.8 10.16.2.1": {
                                        "source": "10.16.2.1",
                                        "group": "239.8.8.8"
                                   }
                              },
                              "query_max_response_time": 10,
                              "last_member_query_interval": 100,
                              "version": 3,
                              "enable": True,
                              "joined_group": [
                                   "224.0.1.40",
                                   "239.1.1.1",
                                   "239.2.2.2",
                                   "239.3.3.3",
                                   "239.4.4.4",
                              ],
                              "query_interval": 133
                         }
                    }
               }
          }
     }
