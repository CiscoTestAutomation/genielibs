''' 
Mld Genie Ops Object Outputs for NXOS.
'''


class MldOutput(object):

    ShowIpv6MldInterface = {
         "vrfs": {
            "VRF1": {
                 "interface": {
                      "Ethernet2/2": {
                           "query_max_response_time": 16,
                           "querier": "fe80::5054:ff:fed7:c01f",
                           "group_policy": "test",
                           "group_timeout": 2578,
                           "enable_refcount": 4,
                           "version": 2,
                           "link_status": "up",
                           "immediate_leave": True,
                           "startup_query": {
                                "interval": 91,
                                "configured_interval": 31,
                                "count": 7
                           },
                           "last_member": {
                                "query_count": 7,
                                "mrt": 1
                           },
                           "robustness_variable": 7,
                           "oper_status": "up",
                           "host_version": 2,
                           "available_groups": 6400,
                           "membership_count": 2,
                           "query_interval": 366,
                           "configured_robustness_variable": 7,
                           "statistics": {
                                "sent": {
                                     "v1_queries": 0,
                                     "v2_reports": 102,
                                     "v1_leaves": 0,
                                     "v1_reports": 0,
                                     "v2_queries": 82
                                },
                                "received": {
                                     "v1_queries": 0,
                                     "v2_reports": 416,
                                     "v1_leaves": 0,
                                     "v1_reports": 0,
                                     "v2_queries": 82
                                }
                           },
                           "configured_querier_timeout": 255,
                           "link_local_groups_reporting": False,
                           "max_groups": 6400,
                           "enable": True,
                           "next_query_sent_in": "00:05:18",
                           "querier_timeout": 2570,
                           "ipv6": {
                                "2001:db8:8404:751c::1/64": {
                                     "ip": "2001:db8:8404:751c::1",
                                     "prefix_length": "64",
                                     "status": "valid"
                                }
                           },
                           "configured_query_max_response_time": 16,
                           "link_local": {
                                "ipv6_address": "fe80::5054:ff:fed7:c01f",
                                "address": "fe80::5054:ff:fed7:c01f",
                                "status": "valid"
                           },
                           "unsolicited_report_interval": 1,
                           "querier_version": 2,
                           "configured_query_interval": 366,
                           "configured_group_timeout": 260
                      }
                 }
            },
            "default": {
                 "interface": {
                      "Ethernet2/1": {
                           "query_max_response_time": 16,
                           "querier": "fe80::5054:ff:fed7:c01f",
                           "group_policy": "test",
                           "group_timeout": 2578,
                           "enable_refcount": 5,
                           "version": 2,
                           "link_status": "up",
                           "immediate_leave": True,
                           "startup_query": {
                                "interval": 91,
                                "configured_interval": 31,
                                "count": 7
                           },
                           "last_member": {
                                "query_count": 7,
                                "mrt": 1
                           },
                           "robustness_variable": 7,
                           "oper_status": "up",
                           "host_version": 2,
                           "available_groups": 6400,
                           "membership_count": 2,
                           "query_interval": 366,
                           "configured_robustness_variable": 7,
                           "statistics": {
                                "sent": {
                                     "v1_queries": 0,
                                     "v2_reports": 191,
                                     "v1_leaves": 0,
                                     "v1_reports": 0,
                                     "v2_queries": 792
                                },
                                "received": {
                                     "v1_queries": 0,
                                     "v2_reports": 1775,
                                     "v1_leaves": 0,
                                     "v1_reports": 0,
                                     "v2_queries": 792
                                }
                           },
                           "configured_querier_timeout": 255,
                           "link_local_groups_reporting": False,
                           "max_groups": 6400,
                           "enable": True,
                           "next_query_sent_in": "00:03:01",
                           "querier_timeout": 2570,
                           "ipv6": {
                                "2001:db8:8404:907f::1/64": {
                                     "ip": "2001:db8:8404:907f::1",
                                     "prefix_length": "64",
                                     "status": "valid"
                                }
                           },
                           "configured_query_max_response_time": 16,
                           "link_local": {
                                "ipv6_address": "fe80::5054:ff:fed7:c01f",
                                "address": "fe80::5054:ff:fed7:c01f",
                                "status": "valid"
                           },
                           "unsolicited_report_interval": 1,
                           "querier_version": 2,
                           "configured_query_interval": 366,
                           "configured_group_timeout": 260
                      }
                 }
            }
       }
    }

    ShowIpv6MldGroups = {
        "vrfs": {
            "default": {
                 "groups_count": 2,
                 "interface": {
                      "Ethernet2/1": {
                           "group": {
                                "ff30::2": {
                                     "source": {
                                          "2001:db8:0:abcd::2": {
                                               "last_reporter": "2001:db8:8404:907f::1",
                                               "expire": "never",
                                               "type": "static",
                                               "up_time": "00:26:28"
                                          }
                                     }
                                },
                                "fffe::2": {
                                     "last_reporter": "2001:db8:8404:907f::1",
                                     "expire": "never",
                                     "type": "static",
                                     "up_time": "00:26:05"
                                }
                           }
                      }
                 }
            },
            "VRF1": {
                 "groups_count": 2,
                 "interface": {
                      "Ethernet2/2": {
                           "group": {
                                "ff30::2": {
                                     "source": {
                                          "2001:db8:0:abcd::2": {
                                               "last_reporter": "2001:db8:8404:751c::1",
                                               "expire": "never",
                                               "type": "static",
                                               "up_time": "00:25:49"
                                          }
                                     }
                                },
                                "fffe::2": {
                                     "last_reporter": "2001:db8:8404:751c::1",
                                     "expire": "never",
                                     "type": "static",
                                     "up_time": "00:25:49"
                                }
                           }
                      }
                 }
            }
        }
    }

    ShowIpv6MldLocalGroups = {
        "vrfs": {
            "VRF1": {
                 "interface": {
                      "Ethernet2/2": {
                           "static_group": {
                                "fffe::2 *": {
                                     "group": "fffe::2",
                                     "source": "*"
                                },
                                "ff30::2 2001:db8:0:abcd::2": {
                                     "group": "ff30::2",
                                     "source": "2001:db8:0:abcd::2"
                                }
                           },
                           "group": {
                                "ff30::2": {
                                     "source": {
                                          "2001:db8:0:abcd::2": {
                                               "last_reported": "1d07h",
                                               "type": "static"
                                          }
                                     }
                                },
                                "fffe::2": {
                                     "last_reported": "1d07h",
                                     "type": "static"
                                },
                                "fffe::1": {
                                     "last_reported": "00:01:04",
                                     "type": "local"
                                },
                                "ff30::1": {
                                     "source": {
                                          "2001:db8:0:abcd::1": {
                                               "last_reported": "00:01:01",
                                               "type": "local"
                                          }
                                     }
                                }
                           },
                           "join_group": {
                                "ff30::1 2001:db8:0:abcd::1": {
                                     "group": "ff30::1",
                                     "source": "2001:db8:0:abcd::1"
                                },
                                "fffe::1 *": {
                                     "group": "fffe::1",
                                     "source": "*"
                                }
                           }
                      }
                 }
            },
            "default": {
                 "interface": {
                      "Ethernet2/1": {
                           "static_group": {
                                "fffe::2 *": {
                                     "group": "fffe::2",
                                     "source": "*"
                                },
                                "ff30::2 2001:db8:0:abcd::2": {
                                     "group": "ff30::2",
                                     "source": "2001:db8:0:abcd::2"
                                }
                           },
                           "group": {
                                "ff30::2": {
                                     "source": {
                                          "2001:db8:0:abcd::2": {
                                               "last_reported": "1d07h",
                                               "type": "static"
                                          }
                                     }
                                },
                                "fffe::2": {
                                     "last_reported": "1d07h",
                                     "type": "static"
                                },
                                "fffe::1": {
                                     "last_reported": "00:03:07",
                                     "type": "local"
                                },
                                "ff30::1": {
                                     "source": {
                                          "2001:db8:0:abcd::1": {
                                               "last_reported": "00:03:19",
                                               "type": "local"
                                          }
                                     }
                                }
                           },
                           "join_group": {
                                "ff30::1 2001:db8:0:abcd::1": {
                                     "group": "ff30::1",
                                     "source": "2001:db8:0:abcd::1"
                                },
                                "fffe::1 *": {
                                     "group": "fffe::1",
                                     "source": "*"
                                }
                           }
                      }
                 }
            }
        }
    }


    Mld_info = {
    	"vrfs": {
	          "VRF1": {
                 "groups_count": 2,
	               "interfaces": {
	                    "Ethernet2/2": {
	                         "query_interval": 366,
	                         "version": 2,
	                         "immediate_leave": True,
	                         "group_policy": "test",
	                         "robustness_variable": 7,
	                         "group": {
	                              "ff30::2": {
	                                   "source": {
	                                        "2001:db8:0:abcd::2": {
	                                             "last_reporter": "2001:db8:8404:751c::1",
	                                             "up_time": "00:25:49",
	                                             "expire": "never"
	                                        }
	                                   }
	                              },
	                              "fffe::2": {
	                                   "last_reporter": "2001:db8:8404:751c::1",
	                                   "up_time": "00:25:49",
	                                   "expire": "never"
	                              }
	                         },
	                         "max_groups": 6400,
	                         "join_group": {
	                              "ff30::1 2001:db8:0:abcd::1": {
	                                   "source": "2001:db8:0:abcd::1",
	                                   "group": "ff30::1"
	                              },
	                              "fffe::1 *": {
	                                   "source": "*",
	                                   "group": "fffe::1"
	                              }
	                         },
	                         "enable": True,
	                         "querier": "fe80::5054:ff:fed7:c01f",
	                         "query_max_response_time": 16,
	                         "oper_status": "up",
	                         "static_group": {
	                              "ff30::2 2001:db8:0:abcd::2": {
	                                   "source": "2001:db8:0:abcd::2",
	                                   "group": "ff30::2"
	                              },
	                              "fffe::2 *": {
	                                   "source": "*",
	                                   "group": "fffe::2"
	                              }
	                         }
	                    }
	               }
	          },
	          "default": {
                 "groups_count": 2,
	               "interfaces": {
	                    "Ethernet2/1": {
	                         "query_interval": 366,
	                         "version": 2,
	                         "immediate_leave": True,
	                         "group_policy": "test",
	                         "robustness_variable": 7,
	                         "group": {
	                              "ff30::2": {
	                                   "source": {
	                                        "2001:db8:0:abcd::2": {
	                                             "last_reporter": "2001:db8:8404:907f::1",
	                                             "up_time": "00:26:28",
	                                             "expire": "never"
	                                        }
	                                   }
	                              },
	                              "fffe::2": {
	                                   "last_reporter": "2001:db8:8404:907f::1",
	                                   "up_time": "00:26:05",
	                                   "expire": "never"
	                              }
	                         },
	                         "max_groups": 6400,
	                         "join_group": {
	                              "ff30::1 2001:db8:0:abcd::1": {
	                                   "source": "2001:db8:0:abcd::1",
	                                   "group": "ff30::1"
	                              },
	                              "fffe::1 *": {
	                                   "source": "*",
	                                   "group": "fffe::1"
	                              }
	                         },
	                         "enable": True,
	                         "querier": "fe80::5054:ff:fed7:c01f",
	                         "query_max_response_time": 16,
	                         "oper_status": "up",
	                         "static_group": {
	                              "ff30::2 2001:db8:0:abcd::2": {
	                                   "source": "2001:db8:0:abcd::2",
	                                   "group": "ff30::2"
	                              },
	                              "fffe::2 *": {
	                                   "source": "*",
	                                   "group": "fffe::2"
	                              }
	                         }
	                    }
	               }
	          }
	    }
    }
