''' 
Vrf Genie Ops Object Outputs for IOSXR.
'''


class VrfOutput(object):
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
        },
        "VRF2": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                "ipv6 unicast": {
                    "route_target": {
                        "200:2": {
                            "rt_type": "both",
                            "route_target": "200:2"
                        }
                    }
                },
                "ipv4 unicast": {
                    "route_target": {
                        "200:2": {
                            "rt_type": "both",
                            "route_target": "200:2"
                        }
                    }
                }
            },
            "route_distinguisher": "200:2",
            "interfaces": [
                "GigabitEthernet0/0/0/2"
            ]}
    }
    ShowVrfAllDetailCustom = {
        "VRF2": {
            "description": "not set",
            "vrf_mode": "regular",
            "address_family": {
                "ipv6 unicast": {
                    "route_target": {
                        "200:2": {
                            "rt_type": "both",
                            "route_target": "200:2"
                        }
                    }
                },
                "ipv4 unicast": {
                    "route_target": {
                        "200:2": {
                            "rt_type": "both",
                            "route_target": "200:2"
                        }
                    }
                }
            },
            "route_distinguisher": "200:2",
            "interfaces": [
                "GigabitEthernet0/0/0/2"
            ]}
    }

    VrfCustomInfo = {
        'vrfs': {
            "VRF2": {
                "route_distinguisher": "200:2",
                "description": "not set",
                "address_family": {
                    "ipv4 unicast": {
                        "route_targets": {
                            "200:2": {
                                "rt_type": "both",
                                "route_target": "200:2"
                            }
                        }
                    },
                    "ipv6 unicast": {
                        "route_targets": {
                            "200:2": {
                                "rt_type": "both",
                                "route_target": "200:2"
                            }
                        }
                    }
                }
            },
        }
    }
    showVrfDetail_all='''
        Mon Sep 18 09:36:51.507 PDT

        VRF VRF1; RD 200:1; VPN ID not set
        VRF mode: Regular
        Description not set
        Interfaces:
          GigabitEthernet0/0/0/1
        Address family IPV4 Unicast
          Import VPN route-target communities:
            RT:200:1
            RT:200:2
            RT:300:1
            RT:400:1
          Export VPN route-target communities:
            RT:200:1
          No import route policy
          No export route policy
        Address family IPV6 Unicast
          Import VPN route-target communities:
            RT:200:1
            RT:200:2
            RT:300:1
            RT:400:1
          Export VPN route-target communities:
            RT:200:1
          No import route policy
          No export route policy

        VRF VRF2; RD 200:2; VPN ID not set
        VRF mode: Regular
        Description not set
        Interfaces:
          GigabitEthernet0/0/0/2
        Address family IPV4 Unicast
          Import VPN route-target communities:
            RT:200:2
          Export VPN route-target communities:
            RT:200:2
          No import route policy
          No export route policy
        Address family IPV6 Unicast
          Import VPN route-target communities:
            RT:200:2
          Export VPN route-target communities:
            RT:200:2
          No import route policy
          No export route policy
    '''
    showVrfDetail_vrf2 = '''
VRF VRF2; RD 200:2; VPN ID not set
        VRF mode: Regular
        Description not set
        Interfaces:
          GigabitEthernet0/0/0/2
        Address family IPV4 Unicast
          Import VPN route-target communities:
            RT:200:2
          Export VPN route-target communities:
            RT:200:2
          No import route policy
          No export route policy
        Address family IPV6 Unicast
          Import VPN route-target communities:
            RT:200:2
          Export VPN route-target communities:
            RT:200:2
          No import route policy
          No export route policy
    '''

    VrfInfo = {
    "vrfs": {
        "VRF2": {
            "route_distinguisher": "200:2",
            "description": "not set",
            "address_family": {
                "ipv6 unicast": {
                    "route_targets": {
                        "200:2": {"route_target": "200:2", "rt_type": "both"}
                    }
                },
                "ipv4 unicast": {
                    "route_targets": {
                        "200:2": {"route_target": "200:2", "rt_type": "both"}
                    }
                },
            },
        },
        "VRF1": {
            "route_distinguisher": "200:1",
            "description": "not set",
            "address_family": {
                "ipv6 unicast": {
                    "route_targets": {
                        "200:1": {"route_target": "200:1", "rt_type": "both"},
                        "200:2": {"route_target": "200:2", "rt_type": "import"},
                        "300:1": {"route_target": "300:1", "rt_type": "import"},
                        "400:1": {"route_target": "400:1", "rt_type": "import"},
                    }
                },
                "ipv4 unicast": {
                    "route_targets": {
                        "200:1": {"route_target": "200:1", "rt_type": "both"},
                        "200:2": {"route_target": "200:2", "rt_type": "import"},
                        "300:1": {"route_target": "300:1", "rt_type": "import"},
                        "400:1": {"route_target": "400:1", "rt_type": "import"},
                    }
                },
            },
        },
    }
}
