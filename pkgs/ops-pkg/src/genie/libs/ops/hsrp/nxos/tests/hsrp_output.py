class HsrpOutput(object):

    # 'show hsrp all' output
    showHsrpAllOutput = {
        "Ethernet1/3": {
            "address_family": {
                "ipv4": {
                    "version": {
                        2: {
                            "groups": {
                                0: {
                                    "active_priority": 110,
                                    "active_router": "local",
                                    "authentication": "cisco123",
                                    "configured_priority": 110,
                                    "hsrp_router_state": "active",
                                    "session_name": "hsrp-Eth1/3-0",
                                    "last_state_change": "00:01:43",
                                    "lower_fwd_threshold": 0,
                                    "num_state_changes": 10,
                                    "preempt": True,
                                    "priority": 110,
                                    "standby_expire": 2.429,
                                    "standby_priority": 90,
                                    "standby_router": "192.168.1.2",
                                    "standby_ip_address": "192.168.1.2",
                                    "timers": {
                                        "hello_sec": 1,
                                        "hold_sec": 3
                                    },
                                    'tracked_objects': {
                                        1: {
                                            'object_name': 1,
                                            'priority_decrement': 22,
                                            'status': 'UP',
                                        }
                                    },
                                    "upper_fwd_threshold": 110,
                                    'primary_ipv4_address': {
                                        'address': "192.168.1.254",
                                    },
                                    "virtual_mac_address": "0000.0c9f.f000"
                                },
                                2: {
                                    "active_router": "unknown",
                                    "authentication": "cisco",
                                    "configured_priority": 1,
                                    "hsrp_router_state": "disabled(virtual ip not cfged)",
                                    "session_name": "hsrp-Eth1/3-2",
                                    "last_state_change": "never",
                                    "lower_fwd_threshold": 0,
                                    "num_state_changes": 0,
                                    "priority": 1,
                                    "standby_router": "unknown",
                                    "timers": {
                                        "hello_sec": 3,
                                        "hold_sec": 10
                                    },
                                    "upper_fwd_threshold": 1,
                                    "virtual_mac_address": "0000.0c9f.f002"
                                }
                            }
                        }
                    }
                },
                "ipv6": {
                    "version": {
                        2: {
                            "groups": {
                                2: {
                                    "active_priority": 100,
                                    "active_router": "local",
                                    "authentication": "cisco",
                                    "configured_priority": 100,
                                    "hsrp_router_state": "active",
                                    "session_name": "hsrp-Eth1/3-2-V6",
                                    "last_state_change": "02:43:40",
                                    "lower_fwd_threshold": 0,
                                    "num_state_changes": 2,
                                    "priority": 100,
                                    "secondary_vips": "2001:db8:7746:fa41::1",
                                    "standby_expire": 8.96,
                                    "standby_priority": 90,
                                    "standby_router": "fe80::20c:29ff:fe69:14bb",
                                    "standby_ipv6_address": "fe80::20c:29ff:fe69:14bb",
                                    "timers": {
                                        "hello_sec": 3,
                                        "hold_sec": 10
                                    },
                                    "upper_fwd_threshold": 100,
                                    'link_local_ipv6_address': {
                                        'address': "fe80::5:73ff:fea0:2",
                                    },
                                    "virtual_mac_address": "0005.73a0.0002"
                                }
                            }
                        }
                    }
                }
            },
            "interface": "Ethernet1/3",
        }
    }

    # 'show hsrp summary' output
    showHsrpSummaryOutput = {
        'global_hsrp_bfd': 'enabled',
        'intf_total': 1,
        'nsf': 'enabled',
        'nsf_time': 10,
        'pkt_unknown_groups': 0,
        'total_mts_rx': 85,
        'stats': {
            'total_groups': 3,
            'active': 0,
            'listen': 0,
            'standby': 0,
            'v1_ipv4': 0,
            'v2_ipv4': 3,
            'v2_ipv6': 0,
            'v6_active': 0,
            'v6_listen': 0,
            'v6_standby': 0
        },
        'total_packets': {
            'rx_good': 0,
            'tx_fail': 0,
            'tx_pass': 0,
        }
    }

    showHsrpDelayOutput = {
        'Ethernet1/3': {
            'delay': {
                'minimum_delay': 99,
                'reload_delay': 888,
            }
        }
    }

    # Hsrp Ops Object final output
    hsrpOpsOutput = \
    {
    'Ethernet1/3': {
      'address_family': {
        'ipv4': {
          'version': {
            2: {
              'groups': {
                0: {
                  'active_router': 'local',
                  'authentication': 'cisco123',
                  'hsrp_router_state': 'active',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '192.168.1.254'
                  },
                  'priority': 110,
                  'session_name': 'hsrp-Eth1/3-0',
                  'standby_ip_address': '192.168.1.2',
                  'standby_router': '192.168.1.2',
                  'timers': {
                    'hello_sec': 1,
                    'hold_sec': 3
                  },
                  'tracked_objects': {
                    1: {
                      'object_name': 1,
                      'priority_decrement': 22
                      }
                  },
                  'virtual_mac_address': '0000.0c9f.f000'
                },
                2: {
                  'active_router': 'unknown',
                  'authentication': 'cisco',
                  'hsrp_router_state': 'disabled(virtual '
                  'ip '
                  'not '
                  'cfged)',
                  'priority': 1,
                  'session_name': 'hsrp-Eth1/3-2',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_sec': 3,
                    'hold_sec': 10
                  },
                  'virtual_mac_address': '0000.0c9f.f002'
                  }
                }
              }
            }
        },
        'ipv6': {
          'version': {
            2: {
              'groups': {
                2: {
                  'active_router': 'local',
                  'authentication': 'cisco',
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::5:73ff:fea0:2'
                  },
                  'priority': 100,
                  'session_name': 'hsrp-Eth1/3-2-V6',
                  'standby_ipv6_address': 'fe80::20c:29ff:fe69:14bb',
                  'standby_router': 'fe80::20c:29ff:fe69:14bb',
                  'timers': {
                    'hello_sec': 3,
                    'hold_sec': 10
                  },
                  'virtual_mac_address': '0005.73a0.0002'
                  }
                }
              }
            }
          }
      },
      'delay': {
        'minimum_delay': 99, 'reload_delay': 888
      },
      'interface': 'Ethernet1/3'
      }
    }



# vim: ft=python et sw=4
