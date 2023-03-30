import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.get import get_mpls_forwarding_table


class TestGetMplsForwardingTable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_mpls_forwarding_table(self):
        result = get_mpls_forwarding_table(self.device)
        expected_output = {'vrf': {'default': {'local_label': {
            18: {
                "outgoing_label_or_vc": {
                    "No Label": {
                        "prefix_or_tunnel_id": {
                            "192.168.12.0/24[V]": {
                                "outgoing_interface": {
                                    "aggregate/red": {"bytes_label_switched": 0}
                                }
                            }
                        }
                    }
                }
            },
            19: {
                "outgoing_label_or_vc": {
                    "No Label": {
                        "prefix_or_tunnel_id": {
                            "2001:12::/64[V]": {
                                "outgoing_interface": {
                                    "aggregate/red": {"bytes_label_switched": 0}
                                }
                            }
                        }
                    }
                }
            },
            20: {
                "outgoing_label_or_vc": {
                    "No Label": {
                        "prefix_or_tunnel_id": {
                            "IPv6 VRF[V]": {
                                "outgoing_interface": {
                                    "aggregate/red": {"bytes_label_switched": 0}
                                }
                            }
                        }
                    }
                }
            },
            21: {
                "outgoing_label_or_vc": {
                    "16": {
                        "prefix_or_tunnel_id": {
                            "1.1.1.1/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            22: {
                "outgoing_label_or_vc": {
                    "17": {
                        "prefix_or_tunnel_id": {
                            "1.1.1.2/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            23: {
                "outgoing_label_or_vc": {
                    "18": {
                        "prefix_or_tunnel_id": {
                            "2.2.2.1/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            24: {
                "outgoing_label_or_vc": {
                    "19": {
                        "prefix_or_tunnel_id": {
                            "2.2.2.2/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            25: {
                "outgoing_label_or_vc": {
                    "20": {
                        "prefix_or_tunnel_id": {
                            "3.3.3.1/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            26: {
                "outgoing_label_or_vc": {
                    "21": {
                        "prefix_or_tunnel_id": {
                            "3.3.3.2/32": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            27: {
                "outgoing_label_or_vc": {
                    "24": {
                        "prefix_or_tunnel_id": {
                            "6.6.6.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            28: {
                "outgoing_label_or_vc": {
                    "25": {
                        "prefix_or_tunnel_id": {
                            "9.9.9.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    },
                                }
                            }
                        }
                    }
                }
            },
            29: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.0.0.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            30: {
                "outgoing_label_or_vc": {
                    "26": {
                        "prefix_or_tunnel_id": {
                            "10.0.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "27": {
                        "prefix_or_tunnel_id": {
                            "10.0.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            31: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.0.1.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            32: {
                "outgoing_label_or_vc": {
                    "27": {
                        "prefix_or_tunnel_id": {
                            "10.0.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "29": {
                        "prefix_or_tunnel_id": {
                            "10.0.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            33: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.1.0.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            34: {
                "outgoing_label_or_vc": {
                    "28": {
                        "prefix_or_tunnel_id": {
                            "10.1.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "31": {
                        "prefix_or_tunnel_id": {
                            "10.1.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            35: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.1.1.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            36: {
                "outgoing_label_or_vc": {
                    "29": {
                        "prefix_or_tunnel_id": {
                            "10.1.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "33": {
                        "prefix_or_tunnel_id": {
                            "10.1.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            37: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.1.2.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            38: {
                "outgoing_label_or_vc": {
                    "30": {
                        "prefix_or_tunnel_id": {
                            "10.1.2.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "35": {
                        "prefix_or_tunnel_id": {
                            "10.1.2.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            39: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "10.1.3.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            40: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.0.0.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            41: {
                "outgoing_label_or_vc": {
                    "33": {
                        "prefix_or_tunnel_id": {
                            "20.0.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "38": {
                        "prefix_or_tunnel_id": {
                            "20.0.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            42: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.0.1.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            43: {
                "outgoing_label_or_vc": {
                    "35": {
                        "prefix_or_tunnel_id": {
                            "20.0.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "39": {
                        "prefix_or_tunnel_id": {
                            "20.0.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            44: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.1.0.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            45: {
                "outgoing_label_or_vc": {
                    "37": {
                        "prefix_or_tunnel_id": {
                            "20.1.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "40": {
                        "prefix_or_tunnel_id": {
                            "20.1.0.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            46: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.1.1.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            47: {
                "outgoing_label_or_vc": {
                    "39": {
                        "prefix_or_tunnel_id": {
                            "20.1.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "41": {
                        "prefix_or_tunnel_id": {
                            "20.1.1.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            48: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.1.2.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            49: {
                "outgoing_label_or_vc": {
                    "41": {
                        "prefix_or_tunnel_id": {
                            "20.1.2.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                    "42": {
                        "prefix_or_tunnel_id": {
                            "20.1.2.0/30": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    },
                }
            },
            50: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "20.1.3.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            51: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "98.98.98.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/2": {
                                        "next_hop": "20.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            52: {
                "outgoing_label_or_vc": {
                    "Pop Label": {
                        "prefix_or_tunnel_id": {
                            "99.99.99.0/24": {
                                "outgoing_interface": {
                                    "Ethernet0/1": {
                                        "next_hop": "10.1.3.1",
                                        "bytes_label_switched": 0,
                                    }
                                }
                            }
                        }
                    }
                }
            },
            53: {
                "outgoing_label_or_vc": {
                    "No Label": {
                        "prefix_or_tunnel_id": {
                            "IPv4 VRF[V]": {
                                "outgoing_interface": {
                                    "aggregate/red": {"bytes_label_switched": 0}
                                }
                            }
                        }
                    }
                }
            },
        }}}}
 
        self.assertEqual(result, expected_output)
