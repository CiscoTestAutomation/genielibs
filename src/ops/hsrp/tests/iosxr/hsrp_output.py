class HsrpOutput(object):

    # 'show hsrp detail' output
    showHsrpDetailOutput = \
    {
    'GigabitEthernet0/0/0/0': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                0: {
                  'active_ip_address': 'unknown',
                  'active_router': 'unknown',
                  'bfd': {
                    'address': '10.1.1.1',
                    'interface_name': 'GigabitEthernet0/0/0/1',
                    'state': 'inactive'
                  },
                  'group_number': 0,
                  'hsrp_router_state': 'init',
                  'preempt': True,
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'stored',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': 'never',
                    'num_state_changes': 0
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0000.0c07.ac00'
                },
                10: {
                  'active_ip_address': 'local',
                  'active_priority': 63,
                  'active_router': 'local',
                  'authentication': 'cisco123',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'num_of_slaves': 1,
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '10.1.1.254'
                  },
                  'priority': 63,
                  'session_name': 'group10',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:36:53',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'cfgd_hello_msec': 10000,
                    'cfgd_hold_msec': 30000,
                    'hello_msec': 10000,
                    'hello_msec_flag': True,
                    'hold_msec': 30000,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 123
                      }
                  },
                  'tracked_objects': {
                    '1': {
                      'object_name': '1',
                      'priority_decrement': 25
                    },
                    'num_tracked_objects': 2,
                    'num_tracked_objects_up': 1
                  },
                  'virtual_mac_address': '0000.0c07.ac0a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'primary_ipv4_address': {
                    'address': '10.1.1.128'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:52',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'cfgd_hello_msec': 111,
                    'cfgd_hold_msec': 333,
                    'hello_msec': 111,
                    'hello_msec_flag': True,
                    'hold_msec': 333,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 251
                      }
                  },
                  'tracked_objects': {
                    'num_tracked_objects': 1,
                    'num_tracked_objects_up': 1
                  },
                  'virtual_mac_address': '0000.0c07.ac14'
                  }
              },
              'slave_groups': {
                30: {
                  'follow': 'group10',
                  'group_number': 30,
                  'hsrp_router_state': 'init',
                  'primary_ipv4_address': {
                    'address': 'unknown'
                  },
                  'priority': 100,
                  'standby_state': 'stored',
                  'virtual_mac_address': '0000.0c07.ac1e'
                  }
                }
              }
            }
        },
        'ipv6': {
          'version': {
            2: {
              'groups': {
                10: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:a'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.000a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:14'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.0014'
                },
                30: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 30,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:1e'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.001e'
                  }
                }
              }
            }
          }
      },
      'bfd': {
        'detection_multiplier': 3,
        'enabled': True,
        'interval': 15
      },
      'delay': {
        'minimum_delay': 100,
        'reload_delay': 1000
      },
      'interface': 'GigabitEthernet0/0/0/0',
      'redirects_disable': True,
      'use_bia': False
      }
    }

    showHsrpDetailOutputIncomplete = \
    {
    'GigabitEthernet0/0/0/0': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                0: {
                  'active_ip_address': 'unknown',
                  'active_router': 'unknown',
                  'bfd': {
                    'address': '10.1.1.1',
                    'interface_name': 'GigabitEthernet0/0/0/1',
                    'state': 'inactive'
                  },
                  'group_number': 0,
                  'hsrp_router_state': 'init',
                  'preempt': True,
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'stored',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': 'never',
                    'num_state_changes': 0
                  },
                  'virtual_mac_address': '0000.0c07.ac00'
                },
                10: {
                  'active_ip_address': 'local',
                  'active_priority': 63,
                  'active_router': 'local',
                  'authentication': 'cisco123',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'num_of_slaves': 1,
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '10.1.1.254'
                  },
                  'priority': 63,
                  'session_name': 'group10',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:36:53',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'cfgd_hello_msec': 10000,
                    'cfgd_hold_msec': 30000,
                    'hello_msec': 10000,
                    'hello_msec_flag': True,
                    'hold_msec': 30000,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 123
                      }
                  },
                  'tracked_objects': {
                    '1': {
                      'object_name': '1',
                      'priority_decrement': 25
                    },
                    'num_tracked_objects': 2,
                    'num_tracked_objects_up': 1
                  },
                  'virtual_mac_address': '0000.0c07.ac0a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'primary_ipv4_address': {
                    'address': '10.1.1.128'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:52',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'cfgd_hello_msec': 111,
                    'cfgd_hold_msec': 333,
                    'hello_msec': 111,
                    'hello_msec_flag': True,
                    'hold_msec': 333,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 251
                      }
                  },
                  'tracked_objects': {
                    'num_tracked_objects': 1,
                    'num_tracked_objects_up': 1
                  },
                  'virtual_mac_address': '0000.0c07.ac14'
                  }
              },
              'slave_groups': {
                30: {
                  'follow': 'group10',
                  'group_number': 30,
                  'hsrp_router_state': 'init',
                  'primary_ipv4_address': {
                    'address': 'unknown'
                  },
                  'priority': 100,
                  'standby_state': 'stored',
                  'virtual_mac_address': '0000.0c07.ac1e'
                  }
                }
              }
            }
        },
        'ipv6': {
          'version': {
            2: {
              'groups': {
                10: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:a'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.000a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:14'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.0014'
                },
                30: {
                  'active_ip_address': 'local',
                  'active_priority': 100,
                  'active_router': 'local',
                  'group_number': 30,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:1e'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'standby_state': 'reserving',
                  'statistics': {
                    'last_coup_received': 'Never',
                    'last_coup_sent': 'Never',
                    'last_resign_received': 'Never',
                    'last_resign_sent': 'Never',
                    'last_state_change': '09:37:18',
                    'num_state_changes': 4
                  },
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.001e'
                  }
                }
              }
            }
          }
      },
      'bfd': {
        'detection_multiplier': 3,
        'enabled': True,
        'interval': 15
      },
      'delay': {
        'minimum_delay': 100,
        'reload_delay': 1000
      },
      'interface': 'GigabitEthernet0/0/0/0',
      'redirects_disable': True,
      'use_bia': False
      }
    }

    # 'show hsrp summary' output
    showHsrpSummaryOutput = \
    {
    'address_family': {
      'ipv4': {
        'intf_down': 0,
        'intf_total': 1,
        'intf_up': 1,
        'state': {
          'ACTIVE': {
            'sessions': 2,
            'slaves': 0,
            'total': 2
          },
          'ALL': {
            'sessions': 3,
            'slaves': 1,
            'total': 4
          },
          'INIT': {
            'sessions': 1,
            'slaves': 1,
            'total': 2
          },
          'LEARN': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'LISTEN': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'SPEAK': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'STANDBY': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
            }
        },
        'virtual_addresses_active': 3,
        'virtual_addresses_inactive': 0,
        'vritual_addresses_total': 3
      },
      'ipv6': {
        'intf_down': 0,
        'intf_total': 1,
        'intf_up': 1,
        'state': {
          'ACTIVE': {
            'sessions': 3,
            'slaves': 0,
            'total': 3
          },
          'ALL': {
            'sessions': 3,
            'slaves': 0,
            'total': 3
          },
          'INIT': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'LEARN': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'LISTEN': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'SPEAK': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
          },
          'STANDBY': {
            'sessions': 0,
            'slaves': 0,
            'total': 0
            }
        },
        'virtual_addresses_active': 5,
        'virtual_addresses_inactive': 0,
        'vritual_addresses_total': 5
        }
    },
    'bfd_sessions_down': 0,
    'bfd_sessions_inactive': 1,
    'bfd_sessions_up': 0,
    'num_bfd_sessions': 1,
    'num_tracked_objects': 2,
    'tracked_objects_down': 1,
    'tracked_objects_up': 1
    }


    # Hsrp Ops Object final output
    hsrpOpsOutput = \
    {
    'GigabitEthernet0/0/0/0': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                0: {
                  'active_ip_address': 'unknown',
                  'active_router': 'unknown',
                  'bfd': {
                    'address': '10.1.1.1',
                    'interface_name': 'GigabitEthernet0/0/0/1'
                  },
                  'group_number': 0,
                  'hsrp_router_state': 'init',
                  'preempt': True,
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0000.0c07.ac00'
                },
                10: {
                  'active_ip_address': 'local',
                  'active_router': 'local',
                  'authentication': 'cisco123',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '10.1.1.254'
                  },
                  'priority': 63,
                  'session_name': 'group10',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 10000,
                    'hello_msec_flag': True,
                    'hold_msec': 30000,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 123
                      }
                  },
                  'tracked_objects': {
                    '1': {
                      'object_name': '1',
                      'priority_decrement': 25
                      }
                  },
                  'virtual_mac_address': '0000.0c07.ac0a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'primary_ipv4_address': {
                    'address': '10.1.1.128'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 111,
                    'hello_msec_flag': True,
                    'hold_msec': 333,
                    'hold_msec_flag': True
                  },
                  'tracked_interfaces': {
                    'GigabitEthernet0/0/0/1': {
                      'interface_name': 'GigabitEthernet0/0/0/1',
                      'priority_decrement': 251
                      }
                  },
                  'virtual_mac_address': '0000.0c07.ac14'
                  }
              },
              'slave_groups': {
                30: {
                  'follow': 'group10',
                  'primary_ipv4_address': {
                    'address': 'unknown'
                  },
                  'virtual_mac_address': '0000.0c07.ac1e'
                  }
                }
              }
            }
        },
        'ipv6': {
          'version': {
            2: {
              'groups': {
                10: {
                  'active_ip_address': 'local',
                  'active_router': 'local',
                  'group_number': 10,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:a'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.000a'
                },
                20: {
                  'active_ip_address': 'local',
                  'active_router': 'local',
                  'group_number': 20,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:14'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.0014'
                },
                30: {
                  'active_ip_address': 'local',
                  'active_router': 'local',
                  'group_number': 30,
                  'hsrp_router_state': 'active',
                  'link_local_ipv6_address': {
                    'address': 'fe80::205:73ff:fea0:1e'
                  },
                  'priority': 100,
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec': 3000,
                    'hello_msec_flag': True,
                    'hold_msec': 10000,
                    'hold_msec_flag': True
                  },
                  'virtual_mac_address': '0005.73a0.001e'
                  }
                }
              }
            }
          }
      },
      'bfd': {
        'detection_multiplier': 3,
        'enabled': True,
        'interval': 15
      },
      'delay': {
        'minimum_delay': 100,
        'reload_delay': 1000
      },
      'interface': 'GigabitEthernet0/0/0/0',
      'redirects_disable': True,
      'use_bia': False
      }
    }

# vim: ft=python et sw=4
