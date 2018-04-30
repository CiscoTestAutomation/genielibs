class HsrpOutput(object):

    # 'show standby all' output
    showStandbyAllOutput =  \
    {
    'GigabitEthernet1/0/1': {
      'address_family': {
        'ipv4': {
          'version': {
            2: {
              'groups': {
                0: {
                  'active_router': 'local',
                  'authentication': '5',
                  'authentication_type': 'MD5',
                  'default_priority': 100,
                  'group_number': 0,
                  'hsrp_router_state': 'active',
                  'last_state_change': '1w0d',
                  'local_virtual_mac_address': '0000.0c9f.f000',
                  'local_virtual_mac_address_conf': 'v2 '
                  'default',
                  'preempt': True,
                  'preempt_min_delay': 5,
                  'preempt_reload_delay': 10,
                  'preempt_sync_delay': 20,
                  'primary_ipv4_address': {
                    'address': '192.168.1.254'
                  },
                  'priority': 100,
                  'session_name': 'hsrp-Gi1/0/1-0',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'statistics': {
                    'num_state_changes': 8
                  },
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 5,
                    'hold_msec_flag': False,
                    'hold_sec': 20,
                    'next_hello_sent': 2.848
                  },
                  'virtual_mac_address': '0000.0c9f.f000',
                  'virtual_mac_address_mac_in_use': True
                  }
                }
              }
            }
          }
      },
      'interface': 'GigabitEthernet1/0/1',
      'redirects_disable': False,
      'use_bia': False
    },
    'GigabitEthernet1/0/2': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                10: {
                  'active_router': 'unknown',
                  'authentication': 'cisco123',
                  'authentication_type': 'MD5',
                  'configured_priority': 110,
                  'group_number': 10,
                  'hsrp_router_state': 'disabled',
                  'local_virtual_mac_address': '0000.0c07.ac0a',
                  'local_virtual_mac_address_conf': 'v1 '
                  'default',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': 'unknown'
                  },
                  'priority': 110,
                  'session_name': 'hsrp-Gi1/0/2-10',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 3,
                    'hold_msec_flag': False,
                    'hold_sec': 10
                  },
                  'virtual_mac_address': 'unknown',
                  'virtual_mac_address_mac_in_use': False
                  }
                }
              }
            }
          }
      },
      'interface': 'GigabitEthernet1/0/2',
      'redirects_disable': False,
      'use_bia': False
    },
    'GigabitEthernet3': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                10: {
                  'active_expires_in': 0.816,
                  'active_ip_address': '10.1.2.1',
                  'active_router': '10.1.2.1',
                  'active_router_priority': 120,
                  'configured_priority': 110,
                  'group_number': 10,
                  'hsrp_router_state': 'standby',
                  'local_virtual_mac_address': '0000.0c07.ac0a',
                  'local_virtual_mac_address_conf': 'v1 '
                  'default',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '10.1.2.254'
                  },
                  'priority': 110,
                  'session_name': 'hsrp-Gi3-10',
                  'standby_router': 'local',
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 3,
                    'hold_msec_flag': False,
                    'hold_sec': 10,
                    'next_hello_sent': 2.096
                  },
                  'virtual_mac_address': '0050.568e.3a40',
                  'virtual_mac_address_mac_in_use': False
                  }
                }
              }
            }
          }
      },
      'interface': 'GigabitEthernet3',
      'redirects_disable': False,
      'use_bia': False
      }
    }


    # 'show standby internal' output
    showStandbyInternalOutput = \
    {
    'hsrp_common_process_state': 'running',
    'hsrp_ha_state': 'capable',
    'hsrp_ipv4_process_state': 'running',
    'hsrp_ipv6_process_state': 'running',
    'hsrp_timer_wheel_state': 'running',
    'msgQ_max_size': 3,
    'msgQ_size': 0,
    'v3_to_v4_transform': 'disabled',
    'virtual_ip_hash_table': {
      'ipv4': {
        10: {
          'group': 10,
          'interface': 'gi1',
          'ip': '10.1.1.254'
          }
      },
      'ipv6': {
        78: {
          'group': 20,
          'interface': 'gi1',
          'ip': '2001:DB8:10:1:1::254'
        },
        167: {
          'group': 20,
          'interface': 'gi1',
          'ip': 'FE80::5:73FF:FEA0:14'
        },
        197: {
          'group': 50,
          'interface': 'gi1',
          'ip': 'FE80::5:73FF:FEA0:32'
          }
        }
      }
    }


    showStandbyDelayOutput = \
    {
      "GigabitEthernet1/0/1": {
        "delay": {
          "minimum_delay": 99,
          "reload_delay": 888
        }
      }
    }

    # Hsrp Ops Object final output
    hsrpOpsOutput = \
    {
    'GigabitEthernet1/0/1': {
      'address_family': {
        'ipv4': {
          'version': {
            2: {
              'groups': {
                0: {
                  'active_router': 'local',
                  'authentication': '5',
                  'group_number': 0,
                  'hsrp_router_state': 'active',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '192.168.1.254'
                  },
                  'priority': 100,
                  'session_name': 'hsrp-Gi1/0/1-0',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 5,
                    'hold_msec_flag': False,
                    'hold_sec': 20
                  },
                  'virtual_mac_address': '0000.0c9f.f000'
                  }
                }
              }
            }
          }
      },
      'delay': {
        'minimum_delay': 99, 'reload_delay': 888
      },
      'interface': 'GigabitEthernet1/0/1',
      'redirects_disable': False,
      'use_bia': False
    },
    'GigabitEthernet1/0/2': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                10: {
                  'active_router': 'unknown',
                  'authentication': 'cisco123',
                  'group_number': 10,
                  'hsrp_router_state': 'disabled',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': 'unknown'
                  },
                  'priority': 110,
                  'session_name': 'hsrp-Gi1/0/2-10',
                  'standby_ip_address': 'unknown',
                  'standby_router': 'unknown',
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 3,
                    'hold_msec_flag': False,
                    'hold_sec': 10
                  },
                  'virtual_mac_address': 'unknown'
                  }
                }
              }
            }
          }
      },
      'interface': 'GigabitEthernet1/0/2',
      'redirects_disable': False,
      'use_bia': False
    },
    'GigabitEthernet3': {
      'address_family': {
        'ipv4': {
          'version': {
            1: {
              'groups': {
                10: {
                  'active_ip_address': '10.1.2.1',
                  'active_router': '10.1.2.1',
                  'group_number': 10,
                  'hsrp_router_state': 'standby',
                  'preempt': True,
                  'primary_ipv4_address': {
                    'address': '10.1.2.254'
                  },
                  'priority': 110,
                  'session_name': 'hsrp-Gi3-10',
                  'standby_router': 'local',
                  'timers': {
                    'hello_msec_flag': False,
                    'hello_sec': 3,
                    'hold_msec_flag': False,
                    'hold_sec': 10
                  },
                  'virtual_mac_address': '0050.568e.3a40'
                  }
                }
              }
            }
          }
      },
      'interface': 'GigabitEthernet3',
      'redirects_disable': False,
      'use_bia': False
      }
    }

# vim: ft=python et sw=4
