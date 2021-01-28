''' 
Mld Genie Ops Object Outputs for IOSXR.
'''


class MldOutput(object):

    # from: genieparser/src/genie/libs/parser/iosxr/tests/test_show_vrf.py -> golden_parsed_output
    ShowVrfAllDetail = {
        "VRF1": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                "ipv6 unicast": {
                    "route_target": {
                        "400:1": {
                            "rt_type": "import",
                            "route_target": "400:1"
                        },
                        "300:1": {
                            "rt_type": "import",
                            "route_target": "300:1"
                        },
                        "200:1": {
                            "rt_type": "both",
                            "route_target": "200:1"
                        },
                        "200:2": {
                            "rt_type": "import",
                            "route_target": "200:2"
                        }
                    }
                },
                "ipv4 unicast": {
                    "route_target": {
                        "400:1": {
                            "rt_type": "import",
                            "route_target": "400:1"
                        },
                        "300:1": {
                            "rt_type": "import",
                            "route_target": "300:1"
                        },
                        "200:1": {
                            "rt_type": "both",
                            "route_target": "200:1"
                        },
                        "200:2": {
                            "rt_type": "import",
                            "route_target": "200:2"
                        }
                    }
                }
            },
            "route_distinguisher": "200:1",
            "interfaces": [
                "GigabitEthernet0/0/0/1"
            ]
        }
    }

    # show mld summary internal
    # from: test_show_mld.py -> golden_parsed_output1
    ShowMldSummaryInternal_default = {
        'vrf': {
            'default': {
                'disabled_intf': 0,
                'enabled_intf': 1,
                'interface': {
                    'GigabitEthernet0/0/0/0': {
                        'igmp_r_uptime': '1d06h',
                        'last_query': '00:29:26',
                        'last_report': '00:04:16',
                        'max_groups': 6400,
                        'num_groups': 13,
                        'on': True,
                        'parent': '0x0'
                    }
                },
                'max_num_groups_x_intfs': 75000,
                'mte_tuple_count': 0,
                'num_groups_x_intf': 13,
                'robustness_value': 10,
                'supported_intf': 1,
                'unsupported_intf': 0
            }
        }
    }

    # from: test_show_mld.py -> golden_output2
    ShowMldSummaryInternal_VRF = '''\
        RP/0/0/CPU0:ios#show mld vrf VRF1 summary internal

        Robustness Value 10
        No. of Group x Interfaces 10
        Maximum number of Group x Interfaces 75000

        Supported Interfaces   : 1
        Unsupported Interfaces : 0
        Enabled Interfaces     : 1
        Disabled Interfaces    : 0

        MTE tuple count        : 0

        Interface                       Number  Max #   On Parent     Last     Last     IGMP R
                                        Groups  Groups                query    Report   Uptime
        GigabitEthernet0/0/0/1          10      6400    Y  0x0        00:00:03 00:00:01    1d06h
    '''

    # show mld interface
    # from: test_show_mld.py -> golden_parsed_output1
    ShowMldInterface_default = {
        'vrf': {
            'default': {
                'interface': {
                    'GigabitEthernet0/0/0/0': {
                        'counters': {
                            'joins': 18,
                            'leaves': 5
                        },
                        'enable': True,
                        'internet_address': 'fe80::5054:ff:fefa:9ad7',
                        'interface_status': 'up',
                        'last_member_query_interval': 1,
                        'oper_status': 'up',
                        'querier': 'fe80::5054:ff:fed7:c01f',
                        'querier_timeout': 3666,
                        'query_interval': 366,
                        'query_max_response_time': 12,
                        'time_elapsed_since_igmp_router_enabled': '1d06h',
                        'time_elapsed_since_last_query_sent': '00:30:16',
                        'time_elapsed_since_last_report_received': '00:05:05',
                        'version': 2
                    }
                }
            }
        }
    }

    ShowMldInterface_VRF = '''\
        RP/0/0/CPU0:ios#show mld vrf VRF1 interface

        GigabitEthernet0/0/0/1 is up, line protocol is up
          Internet address is fe80::5054:ff:fe35:f846
          MLD is enabled on interface
          Current MLD version is 2
          MLD query interval is 366 seconds
          MLD querier timeout is 3666 seconds
          MLD max query response time is 12 seconds
          Last member query response interval is 1 seconds
          MLD activity: 12 joins, 2 leaves
          MLD querying router is fe80::5054:ff:fe35:f846 (this system)
          Time elapsed since last query sent 00:00:53
          Time elapsed since IGMP router enabled 1d06h
          Time elapsed since last report received 00:00:51
    '''

    """
    # show mld ssm map detail
    # from: test_show_mld.py -> golden_parsed_output1
    ShowMldSsmMapDetail_default = {
        
    }

    # from: test_show_mld.py -> golden_output2
    ShowMldSsmMapDetail_VRF = '''\
    '''

    """

    # show mld groups detail
    # from: test_show_mld.py -> golden_parsed_output1
    ShowMldGroupsDetail_default = {
        'vrf': {
            'default': {
                'interface': {
                    'GigabitEthernet0/0/0/0': {
                        'group': {
                            'ff02::16': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'host_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff28:cd4b': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff60:50aa': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ffae:4aba': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ffd7:c01f': {
                                'expire': '00:29:15',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fed7:c01f',
                                'up_time': '00:33:19'
                            },
                            'ff02::1:ffda:f428': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '06:27:46'
                            },
                            'ff02::2': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'host_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff02::d': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'host_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff15:1::1': {
                                'filter_mode': 'include',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'source': {
                                    '2001:db8:2:2::2': {
                                        'expire': '01:00:00',
                                        'flags': 'Remote Local 2d',
                                        'forward': True,
                                        'up_time': '08:06:00'
                                    }
                                },
                                'up_time': '08:06:00'
                            },
                            'ff25:2::1': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'host_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '08:06:00'
                            },
                            'ff35:1::1': {
                                'filter_mode': 'include',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'source': {
                                    '2001:db8:3:3::3': {
                                        'expire': '01:00:00',
                                        'flags': 'Remote Local e',
                                        'forward': True,
                                        'up_time': '00:33:28'
                                    }
                                },
                                'up_time': '00:33:28'
                            },
                            'ff45:1::1': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'host_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '00:33:28'
                            },
                            'fffe::1': {
                                'expire': '00:59:49',
                                'filter_mode': 'exclude',
                                'host_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fed7:c01f',
                                'up_time': '07:59:31'
                            }
                        },
                        'join_group': {
                            'ff15:1::1 2001:db8:2:2::2': {
                                'group': 'ff15:1::1',
                                'source': '2001:db8:2:2::2'
                            }
                        },
                        'static_group': {
                            'ff35:1::1 2001:db8:3:3::3': {
                                'group': 'ff35:1::1',
                                'source': '2001:db8:3:3::3'
                            }
                        }
                    }
                }
            }
        }
    }

    # from: test_show_mld.py -> golden_output2
    ShowMldGroupsDetail_VRF = '''\
       RP/0/0/CPU0:ios#show mld vrf VRF1 groups detail

        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::2
        Uptime:         1d06h
        Router mode:    EXCLUDE (Expires: never)
        Host mode:      EXCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::d
        Uptime:         1d06h
        Router mode:    EXCLUDE (Expires: never)
        Host mode:      EXCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::16
        Uptime:         1d06h
        Router mode:    EXCLUDE (Expires: never)
        Host mode:      EXCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::1:ff00:1
        Uptime:         09:00:17
        Router mode:    EXCLUDE (Expires: 00:58:14)
        Host mode:      INCLUDE
        Last reporter:  fe80::5054:ff:fe7c:dc70
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::1:ff24:c88d
        Uptime:         1d06h
        Router mode:    EXCLUDE (Expires: 00:58:30)
        Host mode:      INCLUDE
        Last reporter:  fe80::7c2f:c2ff:fe24:c88d
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff02::1:ff7c:dc70
        Uptime:         09:00:17
        Router mode:    EXCLUDE (Expires: 00:58:14)
        Host mode:      INCLUDE
        Last reporter:  fe80::5054:ff:fe7c:dc70
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff15:1::1
        Uptime:         08:11:27
        Router mode:    INCLUDE
        Host mode:      INCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Group source list:
          Source Address                          Uptime    Expires   Fwd  Flags
          2001:db8:2:2::2                       08:10:33  00:58:30  Yes  Remote Local 2d
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff25:2::1
        Uptime:         08:11:12
        Router mode:    EXCLUDE (Expires: never)
        Host mode:      EXCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Source list is empty
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff35:1::1
        Uptime:         00:39:52
        Router mode:    INCLUDE
        Host mode:      INCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Group source list:
          Source Address                          Uptime    Expires   Fwd  Flags
          2001:db8:3:3::3                       00:39:52  00:58:30  Yes  Remote Local e
        Interface:      GigabitEthernet0/0/0/1
        Group:          ff45:1::1
        Uptime:         00:39:44
        Router mode:    EXCLUDE (Expires: never)
        Host mode:      EXCLUDE
        Last reporter:  fe80::5054:ff:fe35:f846
        Source list is empty 
    '''

    Mld_info = {
        'vrfs': {
            'VRF1': {
                'interfaces': {
                    'GigabitEthernet0/0/0/1': {
                        'enable': True,
                        'group': {
                            'ff02::16': {
                                'expire': 'never',
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff00:1': {
                                'expire': '00:58:14',
                                'last_reporter': 'fe80::5054:ff:fe7c:dc70',
                                'up_time': '09:00:17'
                            },
                            'ff02::1:ff24:c88d': {
                                'expire': '00:58:30',
                                'last_reporter': 'fe80::7c2f:c2ff:fe24:c88d',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff7c:dc70': {
                                'expire': '00:58:14',
                                'last_reporter': 'fe80::5054:ff:fe7c:dc70',
                                'up_time': '09:00:17'
                            },
                            'ff02::2': {
                                'expire': 'never',
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'up_time': '1d06h'
                            },
                            'ff02::d': {
                                'expire': 'never',
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'up_time': '1d06h'
                            },
                            'ff15:1::1': {
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'source': {
                                    '2001:db8:2:2::2': {
                                        'expire': '00:58:30',
                                        'up_time': '08:10:33'
                                    }
                                },
                                'up_time': '08:11:27'
                            },
                            'ff25:2::1': {
                                'expire': 'never',
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'up_time': '08:11:12'
                            },
                            'ff35:1::1': {
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'source': {
                                    '2001:db8:3:3::3': {
                                        'expire': '00:58:30',
                                        'up_time': '00:39:52'
                                    }
                                },
                                'up_time': '00:39:52'
                            },
                            'ff45:1::1': {
                                'expire': 'never',
                                'last_reporter': 'fe80::5054:ff:fe35:f846',
                                'up_time': '00:39:44'
                            }
                        },
                        'join_group': {
                            'ff15:1::1 2001:db8:2:2::2': {
                                'group': 'ff15:1::1',
                                'source': '2001:db8:2:2::2'
                            }
                        },
                        'oper_status': 'up',
                        'query_interval': 366,
                        'query_max_response_time': 12,
                        'static_group': {
                            'ff35:1::1 2001:db8:3:3::3': {
                                'group': 'ff35:1::1',
                                'source': '2001:db8:3:3::3'
                            }
                        },
                        'version': 2
                    }
                }
            },
            'default': {
                'interfaces': {
                    'GigabitEthernet0/0/0/0': {
                        'enable': True,
                        'group': {
                            'ff02::16': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff28:cd4b': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ff60:50aa': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ffae:4aba': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '1d06h'
                            },
                            'ff02::1:ffd7:c01f': {
                                'expire': '00:29:15',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fed7:c01f',
                                'up_time': '00:33:19'
                            },
                            'ff02::1:ffda:f428': {
                                'expire': '01:00:01',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::eca7:a4ff:fe28:cd4b',
                                'up_time': '06:27:46'
                            },
                            'ff02::2': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff02::d': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '1d06h'
                            },
                            'ff15:1::1': {
                                'filter_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'source': {
                                    '2001:db8:2:2::2': {
                                        'expire': '01:00:00',
                                        'up_time': '08:06:00'
                                    }
                                },
                                'up_time': '08:06:00'
                            },
                            'ff25:2::1': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '08:06:00'
                            },
                            'ff35:1::1': {
                                'filter_mode': 'include',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'source': {
                                    '2001:db8:3:3::3': {
                                        'expire': '01:00:00',
                                        'up_time': '00:33:28'
                                    }
                                },
                                'up_time': '00:33:28'
                            },
                            'ff45:1::1': {
                                'expire': 'never',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fefa:9ad7',
                                'up_time': '00:33:28'
                            },
                            'fffe::1': {
                                'expire': '00:59:49',
                                'filter_mode': 'exclude',
                                'last_reporter': 'fe80::5054:ff:fed7:c01f',
                                'up_time': '07:59:31'
                            }
                        },
                        'join_group': {
                            'ff15:1::1 2001:db8:2:2::2': {
                                'group': 'ff15:1::1',
                                'source': '2001:db8:2:2::2'
                            }
                        },
                        'oper_status': 'up',
                        'querier': 'fe80::5054:ff:fed7:c01f',
                        'query_interval': 366,
                        'query_max_response_time': 12,
                        'static_group': {
                            'ff35:1::1 2001:db8:3:3::3': {
                                'group': 'ff35:1::1',
                                'source': '2001:db8:3:3::3'
                            }
                        },
                        'version': 2
                    }
                }
            }
        }
    }
