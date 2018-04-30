"""
 Routing Genie Ops Object Outputs for IOSXR.
"""

class RoutingOutput(object):
    """ show route ops output """

    showRouteIpv4 ={
        "vrf": {
            "default": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "1.1.1.1/32": {
                                "route": "1.1.1.1/32",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/0/0": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "01:51:13"
                                        },
                                        "GigabitEthernet0/0/0/3": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:51:13"
                                        },
                                    },
                                },
                            },
                            "2.2.2.2/32": {
                                "route": "2.2.2.2/32",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {
                                            "outgoing_interface": "Loopback0",
                                            "updated": "01:51:14"
                                        },
                                    },
                                },
                            },
                            "3.3.3.3/32": {
                                "route": "3.3.3.3/32",
                                "active": True,
                                "route_preference": 1,
                                "metric": 0,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.2.3.3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/1",
                                            "updated": "01:51:13"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "20.2.3.3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/2",
                                            "updated": "01:51:13"
                                        },
                                    },
                                },
                            },
                            "10.1.2.0/24": {
                                "route": "10.1.2.0/24",
                                "active": True,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/0/3": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:51:13"
                                        },
                                    },
                                },
                            },
                            "21.21.21.21/32": {
                                "route": "21.21.21.21/32",
                                "active": True,
                                "route_preference": 115,
                                "metric": 20,
                                "source_protocol_codes": "i L1",
                                "source_protocol": "isis",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "20.1.2.1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "01:50:50"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.1.2.1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:50:50"
                                        },
                                    },
                                },
                            },
                            "31.31.31.31/32": {
                                "route": "31.31.31.31/32",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "11.11.11.11",
                                            "updated": "00:55:14"
                                        },
                                    },
                                },
                            },
                            "32.32.32.32/32": {
                                "route": "32.32.32.32/32",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback3": {
                                            "outgoing_interface": "Loopback3",
                                            "updated": "01:51:14"
                                        },
                                    },
                                },
                            },
                            "33.33.33.33/32": {
                                "route": "33.33.33.33/32",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "13.13.13.13",
                                            "updated": "00:52:31"
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    showRouteIpv6 = {
        "vrf": {
            "default": {
                "address_family": {
                    "ipv6": {
                        "routes": {
                            "2001:1:1:1::1/128": {
                                "route": "2001:1:1:1::1/128",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "route_preference": 1,
                                "metric": 0,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:20:1:2::1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "01:52:23"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "2001:10:1:2::1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:52:23"
                                        },

                                    },
                                },
                            },
                            "2001:2:2:2::2/128": {
                                "route": "2001:2:2:2::2/128",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {
                                            "outgoing_interface": "Loopback0",
                                            "updated": "01:52:24"
                                        },
                                    },
                                },
                            },
                            "2001:3:3:3::3/128": {
                                "route": "2001:3:3:3::3/128",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "route_preference": 1,
                                "metric": 0,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:10:2:3::3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/1",
                                            "updated": "01:52:23"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "2001:20:2:3::3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/2",
                                            "updated": "01:52:23"
                                        },
                                    },
                                },
                            },
                            "2001:21:21:21::21/128": {
                                "route": "2001:21:21:21::21/128",
                                "active": True,
                                "source_protocol_codes": "i L1",
                                "source_protocol": "isis",
                                "route_preference": 115,
                                "metric": 20,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "fe80::5054:ff:fe54:6569",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "00:56:34"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "fe80::5054:ff:fea5:829",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "00:56:34"
                                        },
                                    },
                                },
                            },
                            "2001:32:32:32::32/128": {
                                "route": "2001:32:32:32::32/128",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback3": {
                                            "outgoing_interface": "Loopback3",
                                            "updated": "01:52:24"
                                        },
                                    },
                                },
                            },
                            "2001:33:33:33::33/128": {
                                "route": "2001:33:33:33::33/128",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:13:13:13::13",
                                            "updated": "00:53:22"
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


    showRouteOpsOutput = {
        "vrf": {
            "default": {
                "address_family": {
                    "ipv4": {
                        "routes": {
                            "1.1.1.1/32": {
                                "route": "1.1.1.1/32",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/0/0": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                        },
                                        "GigabitEthernet0/0/0/3": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                        },
                                    },
                                },
                            },
                            "2.2.2.2/32": {
                                "route": "2.2.2.2/32",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {
                                            "outgoing_interface": "Loopback0",
                                        },
                                    },
                                },
                            },
                            "3.3.3.3/32": {
                                "route": "3.3.3.3/32",
                                "active": True,
                                "route_preference": 1,
                                "metric": 0,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "10.2.3.3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/1",
                                            "updated": "01:51:13"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "20.2.3.3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/2",
                                            "updated": "01:51:13"
                                        },
                                    },
                                },
                            },
                            "10.1.2.0/24": {
                                "route": "10.1.2.0/24",
                                "active": True,
                                "source_protocol_codes": "C",
                                "source_protocol": "connected",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "GigabitEthernet0/0/0/3": {
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                        },
                                    },
                                },
                            },
                            "21.21.21.21/32": {
                                "route": "21.21.21.21/32",
                                "active": True,
                                "route_preference": 115,
                                "metric": 20,
                                "source_protocol_codes": "i L1",
                                "source_protocol": "isis",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "20.1.2.1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "01:50:50"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "10.1.2.1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:50:50"
                                        },
                                    },
                                },
                            },
                            "31.31.31.31/32": {
                                "route": "31.31.31.31/32",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "11.11.11.11",
                                            "updated": "00:55:14"
                                        },
                                    },
                                },
                            },
                            "32.32.32.32/32": {
                                "route": "32.32.32.32/32",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback3": {
                                            "outgoing_interface": "Loopback3",
                                        },
                                    },
                                },
                            },
                            "33.33.33.33/32": {
                                "route": "33.33.33.33/32",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "13.13.13.13",
                                            "updated": "00:52:31"
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "ipv6": {
                        "routes": {
                            "2001:1:1:1::1/128": {
                                "route": "2001:1:1:1::1/128",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "route_preference": 1,
                                "metric": 0,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:20:1:2::1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "01:52:23"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "2001:10:1:2::1",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "01:52:23"
                                        },
                                    },
                                },
                            },
                            "2001:2:2:2::2/128": {
                                "route": "2001:2:2:2::2/128",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback0": {
                                            "outgoing_interface": "Loopback0",
                                        },
                                    },
                                },
                            },
                            "2001:3:3:3::3/128": {
                                "route": "2001:3:3:3::3/128",
                                "active": True,
                                "source_protocol_codes": "S",
                                "source_protocol": "static",
                                "route_preference": 1,
                                "metric": 0,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:10:2:3::3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/1",
                                            "updated": "01:52:23"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "2001:20:2:3::3",
                                            "outgoing_interface": "GigabitEthernet0/0/0/2",
                                            "updated": "01:52:23"
                                        },
                                    },
                                },
                            },
                            "2001:21:21:21::21/128": {
                                "route": "2001:21:21:21::21/128",
                                "active": True,
                                "source_protocol_codes": "i L1",
                                "source_protocol": "isis",
                                "route_preference": 115,
                                "metric": 20,
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "fe80::5054:ff:fe54:6569",
                                            "outgoing_interface": "GigabitEthernet0/0/0/0",
                                            "updated": "00:56:34"
                                        },
                                        2: {
                                            "index": 2,
                                            "next_hop": "fe80::5054:ff:fea5:829",
                                            "outgoing_interface": "GigabitEthernet0/0/0/3",
                                            "updated": "00:56:34"
                                        },
                                    },
                                },
                            },
                            "2001:32:32:32::32/128": {
                                "route": "2001:32:32:32::32/128",
                                "active": True,
                                "source_protocol_codes": "L",
                                "source_protocol": "local",
                                "next_hop": {
                                    "outgoing_interface": {
                                        "Loopback3": {
                                            "outgoing_interface": "Loopback3",
                                        },
                                    },
                                },
                            },
                            "2001:33:33:33::33/128": {
                                "route": "2001:33:33:33::33/128",
                                "active": True,
                                "route_preference": 200,
                                "metric": 0,
                                "source_protocol_codes": "B",
                                "source_protocol": "bgp",
                                "next_hop": {
                                    "next_hop_list": {
                                        1: {
                                            "index": 1,
                                            "next_hop": "2001:13:13:13::13",
                                            "updated": "00:53:22"
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },

    }
