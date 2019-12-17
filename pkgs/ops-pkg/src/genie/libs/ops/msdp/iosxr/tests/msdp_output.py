"""
 Msdp Genie Ops Object Outputs for IOSXR.
"""

class MsdpOutput(object):
    # show msdp peer
    showMsdpPeer = '''
        Router# show msdp peer

        MSDP Peer 192.168.229.3 (?), AS 65109
        Description:
            Connection status:
            State: Inactive, Resets: 999, Connection Source: 192.168.100.1
            Uptime(Downtime): 00:00:09, SA messages received: 0
            TLV messages sent/received: 3/0
            Output messages discarded: 0
            Connection and counters cleared 00:01:25 ago
            SA Filtering:
            Input (S,G) filter: none
            Input RP filter: none
            Output (S,G) filter: none
            Output RP filter: none
            SA-Requests:
            Input filter: none
            Sending SA-Requests to peer: disabled
            Password: None
            Peer ttl threshold: 2
            Input queue size: 0, Output queue size: 0
            KeepAlive timer period: 30
            Peer Timeout timer period: 75
            NSR:
            State: StopRead, Oper-Downs: 0
            NSR-Uptime(NSR-Downtime): 1d02h
    '''

    # show msdp vrf VRF1 peer
    showMsdpVRFPeer = '''
        Router# show msdp vrf VRF1 peer   
        
        MSDP Peer 10.4.1.1 (?), AS 0
        Description: R1
            Connection status:
            State: Listen, Resets: 0, Connection Source: 10.151.22.23
            Uptime(Downtime): 18:19:47, SA messages received: 0
            TLV messages sent/received: 0/0
            Output messages discarded: 0
            Connection and counters cleared 22:46:31 ago
            SA Filtering:
            Input (S,G) filter: safilin
            Input RP filter: none
            Output (S,G) filter: safilout
            Output RP filter: none
            SA-Requests:
            Input filter: none
            Sending SA-Requests to peer: disabled
            Password: None   
            Peer ttl threshold: 222
            Input queue size: 0, Output queue size: 0
            KeepAlive timer period: 30
            Peer Timeout timer period: 75
            NSR:
            State: Unknown, Oper-Downs: 0
            NSR-Uptime(NSR-Downtime): 22:46:31
        '''

    # show msdp vrf VRF1 peer 10.4.1.1
    showMsdpVRFPeerArg = '''
     +++ Device: executing command 'show msdp vrf VRF1 peer 10.4.1.1' +++
    show msdp vrf VRF1 peer 10.4.1.1
    Fri Nov 22 19:26:17.324 UTC
    MSDP Peer 10.4.1.1 (?), AS 65000
    Description: 
      Connection status:
        State: Established, Resets: 0, Connection Source: 10.16.2.2
        Uptime(Downtime): 1d09h, SA messages received: 6561
        TLV messages sent/received: 4079/2188
      Output messages discarded: 0
        Connection and counters cleared 1d09h ago
      SA Filtering:
        Input (S,G) filter: none
        Input RP filter: none
        Output (S,G) filter: none
        Output RP filter: none
      SA-Requests:
        Input filter: none
        Sending SA-Requests to peer: disabled
      Password: None 
      Peer ttl threshold: 2
      Input queue size: 0, Output queue size: 0
      KeepAlive timer period: 30
      Peer Timeout timer period: 75
      NSR:
        State: Unknown, Oper-Downs: 0
        NSR-Uptime(NSR-Downtime): 1d10h
    '''

    # show msdp context
    showMsdpContext = '''
    Router# show msdp context

    MSDP context information for default
        VRF ID    : 0x60000000
        Table ID    : 0xe0000000
        Table Count (Active/Total) : 2/2
    Inheritable Configuration
        TTL    : 2
        Maximum SAs    : 0
        Keepalive Period    : 30
        Peer Timeout Period : 75
        Connect Source    :   
        SA Filter In    :   
        SA Filter Out    :   
        RP Filter In    :   
        RP Filter Out    :   
    Configuration
        Originator Address    : 172.16.76.1
        Originator Interface Name    : Loopback150
        Default Peer Address    : 0.0.0.0
        SA Holdtime    : 150
        Allow Encaps Count    : 0
        Context Maximum SAs    : 20000
    SA Cache Counts    (Current/High Water Mark)
        Groups    :    2/2   
        Sources    :    12/12   
        RPs    :    3/0   
        External SAs :    3/3   
    MRIB Update Counts
        Total updates    : 473
        With no changes    : 0
        (*,G) routes    : 26
        (S,G) routes    : 447
    MRIB Update Drops
        Invalid group    : 0
        Invalid group length : 0
        Invalid source    : 0
        Auto-RP Address    : 2
    '''

    # show msdp vrf VRF1 context
    showMsdpVRFContext = '''
             
    Router# show msdp vrf VRF1 context

    MSDP context information for VRF1
        VRF ID    : 0x60000002
        Table ID    : 0xe0000011
        Table Count (Active/Total) : 1/1
    Inheritable Configuration
        TTL    : 222
        Maximum SAs    : 0
        Keepalive Period    : 30
        Peer Timeout Period : 75
        Connect Source    : Loopback3
        SA Filter In    : safilin
        SA Filter Out    : safilout
        RP Filter In    :   
        RP Filter Out    :   
    Configuration
        Originator Address    : 10.151.22.23
        Originator Interface Name    : Loopback3
        Default Peer Address    : 0.0.0.0
        SA Holdtime    : 150
        Allow Encaps Count    : 0
        Context Maximum SAs    : 22222
    SA Cache Counts    (Current/High Water Mark)
        Groups    :    0/0   
        Sources    :    0/0   
        RPs    :    0/0   
        External SAs :    0/0   
    MRIB Update Counts
        Total updates    : 0
        With no changes    : 0
        (*,G) routes    : 0
        (S,G) routes    : 0
    MRIB Update Drops
        Invalid group    : 0
        Invalid group length : 0
        Invalid source    : 0
        Auto-RP Address    : 0'''

    # show msdp summary
    showMsdpSummary = '''
    RP/0/0/CPU0:R2_xrvr#show msdp summary
    
    Maximum External SA's Global : 20000
    Current External Active SAs : 0

    MSDP Peer Status Summary
       Peer Address    AS    State    Uptime/    Reset Peer    Active Cfg.Max    TLV
        Downtime    Count Name    SA Cnt Ext.SAs recv/sent
       10.64.4.4    200    Connect    20:35:48    0    R4    0    444    0/0'''

    # show msdp vrf VRF1 summary
    showMsdpVRFSummary = '''
    Router# show msdp vrf VRF1 summary

    Maximum External SA's Global : 20000
    Current External Active SAs : 0

    MSDP Peer Status Summary
       Peer Address    AS    State    Uptime/    Reset Peer    Active Cfg.Max    TLV
        Downtime    Count Name    SA Cnt Ext.SAs recv/sent
       10.4.1.1    0    Listen    18:25:02    0    R1    0    0    0/0
       10.229.11.11    0    Listen    18:14:53    0    ?    0    0    0/0
       '''

    # show msdp sa-cache
    showMsdpSaCache = '''
    RP/0/0/CPU0:XR5#show msdp sa-cache

    MSDP Flags:
    E - set MRIB E flag , L - domain local source is active,
    EA - externally active source, PI - PIM is interested in the group,
    DE - SAs have been denied.    Timers age/expiration,
    Cache Entry:
    (10.1.1.10, 239.1.1.1), RP 192.168.1.1, MBGP/AS 200, 00:01:02/00:01:32
        Learned from peer 192.168.1.1, RPF peer 192.168.1.1
        SAs recvd 2, Encapsulated data received: 0
        grp flags: PI,    src flags: E, EA, PI
    '''

    # show msdp vrf VRF1 sa-cache
    showMsdpVRFSaCache = '''
    RP/0/0/CPU0:XR5#show msdp vrf VRF1 sa-cache

    MSDP Flags:
    E - set MRIB E flag , L - domain local source is active,
    EA - externally active source, PI - PIM is interested in the group,
    DE - SAs have been denied.    Timers age/expiration,
    Cache Entry:
    (10.1.1.10, 239.1.1.1), RP 192.168.1.1, MBGP/AS 200, 00:01:02/00:01:32
        Learned from peer 192.168.1.1, RPF peer 192.168.1.1
        SAs recvd 2, Encapsulated data received: 0
        grp flags: PI,    src flags: E, EA, PI
        
    '''

    # show msdp statistics peer
    showMsdpStatisticsPeer = '''
    P/0/0/CPU0:R2_xrvr#show msdp statistics peer 
    Fri Jun 16 15:52:01.005 UTC
    
    MSDP Peer Statistics :- default
    Peer 10.64.4.4 : AS is 200, State is Connect, 0 active SAs
        TLV Rcvd : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses, 0 unknowns
        TLV Sent : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses
        SA msgs  : 0 received, 0 sent
    '''

    # show msdp vrf VRF1 statistics peer
    showMsdpVRFStatisticsPeer = '''
    RP/0/0/CPU0:R2_xrvr#show msdp vrf VRF1 statistics peer 
    Fri Jun 16 15:52:06.775 UTC
    
    MSDP Peer Statistics :- VRF1
    Peer 10.4.1.1 : AS is 0, State is Listen, 0 active SAs
        TLV Rcvd : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses, 0 unknowns
        TLV Sent : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses
        SA msgs  : 0 received, 0 sent
    Peer 10.229.11.11 : AS is 0, State is Listen, 0 active SAs
        TLV Rcvd : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses, 0 unknowns
        TLV Sent : 0 total
                   0 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses
        SA msgs  : 0 received, 0 sent
    '''

    # show msdp vrf VRF1 statistics peer 10.4.1.1
    showMsdpVRFStatisticsPeerArg = '''
     +++ Device: executing command 'show msdp vrf VRF1 statistics peer 10.4.1.1' +++
    show msdp vrf VRF1 statistics peer 10.4.1.1
    Fri Nov 22 19:28:49.882 UTC
    MSDP Peer Statistics :- VRF1
    Peer 10.4.1.1 : AS is 65000, State is Established, 3 active SAs
        TLV Rcvd : 2191 total
                   1 keepalives, 0 notifications
                   2190 SAs, 0 SA Requests
                   0 SA responses, 0 unknowns
        TLV Sent : 4085 total
                   4085 keepalives, 0 notifications
                   0 SAs, 0 SA Requests
                   0 SA responses
        SA msgs  : 6570 received, 0 sent
    RP/0/RP0/CPU0:Device#'''

    # show vrf all detail:
    showVrfAllDetail = {
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
                 'GigabitEthernet0/0/0/1',
                 'GigabitEthernet0/0/0/0.415',
                 'GigabitEthernet0/0/0/0.420',
                 'GigabitEthernet0/0/0/1.390',
                 'GigabitEthernet0/0/0/1.410',
                 'GigabitEthernet0/0/0/1.415',
                 'GigabitEthernet0/0/0/1.420'
            ]
            },
    }

    showMsdpVrfDefaultOutput = {
    'vrf': {
        'default': {
            'global': {
                'default_peer': {
                    'peer_addr': '0.0.0.0',
                },
                'originating_rp': 'Loopback150',
                'sa_limit': 20000,
                'ttl_threshold': 2,
            },
            'peer': {
                '192.168.229.3': {
                    'elapsed_time': '00:00:09',
                    'peer_as': 65109,
                    'sa_filter': {
                        'in': 'none',
                        'out': 'none',
                    },
                    'session_state': 'inactive',
                    'statistics': {
                        'queue': {
                            'size_in': 0,
                            'size_out': 0,
                        },
                    },
                    'timer': {
                        'holdtime_interval': 75,
                        'keepalive_interval': 30,
                    },
                    'ttl_threshold': 2,
                },
                '10.64.4.4': {
                    'peer_as': 200,
                    'session_state': 'established',
                    'statistics': {
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                },
            },
            'sa_cache': {
                '239.1.1.1 10.1.1.10': {
                    'expire': '00:01:32',
                    'group': '239.1.1.1',
                    'origin_rp': {
                        '192.168.1.1': {
                            'rp_address': '192.168.1.1',
                        },
                    },
                    'peer_learned_from': '192.168.1.1',
                    'rpf_peer': '192.168.1.1',
                    'source_addr': '10.1.1.10',
                    'up_time': '00:01:02',
                },
            },
        },
    },
}

    showMsdpVrfOpsOutput = {
    'vrf': {
        'VRF1': {
            'global': {
                'connect_source': 'Loopback3',
                'default_peer': {
                    'peer_addr': '0.0.0.0',
                },
                'originating_rp': 'Loopback3',
                'sa_filter': {
                    'in': 'safilin',
                    'out': 'safilout',
                },
                'sa_limit': 20000,
                'ttl_threshold': 222,
            },
            'peer': {
                '10.4.1.1': {
                    'description': 'R1',
                    'elapsed_time': '18:19:47',
                    'peer_as': 0,
                    'sa_filter': {
                        'in': 'safilin',
                        'out': 'safilout',
                    },
                    'session_state': 'listen',
                    'statistics': {
                        'queue': {
                            'size_in': 0,
                            'size_out': 0,
                        },
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                    'timer': {
                        'holdtime_interval': 75,
                        'keepalive_interval': 30,
                    },
                    'ttl_threshold': 222,
                },
                '10.229.11.11': {
                    'peer_as': 0,
                    'session_state': 'listen',
                    'statistics': {
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                },
            },
            'sa_cache': {
                '239.1.1.1 10.1.1.10': {
                    'expire': '00:01:32',
                    'group': '239.1.1.1',
                    'origin_rp': {
                        '192.168.1.1': {
                            'rp_address': '192.168.1.1',
                        },
                    },
                    'peer_learned_from': '192.168.1.1',
                    'rpf_peer': '192.168.1.1',
                    'source_addr': '10.1.1.10',
                    'up_time': '00:01:02',
                },
            },
        },
    },
}

    showMsdpVrfLoopsOutput = {
    'vrf': {
        'VRF1': {
            'global': {
                'connect_source': 'Loopback3',
                'default_peer': {
                    'peer_addr': '0.0.0.0',
                },
                'originating_rp': 'Loopback3',
                'sa_filter': {
                    'in': 'safilin',
                    'out': 'safilout',
                },
                'sa_limit': 20000,
                'ttl_threshold': 222,
            },
            'peer': {
                '10.4.1.1': {
                    'description': 'R1',
                    'elapsed_time': '18:19:47',
                    'peer_as': 0,
                    'sa_filter': {
                        'in': 'safilin',
                        'out': 'safilout',
                    },
                    'session_state': 'listen',
                    'statistics': {
                        'queue': {
                            'size_in': 0,
                            'size_out': 0,
                        },
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                    'timer': {
                        'holdtime_interval': 75,
                        'keepalive_interval': 30,
                    },
                    'ttl_threshold': 222,
                },
                '10.229.11.11': {
                    'peer_as': 0,
                    'session_state': 'listen',
                    'statistics': {
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                },
            },
            'sa_cache': {
                '239.1.1.1 10.1.1.10': {
                    'expire': '00:01:32',
                    'group': '239.1.1.1',
                    'origin_rp': {
                        '192.168.1.1': {
                            'rp_address': '192.168.1.1',
                        },
                    },
                    'peer_learned_from': '192.168.1.1',
                    'rpf_peer': '192.168.1.1',
                    'source_addr': '10.1.1.10',
                    'up_time': '00:01:02',
                },
            },
        },
        'default': {
            'global': {
                'default_peer': {
                    'peer_addr': '0.0.0.0',
                },
                'originating_rp': 'Loopback150',
                'sa_limit': 20000,
                'ttl_threshold': 2,
            },
            'peer': {
                '192.168.229.3': {
                    'elapsed_time': '00:00:09',
                    'peer_as': 65109,
                    'sa_filter': {
                        'in': 'none',
                        'out': 'none',
                    },
                    'session_state': 'inactive',
                    'statistics': {
                        'queue': {
                            'size_in': 0,
                            'size_out': 0,
                        },
                    },
                    'timer': {
                        'holdtime_interval': 75,
                        'keepalive_interval': 30,
                    },
                    'ttl_threshold': 2,
                },
                '10.64.4.4': {
                    'peer_as': 200,
                    'session_state': 'established',
                    'statistics': {
                        'received': {
                            'sa_message': 0,
                            'total': 0,
                        },
                        'sent': {
                            'sa_message': 0,
                            'sa_response': 0,
                        },
                    },
                },
            },
            'sa_cache': {
                '239.1.1.1 10.1.1.10': {
                    'expire': '00:01:32',
                    'group': '239.1.1.1',
                    'origin_rp': {
                        '192.168.1.1': {
                            'rp_address': '192.168.1.1',
                        },
                    },
                    'peer_learned_from': '192.168.1.1',
                    'rpf_peer': '192.168.1.1',
                    'source_addr': '10.1.1.10',
                    'up_time': '00:01:02',
                },
            },
        },
    },
}

    showMsdpVrf1PeerArgOutput = {
    'vrf': {
        'VRF1': {
            'global': {
                'connect_source': 'Loopback3',
                'default_peer': {
                    'peer_addr': '0.0.0.0',
                },
                'originating_rp': 'Loopback3',
                'sa_filter': {
                    'in': 'safilin',
                    'out': 'safilout',
                },
                'sa_limit': 20000,
                'ttl_threshold': 222,
            },
            'peer': {
                '10.4.1.1': {
                    'elapsed_time': '1d09h',
                    'peer_as': 65000,
                    'sa_filter': {
                        'in': 'none',
                        'out': 'none',
                    },
                    'statistics': {
                        'queue': {
                            'size_in': 0,
                            'size_out': 0,
                        },
                        'received': {
                            'sa_message': 6570,
                            'total': 2191,
                        },
                        'sent': {
                            'sa_response': 0,
                            'sa_message': 0,
                        },
                    },
                    'timer': {
                        'holdtime_interval': 75,
                        'keepalive_interval': 30,
                    },
                    'ttl_threshold': 2,
                },
            },
            'sa_cache': {
                '239.1.1.1 10.1.1.10': {
                    'expire': '00:01:32',
                    'group': '239.1.1.1',
                    'origin_rp': {
                        '192.168.1.1': {
                            'rp_address': '192.168.1.1',
                        },
                    },
                    'peer_learned_from': '192.168.1.1',
                    'rpf_peer': '192.168.1.1',
                    'source_addr': '10.1.1.10',
                    'up_time': '00:01:02',
                },
            },
        },
    },
}