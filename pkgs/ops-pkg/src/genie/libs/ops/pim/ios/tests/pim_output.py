''' 
Pim Genie Ops Object Outputs for IOS
'''


class PimOutput(object):

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

    ShowIpv6PimInterface_default = {
        "vrf": {
          "default": {
               "interface": {
                    "Tunnel4": {
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    },
                    "Null0": {
                         "address": ["FE80::1"],
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    },
                    "Loopback0": {
                         "address": ["FE80::21E:F6FF:FEAC:A600"],
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": True
                    },
                    "Tunnel3": {
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    },
                    "Tunnel1": {
                         "address": ["FE80::21E:F6FF:FEAC:A600"],
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    },
                    "GigabitEthernet1": {
                         "address": ["FE80::5054:FF:FE2C:6CDF"],
                         "dr_address": "FE80::5054:FF:FEAC:64B3",
                         "pim_enabled": True,
                         "dr_priority": 1,
                         "neighbor_count": 1,
                         "hello_interval": 30
                    },
                    "Tunnel2": {
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    },
                    "GigabitEthernet2": {
                         "address": ["FE80::5054:FF:FEBE:8787"],
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": True
                    },
                    "Tunnel0": {
                         "address": ["FE80::21E:F6FF:FEAC:A600"],
                         "dr_priority": 1,
                         "neighbor_count": 0,
                         "hello_interval": 30,
                         "pim_enabled": False
                    }}}}}

    ShowIpv6PimInterface_VRF1 = {
        "vrf": {
            "VRF1": {
                 "interface": {
                      "Loopback1": {
                           "dr_priority": 1,
                           "neighbor_count": 0,
                           "address": [
                                "FE80::21E:F6FF:FEAC:A600"
                           ],
                           "pim_enabled": True,
                           "hello_interval": 30
                      },
                      "Tunnel6": {
                           "dr_priority": 1,
                           "neighbor_count": 0,
                           "pim_enabled": False,
                           "hello_interval": 30
                      },
                      "Tunnel5": {
                           "dr_priority": 1,
                           "neighbor_count": 0,
                           "address": [
                                "FE80::21E:F6FF:FEAC:A600"
                           ],
                           "pim_enabled": False,
                           "hello_interval": 30
                      },
                      "Tunnel7": {
                           "dr_priority": 1,
                           "neighbor_count": 0,
                           "pim_enabled": False,
                           "hello_interval": 30
                      },
                      "GigabitEthernet3": {
                           "dr_priority": 1,
                           "neighbor_count": 0,
                           "address": [
                                "FE80::5054:FF:FE84:F097"
                           ],
                           "pim_enabled": True,
                           "hello_interval": 30
                      }}}}}

    ShowIpPimInterface_default = {
        'vrf':
            {'default':
                {'interfaces':
                    {'GigabitEthernet1':
                        {
                            'address_family': {
                                'ipv4': {
                                    'dr_priority': 1,
                                    'hello_interval': 30,
                                    'neighbor_count': 1,
                                    'version': 2,
                                    'mode': 'sparse-mode',
                                    'dr_address': '10.1.2.2',
                                    'address': ['10.1.2.1'],
                                },
                            },
                        },
                        'GigabitEthernet2': {
                            'address_family': {
                                'ipv4': {
                                    'dr_priority': 1,
                                    'hello_interval': 30,
                                    'neighbor_count': 1,
                                    'version': 2,
                                    'mode': 'sparse-mode',
                                    'dr_address': '10.1.3.3',
                                    'address': ['10.1.3.1'],
                                },
                            },
                        },
                        'Loopback0': {
                            'address_family': {
                                'ipv4': {
                                    'dr_priority': 1,
                                    'hello_interval': 30,
                                    'neighbor_count': 0,
                                    'version': 2,
                                    'mode': 'sparse-mode',
                                    'dr_address': '10.4.1.1',
                                    'address': ['10.4.1.1'],
                                },
                            },
                        },
                    },
                },
            },
    }

    ShowIpPimInterface_VRF1 = {
        'vrf':
            {'VRF1':
                {'interfaces':
                    {'GigabitEthernet3':
                        {
                            'address_family':
                                {
                                    'ipv4': {
                                        'dr_priority': 1,
                                        'hello_interval': 30,
                                        'neighbor_count': 1,
                                        'version': 2,
                                        'mode': 'dense-mode',
                                        'dr_address': '10.1.5.5',
                                        'address': ['10.1.5.1'],
                                    },
                                },
                        },
                    },
                },
            },
    }

    ShowIpv6PimBsrElection_default = {
        'vrf':
            {'default':
                {
                    'address_family':
                        {'ipv6':
                            {'rp':
                                {'bsr':
                                    {'bsr_candidate': {
                                        'address': '2001:1:1:1::1',
                                        'priority': 0,
                                        'hash_mask_length': 126,
                                    },
                                        'bsr': {
                                            'address': '2001:1:1:1::1',
                                            'hash_mask_length': 126,
                                            'priority': 0,
                                            'up_time': '00:00:07',
                                            'scope_range_list': 'ff00::/8',
                                            'rpf_address': 'FE80::21E:F6FF:FE2D:3600',
                                            'rpf_interface': 'Loopback0',
                                            'expires': '00:00:52',
                                        },
                                    },
                                },
                            },
                        },
                },
            },
    }

    ShowIpv6PimBsrElection_VRF1 = {
        'vrf':
            {'VRF1':
                {
                    'address_family':
                        {'ipv6':
                            {'rp':
                                {'bsr':
                                    {'bsr_candidate': {
                                        'address': '2001:DB8:1:5::1',
                                        'priority': 0,
                                        'hash_mask_length': 126,
                                    },
                                        'bsr': {
                                            'address': '2001:DB8:1:5::1',
                                            'hash_mask_length': 126,
                                            'priority': 0,
                                            'up_time': '00:08:39',
                                            'scope_range_list': 'ff00::/8',
                                            'rpf_address': 'FE80::5054:FF:FEC3:D71C',
                                            'rpf_interface': 'GigabitEthernet3',
                                            'expires': '00:00:22',
                                        },
                                    },
                                },
                            },
                        },
                },
            },
    }

    ShowIpv6PimBsrCandidateRp_default = {
            'vrf':
                {'default':
                    {
                        'address_family':
                            {'ipv6':
                                {'rp':
                                    {'bsr':
                                        {'2001:3:3:3::3': {
                                            'address': '2001:3:3:3::3',
                                            'priority': 5,
                                            'mode': 'SM',
                                            'holdtime': 150,
                                            'interval': 60,
                                        },
                                            'rp_candidate_next_advertisement': '00:00:48',
                                        },
                                    },
                                },
                            },
                    },
                },
    }

    ShowIpv6PimBsrCandidateRp_VRF1 = {
            'vrf':
                {'VRF1':
                    {
                        'address_family':
                            {'ipv6':
                                {'rp':
                                    {'bsr':
                                        {'2001:DB8:1:5::1': {
                                            'address': '2001:DB8:1:5::1',
                                            'priority': 192,
                                            'mode': 'SM',
                                            'holdtime': 150,
                                            'interval': 60,
                                        },
                                            'rp_candidate_next_advertisement': '00:00:50',
                                        },
                                    },
                                },
                            },
                    },
                },
    }

    ShowIpPimBsrRouter_default = {
        'vrf':
            {'default':
                {
                    'address_family':
                        {'ipv4':
                            {'rp':
                                {'bsr':
                                    {'Loopback0': {
                                        'interface': 'Loopback0',
                                        'address': '10.16.2.2',
                                        'holdtime': 150,
                                        'next_advertisment': '00:00:26',
                                        'priority': 10,
                                        'interval': 60,
                                        },
                                    'bsr': {
                                        'address': '10.64.4.4',
                                        'hash_mask_length': 0,
                                        'priority': 0,
                                        'address_host': '?',
                                        'up_time': '3d07h',
                                    },
                                    'bsr_next_bootstrap':'00:00:06',
                                },
                            },
                        },
                    },
                },
            },
    }

    ShowIpPimBsrRouter_VRF1 = {
        'vrf':
            {'VRF1':
                {
                    'address_family':
                        {'ipv4':
                            {'rp':
                                {'bsr':
                                    {'GigabitEthernet0/2': {
                                        'interface': 'GigabitEthernet0/2',
                                        'address': '10.4.6.4',
                                        'holdtime': 150,
                                        'next_advertisment': '00:00:00',
                                        'priority': 5,
                                        'interval': 60,
                                    },
                                    'bsr': {
                                        'address': '10.4.6.6',
                                        'hash_mask_length': 0,
                                        'priority': 0,
                                        'address_host': '?',
                                        'up_time': '4d03h',
                                        'expires': '00:02:00',
                                    },
                                },
                            },
                        },
                    },
                },
            },
    }

    ShowIpPimRpMapping_default = {
        "vrf": {
              "default": {
                   "address_family": {
                        "ipv4": {
                             "rp": {
                                  "rp_list": {
                                       "10.36.3.3 BIDIR static": {
                                            "info_source_type": "static",
                                            "address": "10.36.3.3",
                                            'mode': 'BIDIR'
                                       },
                                       "10.145.0.3 SM autorp": {
                                            "address": "10.145.0.3",
                                            "info_source_address": "10.145.0.2",
                                            "bsr_version": "v2v1",
                                            "info_source_type": "autorp",
                                            "expiration": "00:02:40",
                                            "up_time": "00:22:08",
                                            'mode': 'SM'
                                       },
                                       "10.16.2.2 SM bootstrap": {
                                            "address": "10.16.2.2",
                                            "info_source_address": "10.64.4.4",
                                            "bsr_version": "v2",
                                            "info_source_type": "bootstrap",
                                            "expiration": "00:02:03",
                                            "up_time": "00:00:35",
                                            'mode': 'SM'
                                       },
                                       "10.36.3.3 SM bootstrap": {
                                            "address": "10.36.3.3",
                                            "info_source_address": "10.64.4.4",
                                            "bsr_version": "v2",
                                            "info_source_type": "bootstrap",
                                            "expiration": "00:02:19",
                                            "up_time": "00:00:19",
                                            'mode': 'SM'
                                       }
                                  },
                                  "rp_mappings": {
                                       "224.0.0.0/4 10.145.0.3 autorp": {
                                            "group": "224.0.0.0/4",
                                            "rp_address_host": "?",
                                            "protocol": "autorp",
                                            "expiration": "00:02:40",
                                            "rp_address": "10.145.0.3",
                                            "up_time": "00:22:08"
                                       },
                                       "224.0.0.0/4 10.16.2.2 bootstrap": {
                                            "group": "224.0.0.0/4",
                                            "rp_address_host": "?",
                                            "hold_time": 150,
                                            "priority": 10,
                                            "protocol": "bootstrap",
                                            "expiration": "00:02:03",
                                            "rp_address": "10.16.2.2",
                                            "up_time": "00:00:35"
                                       },
                                       "224.0.0.0/4 10.36.3.3 bootstrap": {
                                            "group": "224.0.0.0/4",
                                            "rp_address_host": "?",
                                            "hold_time": 150,
                                            "priority": 5,
                                            "protocol": "bootstrap",
                                            "expiration": "00:02:19",
                                            "rp_address": "10.36.3.3",
                                            "up_time": "00:00:19"
                                       },
                                       "224.0.0.0/4 10.36.3.3 static": {
                                            "group": "224.0.0.0/4",
                                            "protocol": "static",
                                            "rp_address": "10.36.3.3",
                                            "rp_address_host": "?"
                                       }
                                  },
                                  "static_rp": {
                                       "10.36.3.3": {
                                            "bidir": {}
                                       }
                                  },
                                  "bsr": {
                                       "rp": {
                                            "rp_address": "10.16.2.2",
                                            "up_time": "00:22:08",
                                            "group_policy": "224.0.0.0/4"
                                       }
                                  },
                             }
                        }
                   }
              }
         }
    }

    ShowIpPimRpMapping_VRF1 = {
        "vrf": {
              "VRF1": {
                   "address_family": {
                        "ipv4": {
                             "rp": {
                                  "rp_mappings": {
                                       "STATIC_RP_V4 192.168.151.1 static": {
                                            "rp_address_host": "?",
                                            "protocol": "static",
                                            "rp_address": "192.168.151.1",
                                            "group": "STATIC_RP_V4"
                                       },
                                       "224.0.0.0/4 10.1.5.5 static": {
                                            "rp_address_host": "?",
                                            "protocol": "static",
                                            "rp_address": "10.1.5.5",
                                            "group": "224.0.0.0/4"
                                       }
                                  },
                                  "rp_list": {
                                       "10.1.5.5 SM static": {
                                            "mode": "SM",
                                            "address": "10.1.5.5",
                                            "info_source_type": "static"
                                       },
                                       "192.168.151.1 SM static": {
                                            "mode": "SM",
                                            "address": "192.168.151.1",
                                            "info_source_type": "static"
                                       }
                                  },
                                  "static_rp": {
                                       "192.168.151.1": {
                                            "sm": {
                                                 "policy_name": "STATIC_RP_V4",
                                                 "override": True
                                            }
                                       }
                                  }
                             }
                        }
                   }
              }
        }
    }

    ShowIpPimInterfaceDetail_default = {
        'vrf':
            {'default':
                {'interfaces':{
                    'GigabitEthernet1':{
                        'address_family':{
                            'ipv4': {
                                'bfd': {
                                    'enable': False,
                                },
                                'hello_interval': 30,
                                'hello_packets_in': 8,
                                'hello_packets_out': 10,
                                'oper_status': 'up',
                                'enable': True,
                                'neighbor_filter': '7',
                                'address': ['10.1.2.1/24'],
                                'multicast': {
                                    'switching': 'fast',
                                    'packets_in': 5,
                                    'packets_out': 0,
                                    'ttl_threshold': 0,
                                    'tag_switching': False,
                                },
                                'pim_status': 'enabled',
                                'version': 2,
                                'mode': 'sparse',
                                'sm': {},
                                'dr_address': '10.1.2.2',
                                'neighbor_count': 1,
                                'jp_interval': 60,
                                'state_refresh_processing': 'enabled',
                                'state_refresh_origination': 'disabled',
                                'nbma_mode': 'disabled',
                                'atm_multipoint_signalling': 'disabled',
                                'bsr_border': False,
                                'neighbors_rpf_proxy_capable': True,
                                'none_dr_join': False,
                            },
                        },
                    },
                    'GigabitEthernet2': {
                        'address_family': {
                            'ipv4': {
                                'bfd': {
                                    'enable': False,
                                },
                                'hello_interval': 30,
                                'hello_packets_in': 7,
                                'hello_packets_out': 10,
                                'oper_status': 'up',
                                'enable': True,
                                'address': ['10.1.3.1/24'],
                                'multicast': {
                                    'switching': 'fast',
                                    'packets_in': 5,
                                    'packets_out': 0,
                                    'ttl_threshold': 0,
                                    'tag_switching': False,
                                },
                                'pim_status': 'enabled',
                                'version': 2,
                                'mode': 'dense',
                                'dm': {},
                                'dr_address': '10.1.3.3',
                                'neighbor_count': 1,
                                'jp_interval': 60,
                                'state_refresh_processing': 'enabled',
                                'state_refresh_origination': 'disabled',
                                'nbma_mode': 'disabled',
                                'atm_multipoint_signalling': 'disabled',
                                'bsr_border': False,
                                'neighbors_rpf_proxy_capable': True,
                                'none_dr_join': False,
                            },
                        },
                    },
                    'Loopback0': {
                        'address_family': {
                            'ipv4': {
                                'bfd': {
                                    'enable': False,
                                },
                                'hello_interval': 30,
                                'hello_packets_in': 8,
                                'hello_packets_out': 8,
                                'oper_status': 'up',
                                'enable': True,
                                'address': ['10.4.1.1/32'],
                                'multicast': {
                                    'switching': 'fast',
                                    'packets_in': 0,
                                    'packets_out': 0,
                                    'ttl_threshold': 0,
                                    'tag_switching': False,
                                },
                                'pim_status': 'enabled',
                                'version': 2,
                                'mode': 'sparse',
                                'sm': {},
                                'dr_address': '10.4.1.1',
                                'neighbor_count': 0,
                                'jp_interval': 60,
                                'state_refresh_processing': 'enabled',
                                'state_refresh_origination': 'disabled',
                                'nbma_mode': 'disabled',
                                'atm_multipoint_signalling': 'disabled',
                                'bsr_border': False,
                                'neighbors_rpf_proxy_capable': False,
                                'none_dr_join': False,
                            },
                        },
                    },
                },
            },
        }
    }

    ShowIpPimInterfaceDetail_VRF1 = {
        'vrf':
            {'VRF1':
                {'interfaces':
                    {'GigabitEthernet3':
                        {
                        'address_family':
                            {
                            'ipv4': {
                                'bfd': {
                                    'enable': False,
                                },
                                'hello_interval': 30,
                                'hello_packets_in': 6,
                                'hello_packets_out': 6,
                                'oper_status': 'up',
                                'enable': True,
                                'address': ['10.1.5.1/24'],
                                'multicast': {
                                    'switching': 'fast',
                                    'packets_in': 4,
                                    'packets_out': 0,
                                    'ttl_threshold': 0,
                                    'tag_switching': False,
                                },
                                'pim_status': 'enabled',
                                'version': 2,
                                'mode': 'passive',
                                'sm': {
                                    'passive': True,
                                },
                                'dr_address': '10.1.5.5',
                                'neighbor_count': 1,
                                'jp_interval': 60,
                                'state_refresh_processing': 'enabled',
                                'state_refresh_origination': 'disabled',
                                'nbma_mode': 'disabled',
                                'atm_multipoint_signalling': 'disabled',
                                'bsr_border': False,
                                'neighbors_rpf_proxy_capable': True,
                                'none_dr_join': False,
                                },
                             },
                        },
                    },
                },
            },
    }

    ShowIpMroute_default = {
        "vrf": {
            "default": {
                 "address_family": {
                      "ipv4": {
                           "multicast_group": {
                                "239.1.1.1": {
                                     "source_address": {
                                          "*": {
                                               "expire": "stopped",
                                               "rp": "10.4.1.1",
                                               "flags": "SPF",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "uptime": "00:00:03",
                                               "rpf_nbr": "0.0.0.0",
                                          },
                                          "10.4.1.1": {
                                               "expire": "00:02:57",
                                               "flags": "PFT",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "uptime": "00:00:03",
                                               "rpf_info": "registering",
                                               "rpf_nbr": "0.0.0.0",
                                               "incoming_interface_list": {
                                                    "Loopback0": {
                                                         "rpf_info": "registering",
                                                         "rpf_nbr": "0.0.0.0"
                                                    }
                                               }
                                          },
                                          "10.1.3.1": {
                                               "expire": "00:02:57",
                                               "flags": "PFT",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "uptime": "00:00:03",
                                               "rpf_info": "registering",
                                               "rpf_nbr": "0.0.0.0",
                                               "incoming_interface_list": {
                                                    "GigabitEthernet2": {
                                                         "rpf_info": "registering",
                                                         "rpf_nbr": "0.0.0.0"
                                                    }
                                               }
                                          }
                                     }
                                },
                                "224.0.1.40": {
                                     "source_address": {
                                          "*": {
                                               "expire": "00:02:56",
                                               "outgoing_interface_list": {
                                                    "Loopback0": {
                                                         "expire": "00:02:56",
                                                         "uptime": "2d09h",
                                                         "state_mode": "forward/sparse"
                                                    }
                                               },
                                               "flags": "SCL",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rp": "10.16.2.2",
                                               "uptime": "2d09h",
                                               "rpf_nbr": "0.0.0.0",
                                          }
                                     }
                                },
                                "224.1.1.1": {
                                     "source_address": {
                                          "*": {
                                               "expire": "00:02:54",
                                               "outgoing_interface_list": {
                                                    "ATM0/0": {
                                                         "expire": "00:02:53",
                                                         "uptime": "00:03:57",
                                                         "vcd": "14",
                                                         "state_mode": "forward/sparse"
                                                    }
                                               },
                                               "flags": "SJ",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rp": "172.16.0.0",
                                               "uptime": "00:03:57",
                                               "rpf_nbr": "224.0.0.0224.0.0.0"}}}}}}}}}

    ShowIpMroute_VRF1 = {
        "vrf": {
            "VRF1": {
                 "address_family": {
                      "ipv4": {
                           "multicast_group": {
                                "239.1.1.1": {
                                     "source_address": {
                                          "10.229.11.11": {
                                               "expire": "00:02:55",
                                               "uptime": "00:00:04",
                                               "flags": "PFT",
                                               "rpf_info": "registering",
                                               "rpf_nbr": "0.0.0.0",
                                               "incoming_interface_list": {
                                                    "Loopback1": {
                                                         "rpf_info": "registering",
                                                         "rpf_nbr": "0.0.0.0"
                                                    }
                                               }
                                          },
                                          "*": {
                                               "expire": "stopped",
                                               "uptime": "00:00:04",
                                               "flags": "SPF",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rp": "10.229.11.11",
                                               "rpf_nbr": "0.0.0.0",
                                          }
                                     }
                                },
                                "224.0.1.40": {
                                     "source_address": {
                                          "*": {
                                               "expire": "00:02:52",
                                               "uptime": "00:08:58",
                                               "rpf_nbr": "0.0.0.0",
                                               "outgoing_interface_list": {
                                                    "Loopback1": {
                                                         "state_mode": "forward/sparse",
                                                         "uptime": "00:08:58",
                                                         "expire": "00:02:52"
                                                    }
                                               },
                                               "flags": "SJCL",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rp": "10.229.11.11"}}}}}}}}}

    ShowIpv6Mroute_default = {
        "vrf": {
            "default": {
                 "address_family": {
                      "ipv6": {
                           "multicast_group": {
                                "FF07::1": {
                                     "source_address": {
                                          "2001:DB8:999::99": {
                                               "outgoing_interface_list": {
                                                    "POS4/0": {
                                                         "state_mode": "forward",
                                                         "uptime": "00:02:06",
                                                         "expire": "00:03:27"
                                                    }
                                               },
                                               "incoming_interface_list": {
                                                    "POS1/0": {
                                                         "rpf_nbr": "2001:DB8:999::99"
                                                    }
                                               },
                                               "uptime": "00:02:06",
                                               "flags": "SFT",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rpf_nbr": "2001:DB8:999::99",
                                               "expire": "00:01:23"
                                          },
                                          "*": {
                                               "outgoing_interface_list": {
                                                    "POS4/0": {
                                                         "state_mode": "forward",
                                                         "uptime": "00:04:45",
                                                         "expire": "00:02:47"
                                                    }
                                               },
                                               "incoming_interface_list": {
                                                    "Tunnel5": {
                                                         "rpf_nbr": "2001:db8:90:24::6"
                                                    }
                                               },
                                               "uptime": "00:04:45",
                                               "rp": "2001:DB8:6::6",
                                               "flags": "S",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rpf_nbr": "2001:db8:90:24::6",
                                               "expire": "00:02:47"
                                          }}}}}}}}}

    ShowIpv6Mroute_VRF1 = {
        "vrf": {
            "VRF1": {
                 "address_family": {
                      "ipv6": {
                           "multicast_group": {
                                "FF07::1": {
                                     "source_address": {
                                          "2001:DB8:999::99": {
                                               "outgoing_interface_list": {
                                                    "POS4/0": {
                                                         "state_mode": "forward",
                                                         "uptime": "00:02:06",
                                                         "expire": "00:03:27"
                                                    }
                                               },
                                               "incoming_interface_list": {
                                                    "POS1/0": {
                                                         "rpf_nbr": "2001:DB8:999::99"
                                                    }
                                               },
                                               "uptime": "00:02:06",
                                               "flags": "SFT",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rpf_nbr": "2001:DB8:999::99",
                                               "expire": "00:01:23"
                                          },
                                          "*": {
                                               "outgoing_interface_list": {
                                                    "POS4/0": {
                                                         "state_mode": "forward",
                                                         "uptime": "00:04:45",
                                                         "expire": "00:02:47"
                                                    }
                                               },
                                               "incoming_interface_list": {
                                                    "Tunnel5": {
                                                         "rpf_nbr": "2001:db8:90:24::6"
                                                    }
                                               },
                                               "uptime": "00:04:45",
                                               "rp": "2001:DB8:6::6",
                                               "flags": "S",
                                               'msdp_learned': False,
                                               'rp_bit': False,
                                               "rpf_nbr": "2001:db8:90:24::6",
                                               "expire": "00:02:47"
                                          }}}}}}}}

    }

    ShowIpPimNeighbor_default = {
        "vrf": {
              "default": {
                   "interfaces": {
                        "Port-channel1.100": {
                             "address_family": {
                                  "ipv4": {
                                       "neighbors": {
                                            "192.168.4.1": {
                                                 "dr_priority": 1,
                                                 "state_refresh_capable": True,
                                                 "proxy_capable": True,
                                                 "interface": "Port-channel1.100",
                                                 "genid_capable": True,
                                                 "version": "v2",
                                                 "expiration": "00:01:40",
                                                 "up_time": "4w4d"
                                            }
                                       }
                                  }
                             }
                        },
                        "GigabitEthernet0/2/3.100": {
                             "address_family": {
                                  "ipv4": {
                                       "neighbors": {
                                            "192.168.205.2": {
                                                 "dr_priority": 1,
                                                 "designated_router": True,
                                                 "proxy_capable": True,
                                                 "interface": "GigabitEthernet0/2/3.100",
                                                 "bidir_capable": True,
                                                 "expiration": "00:01:19",
                                                 "version": "v2",
                                                 "state_refresh_capable": True,
                                                 "genid_capable": True,
                                                 "up_time": "4w4d"
                                            }
                                       }
                                  }
                             }
                        }
                   }
              }
         }
    }
    ShowIpPimNeighbor_VRF1 = {}

    ShowIpv6PimNeighborDetail_default = {
        "vrf": {
              "default": {
                   "interfaces": {
                        "Port-channel1.100": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "secondary_address": [
                                                 "2001::1:1"
                                            ],
                                            "FE80::21A:30FF:FE47:6EC0": {
                                                 "up_time": "3w3d",
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:37",
                                                 "interface": "Port-channel1.100",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            }
                                       }
                                  }
                             }
                        },
                        "Port-channel1.101": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "secondary_address": [
                                                 "2001:1::1:1"
                                            ],
                                            "FE80::21A:30FF:FE47:6EC0": {
                                                 "up_time": "3w3d",
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:38",
                                                 "interface": "Port-channel1.101",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            }
                                       }
                                  }
                             }
                        },
                        "GigabitEthernet0/2/3.100": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "secondary_address": [
                                                 "2001::4:2"
                                            ],
                                            "FE80::2D7:8FFF:FECB:8602": {
                                                 "up_time": "3w3d",
                                                 "designated_router": True,
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:25",
                                                 "interface": "GigabitEthernet0/2/3.100",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            }
                                       }
                                  }
                             }
                        },
                        "GigabitEthernet0/2/0.101": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "FE80::21A:30FF:FE47:6E01": {
                                                 "up_time": "3w3d",
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:24",
                                                 "interface": "GigabitEthernet0/2/0.101",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            },
                                            "secondary_address": [
                                                 "2001:1::1"
                                            ]
                                       }
                                  }
                             }
                        },
                        "GigabitEthernet0/2/3.101": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "secondary_address": [
                                                 "2001:1::4:2"
                                            ],
                                            "FE80::2D7:8FFF:FECB:8602": {
                                                 "up_time": "3w3d",
                                                 "designated_router": True,
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:42",
                                                 "interface": "GigabitEthernet0/2/3.101",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            }
                                       }
                                  }
                             }
                        },
                        "GigabitEthernet0/2/0.100": {
                             "address_family": {
                                  "ipv6": {
                                       "neighbors": {
                                            "FE80::21A:30FF:FE47:6E01": {
                                                 "up_time": "3w3d",
                                                 "dr_priority": 1,
                                                 "expiration": "00:01:33",
                                                 "interface": "GigabitEthernet0/2/0.100",
                                                 "genid_capable": True,
                                                 "bidir_capable": True
                                            },
                                            "secondary_address": [
                                                 "2001::1"
                                            ]
                                       }
                                  }
                             }
                        }
                   }
              }
         }
    }

    ShowIpv6PimNeighborDetail_VRF1 = {}
    
    ShowIpPimInterfaceDf_default = {
        "vrf": {
            "default": {
               "address_family": {
                    "ipv4": {
                         "rp": {
                              "bidir": {
                                   "interface_df_election": {
                                        "10.10.0.2 Ethernet3/3": {
                                             "df_address": "10.4.0.2",
                                             "metric": 0,
                                             "df_uptime": "00:03:49",
                                             "address": "10.10.0.2",
                                             "winner_metric": 0,
                                             "interface_name": "Ethernet3/3"
                                        },
                                        "10.10.0.3 Ethernet3/3": {
                                             "df_address": "10.4.0.3",
                                             "metric": 0,
                                             "df_uptime": "00:01:49",
                                             "address": "10.10.0.3",
                                             "winner_metric": 0,
                                             "interface_name": "Ethernet3/3"
                                        },
                                        "10.10.0.3 Ethernet3/4": {
                                             "df_address": "10.5.0.2",
                                             "metric": 409600,
                                             "df_uptime": "00:02:32",
                                             "address": "10.10.0.3",
                                             "winner_metric": 409600,
                                             "interface_name": "Ethernet3/4"
                                        },
                                        "10.10.0.5 Ethernet3/4": {
                                             "df_address": "10.5.0.2",
                                             "metric": 435200,
                                             "df_uptime": "00:02:16",
                                             "address": "10.10.0.5",
                                             "winner_metric": 435200,
                                             "interface_name": "Ethernet3/4"
                                        },
                                        "10.10.0.2 Loopback0": {
                                             "df_address": "10.10.0.2",
                                             "metric": 0,
                                             "df_uptime": "00:03:49",
                                             "address": "10.10.0.2",
                                             "winner_metric": 0,
                                             "interface_name": "Loopback0"
                                        },
                                        "10.10.0.2 Ethernet3/4": {
                                             "df_address": "10.5.0.2",
                                             "metric": 0,
                                             "df_uptime": "00:03:49",
                                             "address": "10.10.0.2",
                                             "winner_metric": 0,
                                             "interface_name": "Ethernet3/4"
                                        },
                                        "10.10.0.3 Loopback0": {
                                             "df_address": "10.10.0.2",
                                             "metric": 409600,
                                             "df_uptime": "00:02:32",
                                             "address": "10.10.0.3",
                                             "winner_metric": 409600,
                                             "interface_name": "Loopback0"
                                        },
                                        "10.10.0.5 Loopback0": {
                                             "df_address": "10.10.0.2",
                                             "metric": 435200,
                                             "df_uptime": "00:02:16",
                                             "address": "10.10.0.5",
                                             "winner_metric": 435200,
                                             "interface_name": "Loopback0"
                                        },
                                        "10.10.0.5 Ethernet3/3": {
                                             "df_address": "10.4.0.4",
                                             "metric": 409600,
                                             "df_uptime": "00:01:49",
                                             "address": "10.10.0.5",
                                             "winner_metric": 409600,
                                             "interface_name": "Ethernet3/3"
                                        }
                                   }
                              }
                         }
                    }
               }
            }
        }
    }
    
    ShowIpPimInterfaceDf_VRF1 = {
        "vrf": {
            "VRF1": {
               "address_family": {
                    "ipv4": {
                         "rp": {
                              "bidir": {
                                   "interface_df_election": {
                                        "10.186.0.1 Tunnel9": {
                                             "address": "10.186.0.1",
                                             "interface_name": "Tunnel9",
                                             "metric": 20,
                                             "df_address": "0.0.0.0",
                                             "df_uptime": "00:00:00",
                                             "winner_metric": 20
                                        },
                                        "10.186.0.1 Ethernet0/1": {
                                             "address": "10.186.0.1",
                                             "interface_name": "Ethernet0/1",
                                             "metric": 20,
                                             "df_address": "10.4.0.4",
                                             "df_uptime": "00:00:39",
                                             "winner_metric": 20
                                        }
                                   }
                              }
                         }
                    }
                }
            }
        }}

    Pim_info = {
    'vrf': {'VRF1': {'address_family': {'ipv4': {'bidir': {},
                                              'rp': {'bidir': {'interface_df_election': {'10.186.0.1 Ethernet0/1': {'address': '10.186.0.1',
                                                                                                                    'df_address': '10.4.0.4',
                                                                                                                    'interface_name': 'Ethernet0/1'},
                                                                                         '10.186.0.1 Tunnel9': {'address': '10.186.0.1',
                                                                                                                'df_address': '0.0.0.0',
                                                                                                                'interface_name': 'Tunnel9'}}},
                                                     'bsr': {'GigabitEthernet0/2': {'address': '10.4.6.4',
                                                                                    'interface': 'GigabitEthernet0/2',
                                                                                    'interval': 60,
                                                                                    'priority': 5},
                                                             'bsr': {'address': '10.4.6.6',
                                                                     'expires': '00:02:00',
                                                                     'hash_mask_length': 0,
                                                                     'priority': 0,
                                                                     'up_time': '4d03h'}},
                                                     'rp_list': {'10.1.5.5 SM static': {'address': '10.1.5.5',
                                                                                        'info_source_type': 'static',
                                                                                        'mode': 'SM'},
                                                                 '192.168.151.1 SM static': {'address': '192.168.151.1',
                                                                                             'info_source_type': 'static',
                                                                                             'mode': 'SM'}},
                                                     'rp_mappings': {'224.0.0.0/4 10.1.5.5 static': {'group': '224.0.0.0/4',
                                                                                                     'protocol': 'static',
                                                                                                     'rp_address': '10.1.5.5'},
                                                                     'STATIC_RP_V4 192.168.151.1 static': {'group': 'STATIC_RP_V4',
                                                                                                           'protocol': 'static',
                                                                                                           'rp_address': '192.168.151.1'}},
                                                     'static_rp': {'192.168.151.1': {'sm': {'override': True,
                                                                                            'policy_name': 'STATIC_RP_V4'}}}},
                                              'topology_tree_info': {'224.0.1.40 * True': {'expiration': '00:02:52',
                                                                                           'group': '224.0.1.40',
                                                                                           'is_rpt': True,
                                                                                           'msdp_learned': False,
                                                                                           'outgoing_interface': {'Loopback1': {'up_time': '00:08:58'}},
                                                                                           'rp_address': '10.229.11.11',
                                                                                           'rp_bit': False,
                                                                                           'rpf_neighbor': '0.0.0.0',
                                                                                           'source_address': '*',
                                                                                           'up_time': '00:08:58'},
                                                                     '239.1.1.1 * True': {'expiration': 'stopped',
                                                                                          'group': '239.1.1.1',
                                                                                          'is_rpt': True,
                                                                                          'msdp_learned': False,
                                                                                          'rp_address': '10.229.11.11',
                                                                                          'rp_bit': False,
                                                                                          'rpf_neighbor': '0.0.0.0',
                                                                                          'source_address': '*',
                                                                                          'up_time': '00:00:04'},
                                                                     '239.1.1.1 10.229.11.11 False': {'expiration': '00:02:55',
                                                                                                      'group': '239.1.1.1',
                                                                                                      'incoming_interface': 'Loopback1',
                                                                                                      'is_rpt': False,
                                                                                                      'rpf_neighbor': '0.0.0.0',
                                                                                                      'source_address': '10.229.11.11',
                                                                                                      'up_time': '00:00:04'}}}},
                  'interfaces': {'GigabitEthernet3': {'address_family': {'ipv4': {'address': ['10.1.5.1/24'],
                                                                                  'bfd': {'enable': False},
                                                                                  'bsr_border': False,
                                                                                  'dr_priority': 1,
                                                                                  'hello_interval': 30,
                                                                                  'jp_interval': 60,
                                                                                  'mode': 'dense-mode',
                                                                                  'oper_status': 'up',
                                                                                  'sm': {'passive': True}}}}}},
         'default': {'address_family': {'ipv4': {'bidir': {},
                                                 'rp': {'bidir': {'interface_df_election': {'10.10.0.2 Ethernet3/3': {'address': '10.10.0.2',
                                                                                                                      'df_address': '10.4.0.2',
                                                                                                                      'interface_name': 'Ethernet3/3'},
                                                                                            '10.10.0.2 Ethernet3/4': {'address': '10.10.0.2',
                                                                                                                      'df_address': '10.5.0.2',
                                                                                                                      'interface_name': 'Ethernet3/4'},
                                                                                            '10.10.0.2 Loopback0': {'address': '10.10.0.2',
                                                                                                                    'df_address': '10.10.0.2',
                                                                                                                    'interface_name': 'Loopback0'},
                                                                                            '10.10.0.3 Ethernet3/3': {'address': '10.10.0.3',
                                                                                                                      'df_address': '10.4.0.3',
                                                                                                                      'interface_name': 'Ethernet3/3'},
                                                                                            '10.10.0.3 Ethernet3/4': {'address': '10.10.0.3',
                                                                                                                      'df_address': '10.5.0.2',
                                                                                                                      'interface_name': 'Ethernet3/4'},
                                                                                            '10.10.0.3 Loopback0': {'address': '10.10.0.3',
                                                                                                                    'df_address': '10.10.0.2',
                                                                                                                    'interface_name': 'Loopback0'},
                                                                                            '10.10.0.5 Ethernet3/3': {'address': '10.10.0.5',
                                                                                                                      'df_address': '10.4.0.4',
                                                                                                                      'interface_name': 'Ethernet3/3'},
                                                                                            '10.10.0.5 Ethernet3/4': {'address': '10.10.0.5',
                                                                                                                      'df_address': '10.5.0.2',
                                                                                                                      'interface_name': 'Ethernet3/4'},
                                                                                            '10.10.0.5 Loopback0': {'address': '10.10.0.5',
                                                                                                                    'df_address': '10.10.0.2',
                                                                                                                    'interface_name': 'Loopback0'}}},
                                                        'bsr': {'Loopback0': {'address': '10.16.2.2',
                                                                              'interface': 'Loopback0',
                                                                              'interval': 60,
                                                                              'priority': 10},
                                                                'bsr': {'address': '10.64.4.4',
                                                                        'hash_mask_length': 0,
                                                                        'priority': 0,
                                                                        'up_time': '3d07h'},
                                                                'bsr_next_bootstrap': '00:00:06',
                                                                'rp': {'group_policy': '224.0.0.0/4',
                                                                       'rp_address': '10.16.2.2',
                                                                       'up_time': '00:22:08'}},
                                                        'rp_list': {'10.145.0.3 SM autorp': {'address': '10.145.0.3',
                                                                                             'expiration': '00:02:40',
                                                                                             'info_source_address': '10.145.0.2',
                                                                                             'info_source_type': 'autorp',
                                                                                             'mode': 'SM',
                                                                                             'up_time': '00:22:08'},
                                                                    '10.16.2.2 SM bootstrap': {'address': '10.16.2.2',
                                                                                               'expiration': '00:02:03',
                                                                                               'info_source_address': '10.64.4.4',
                                                                                               'info_source_type': 'bootstrap',
                                                                                               'mode': 'SM',
                                                                                               'up_time': '00:00:35'},
                                                                    '10.36.3.3 BIDIR static': {'address': '10.36.3.3',
                                                                                               'info_source_type': 'static',
                                                                                               'mode': 'BIDIR'},
                                                                    '10.36.3.3 SM bootstrap': {'address': '10.36.3.3',
                                                                                               'expiration': '00:02:19',
                                                                                               'info_source_address': '10.64.4.4',
                                                                                               'info_source_type': 'bootstrap',
                                                                                               'mode': 'SM',
                                                                                               'up_time': '00:00:19'}},
                                                        'rp_mappings': {'224.0.0.0/4 10.145.0.3 autorp': {'expiration': '00:02:40',
                                                                                                          'group': '224.0.0.0/4',
                                                                                                          'protocol': 'autorp',
                                                                                                          'rp_address': '10.145.0.3',
                                                                                                          'up_time': '00:22:08'},
                                                                        '224.0.0.0/4 10.16.2.2 bootstrap': {'expiration': '00:02:03',
                                                                                                            'group': '224.0.0.0/4',
                                                                                                            'protocol': 'bootstrap',
                                                                                                            'rp_address': '10.16.2.2',
                                                                                                            'up_time': '00:00:35'},
                                                                        '224.0.0.0/4 10.36.3.3 bootstrap': {'expiration': '00:02:19',
                                                                                                            'group': '224.0.0.0/4',
                                                                                                            'protocol': 'bootstrap',
                                                                                                            'rp_address': '10.36.3.3',
                                                                                                            'up_time': '00:00:19'},
                                                                        '224.0.0.0/4 10.36.3.3 static': {'group': '224.0.0.0/4',
                                                                                                         'protocol': 'static',
                                                                                                         'rp_address': '10.36.3.3'}},
                                                        'static_rp': {'10.36.3.3': {'bidir': {}}}},
                                                 'topology_tree_info': {'224.0.1.40 * True': {'expiration': '00:02:56',
                                                                                              'group': '224.0.1.40',
                                                                                              'is_rpt': True,
                                                                                              'msdp_learned': False,
                                                                                              'outgoing_interface': {'Loopback0': {'up_time': '2d09h'}},
                                                                                              'rp_address': '10.16.2.2',
                                                                                              'rp_bit': False,
                                                                                              'rpf_neighbor': '0.0.0.0',
                                                                                              'source_address': '*',
                                                                                              'up_time': '2d09h'},
                                                                        '224.1.1.1 * True': {'expiration': '00:02:54',
                                                                                             'group': '224.1.1.1',
                                                                                             'is_rpt': True,
                                                                                             'msdp_learned': False,
                                                                                             'outgoing_interface': {'ATM0/0': {'up_time': '00:03:57'}},
                                                                                             'rp_address': '172.16.0.0',
                                                                                             'rp_bit': False,
                                                                                             'rpf_neighbor': '224.0.0.0224.0.0.0',
                                                                                             'source_address': '*',
                                                                                             'up_time': '00:03:57'},
                                                                        '239.1.1.1 * True': {'expiration': 'stopped',
                                                                                             'group': '239.1.1.1',
                                                                                             'is_rpt': True,
                                                                                             'msdp_learned': False,
                                                                                             'rp_address': '10.4.1.1',
                                                                                             'rp_bit': False,
                                                                                             'rpf_neighbor': '0.0.0.0',
                                                                                             'source_address': '*',
                                                                                             'up_time': '00:00:03'},
                                                                        '239.1.1.1 10.1.3.1 False': {'expiration': '00:02:57',
                                                                                                     'group': '239.1.1.1',
                                                                                                     'incoming_interface': 'GigabitEthernet2',
                                                                                                     'is_rpt': False,
                                                                                                     'msdp_learned': False,
                                                                                                     'rp_bit': False,
                                                                                                     'rpf_neighbor': '0.0.0.0',
                                                                                                     'source_address': '10.1.3.1',
                                                                                                     'up_time': '00:00:03'},
                                                                        '239.1.1.1 10.4.1.1 False': {'expiration': '00:02:57',
                                                                                                     'group': '239.1.1.1',
                                                                                                     'incoming_interface': 'Loopback0',
                                                                                                     'is_rpt': False,
                                                                                                     'msdp_learned': False,
                                                                                                     'rp_bit': False,
                                                                                                     'rpf_neighbor': '0.0.0.0',
                                                                                                     'source_address': '10.4.1.1',
                                                                                                     'up_time': '00:00:03'}}},
                                        'ipv6': {'rp': {'bsr': {'2001:3:3:3::3': {'address': '2001:3:3:3::3',
                                                                                  'interval': 60,
                                                                                  'mode': 'SM',
                                                                                  'priority': 5},
                                                                'bsr': {'address': '2001:1:1:1::1',
                                                                        'expires': '00:00:52',
                                                                        'hash_mask_length': 126,
                                                                        'priority': 0,
                                                                        'up_time': '00:00:07'},
                                                                'bsr_candidate': {'address': '2001:1:1:1::1',
                                                                                  'hash_mask_length': 126,
                                                                                  'priority': 0},
                                                                'rp_candidate_next_advertisement': '00:00:48'}},
                                                 'topology_tree_info': {'FF07::1 * True': {'expiration': '00:02:47',
                                                                                           'group': 'FF07::1',
                                                                                           'incoming_interface': 'Tunnel5',
                                                                                           'is_rpt': True,
                                                                                           'msdp_learned': False,
                                                                                           'outgoing_interface': {'POS4/0': {'up_time': '00:04:45'}},
                                                                                           'rp_address': '2001:DB8:6::6',
                                                                                           'rp_bit': False,
                                                                                           'rpf_neighbor': '2001:db8:90:24::6',
                                                                                           'source_address': '*',
                                                                                           'up_time': '00:04:45'},
                                                                        'FF07::1 2001:DB8:999::99 False': {'expiration': '00:01:23',
                                                                                                           'group': 'FF07::1',
                                                                                                           'incoming_interface': 'POS1/0',
                                                                                                           'is_rpt': False,
                                                                                                           'msdp_learned': False,
                                                                                                           'outgoing_interface': {'POS4/0': {'up_time': '00:02:06'}},
                                                                                                           'rp_bit': False,
                                                                                                           'rpf_neighbor': '2001:DB8:999::99',
                                                                                                           'source_address': '2001:DB8:999::99',
                                                                                                           'up_time': '00:02:06'}}}},
                     'interfaces': {'GigabitEthernet0/2/0.100': {'address_family': {'ipv6': {'neighbors': {'FE80::21A:30FF:FE47:6E01': {'bidir_capable': True,
                                                                                                                                        'dr_priority': 1,
                                                                                                                                        'expiration': '00:01:33',
                                                                                                                                        'interface': 'GigabitEthernet0/2/0.100',
                                                                                                                                        'up_time': '3w3d'}}}}},
                                    'GigabitEthernet0/2/0.101': {'address_family': {'ipv6': {'neighbors': {'FE80::21A:30FF:FE47:6E01': {'bidir_capable': True,
                                                                                                                                        'dr_priority': 1,
                                                                                                                                        'expiration': '00:01:24',
                                                                                                                                        'interface': 'GigabitEthernet0/2/0.101',
                                                                                                                                        'up_time': '3w3d'}}}}},
                                    'GigabitEthernet0/2/3.100': {'address_family': {'ipv4': {'neighbors': {'192.168.205.2': {'bidir_capable': True,
                                                                                                                             'dr_priority': 1,
                                                                                                                             'expiration': '00:01:19',
                                                                                                                             'interface': 'GigabitEthernet0/2/3.100',
                                                                                                                             'up_time': '4w4d'}}},
                                                                                    'ipv6': {'neighbors': {'FE80::2D7:8FFF:FECB:8602': {'bidir_capable': True,
                                                                                                                                        'dr_priority': 1,
                                                                                                                                        'expiration': '00:01:25',
                                                                                                                                        'interface': 'GigabitEthernet0/2/3.100',
                                                                                                                                        'up_time': '3w3d'}}}}},
                                    'GigabitEthernet0/2/3.101': {'address_family': {'ipv6': {'neighbors': {'FE80::2D7:8FFF:FECB:8602': {'bidir_capable': True,
                                                                                                                                        'dr_priority': 1,
                                                                                                                                        'expiration': '00:01:42',
                                                                                                                                        'interface': 'GigabitEthernet0/2/3.101',
                                                                                                                                        'up_time': '3w3d'}}}}},
                                    'GigabitEthernet1': {'address_family': {'ipv4': {'address': ['10.1.2.1/24'],
                                                                                     'bfd': {'enable': False},
                                                                                     'bsr_border': False,
                                                                                     'dr_priority': 1,
                                                                                     'hello_interval': 30,
                                                                                     'jp_interval': 60,
                                                                                     'mode': 'sparse-mode',
                                                                                     'neighbor_filter': '7',
                                                                                     'oper_status': 'up',
                                                                                     'sm': {}},
                                                                            'ipv6': {'address': ['FE80::5054:FF:FE2C:6CDF'],
                                                                                     'dr_priority': 1,
                                                                                     'hello_interval': 30}}},
                                    'GigabitEthernet2': {'address_family': {'ipv4': {'address': ['10.1.3.1/24'],
                                                                                     'bfd': {'enable': False},
                                                                                     'bsr_border': False,
                                                                                     'dm': {},
                                                                                     'dr_priority': 1,
                                                                                     'hello_interval': 30,
                                                                                     'jp_interval': 60,
                                                                                     'mode': 'sparse-mode',
                                                                                     'oper_status': 'up'},
                                                                            'ipv6': {'address': ['FE80::5054:FF:FEBE:8787'],
                                                                                     'dr_priority': 1,
                                                                                     'hello_interval': 30}}},
                                    'Loopback0': {'address_family': {'ipv4': {'address': ['10.4.1.1/32'],
                                                                              'bfd': {'enable': False},
                                                                              'bsr_border': False,
                                                                              'dr_priority': 1,
                                                                              'hello_interval': 30,
                                                                              'jp_interval': 60,
                                                                              'mode': 'sparse-mode',
                                                                              'oper_status': 'up',
                                                                              'sm': {}},
                                                                     'ipv6': {'address': ['FE80::21E:F6FF:FEAC:A600'],
                                                                              'dr_priority': 1,
                                                                              'hello_interval': 30}}},
                                    'Null0': {'address_family': {'ipv6': {'address': ['FE80::1'],
                                                                          'dr_priority': 1,
                                                                          'hello_interval': 30}}},
                                    'Port-channel1.100': {'address_family': {'ipv4': {'neighbors': {'192.168.4.1': {'dr_priority': 1,
                                                                                                                    'expiration': '00:01:40',
                                                                                                                    'interface': 'Port-channel1.100',
                                                                                                                    'up_time': '4w4d'}}},
                                                                             'ipv6': {'neighbors': {'FE80::21A:30FF:FE47:6EC0': {'bidir_capable': True,
                                                                                                                                 'dr_priority': 1,
                                                                                                                                 'expiration': '00:01:37',
                                                                                                                                 'interface': 'Port-channel1.100',
                                                                                                                                 'up_time': '3w3d'}}}}},
                                    'Port-channel1.101': {'address_family': {'ipv6': {'neighbors': {'FE80::21A:30FF:FE47:6EC0': {'bidir_capable': True,
                                                                                                                                 'dr_priority': 1,
                                                                                                                                 'expiration': '00:01:38',
                                                                                                                                 'interface': 'Port-channel1.101',
                                                                                                                                 'up_time': '3w3d'}}}}},
                                    'Tunnel0': {'address_family': {'ipv6': {'address': ['FE80::21E:F6FF:FEAC:A600'],
                                                                            'dr_priority': 1,
                                                                            'hello_interval': 30}}},
                                    'Tunnel1': {'address_family': {'ipv6': {'address': ['FE80::21E:F6FF:FEAC:A600'],
                                                                            'dr_priority': 1,
                                                                            'hello_interval': 30}}},
                                    'Tunnel2': {'address_family': {'ipv6': {'dr_priority': 1,
                                                                            'hello_interval': 30}}},
                                    'Tunnel3': {'address_family': {'ipv6': {'dr_priority': 1,
                                                                            'hello_interval': 30}}},
                                    'Tunnel4': {'address_family': {'ipv6': {'dr_priority': 1,
                                                                            'hello_interval': 30}}}}}}}