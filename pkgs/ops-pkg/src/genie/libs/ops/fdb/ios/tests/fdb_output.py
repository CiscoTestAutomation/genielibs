'''Fdb Genie Ops Object Outputs for IOS'''


class FdbOutput(object):

    ShowMacAddressTable = {
        "mac_table": {
         "vlans": {
               '100': {
                   "mac_addresses": {
                         "ecbd.1d09.5689": {
                             "drop": {
                                   "drop": True,
                                   "entry_type": "dynamic"
                             },
                             "mac_address": "ecbd.1d09.5689"
                         },
                         "3820.5672.fc03": {
                             "interfaces": {
                                   "Port-channel12": {
                                       "interface": "Port-channel12",
                                       "entry_type": "dynamic"
                                   }
                             },
                             "mac_address": "3820.5672.fc03"
                         },
                         "58bf.eab6.2f51": {
                             "interfaces": {
                                   "Vlan100": {
                                       "interface": "Vlan100",
                                       "entry_type": "static"
                                   }
                             },
                             "mac_address": "58bf.eab6.2f51"
                         }
                   },
                   "vlan": 100
               },
               "all": {
                   "mac_addresses": {
                         "0100.0ccc.cccc": {
                             "interfaces": {
                                   "CPU": {
                                       "interface": "CPU",
                                       "entry_type": "static"
                                   }
                             },
                             "mac_address": "0100.0ccc.cccc"
                         },
                         "0100.0ccc.cccd": {
                             "interfaces": {
                                   "CPU": {
                                       "interface": "CPU",
                                       "entry_type": "static"
                                   }
                             },
                             "mac_address": "0100.0ccc.cccd"
                         }
                   },
                   "vlan": "all"
               },
               '20': {
                   "mac_addresses": {
                         "aaaa.bbbb.cccc": {
                             "drop": {
                                   "drop": True,
                                   "entry_type": "static"
                             },
                             "mac_address": "aaaa.bbbb.cccc"
                         }
                   },
                   "vlan": 20
               },
               '10': {
                   "mac_addresses": {
                         "aaaa.bbbb.cccc": {
                             "interfaces": {
                                   "GigabitEthernet1/0/8": {
                                       "interface": "GigabitEthernet1/0/8",
                                       "entry_type": "static"
                                   },
                                   "GigabitEthernet1/0/9": {
                                       "interface": "GigabitEthernet1/0/9",
                                       "entry_type": "static"
                                   }
                             },
                             "mac_address": "aaaa.bbbb.cccc"
                         }
                   },
                   "vlan": 10
               },
               '101': {
                   "mac_addresses": {
                         "58bf.eab6.2f41": {
                             "interfaces": {
                                   "Vlan101": {
                                       "interface": "Vlan101",
                                       "entry_type": "static"
                                   }
                             },
                             "mac_address": "58bf.eab6.2f41"
                         },
                         "3820.5672.fc41": {
                             "interfaces": {
                                   "Port-channel12": {
                                       "interface": "Port-channel12",
                                       "entry_type": "dynamic"
                                   }
                             },
                             "mac_address": "3820.5672.fc41"
                         },
                         "3820.5672.fc03": {
                             "interfaces": {
                                   "Port-channel12": {
                                       "interface": "Port-channel12",
                                       "entry_type": "dynamic"
                                   }
                             },
                             "mac_address": "3820.5672.fc03"
                         }
                   },
                   "vlan": 101
               }
         }
     },
     "total_mac_addresses": 10

    }

    ShowMacAddressTableAgingTime = {
        'mac_aging_time': 0,
        'vlans': {
            '10': {
                'mac_aging_time': 10,
                'vlan': 10
            }
        }

    }

    ShowMacAddressTableLearning = {
        "vlans": {
            '10': {
                 "vlan": 10,
                 "mac_learning": False
            },
            '105': {
                 "vlan": 105,
                 "mac_learning": False
            },
            '101': {
                 "vlan": 101,
                 "mac_learning": False
            },
            '102': {
                 "vlan": 102,
                 "mac_learning": False
            },
            '103': {
                 "vlan": 103,
                 "mac_learning": False
            }
        }
    }

    Fdb_info = {
        "mac_aging_time": 0,
        "total_mac_addresses": 10,
        "mac_table": {
            "vlans": {
                  '100': {
                      "mac_addresses": {
                            "ecbd.1d09.5689": {
                                "drop": {
                                      "drop": True,
                                      "entry_type": "dynamic"
                                },
                                "mac_address": "ecbd.1d09.5689"
                            },
                            "3820.5672.fc03": {
                                "interfaces": {
                                      "Port-channel12": {
                                          "interface": "Port-channel12",
                                          "entry_type": "dynamic"
                                      }
                                },
                                "mac_address": "3820.5672.fc03"
                            },
                            "58bf.eab6.2f51": {
                                "interfaces": {
                                      "Vlan100": {
                                          "interface": "Vlan100",
                                          "entry_type": "static"
                                      }
                                },
                                "mac_address": "58bf.eab6.2f51"
                            }
                      },
                      "vlan": 100
                  },
                  '20': {
                      "mac_addresses": {
                            "aaaa.bbbb.cccc": {
                                "drop": {
                                      "drop": True,
                                      "entry_type": "static"
                                },
                                "mac_address": "aaaa.bbbb.cccc"
                            }
                      },
                      "vlan": 20
                  },
                  '10': {
                      "mac_addresses": {
                            "aaaa.bbbb.cccc": {
                                "interfaces": {
                                      "GigabitEthernet1/0/8": {
                                          "interface": "GigabitEthernet1/0/8",
                                          "entry_type": "static"
                                      },
                                      "GigabitEthernet1/0/9": {
                                          "interface": "GigabitEthernet1/0/9",
                                          "entry_type": "static"
                                      }
                                },
                                "mac_address": "aaaa.bbbb.cccc"
                            }
                      },
                      "vlan": 10,
                      "mac_aging_time": 10,
                      "mac_learning": False
                  },
                  '101': {
                      "mac_addresses": {
                            "58bf.eab6.2f41": {
                                "interfaces": {
                                      "Vlan101": {
                                          "interface": "Vlan101",
                                          "entry_type": "static"
                                      }
                                },
                                "mac_address": "58bf.eab6.2f41"
                            },
                            "3820.5672.fc41": {
                                "interfaces": {
                                      "Port-channel12": {
                                          "interface": "Port-channel12",
                                          "entry_type": "dynamic"
                                      }
                                },
                                "mac_address": "3820.5672.fc41"
                            },
                            "3820.5672.fc03": {
                                "interfaces": {
                                      "Port-channel12": {
                                          "interface": "Port-channel12",
                                          "entry_type": "dynamic"
                                      }
                                },
                                "mac_address": "3820.5672.fc03"
                            }
                      },
                      "vlan": 101,
                      "mac_learning": False
                  },
                  '102': {
                      "mac_learning": False
                  },
                  '103': {
                      "mac_learning": False
                  },
                  '105': {
                      "mac_learning": False
                  }
            }
        },
    }