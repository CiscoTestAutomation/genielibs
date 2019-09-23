"""
MSDP Genie Ops Object Outputs for IOS

"""


class MsdpOutput(object):

    # 'show ip msdp peer'
    ShowIpMsdpPeer = {
        "vrf": {
            "default": {
                "peer": {
                    "10.16.2.2": {
                        "peer_as": 65000,
                        "session_state": "Up",
                        "resets": "0",
                        "connect_source": "Loopback0",
                        "connect_source_address": "10.4.1.1",
                        "elapsed_time": "00:13:18",
                        "statistics": {
                            "sent": {
                                "data_message": 15,
                                "sa_message": 14,
                                "sa_response": 0,
                                "data_packets": 0,
                            },
                            "received": {
                                "data_message": 28,
                                "sa_message": 0,
                                "sa_request": 0,
                                "data_packets": 0,
                            },
                            "output_msg_discarded": 0,
                            "established_transitions": 1,
                            "queue": {"size_in": 0, "size_out": 0},
                            "error": {"rpf_failure": 0},
                        },
                        "conn_count_cleared": "00:22:05",
                        "sa_filter": {
                            "in": {
                                "(S,G)": {"filter": "none", "route_map": "none"},
                                "RP": {"filter": "none", "route_map": "none"},
                            },
                            "out": {
                                "(S,G)": {"filter": "none", "route_map": "none"},
                                "RP": {"filter": "none", "route_map": "none"},
                            },
                        },
                        "sa_request": {"input_filter": "none"},
                        "ttl_threshold": 0,
                        "sa_learned_from": 0,
                        "signature_protection": False,
                    },
                    "10.36.3.3": {
                        "peer_as": 65000,
                        "session_state": "Up",
                        "resets": "0",
                        "connect_source": "Loopback0",
                        "connect_source_address": "10.4.1.1",
                        "elapsed_time": "00:16:57",
                        "statistics": {
                            "sent": {
                                "data_message": 20,
                                "sa_message": 19,
                                "sa_response": 0,
                                "data_packets": 0,
                            },
                            "received": {
                                "data_message": 19,
                                "sa_message": 0,
                                "sa_request": 0,
                                "data_packets": 0,
                            },
                            "output_msg_discarded": 0,
                            "established_transitions": 1,
                            "queue": {"size_in": 0, "size_out": 0},
                            "error": {"rpf_failure": 0},
                        },
                        "conn_count_cleared": "00:22:14",
                        "sa_filter": {
                            "in": {
                                "(S,G)": {"filter": "none", "route_map": "none"},
                                "RP": {"filter": "none", "route_map": "none"},
                            },
                            "out": {
                                "(S,G)": {"filter": "none", "route_map": "none"},
                                "RP": {"filter": "none", "route_map": "none"},
                            },
                        },
                        "sa_request": {"input_filter": "none"},
                        "ttl_threshold": 0,
                        "sa_learned_from": 0,
                        "signature_protection": False,
                    },
                }
            }
        }
    }

    ShowIpMsdpPeer_golden = """
        MSDP Peer 10.16.2.2 (?), AS 65000
          Connection status:
            State: Up, Resets: 0, Connection source: Loopback0 (10.4.1.1)
            Uptime(Downtime): 00:13:18, Messages sent/received: 15/28
            Output messages discarded: 0
            Connection and counters cleared 00:22:05 ago
          SA Filtering:
            Input (S,G) filter: none, route-map: none
            Input RP filter: none, route-map: none
            Output (S,G) filter: none, route-map: none
            Output RP filter: none, route-map: none
          SA-Requests:
            Input filter: none
          Peer ttl threshold: 0
          SAs learned from this peer: 0
          Number of connection transitions to Established state: 1
            Input queue size: 0, Output queue size: 0
          MD5 signature protection on MSDP TCP connection: not enabled
          Message counters:
            RPF Failure count: 0
            SA Messages in/out: 0/14
            SA Requests in: 0
            SA Responses out: 0
            Data Packets in/out: 0/0
        MSDP Peer 10.36.3.3 (?), AS 65000
          Connection status:
            State: Up, Resets: 0, Connection source: Loopback0 (10.4.1.1)
            Uptime(Downtime): 00:16:57, Messages sent/received: 20/19
            Output messages discarded: 0
            Connection and counters cleared 00:22:14 ago
          SA Filtering:
            Input (S,G) filter: none, route-map: none
            Input RP filter: none, route-map: none
            Output (S,G) filter: none, route-map: none
            Output RP filter: none, route-map: none
          SA-Requests:
            Input filter: none
          Peer ttl threshold: 0
          SAs learned from this peer: 0
          Number of connection transitions to Established state: 1
            Input queue size: 0, Output queue size: 0
          MD5 signature protection on MSDP TCP connection: not enabled
          Message counters:
            RPF Failure count: 0
            SA Messages in/out: 0/19
            SA Requests in: 0
            SA Responses out: 0
            Data Packets in/out: 0/0
    """

    # 'show ip msdp sa-cache'
    ShowIpMsdpSaCache = {
        "vrf": {
            "default": {
                "num_of_sa_cache": 1,
                "sa_cache": {
                    "225.1.1.1 10.3.3.18": {
                        "group": "225.1.1.1",
                        "source_addr": "10.3.3.18",
                        "up_time": "00:00:10",
                        "expire": "00:05:49",
                        "peer_as": 3,
                        "peer": "10.1.100.4",
                        "origin_rp": {"10.3.100.8": {"rp_address": "10.3.100.8"}},
                        "peer_learned_from": "10.1.100.4",
                        "rpf_peer": "10.1.100.4",
                        "statistics": {
                            "received": {"sa": 1, "encapsulated_data_received": 1}
                        },
                    }
                },
            }
        }
    }

    ShowIpMsdpSaCache_golden = """
        MSDP Source-Active Cache - 1 entries
            (10.3.3.18, 225.1.1.1), RP 10.3.100.8, BGP/AS 3, 00:00:10/00:05:49, Peer 10.1.100.4
            Learned from peer 10.1.100.4, RPF peer 10.1.100.4, 
            SAs received: 1, Encapsulated data received: 1
    """

    MsdpInfo = {
        "vrf": {
            "default": {
                "peer": {
                    "10.36.3.3": {
                        "elapsed_time": "00:16:57",
                        "peer_as": 65000,
                        "connect_source": "Loopback0",
                        "ttl_threshold": 0,
                        "session_state": "established",
                        "statistics": {
                            "received": {"sa_message": 0, "sa_request": 0},
                            "queue": {"size_in": 0, "size_out": 0},
                            "sent": {"sa_message": 19, "sa_response": 0},
                            "error": {"rpf_failure": 0},
                        },
                    },
                    "10.16.2.2": {
                        "elapsed_time": "00:13:18",
                        "peer_as": 65000,
                        "connect_source": "Loopback0",
                        "ttl_threshold": 0,
                        "session_state": "established",
                        "statistics": {
                            "received": {"sa_message": 0, "sa_request": 0},
                            "queue": {"size_in": 0, "size_out": 0},
                            "sent": {"sa_message": 14, "sa_response": 0},
                            "error": {"rpf_failure": 0},
                        },
                    },
                },
                "sa_cache": {
                    "225.1.1.1 10.3.3.18": {
                        "group": "225.1.1.1",
                        "source_addr": "10.3.3.18",
                        "peer_learned_from": "10.1.100.4",
                        "rpf_peer": "10.1.100.4",
                        "up_time": "00:00:10",
                        "expire": "00:05:49",
                        "origin_rp": {"10.3.100.8": {"rp_address": "10.3.100.8"}},
                    }
                },
            }
        }
    }
