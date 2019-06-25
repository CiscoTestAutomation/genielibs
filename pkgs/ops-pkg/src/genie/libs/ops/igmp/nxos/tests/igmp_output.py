''' 
Igmp Genie Ops Object Outputs for NXOS.
'''


class IgmpOutput(object):

    ShowIpIgmpInterface = {
        "vrfs": {
            "default": {
                 "groups_count": 2,
                 "interface": {
                      "Ethernet2/2": {
                           "query_max_response_time": 10,
                           "vrf_name": "default",
                           "statistics": {
                                "general": {
                                     "sent": {
                                          "v2_reports": 0,
                                          "v2_queries": 16,
                                          "v2_leaves": 0
                                     },
                                     "received": {
                                          "v2_reports": 0,
                                          "v2_queries": 16,
                                          "v2_leaves": 0
                                     }
                                }
                           },
                           "configured_query_max_response_time": 10,
                           "pim_dr": True,
                           "vrf_id": 1,
                           "querier": "10.1.3.1",
                           "membership_count": 0,
                           "last_member": {
                               "query_count": 2,
                               "mrt": 1,
                           },
                           "startup_query": {
                               "interval": 31,
                               "configured_interval": 31,
                               "count": 2,
                           },
                           "link_status": "up",
                           "subnet": "10.1.3.0/24",
                           "address": "10.1.3.1",
                           "link_local_groups_reporting": False,
                           "unsolicited_report_interval": 10,
                           "enable_refcount": 1,
                           "enable": True,
                           "next_query_sent_in": "00:00:55",
                           "configured_query_interval": 125,
                           "old_membership_count": 0,
                           "group_timeout": 260,
                           "configured_robustness_variable": 2,
                           "vpc_svi": False,
                           "querier_version": 2,
                           "version": 2,
                           "query_interval": 125,
                           "querier_timeout": 255,
                           "immediate_leave": False,
                           "configured_group_timeout": 260,
                           "host_version": 2,
                           "configured_querier_timeout": 255,
                           "robustness_variable": 2,
                           "oper_status": "up"
                      },
                      "Ethernet2/1": {
                           "query_max_response_time": 15,
                           "vrf_name": "default",
                           "statistics": {
                                "errors": {
                                     "router_alert_check": 19,
                                },
                                "general": {
                                     "sent": {
                                          "v2_reports": 0,
                                          "v3_queries": 11,
                                          "v2_leaves": 0,
                                          "v3_reports": 56,
                                          "v2_queries": 5
                                     },
                                     "received": {
                                          "v2_reports": 0,
                                          "v3_queries": 11,
                                          "v2_leaves": 0,
                                          "v3_reports": 56,
                                          "v2_queries": 5
                                     }
                                }
                           },
                           "configured_query_max_response_time": 15,
                           "max_groups": 10,
                           "vrf_id": 1,
                           "querier": "10.1.2.1",
                           "membership_count": 4,
                           "last_member": {
                               "query_count": 5,
                               "mrt": 1,
                           },
                           "startup_query": {
                               "interval": 33,
                               "configured_interval": 31,
                               "count": 5,
                           },
                           "pim_dr": True,
                           "link_status": "up",
                           "subnet": "10.1.2.0/24",
                           "address": "10.1.2.1",
                           "link_local_groups_reporting": False,
                           "unsolicited_report_interval": 10,
                           "enable_refcount": 9,
                           "enable": True,
                           "group_policy": "access-group-filter",
                           "next_query_sent_in": "00:00:47",
                           "configured_query_interval": 133,
                           "old_membership_count": 0,
                           "group_timeout": 680,
                           "configured_robustness_variable": 5,
                           "vpc_svi": False,
                           "querier_version": 3,
                           "available_groups": 10,
                           "version": 3,
                           "query_interval": 133,
                           "querier_timeout": 672,
                           "immediate_leave": True,
                           "configured_group_timeout": 260,
                           "host_version": 3,
                           "configured_querier_timeout": 255,
                           "robustness_variable": 5,
                           "oper_status": "up"
                      }
                 }
            },
            "VRF1": {
                 "groups_count": 2,
                 "interface": {
                      "Ethernet2/4": {
                           "query_max_response_time": 15,
                           "vrf_name": "VRF1",
                           "statistics": {
                                "general": {
                                     "sent": {
                                          "v2_reports": 0,
                                          "v3_queries": 8,
                                          "v2_leaves": 0,
                                          "v3_reports": 44,
                                          "v2_queries": 8
                                     },
                                     "received": {
                                          "v2_reports": 0,
                                          "v3_queries": 8,
                                          "v2_leaves": 0,
                                          "v3_reports": 44,
                                          "v2_queries": 8
                                     }
                                }
                           },
                           "configured_query_max_response_time": 15,
                           "max_groups": 10,
                           "vrf_id": 3,
                           "querier": "10.186.2.1",
                           "membership_count": 4,
                           "last_member": {
                               "query_count": 5,
                               "mrt": 1,
                           },
                           "startup_query": {
                               "interval": 33,
                               "configured_interval": 31,
                               "count": 5,
                           },
                           "pim_dr": True,
                           "link_status": "up",
                           "subnet": "10.186.2.0/24",
                           "address": "10.186.2.1",
                           "link_local_groups_reporting": False,
                           "unsolicited_report_interval": 10,
                           "enable_refcount": 9,
                           "enable": True,
                           "group_policy": "access-group-filter",
                           "next_query_sent_in": "00:00:06",
                           "configured_query_interval": 133,
                           "old_membership_count": 0,
                           "group_timeout": 680,
                           "configured_robustness_variable": 5,
                           "vpc_svi": False,
                           "querier_version": 3,
                           "available_groups": 10,
                           "version": 3,
                           "query_interval": 133,
                           "querier_timeout": 672,
                           "immediate_leave": True,
                           "configured_group_timeout": 260,
                           "host_version": 3,
                           "configured_querier_timeout": 255,
                           "robustness_variable": 5,
                           "oper_status": "up"
                      },
                      "Ethernet2/3": {
                           "query_max_response_time": 10,
                           "vrf_name": "VRF1",
                           "statistics": {
                                "general": {
                                     "sent": {
                                          "v2_reports": 0,
                                          "v2_queries": 16,
                                          "v2_leaves": 0
                                     },
                                     "received": {
                                          "v2_reports": 0,
                                          "v2_queries": 16,
                                          "v2_leaves": 0
                                     }
                                }
                           },
                           "configured_query_max_response_time": 10,
                           "pim_dr": True,
                           "vrf_id": 3,
                           "querier": "10.186.3.1",
                           "membership_count": 0,
                           "last_member": {
                               "query_count": 2,
                               "mrt": 1,
                           },
                           "startup_query": {
                               "interval": 31,
                               "configured_interval": 31,
                               "count": 2,
                           },
                           "link_status": "up",
                           "subnet": "10.186.3.0/24",
                           "address": "10.186.3.1",
                           "link_local_groups_reporting": False,
                           "unsolicited_report_interval": 10,
                           "enable_refcount": 1,
                           "enable": True,
                           "next_query_sent_in": "00:00:47",
                           "configured_query_interval": 125,
                           "old_membership_count": 0,
                           "group_timeout": 260,
                           "configured_robustness_variable": 2,
                           "vpc_svi": False,
                           "querier_version": 2,
                           "version": 2,
                           "query_interval": 125,
                           "querier_timeout": 255,
                           "immediate_leave": False,
                           "configured_group_timeout": 260,
                           "host_version": 2,
                           "configured_querier_timeout": 255,
                           "robustness_variable": 2,
                           "oper_status": "up"
                      }
                 }
            },
            "tenant1": {
                 "groups_count": 0,
            },
            "manegement": {
                 "groups_count": 0,
            }
        }
    }

    ShowIpIgmpGroups = {
        "vrfs": {
            "VRF1": {
                 "interface": {
                      "Ethernet2/4": {
                           "group": {
                                "239.6.6.6": {
                                     "expire": "never",
                                     "type": "S",
                                     "last_reporter": "10.186.2.1",
                                     "up_time": "00:15:27"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "expire": "never",
                                               "type": "S",
                                               "last_reporter": "10.186.2.1",
                                               "up_time": "00:15:27"
                                          }
                                     },
                                },
                                "239.5.5.5": {
                                     "expire": "never",
                                     "type": "S",
                                     "last_reporter": "10.186.2.1",
                                     "up_time": "00:15:27"
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "expire": "never",
                                               "type": "S",
                                               "last_reporter": "10.186.2.1",
                                               "up_time": "00:15:27"
                                          }
                                     },
                                }
                           }
                      }
                 },
                 "total_entries": 4
            },
            "default": {
                 "interface": {
                      "Ethernet2/1": {
                           "group": {
                                "239.6.6.6": {
                                     "expire": "never",
                                     "type": "S",
                                     "last_reporter": "10.1.2.1",
                                     "up_time": "00:20:53"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "expire": "never",
                                               "type": "S",
                                               "last_reporter": "10.1.2.1",
                                               "up_time": "00:20:34"
                                          }
                                     },
                                },
                                "239.5.5.5": {
                                     "expire": "never",
                                     "type": "S",
                                     "last_reporter": "10.1.2.1",
                                     "up_time": "00:21:00"
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "expire": "never",
                                               "type": "S",
                                               "last_reporter": "10.1.2.1",
                                               "up_time": "00:20:42"
                                          }
                                     },
                                }
                           }
                      }
                 },
                 "total_entries": 4
            }
        }

    }

    ShowIpIgmpLocalGroups = {
        "vrfs": {
            "default": {
                 "interface": {
                      "Ethernet2/1": {
                           "join_group": {
                                "239.1.1.1 *": {
                                     "source": "*",
                                     "group": "239.1.1.1"
                                },
                                "239.3.3.3 10.4.1.1": {
                                     "source": "10.4.1.1",
                                     "group": "239.3.3.3"
                                },
                                "239.2.2.2 *": {
                                     "source": "*",
                                     "group": "239.2.2.2"
                                },
                                "239.4.4.4 10.4.1.2": {
                                     "source": "10.4.1.2",
                                     "group": "239.4.4.4"
                                }
                           },
                           "static_group": {
                                "239.5.5.5 *": {
                                     "source": "*",
                                     "group": "239.5.5.5"
                                },
                                "239.8.8.8 10.16.2.2": {
                                     "source": "10.16.2.2",
                                     "group": "239.8.8.8"
                                },
                                "239.6.6.6 *": {
                                     "source": "*",
                                     "group": "239.6.6.6"
                                },
                                "239.7.7.7 10.16.2.1": {
                                     "source": "10.16.2.1",
                                     "group": "239.7.7.7"
                                }
                           },
                           "group": {
                                "239.1.1.1": {
                                     "last_reporter": "00:00:13",
                                     "type": "local"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "last_reporter": "01:06:47",
                                               "type": "static"
                                          }
                                     },
                                },
                                "239.2.2.2": {
                                     "last_reporter": "00:00:18",
                                     "type": "local"
                                },
                                "239.4.4.4": {
                                     "source": {
                                          "10.4.1.2": {
                                               "last_reporter": "00:00:06",
                                               "type": "local"
                                          }
                                     },
                                },
                                "239.6.6.6": {
                                     "last_reporter": "01:06:47",
                                     "type": "static"
                                },
                                "239.5.5.5": {
                                     "last_reporter": "01:06:47",
                                     "type": "static"
                                },
                                "239.3.3.3": {
                                     "source": {
                                          "10.4.1.1": {
                                               "last_reporter": "00:00:11",
                                               "type": "local"
                                          }
                                     },
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "last_reporter": "01:06:47",
                                               "type": "static"
                                          }
                                     },
                                }
                           }
                      }
                 }
            },
            "VRF1": {
                 "interface": {
                      "Ethernet2/4": {
                           "join_group": {
                                "239.1.1.1 *": {
                                     "source": "*",
                                     "group": "239.1.1.1"
                                },
                                "239.3.3.3 10.4.1.1": {
                                     "source": "10.4.1.1",
                                     "group": "239.3.3.3"
                                },
                                "239.2.2.2 *": {
                                     "source": "*",
                                     "group": "239.2.2.2"
                                },
                                "239.4.4.4 10.4.1.2": {
                                     "source": "10.4.1.2",
                                     "group": "239.4.4.4"
                                }
                           },
                           "static_group": {
                                "239.5.5.5 *": {
                                     "source": "*",
                                     "group": "239.5.5.5"
                                },
                                "239.8.8.8 10.16.2.2": {
                                     "source": "10.16.2.2",
                                     "group": "239.8.8.8"
                                },
                                "239.6.6.6 *": {
                                     "source": "*",
                                     "group": "239.6.6.6"
                                },
                                "239.7.7.7 10.16.2.1": {
                                     "source": "10.16.2.1",
                                     "group": "239.7.7.7"
                                }
                           },
                           "group": {
                                "239.1.1.1": {
                                     "last_reporter": "00:00:50",
                                     "type": "local"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "last_reporter": "01:06:47",
                                               "type": "static"
                                          }
                                     },
                                },
                                "239.2.2.2": {
                                     "last_reporter": "00:00:54",
                                     "type": "local"
                                },
                                "239.4.4.4": {
                                     "source": {
                                          "10.4.1.2": {
                                               "last_reporter": "00:00:55",
                                               "type": "local"
                                          }
                                     },
                                },
                                "239.6.6.6": {
                                     "last_reporter": "01:06:47",
                                     "type": "static"
                                },
                                "239.5.5.5": {
                                     "last_reporter": "01:06:47",
                                     "type": "static"
                                },
                                "239.3.3.3": {
                                     "source": {
                                          "10.4.1.1": {
                                               "last_reporter": "00:01:01",
                                               "type": "local"
                                          }
                                     },
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "last_reporter": "01:06:47",
                                               "type": "static"
                                          }
                                     },
                                }}}}}}
    }


    Igmp_info = {
        "vrfs": {
            "VRF1": {
                 "interfaces": {
                      "Ethernet2/4": {
                           "querier": "10.186.2.1",
                           "group_policy": "access-group-filter",
                           "robustness_variable": 5,
                           "join_group": {
                                "239.3.3.3 10.4.1.1": {
                                     "source": "10.4.1.1",
                                     "group": "239.3.3.3"
                                },
                                "239.4.4.4 10.4.1.2": {
                                     "source": "10.4.1.2",
                                     "group": "239.4.4.4"
                                },
                                "239.1.1.1 *": {
                                     "source": "*",
                                     "group": "239.1.1.1"
                                },
                                "239.2.2.2 *": {
                                     "source": "*",
                                     "group": "239.2.2.2"
                                }
                           },
                           "immediate_leave": True,
                           "max_groups": 10,
                           "enable": True,
                           "version": 3,
                           "oper_status": "up",
                           "group": {
                                "239.5.5.5": {
                                     "up_time": "00:15:27",
                                     "last_reporter": "10.186.2.1",
                                     "expire": "never"
                                },
                                "239.6.6.6": {
                                     "up_time": "00:15:27",
                                     "last_reporter": "10.186.2.1",
                                     "expire": "never"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "last_reporter": "10.186.2.1",
                                               "up_time": "00:15:27",
                                               "expire": "never"
                                          }
                                     }
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "last_reporter": "10.186.2.1",
                                               "up_time": "00:15:27",
                                               "expire": "never"
                                          }
                                     }
                                }
                           },
                           "static_group": {
                                "239.7.7.7 10.16.2.1": {
                                     "source": "10.16.2.1",
                                     "group": "239.7.7.7"
                                },
                                "239.5.5.5 *": {
                                     "source": "*",
                                     "group": "239.5.5.5"
                                },
                                "239.6.6.6 *": {
                                     "source": "*",
                                     "group": "239.6.6.6"
                                },
                                "239.8.8.8 10.16.2.2": {
                                     "source": "10.16.2.2",
                                     "group": "239.8.8.8"
                                }
                           },
                           "query_max_response_time": 15,
                           "query_interval": 133
                      },
                      "Ethernet2/3": {
                           "querier": "10.186.3.1",
                           "immediate_leave": False,
                           "enable": True,
                           "version": 2,
                           "oper_status": "up",
                           "query_max_response_time": 10,
                           "robustness_variable": 2,
                           "query_interval": 125
                      }
                 },
                 "groups_count": 2
            },
            "manegement": {
                 "groups_count": 0
            },
            "tenant1": {
                 "groups_count": 0
            },
            "default": {
                 "interfaces": {
                      "Ethernet2/2": {
                           "querier": "10.1.3.1",
                           "immediate_leave": False,
                           "enable": True,
                           "version": 2,
                           "oper_status": "up",
                           "query_max_response_time": 10,
                           "robustness_variable": 2,
                           "query_interval": 125
                      },
                      "Ethernet2/1": {
                           "querier": "10.1.2.1",
                           "group_policy": "access-group-filter",
                           "robustness_variable": 5,
                           "join_group": {
                                "239.3.3.3 10.4.1.1": {
                                     "source": "10.4.1.1",
                                     "group": "239.3.3.3"
                                },
                                "239.4.4.4 10.4.1.2": {
                                     "source": "10.4.1.2",
                                     "group": "239.4.4.4"
                                },
                                "239.1.1.1 *": {
                                     "source": "*",
                                     "group": "239.1.1.1"
                                },
                                "239.2.2.2 *": {
                                     "source": "*",
                                     "group": "239.2.2.2"
                                }
                           },
                           "immediate_leave": True,
                           "max_groups": 10,
                           "enable": True,
                           "version": 3,
                           "oper_status": "up",
                           "group": {
                                "239.5.5.5": {
                                     "up_time": "00:21:00",
                                     "last_reporter": "10.1.2.1",
                                     "expire": "never"
                                },
                                "239.6.6.6": {
                                     "up_time": "00:20:53",
                                     "last_reporter": "10.1.2.1",
                                     "expire": "never"
                                },
                                "239.8.8.8": {
                                     "source": {
                                          "10.16.2.2": {
                                               "last_reporter": "10.1.2.1",
                                               "up_time": "00:20:34",
                                               "expire": "never"
                                          }
                                     }
                                },
                                "239.7.7.7": {
                                     "source": {
                                          "10.16.2.1": {
                                               "last_reporter": "10.1.2.1",
                                               "up_time": "00:20:42",
                                               "expire": "never"
                                          }
                                     }
                                }
                           },
                           "static_group": {
                                "239.7.7.7 10.16.2.1": {
                                     "source": "10.16.2.1",
                                     "group": "239.7.7.7"
                                },
                                "239.5.5.5 *": {
                                     "source": "*",
                                     "group": "239.5.5.5"
                                },
                                "239.6.6.6 *": {
                                     "source": "*",
                                     "group": "239.6.6.6"
                                },
                                "239.8.8.8 10.16.2.2": {
                                     "source": "10.16.2.2",
                                     "group": "239.8.8.8"
                                }
                           },
                           "query_max_response_time": 15,
                           "query_interval": 133
                      }
                 },
                 "groups_count": 2
            }
        }
    }
