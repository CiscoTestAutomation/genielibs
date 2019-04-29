''' 
Vrf Genie Ops Object Outputs for IOSXR.
'''


class VrfOutput(object):

    vrfInfo = {
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


    vrfOutput = {
        "vrfs": {
            "VRF2": {
                "route_distinguisher": "200:2",
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
            "VRF1": {
                "route_distinguisher": "200:1",
                "address_family": {
                    "ipv4 unicast": {
                        "route_targets": {
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
                    "ipv6 unicast": {
                        "route_targets": {
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
                }
            }
        }
    }