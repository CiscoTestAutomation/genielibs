'''IGMP Genie Ops Object Outputs for IOSXR.'''


class IgmpOutput(object):

    ShowVrfAllDetail = {
        "VRF1": {
            "address_family": {
                "ipv4 unicast": {},
                "ipv6 unicast": {}
            },
            "description": "not set",
            "interfaces": [
                "Loopback300"
            ],
            "route_distinguisher": "65000:2",
            "vrf_mode": "regular"
        },
        "management": {
            "address_family": {
                "ipv4 unicast": {},
                "ipv6 unicast": {}
            },
            "description": "not set",
            "interfaces": [],
            "vrf_mode": "regular"
        }
    }

    ShowIgmpInterface = {
        "vrf": {
            "default": {
                "interfaces": {
                    "Loopback0": {
                        "igmp_activity": {
                            "joins": 6,
                            "leaves": 0
                        },
                        "igmp_max_query_response_time": 10,
                        "igmp_querier_timeout": 125,
                        "igmp_query_interval": 60,
                        "igmp_querying_router": "2.2.2.2",
                        "igmp_querying_router_info": "this system",
                        "igmp_state": "enabled",
                        "igmp_version": 3,
                        "interface_status": "up",
                        "ip_address": "2.2.2.2/32",
                        "last_member_query_response_interval": 1,
                        "line_protocol": "up",
                        "oper_status": "up",
                        "time_elapsed_since_last_query_sent": "00:00:44",
                        "time_elapsed_since_last_report_received": "00:00:34",
                        "time_elapsed_since_router_enabled": "06:15:55"
                    }
                }
            }
        }
    }
    
    ShowIgmpInterface_VRF1 = {
        "vrf": {
            "VRF1": {
                "interfaces": {
                    "Loopback300": {
                        "igmp_activity": {
                            "joins": 4,
                            "leaves": 0
                        },
                        "igmp_max_query_response_time": 10,
                        "igmp_querier_timeout": 125,
                        "igmp_query_interval": 60,
                        "igmp_querying_router": "2.2.2.2",
                        "igmp_querying_router_info": "this system",
                        "igmp_state": "enabled",
                        "igmp_version": 3,
                        "interface_status": "up",
                        "ip_address": "2.2.2.2/32",
                        "last_member_query_response_interval": 1,
                        "line_protocol": "up",
                        "oper_status": "up",
                        "time_elapsed_since_last_query_sent": "00:00:51",
                        "time_elapsed_since_last_report_received": "00:00:42",
                        "time_elapsed_since_router_enabled": "07:29:00"
                    }
                }
            }
        }
    }

    ShowIgmpSummary = {
        "vrf": {
            "default": {
                "disabled_interfaces": 0,
                "enabled_interfaces": 1,
                "interfaces": {
                    "Loopback0": {
                        "max_groups": 25000,
                        "number_groups": 6
                    }
                },
                "maximum_number_of_groups_for_vrf": 50000,
                "mte_tuple_count": 0,
                "no_of_group_x_interface": 5,
                "robustness_value": 2,
                "supported_interfaces": 1,
                "unsupported_interfaces": 0
            }
        }
    }
    
    ShowIgmpSummary_VRF1 = {
        "vrf": {
            "VRF1": {
                "disabled_interfaces": 0,
                "enabled_interfaces": 1,
                "interfaces": {
                    "Loopback300": {
                        "max_groups": 25000,
                        "number_groups": 4
                    }
                },
                "maximum_number_of_groups_for_vrf": 50000,
                "mte_tuple_count": 0,
                "no_of_group_x_interface": 3,
                "robustness_value": 2,
                "supported_interfaces": 1,
                "unsupported_interfaces": 0
            }
        }
    }

    ShowIgmpGroupsDetail = {
        "vrf": {
            "default": {
                "interfaces": {
                    "Loopback0": {
                        "group": {
                            "224.0.0.13": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:16"
                            },
                            "224.0.0.2": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:16"
                            },
                            "224.0.0.22": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:16"
                            },
                            "224.0.0.9": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:01"
                            },
                            "224.0.1.39": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:07"
                            },
                            "224.0.1.40": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "06:22:06"
                            }
                        }
                    }
                }
            }
        }
    }
    
    ShowIgmpGroupsDetail_VRF1 = {
        "vrf": {
            "VRF1": {
                "interfaces": {
                    "Loopback300": {
                        "group": {
                            "224.0.0.13": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "07:36:54"
                            },
                            "224.0.0.2": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "07:36:54"
                            },
                            "224.0.0.22": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "07:36:54"
                            },
                            "224.0.0.9": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "07:36:39"
                            }
                        }
                    }
                }
            }
        }
    }

    ShowIgmpGroupsDetail_VRF1_source_list = {
        "vrf": {
            "VRF1": {
                "interfaces": {
                    "Loopback300": {
                        "group": {
                            "224.0.0.13": {
                                "host_mode": "exclude",
                                "last_reporter": "2.2.2.2",
                                "router_mode": "EXCLUDE",
                                "router_mode_expires": "never",
                                "suppress": 0,
                                "up_time": "07:36:54",
                                "source": {
                                    "192.168.1.18": {
                                        "up_time": "00:04:55",
                                        "expire": "00:01:28",
                                        "forward": "Yes",
                                        "flags": "Remote"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    IgmpOpsOutput = {
        "vrfs": {
            "VRF1": {
                "max_groups": 50000,
                "groups_count": 3,
                "interfaces": {
                    "Loopback300": {
                        "enable": True,
                        "oper_status": "up",
                        "last_member_query_interval" :1,
                        "query_max_response_time": 10,
                        "query_interval": 60,
                        "version": 3,
                        "querier": "2.2.2.2",
                        "max_groups": 25000,
                        "group": {
                            "224.0.0.9": {
                                "up_time": "07:36:39",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.22": {
                                "up_time": "07:36:54",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.2": {
                                "up_time": "07:36:54",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.13": {
                                "up_time": "07:36:54",
                                "last_reporter": "2.2.2.2",
                            }
                        }
                    }
                }
            },
            "default": {
                "max_groups": 50000,
                "groups_count": 5,
                "interfaces": {
                    "Loopback0": {
                        "enable": True,
                        "oper_status": "up",
                        "last_member_query_interval": 1,
                        "query_max_response_time": 10,
                        "query_interval": 60,
                        "version": 3,
                        "querier": "2.2.2.2",
                        "max_groups": 25000,
                        "group": {
                            "224.0.1.40": {
                                "up_time": "06:22:06",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.1.39": {
                                "up_time": "06:22:07",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.9": {
                                "up_time": "06:22:01",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.22": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.2": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.13": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            }
                        }
                    }
                }
            }
        }
    }
 
    IgmpOpsOutputSourceList = {
        "vrfs": {
            "VRF1": {
                "max_groups": 50000,
                "groups_count": 3,
                "interfaces": {
                    "Loopback300": {
                        "enable": True,
                        "oper_status": "up",
                        "last_member_query_interval" :1,
                        "query_max_response_time": 10,
                        "query_interval": 60,
                        "version": 3,
                        "querier": "2.2.2.2",
                        "max_groups": 25000,
                        "group": {
                            "224.0.0.13": {
                                "up_time": "07:36:54",
                                "last_reporter": "2.2.2.2",
                                "source": {
                                    "192.168.1.18": {
                                        "up_time": "00:04:55",
                                        "expire": "00:01:28",
                                        "forward": "Yes",
                                        "flags": "Remote"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "default": {
                "max_groups": 50000,
                "groups_count": 5,
                "interfaces": {
                    "Loopback0": {
                        "enable": True,
                        "oper_status": "up",
                        "last_member_query_interval": 1,
                        "query_max_response_time": 10,
                        "query_interval": 60,
                        "version": 3,
                        "querier": "2.2.2.2",
                        "max_groups": 25000,
                        "group": {
                            "224.0.1.40": {
                                "up_time": "06:22:06",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.1.39": {
                                "up_time": "06:22:07",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.9": {
                                "up_time": "06:22:01",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.22": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.2": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            },
                            "224.0.0.13": {
                                "up_time": "06:22:16",
                                "last_reporter": "2.2.2.2",
                            }
                        }
                    }
                }
            }
        }
    }