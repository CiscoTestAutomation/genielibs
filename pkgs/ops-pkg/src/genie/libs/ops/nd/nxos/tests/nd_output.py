'''
 Nd Genie Ops Object Outputs for NXOS.
'''

class NdOutput(object):

    showIpv6NeighborDetail = {
        'interfaces':{
            'Ethernet1/1':{
                'interface': 'Ethernet1/1',
                'neighbors': {
                    '2010:2:3::2': {
                        'ip': '2010:2:3::2',
                        'link_layer_address': 'fa16.3e82.6320',
                        'age': '00:09:27',
                        'preference': 50,
                        'origin': 'other',
                        'physical_interface': 'Ethernet1/1',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
            'Ethernet1/2':{
                'interface': 'Ethernet1/2',
                'neighbors':{
                    '2020:2:3::33': {
                        'ip': '2020:2:3::33',
                        'link_layer_address': 'aaaa.bbbb.cccc',
                        'age': '2d15h',
                        'preference': 1,
                        'origin': 'static',
                        'physical_interface': 'Ethernet1/2',
                        'packet_count': 0,
                        'byte_count': 0,
                        'best': 'Yes',
                        'throttled': 'No',
                    },
                },
            },
        },
    }
    showIpv6NdInterface = {
     "vrf": {
          "vrf1": {
               "interfaces": {
                    "Ethernet1/2": {
                         "router_advertisement": {
                              "default_router_preference": "medium",
                              "interval": 600,
                              "retrans_timer": 0,
                              "suppress_mtu": False,
                              "current_hop_limit": 64,
                              "reachable_time": 0,
                              "mtu": 1500,
                              "suppress": False,
                              "other_stateful_configuration": False,
                              "suppress_route_information": False,
                              "lifetime": 1800,
                              "managed_address_configuration": False
                         },
                         "oper_status": "up",
                         "neighbor_solicitation": {
                              "interval": 1000,
                              "retry_interval": 1000,
                              "retry_base": 1,
                              "retry_attempts": 3
                         },
                         "dad": {
                              "maximum_attempts": 1,
                              "current_attempt": 1
                         },
                         "local_address": "fe80::5c01:c0ff:fe02:7",
                         "error_message": {
                              "unreachables": False,
                              "redirects": True
                         },
                         "enable": True,
                         "link_status": "up",
                         "ip": "2020:2:3::3/64",
                         "mac_extract": "disabled",
                         "active_timers": {
                              "last_router_advertisement": "00:05:42",
                              "last_neighbor_advertisement": "00:01:07",
                              "last_neighbor_solicitation": "00:09:34",
                              "next_router_advertisement": "00:01:46"
                         },
                         "interface": "Ethernet1/2"
                    },
               }
          },
          "default": {
               "interfaces": {
                    "Ethernet1/1": {
                         "router_advertisement": {
                              "default_router_preference": "medium",
                              "interval": 201,
                              "retrans_timer": 0,
                              "suppress_mtu": False,
                              "current_hop_limit": 64,
                              "reachable_time": 0,
                              "mtu": 1500,
                              "suppress": True,
                              "other_stateful_configuration": False,
                              "suppress_route_information": False,
                              "lifetime": 1801,
                              "managed_address_configuration": False
                         },
                         "oper_status": "up",
                         "neighbor_solicitation": {
                              "interval": 1000,
                              "retry_interval": 1000,
                              "retry_base": 1,
                              "retry_attempts": 3
                         },
                         "dad": {
                              "maximum_attempts": 1,
                              "current_attempt": 1
                         },
                         "local_address": "fe80::5c01:c0ff:fe02:7",
                         "error_message": {
                              "unreachables": False,
                              "redirects": True
                         },
                         "enable": True,
                         "link_status": "up",
                         "ip": "2010:2:3::3/64",
                         "mac_extract": "disabled",
                         "active_timers": {
                              "last_router_advertisement": "1d18h",
                              "last_neighbor_advertisement": "00:02:12",
                              "last_neighbor_solicitation": "00:06:16",
                              "next_router_advertisement": "0.000000"
                         },
                         "interface": "Ethernet1/1"
                    },
               }
          }
     }
}
    showIpv6IcmpNeighborDetail = {
       "interfaces": {
            "Ethernet1/2": {
                 "neighbors": {
                      "2020:2:3::33": {
                           "neighbor_state": "stale",
                           "age": "00:03:30",
                           "ip": "2020:2:3::33",
                           "link_layer_address": "fa16.3e8b.59c9",
                           "physical_interface": "Ethernet1/2"
                      },
                 },
                 "interface": "Ethernet1/2"
            },
            "Ethernet1/1": {
                 "neighbors": {
                      "2010:2:3::2": {
                           "neighbor_state": "stale",
                           "age": "00:15:02",
                           "ip": "2010:2:3::2",
                           "link_layer_address": "fa16.3e82.6320",
                           "physical_interface": "Ethernet1/1"
                      }
                 },
                 "interface": "Ethernet1/1"
            },
       }
  }
    showIpv6Routers = {
     "interfaces": {
          "Ethernet1/1": {
               "neighbors": {
                    "2010:2:3::2": {
                         "autonomous_flag": 1,
                         "homeagent_flag": 0,
                         "valid_lifetime": 2592000,
                         "is_router": True,
                         "addr_flag": 0,
                         "ip": "2010:2:3::2",
                         "lifetime": 1800,
                         "onlink_flag": 1,
                         "current_hop_limit": 64,
                         "prefix": "2010:2:3::/64",
                         "retransmission_time": 0,
                         "preferred_lifetime": 604800,
                         "last_update": "3.2",
                         "mtu": 1500,
                         "preference": "medium",
                         "other_flag": 0,
                         "reachable_time": 0
                    }
               },
               "interface": "Ethernet1/1"
          },
          "Ethernet1/2": {
               "neighbors": {
                    "2020:2:3::33": {
                         "autonomous_flag": 1,
                         "homeagent_flag": 0,
                         "valid_lifetime": 2592000,
                         "is_router": True,
                         "addr_flag": 0,
                         "ip": "2020:2:3::33",
                         "lifetime": 1800,
                         "onlink_flag": 1,
                         "current_hop_limit": 64,
                         "prefix": "2020:2:3::/64",
                         "retransmission_time": 0,
                         "preferred_lifetime": 604800,
                         "last_update": "1.5",
                         "mtu": 1500,
                         "preference": "medium",
                         "other_flag": 0,
                         "reachable_time": 0
                    }
               },
               "interface": "Ethernet1/2"
          }
     }
}


    ndOpsOutput = {
        'interfaces':{
            'Ethernet1/1':{
                'interface': 'Ethernet1/1',
                "router_advertisement": {
                    "interval": 201,
                    "suppress": True,
                    "lifetime": 1801,
                },
                'neighbors': {
                    '2010:2:3::2': {
                        'ip': '2010:2:3::2',
                        'link_layer_address': 'fa16.3e82.6320',
                        'age': '00:09:27',
                        'origin': 'other',
                        "is_router": True,
                        "neighbor_state": "stale",
                    },
                },
            },
            'Ethernet1/2':{
                'interface': 'Ethernet1/2',
                "router_advertisement": {
                    "interval": 600,
                    "suppress": False,
                    "lifetime": 1800,
                },
                'neighbors':{
                    '2020:2:3::33': {
                        'ip': '2020:2:3::33',
                        'link_layer_address': 'aaaa.bbbb.cccc',
                        'age': '2d15h',
                        'origin': 'static',
                        "is_router": True,
                        "neighbor_state": "stale",
                    },
                },
            },
        },
    }
