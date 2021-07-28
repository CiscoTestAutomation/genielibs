''' 
Vrf Genie Ops Object Outputs for IOSXE.
'''


class VrfOutput(object):


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
        },
        "VRF2": {
            "interfaces": [
                "GigabitEthernet0/1"
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

    ShowVrfDetailCustom = {
  "vrfs": {
    "VRF2": {
      "route_distinguisher": "6000:1",
      "address_family": {
        "ipv6 unicast": {
          "route_targets": {
            "100:1": {
              "route_target": "100:1",
              "rt_type": "export"
            },
            "300:1": {
              "route_target": "300:1",
              "rt_type": "export"
            },
            "200:1": {
              "route_target": "200:1",
              "rt_type": "import"
            },
            "400:1": {
              "route_target": "400:1",
              "rt_type": "import"
            }
          },
          "table_id": "0x1E000001",
          "export_to_global": {
            "export_to_global_map": "export_to_global_map"
          },
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
          }
        },
        "ipv4 unicast": {
          "route_targets": {
            "100:1": {
              "route_target": "100:1",
              "rt_type": "both"
            },
            "200:1": {
              "route_target": "200:1",
              "rt_type": "both"
            }
          },
          "import_from_global": {
            "import_from_global_map": "import_from_global_map"
          },
          "table_id": "0x1",
          "export_to_global": {
            "export_to_global_map": "export_to_global_map"
          },
          "routing_table_limit": {
            "routing_table_limit_action": {
              "enable_alert_limit_number": {
                "alert_limit_number": 10000
              }
            }
          }
        }
      }
    }
  }
}

    ShowVrfDetailCustom1 = {
    "vrfs": {
        "Mgmt-vrf": {
            "address_family": {
                "ipv4 unicast": {
                    "flags": "0x0",
                    "table_id": "0x1",
                    "vrf_label": {
                        "allocation_mode": "per-prefix"
                    }
                }
            },
            "cli_format": "Old",
            "description": "OOB Mgmt",
            "flags": "0x8",
            "interface": {
                "GigabitEthernet1": {
                    "vrf": "Mgmt-vrf"
                }
            },
            "interfaces": [
                "GigabitEthernet1"
            ],
            "support_af": "IPv4 only",
            "vrf_id": 1
        }
    }
    }

    VrfInfo = {
    "vrfs": {
        "VRF2": {
            "route_distinguisher": "6000:1",
            "address_family": {
                "ipv6 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "export"},
                        "300:1": {"route_target": "300:1", "rt_type": "export"},
                        "200:1": {"route_target": "200:1", "rt_type": "import"},
                        "400:1": {"route_target": "400:1", "rt_type": "import"},
                    },
                    "table_id": "0x1E000001",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_percent": {"alert_percent_value": 70},
                            "enable_alert_limit_number": {"alert_limit_number": 7000},
                        },
                        "routing_table_limit_number": 10000,
                    },
                },
                "ipv4 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "both"},
                        "200:1": {"route_target": "200:1", "rt_type": "both"},
                    },
                    "import_from_global": {
                        "import_from_global_map": "import_from_global_map"
                    },
                    "table_id": "0x1",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_limit_number": {"alert_limit_number": 10000}
                        }
                    },
                },
            },
        },
        "VRF1": {
            "route_distinguisher": "100:1",
            "address_family": {
                "ipv6 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "export"},
                        "300:1": {"route_target": "300:1", "rt_type": "export"},
                        "200:1": {"route_target": "200:1", "rt_type": "import"},
                        "400:1": {"route_target": "400:1", "rt_type": "import"},
                    },
                    "table_id": "0x1E000001",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_percent": {"alert_percent_value": 70},
                            "enable_alert_limit_number": {"alert_limit_number": 7000},
                        },
                        "routing_table_limit_number": 10000,
                    },
                },
                "ipv4 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "both"},
                        "200:1": {"route_target": "200:1", "rt_type": "both"},
                    },
                    "import_from_global": {
                        "import_from_global_map": "import_from_global_map"
                    },
                    "table_id": "0x1",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_limit_number": {"alert_limit_number": 10000}
                        }
                    },
                },
            },
        },
        "Mgmt-vrf": {
            "address_family": {
                "ipv6 unicast": {"table_id": "0x1E000001"},
                "ipv4 unicast": {"table_id": "0x1"},
            }
        },
    }
}

    showVrfDetail_all = '''
        VRF VRF1 (VRF Id = 1); default RD 100:1; default VPNID <not set>
          New CLI format, supports multiple address-families
          Flags: 0x180C
            Interfaces:
                Gi0/0
        Address family ipv4 unicast (Table ID = 0x1):
          Flags: 0x2100
          Export VPN route-target communities
            RT:100:1                 RT:200:1                
          Import VPN route-target communities
            RT:100:1                 RT:200:1                
          Import route-map for ipv4 unicast: import_from_global_map (prefix limit: 1000)
          Global export route-map for ipv4 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route warning limit 10000, current count 0
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 unicast (Table ID = 0x1E000001):
          Flags: 0x100
          Export VPN route-target communities
            RT:100:1                 RT:300:1                
          Import VPN route-target communities
            RT:200:1                 RT:400:1                
          No import route-map
          Global export route-map for ipv6 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route limit 10000, warning limit 70% (7000), current count 1
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv4 multicast not active

        VRF VRF2 (VRF Id = 3); default RD 6000:1; default VPNID <not set>
          New CLI format, supports multiple address-families
          Flags: 0x180C
            Interfaces:
                Gi0/0
        Address family ipv4 unicast (Table ID = 0x1):
          Flags: 0x2100
          Export VPN route-target communities
            RT:100:1                 RT:200:1                
          Import VPN route-target communities
            RT:100:1                 RT:200:1                
          Import route-map for ipv4 unicast: import_from_global_map (prefix limit: 1000)
          Global export route-map for ipv4 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route warning limit 10000, current count 0
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 unicast (Table ID = 0x1E000001):
          Flags: 0x100
          Export VPN route-target communities
            RT:100:1                 RT:300:1                
          Import VPN route-target communities
            RT:200:1                 RT:400:1                
          No import route-map
          Global export route-map for ipv6 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route limit 10000, warning limit 70% (7000), current count 1
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv4 multicast not active

        VRF Mgmt-vrf (VRF Id = 1); default RD <not set>; default VPNID <not set>
          New CLI format, supports multiple address-families
          Flags: 0x1808
          Interfaces:
            Gi0/0                   
        Address family ipv4 unicast (Table ID = 0x1):
          Flags: 0x0
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No global export route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 unicast (Table ID = 0x1E000001):
          Flags: 0x0
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No global export route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv4 multicast not active
        Address family ipv6 multicast not active
    '''

    showVrfDetail_vrf2 = '''
    VRF VRF2 (VRF Id = 3); default RD 6000:1; default VPNID <not set>
          New CLI format, supports multiple address-families
          Flags: 0x180C
            Interfaces:
                Gi0/0
        Address family ipv4 unicast (Table ID = 0x1):
          Flags: 0x2100
          Export VPN route-target communities
            RT:100:1                 RT:200:1                
          Import VPN route-target communities
            RT:100:1                 RT:200:1                
          Import route-map for ipv4 unicast: import_from_global_map (prefix limit: 1000)
          Global export route-map for ipv4 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route warning limit 10000, current count 0
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 unicast (Table ID = 0x1E000001):
          Flags: 0x100
          Export VPN route-target communities
            RT:100:1                 RT:300:1                
          Import VPN route-target communities
            RT:200:1                 RT:400:1                
          No import route-map
          Global export route-map for ipv6 unicast: export_to_global_map (prefix limit: 1000)
          No export route-map
          Route limit 10000, warning limit 70% (7000), current count 1
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv4 multicast not active
        '''
    ShowVrfDetail_Mgmt = '''
    VRF Mgmt-vrf (VRF Id = 1); default RD <not set>; default VPNID <not set>
  Description: OOB Mgmt
  Old CLI format, supports IPv4 only
  Flags: 0x8
  Interfaces:
    Gi1                     
Address family ipv4 unicast (Table ID = 0x1):
  Flags: 0x0
  No Export VPN route-target communities
  No Import VPN route-target communities
  No import route-map
  No global export route-map
  No export route-map
  VRF label distribution protocol: not configured
  VRF label allocation mode: per-prefix
Address family ipv6 unicast not active
Address family ipv4 multicast not active
Address family ipv6 multicast not active
    '''
    VrfCustomInfo = {
    "vrfs": {
        "VRF2": {
            "route_distinguisher": "6000:1",
            "address_family": {
                "ipv6 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "export"},
                        "300:1": {"route_target": "300:1", "rt_type": "export"},
                        "200:1": {"route_target": "200:1", "rt_type": "import"},
                        "400:1": {"route_target": "400:1", "rt_type": "import"},
                    },
                    "table_id": "0x1E000001",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_percent": {"alert_percent_value": 70},
                            "enable_alert_limit_number": {"alert_limit_number": 7000},
                        },
                        "routing_table_limit_number": 10000,
                    },
                },
                "ipv4 unicast": {
                    "route_targets": {
                        "100:1": {"route_target": "100:1", "rt_type": "both"},
                        "200:1": {"route_target": "200:1", "rt_type": "both"},
                    },
                    "import_from_global": {
                        "import_from_global_map": "import_from_global_map"
                    },
                    "table_id": "0x1",
                    "export_to_global": {
                        "export_to_global_map": "export_to_global_map"
                    },
                    "routing_table_limit": {
                        "routing_table_limit_action": {
                            "enable_alert_limit_number": {"alert_limit_number": 10000}
                        }
                    },
                },
            },
        }
    }
}

    VrfCustomInfo1 = {
    "vrfs": {
        "Mgmt-vrf": {
            "description": "OOB Mgmt",
            "address_family": {"ipv4 unicast": {"table_id": "0x1"}},
        }
    }
}
