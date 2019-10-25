''' 
BGP Genie Ops Object Outputs for IOSXR.
'''

import xml.etree.ElementTree as ET

class BgpOutput(object):

    ############################################################################
    #                               BGP INFO
    ############################################################################

    ShowBgpInstances = {
        "instance": {
            "test1": {
                 "num_vrfs": 0,
                 "instance_id": 1,
                 "placed_grp": "bgp2_1",
                 "bgp_id": 333
            },
            "default": {
                 "num_vrfs": 2,
                 "instance_id": 3,
                 "address_families": [
                      "ipv4 unicast",
                      "vpnv4 unicast",
                      "ipv6 unicast",
                      "vpnv6 unicast"
                 ],
                 "placed_grp": "bgp4_1",
                 "bgp_id": 100
            },
            "test": {
                 "num_vrfs": 0,
                 "instance_id": 0,
                 "placed_grp": "v4_routing",
                 "bgp_id": 333
            },
            "test2": {
                 "num_vrfs": 0,
                 "instance_id": 2,
                 "placed_grp": "bgp3_1",
                 "bgp_id": 333}}}

    ShowPlacementProgramAll = {
        'program': 
            {'rcp_fs':
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'central-services',
                        'jid': '1168',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'bgp': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v4-routing',
                        'jid': '1018',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'ospf': 
                {'instance':
                    {'1':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v4-routing',
                        'jid': '1018',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'statsd_manager_g': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'netmgmt',
                        'jid': '1141',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'pim': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'mcast-routing',
                        'jid': '1158',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}},
            'ipv6_local': 
                {'instance':
                    {'default':
                        {'active': '0/0/CPU0',
                        'active_state': 'RUNNING',
                        'group': 'v6-routing',
                        'jid': '1156',
                        'standby': 'NONE',
                        'standby_state': 'NOT_SPAWNED'}}}}
        }

    ShowBgpInstanceSessionGroupConfiguration = {
        "default": {
            "peer_session": {
                "SG": {
                    "remote_as": 333,
                    "fall_over_bfd": True,
                    "password_text": "094F471A1A0A464058",
                    "holdtime": 30,
                    "transport_connection_mode": "active-only",
                    "ebgp_multihop_max_hop": 254,
                    "local_replace_as": True,
                    "ps_minimum_holdtime": 3,
                    "keepalive_interval": 10,
                    "shutdown": True,
                    "local_dual_as": True,
                    "local_no_prepend": True,
                    "ebgp_multihop_enable": True,
                    "suppress_four_byte_as_capability": True,
                    "local_as_as_no": 200,
                    "description": "SG_group",
                    "update_source": 'loopback0',
                    "disable_connected_check": True
                    }
                }
            }
        }

    ShowBgpInstanceAfGroupConfiguration = {
        "instance": {
            "default": {
                "pp_name": {
                    "af_group": {
                        "address_family": "ipv4 unicast",
                        "default_originate": True,
                        "default_originate_route_map": "allpass",
                        "maximum_prefix_max_prefix_no": 429,
                        "maximum_prefix_threshold": 75,
                        "maximum_prefix_restart": 35,
                        "next_hop_self": True,
                        "route_map_name_in": "allpass",
                        "route_map_name_out": "allpass",
                        "route_reflector_client": True,
                        "send_community": "both",
                        "send_comm_ebgp": True,
                        "send_ext_comm_ebgp": True,
                        "soo": "100:1",
                        "soft_reconfiguration": "inbound always",
                        "allowas_in_as_number": 10,
                        "allowas_in": True,
                        "as_override": True
                        }
                    }
                }
            }
        }

    # =====================
    # Process Detail Output
    # =====================

    # 'all all all'
    ProcessAllOutput = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all all all process detail 

        BGP instance 0: 'default'
        =========================

        BGP Process Information: 
        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.4.1.1 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 3, Node: node0_RSP1_CPU0
        Restart count: 32
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               

                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        Address family: VPNv4 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
        Maximum supported label-stack depth:
           For IPv4 Nexthop: 0
           For IPv6 Nexthop: 0
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           18        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.885   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.887   3           3           18        
                           Total triggers: 3
                  
                              Allocated       Freed         
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
                  
        Local Prefixes:       0               0             
        Local Paths:          0               0             
                  
                              Number          Mem Used      
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
        Remote RDs:           0               0             
                  
        Local Prefixes:       0               0             
        Local Paths:          0               0             
        Local RDs:            2               160           
                  
        Total Prefixes:       0               0             
        Total Paths:          0               0             
        Total Path-elems:     0               0             
        Imported Paths:       0               0             
        Total RDs:            2               160           
                  
                  
        Address family: VPNv6 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 0
        RIB has not converged: version 0
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
        Maximum supported label-stack depth:
           For IPv4 Nexthop: 0
           For IPv6 Nexthop: 0
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.883   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.890   3           3           19        
                           Total triggers: 3
                  
                              Allocated       Freed         
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
                  
        Local Prefixes:       0               0             
        Local Paths:          0               0             
                  
                              Number          Mem Used      
        Remote Prefixes:      0               0             
        Remote Paths:         0               0             
        Remote Path-elems:    0               0             
        Remote RDs:           0               0             
                  
        Local Prefixes:       0               0             
        Local Paths:          0               0             
        Local RDs:            2               160           
                  
        Total Prefixes:       0               0             
        Total Paths:          0               0             
        Total Path-elems:     0               0             
        Imported Paths:       0               0             
        Total RDs:            2               160           
                  
                  
        Address family: IPv4 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 2
        Table version synced to RIB: 2
        Table version acked by RIB: 2
        IGP notification: IGPs notified
        RIB has converged: version 4
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 2
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Total triggers: 0
                  
        Import Thread      Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.885   2           2           18        
                           Aug 18 12:00:08.881   0           2           18        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.885   2           2           4         
                           Aug 18 12:00:08.885   2           2           18        
                           Aug 18 12:00:08.882   1           2           4         
                           Aug 18 12:00:08.881   1           2           6         
                           Total triggers: 5
                  
        Update Thread      Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.885   2           2           4         
                           Aug 18 12:00:08.885   2           2           18        
                           Aug 18 12:00:08.884   2           2           18        
                           Aug 18 11:55:08.888   1           2           3         
                           Aug 18 11:55:08.883   1           2           9         
                           Total triggers: 6
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             
                  
                  
        Address family: IPv6 Unicast
        Dampening is not enabled
        Client reflection is enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 2
        Table version synced to RIB: 2
        Table version acked by RIB: 2
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 2
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Total triggers: 0
                  
        Import Thread      Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.886   2           2           19        
                           Aug 18 12:00:08.882   0           2           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.886   2           2           19        
                           Aug 18 12:00:08.882   1           2           4         
                           Aug 18 12:00:08.882   1           2           6         
                           Total triggers: 4
                  
        Update Thread      Aug 18 12:00:11.883   2           2           3         
                           Aug 18 12:00:08.886   2           2           19        
                           Aug 18 12:00:08.886   2           2           19        
                           Aug 18 12:00:08.882   1           2           4         
                           Aug 18 11:55:08.888   1           2           3         
                           Aug 18 11:55:08.883   1           2           9         
                           Total triggers: 6
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0
        '''

    # 'all vrf all ipv4 unicast'
    ProcessIpv4Output = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv4 unicast process detail 

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP Process Information: VRF VRF1
        BGP Route Distinguisher: 200:1

        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 3, Node: node0_RSP1_CPU0
        Restart count: 32
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               
                  
                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF1 Address family: IPv4 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        IGP notification: IGPs notified
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           18        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.885   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.887   3           3           18        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             
                  
                  
        VRF: VRF2 
        --------- 
                  
        BGP Process Information: VRF VRF2
        BGP Route Distinguisher: 200:2
                  
        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60
                  
        BGP Speaker process: 3, Node: node0_RSP1_CPU0
        Restart count: 32
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2
                  
                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               
                  
                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF2 Address family: IPv4 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        IGP notification: IGPs notified
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.887   3           3           18        
                           Aug 18 12:00:08.885   0           3           18        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.885   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.887   3           3           8         
                           Aug 18 12:00:08.887   3           3           18        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0
        '''

    # 'all vrf all ipv6 unicast'
    ProcessIpv6Output = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv6 unicast process detail 

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP Process Information: VRF VRF1
        BGP Route Distinguisher: 200:1

        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60

        BGP Speaker process: 3, Node: node0_RSP1_CPU0
        Restart count: 32
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2

                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               
                  
                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF1 Address family: IPv6 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.883   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.890   3           3           19        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0             
                  
                  
        VRF: VRF2 
        --------- 
                  
        BGP Process Information: VRF VRF2
        BGP Route Distinguisher: 200:2
                  
        BGP is operating in STANDALONE mode
        Autonomous System number format: ASPLAIN
        Autonomous System: 100
        Router ID: 10.229.11.11 (manually configured)
        Default Cluster ID: 10.4.1.1
        Active Cluster IDs:  10.4.1.1
        Fast external fallover enabled
        Platform RLIMIT max: 2281701376 bytes
        Maximum limit for BMP buffer size: 435 MB
        Default value for BMP buffer size: 326 MB
        Current limit for BMP buffer size: 326 MB
        Current utilization of BMP buffer limit: 0 B
        Neighbor logging is enabled
        Enforce first AS enabled
        iBGP to IGP redistribution enabled
        Default local preference: 100
        Default keepalive: 60
        Non-stop routing is enabled
        Update delay: 120
        Generic scan interval: 60
                  
        BGP Speaker process: 3, Node: node0_RSP1_CPU0
        Restart count: 32
                                   Total           Nbrs Estab/Cfg
        Default VRFs:              1               0/3
        Non-Default VRFs:          2               0/4
        This VRF:                                  0/2
                  
                                   Sent            Received
        Updates:                   0               0               
        Notifications:             0               0               
                  
                                   Number          Memory Used
        Attributes:                0               0               
        AS Paths:                  0               0               
        Communities:               0               0               
        Large Communities:         0               0               
        Extended communities:      0               0               
        PMSI Tunnel attr:          0               0               
        RIBRNH Tunnel attr:        0               0               
        PPMP attr:                 0               0               
        Tunnel Encap attr:         0               0               
        PE distinguisher labels:   0               0               
        Route Reflector Entries:   0               0               
        Nexthop Entries:           27              10800           
                  
                                   Alloc           Free          
        Pool 200:                  0               0             
        Pool 300:                  1               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5000:                 0               0             
        Pool 20000:                0               0             
                  
        Message logging pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 500:                  0               0             
        Pool 2200:                 0               0             
        Pool 4500:                 0               0             
                  
        BMP pool summary:
                                   Alloc           Free          
        Pool 100:                  0               0             
        Pool 200:                  0               0             
        Pool 300:                  0               0             
        Pool 400:                  0               0             
        Pool 500:                  0               0             
        Pool 600:                  0               0             
        Pool 700:                  0               0             
        Pool 800:                  0               0             
        Pool 900:                  0               0             
        Pool 1200:                 0               0             
        Pool 2200:                 0               0             
        Pool 3300:                 0               0             
        Pool 4000:                 0               0             
        Pool 4500:                 0               0             
        Pool 5500:                 0               0             
        Pool 6500:                 0               0             
        Pool 7500:                 0               0             
        Pool 8500:                 0               0             
        Pool 10000:                0               0             
        Pool 20000:                0               0             
                  
        VRF VRF2 Address family: IPv6 Unicast
        Dampening is not enabled
        Client reflection is not enabled in global config
        Dynamic MED is Disabled
        Dynamic MED interval : 10 minutes
        Dynamic MED Timer : Not Running
        Dynamic MED Periodic Timer : Not Running
        Scan interval: 60
        Total prefixes scanned: 0
        Prefixes scanned per segment: 100000
        Number of scan segments: 1
        Nexthop resolution minimum prefix-length: 0 (not configured)
        Main Table Version: 3
        Table version synced to RIB: 3
        Table version acked by RIB: 3
        RIB has converged: version 2
        RIB table prefix-limit reached ?  [No], version 0
        Permanent Network Unconfigured
                  
        State: Normal mode.
        BGP Table Version: 3
        Attribute download: Disabled
        Label retention timer value 5 mins
        Soft Reconfig Entries: 0
        Table bit-field size : 1 Chunk element size : 3
                  
                           Last 8 Triggers       Ver         Tbl Ver     Trig TID  
                  
        Label Thread       Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           4         
                           Total triggers: 3
                  
        Import Thread      Aug 18 12:00:11.883   3           3           3         
                           Aug 18 12:00:08.890   3           3           19        
                           Aug 18 12:00:08.882   0           3           19        
                           Total triggers: 3
                  
        RIB Thread         Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.883   1           3           8         
                           Aug 18 12:00:08.882   1           3           6         
                           Total triggers: 3
                  
        Update Thread      Aug 18 12:00:11.883   3           3           8         
                           Aug 18 12:00:08.890   3           3           8         
                           Aug 18 12:00:08.890   3           3           19        
                           Total triggers: 3
                  
                                   Allocated       Freed         
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
                  
                                   Number          Mem Used      
        Prefixes:                  0               0             
        Paths:                     0               0             
        Path-elems:                0               0             
        BMP Prefixes:              0               0             
        BMP Paths:                 0               0
        '''    

    # =======================
    # Neighbors Detail Output
    # =======================

    # 'all all all'
    NeighborsAllOutput = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all all all neighbors detail 

        BGP instance 0: 'default'
        =========================

        BGP neighbor is 10.16.2.2
         Remote AS 100, local AS 100, internal link
         Remote router ID 0.0.0.0
         Speaker ID 3
          BGP state = Idle (No route to multi-hop neighbor)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: VPNv4 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 2097152
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Send Multicast Attributes
                  
         For Address Family: VPNv6 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          AIGP is enabled
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Send Multicast Attributes
                  
          Connections established 0; dropped 0
          Local host: 0.0.0.0, Local port: 0, IF Handle: 0x00000000
          Foreign host: 10.16.2.2, Foreign port: 0
          Last reset 00:00:00

        '''

    # 'all vrf all ipv4 unicast'
    NeighborsIpv4Output = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv4 unicast neighbors detail 
        
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP neighbor is 10.1.5.5, vrf VRF1
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
         Speaker ID 3
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: IPv4 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 1048576
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: 0.0.0.0, Local port: 0, IF Handle: 0x00000000
          Foreign host: 10.1.5.5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
                  
        VRF: VRF2 
        --------- 
                  
        BGP neighbor is 10.186.5.5, vrf VRF2
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
         Speaker ID 3
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: IPv4 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Inbound soft reconfiguration allowed (override route-refresh)
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 495
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: 0.0.0.0, Local port: 0, IF Handle: 0x00000000
          Foreign host: 10.186.5.5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
        '''

    # 'all vrf all ipv6 unicast'
    NeighborsIpv6Output = '''\
        RP/0/RSP1/CPU0:PE1#show bgp instance all vrf all ipv6 unicast neighbors detail 

        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------

        BGP neighbor is 2001:db8:1:5::5, vrf VRF1
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
         Speaker ID 3
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: IPv6 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: ::, Local port: 0, IF Handle: 0x00000000
          Foreign host: 2001:db8:1:5::5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
                  
        VRF: VRF2 
        --------- 
                  
        BGP neighbor is 2001:db8:20:1:5::5, vrf VRF2
         Remote AS 200, local AS 100, external link
         Remote router ID 0.0.0.0
         Speaker ID 3
          BGP state = Idle (No best local address found)
          NSR State: None
          Last read 00:00:00, Last read before reset 00:00:00
          Hold time is 180, keepalive interval is 60 seconds
          Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
          Last write 00:00:00, attempted 0, written 0
          Second last write 00:00:00, attempted 0, written 0
          Last write before reset 00:00:00, attempted 0, written 0
          Second last write before reset 00:00:00, attempted 0, written 0
          Last write pulse rcvd  not set last full not set pulse count 0
          Last write pulse rcvd before reset 00:00:00
          Socket not armed for io, not armed for read, not armed for write
          Last write thread event before reset 00:00:00, second last 00:00:00
          Last KA expiry before reset 00:00:00, second last 00:00:00
          Last KA error before reset 00:00:00, KA not sent 00:00:00
          Last KA start before reset 00:00:00, second last 00:00:00
          Precedence: internet
          Non-stop routing is enabled
          Entered Neighbor NSR TCP mode:
            TCP Initial Sync :              ---                
            TCP Initial Sync Phase Two :    ---                
            TCP Initial Sync Done :         ---                
          Enforcing first AS is enabled
          Multi-protocol capability not received
          Message stats:
            InQ depth: 0, OutQ depth: 0
                            Last_Sent               Sent  Last_Rcvd               Rcvd
            Open:           ---                        0  ---                        0
            Notification:   ---                        0  ---                        0
            Update:         ---                        0  ---                        0
            Keepalive:      ---                        0  ---                        0
            Route_Refresh:  ---                        0  ---                        0
            Total:                                     0                             0
          Minimum time between advertisement runs is 0 secs
          Inbound message logging enabled, 3 messages buffered
          Outbound message logging enabled, 3 messages buffered
                  
         For Address Family: IPv6 Unicast
          BGP neighbor version 0
          Update group: 3.1 Filter-group: 3.0  No Refresh request being processed
          Route refresh request: received 0, sent 0
          Policy for incoming advertisements is all-pass
          Policy for outgoing advertisements is all-pass
          0 accepted prefixes, 0 are bestpaths
          Exact no. of prefixes denied : 0.
          Cumulative no. of prefixes denied: 0. 
          Prefix advertised 0, suppressed 0, withdrawn 0
          Maximum prefixes allowed 524288
          Threshold for warning message 75%, restart interval 0 min
          An EoR was not received during read-only mode
          Last ack version 1, Last synced ack version 0
          Outstanding version objects: current 0, max 0
          Additional-paths operation: None
          Advertise routes with local-label via Unicast SAFI
                  
          Connections established 0; dropped 0
          Local host: ::, Local port: 0, IF Handle: 0x00000000
          Foreign host: 2001:db8:20:1:5::5, Foreign port: 0
          Last reset 00:00:00
          External BGP neighbor not directly connected.
        '''

    ############################################################################
    #                              BGP TABLE
    ############################################################################

    # =============
    # AllAll Output
    # =============

    # 'all all all'
    InstanceAllOutput = '''\
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 10.1.1.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.205.1.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.205.1.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 300:1
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        *>i10.205.1.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 40 prefixes, 55 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 32
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 2001:db8:cdc9:121::/64     2001:db8:1:5::5       2219             0 200 33299 51178 47751 {27016} e
        *                     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:144::/64   2001:db8:1:5::5       2219             0 200 33299 51178 47751 {27016} e
        *                     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:169::/64   2001:db8:1:5::5       2219             0 200 33299 51178 47751 {27016} e
        *                     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:190::/64   2001:db8:1:5::5       2219             0 200 33299 51178 47751 {27016} e
        *                     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:1b9::/64   2001:db8:1:5::5       2219             0 200 33299 51178 47751 {27016} e
        *                     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:121::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:144::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:169::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:190::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:1b9::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 2001:db8:cdc9:121::/64     2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:144::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:169::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:190::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *> 2001:db8:cdc9:1b9::/64   2001:db8:20:1:5::5
                                                    2219             0 200 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:121::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:144::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:169::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:190::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:1b9::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 300:1
        *>i2001:db8:31b9:121::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:144::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:169::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:190::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i2001:db8:31b9:1b9::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i                   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e

        Processed 25 prefixes, 35 paths
        '''

    # 'all vrf all ipv4 unicast'
    InstanceIpv4Output = '''\
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:1
        VRF ID: 0x60000001
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000010   RD version: 47
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF1)
        *> 10.1.1.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.1.5.5              2219             0 200 33299 51178 47751 {27016} e
        *                     10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.205.1.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e

        Processed 15 prefixes, 20 paths

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 47
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:2 (default for vrf VRF2)
        *> 10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.3.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.4.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *> 10.1.5.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *>i10.205.1.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.3.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.4.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.205.5.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        *>i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.2.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.3.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.4.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        *>i10.169.5.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e

        Processed 15 prefixes, 15 paths
        '''

    # 'all vrf all ipv6 unicast'
    InstanceIpv6Output = '''\
        '''

    ############################################################################
    #                         BGP ROUTES PER PEER
    ############################################################################

    # ==============
    # Summary Output
    # ==============

    # 'all all all'
    SummaryAllOutput = '''\
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              47         47         47         47          47           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.16.2.2           0   100   11875   11874       47    0    0     1w1d         10


        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 32
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              32         32         32         32          32           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.16.2.2           0   100   11875   11874       32    0    0     1w1d          5
        '''

    # 'all vrf all ipv4'
    SummaryIpv4Output = '''\
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:1
        VRF ID: 0x60000001
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000010   RD version: 47
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              47         47         47         47          47           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        10.1.5.5          0   200   11858   11864       47    0    0     1w1d          5
        '''

    # 'all vrf all ipv6'
    SummaryIpv6Output = '''\
        BGP instance 0: 'default'
        =========================

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 300:1
        VRF ID: 0x50000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000010   RD version: 47
        BGP main routing table version 47
        BGP NSR Initial initsync version 5 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        BGP is operating in STANDALONE mode.


        Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
        Speaker              47         47         47         47          47           0

        Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
        2001:db8:20:1:5::5
                          0   200   11858   11864       47    0    0     1w1d          5
        '''

    # ========================
    # Advertised Routes Output
    # ========================

    # 'all all all'
    AdvertisedAllOutput = '''\
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        Network            Next Hop        From            AS  Path
        Route Distinguisher: 200:1
        10.1.1.0/24        10.4.1.1         10.186.5.5        200 33299 51178 47751 {27016}e
        10.1.2.0/24        10.4.1.1         10.186.5.5        200 33299 51178 47751 {27016}e

        Processed 2 prefixes, 2 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        Network            Next Hop        From            AS  Path
        Route Distinguisher: 200:1
        2001:db8:cdc9:121::/64     10.4.1.1         2001:db8:20:1:5::5
                                                           200 33299 51178 47751 {27017}e
        2001:db8:cdc9:144::/64   10.4.1.1         2001:db8:20:1:5::5
                                                           200 33299 51178 47751 {27016}e

        Processed 2 prefixes, 2 paths
        '''

    # ======================
    # Received Routes Output
    # ======================

    # 'all all all'
    ReceivedAllOutput = '''\
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 10 prefixes, 10 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i2001:db8:31b9:121::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i2001:db8:31b9:1b9::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i2001:db8:a69:484::/64     10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        * i2001:db8:a69:4c9::/64   10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e

        Processed 10 prefixes, 10 paths
        '''

    # 'all vrf all ipv4 unicast'
    ReceivedIpv4Output = '''\
        BGP instance 0: 'default'
        =========================

        VRF: VRF1
        ---------
        BGP VRF VRF1, state: Active
        BGP Route Distinguisher: 200:2
        VRF ID: 0x60000002
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1 (default for vrf VRF2)
        *  10.1.1.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e
        *  10.1.2.0/24        10.186.5.5              2219             0 200 33299 51178 47751 {27016} e

        Processed 2 prefixes, 2 paths
        '''

    # 'all vrf all ipv6 unicast'
    ReceivedIpv6Output = '''\
        BGP instance 0: 'default'
        =========================

        VRF: VRF2
        ---------
        BGP VRF VRF2, state: Active
        BGP Route Distinguisher: 200:3
        VRF ID: 0x50000006
        BGP router identifier 10.229.11.11, local AS number 100
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0xe0000011   RD version: 63
        BGP main routing table version 63
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:2 (default for vrf VRF1)
        *  10.34.1.0/24        10.196.5.5              2219             0 200 33299 51178 47751 {27016} e
        *  10.34.2.0/24        10.196.5.5              2219             0 200 33299 51178 47751 {27016} e

        Processed 2 prefixes, 2 paths
        '''

    # =============
    # Routes Output
    # =============
    
    # 'all all all'
    RoutesAllOutput = '''\
        BGP instance 0: 'default'
        =========================

        Address Family: VPNv4 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i10.169.1.0/24        10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        
        Route Distinguisher: 400:1
        * i10.9.2.0/24        10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        

        Processed 2 prefixes, 2 paths

        Address Family: VPNv6 Unicast
        -----------------------------

        BGP router identifier 10.4.1.1, local AS number 100
        BGP generic scan interval 60 secs
        Non-stop routing is enabled
        BGP table state: Active
        Table ID: 0x0   RD version: 0
        BGP main routing table version 43
        BGP NSR Initial initsync version 11 (Reached)
        BGP NSR/ISSU Sync-Group versions 0/0
        BGP scan interval 60 secs

        Status codes: s suppressed, d damped, h history, * valid, > best
                      i - internal, r RIB-failure, S stale, N Nexthop-discard
        Origin codes: i - IGP, e - EGP, ? - incomplete
           Network            Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1
        * i2001:db8:31b9:121::/64     10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        * i2001:db8:31b9:144::/64   10.64.4.4               2219    100      0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1
        * i2001:db8:a69:484::/64     10.64.4.4               2219    100      0 400 33299 51178 47751 {27016} e
        

        Processed 3 prefixes, 3 paths
        '''

    # ==============
    # BGP Ops Output
    # ==============

    BgpInfo = {
        'instance': 
            {'default': 
                {'bgp_id': 100,
                'peer_policy': 
                    {'af_group': 
                        {'allowas_in': True,
                        'allowas_in_as_number': 10,
                        'as_override': True,
                        'default_originate': True,
                        'default_originate_route_map': 'allpass',
                        'maximum_prefix_max_prefix_no': 429,
                        'maximum_prefix_restart': 35,
                        'maximum_prefix_threshold': 75,
                        'next_hop_self': True,
                        'route_map_name_in': 'allpass',
                        'route_map_name_out': 'allpass',
                        'route_reflector_client': True,
                        'send_community': 'both',
                        'soft_reconfiguration': 'inbound '
                                               'always',
                        'soo': '100:1'}},
                'peer_session': 
                    {'SG': 
                        {'description': 'SG_group',
                        'disable_connected_check': True,
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 254,
                        'fall_over_bfd': True,
                        'holdtime': 30,
                        'keepalive_interval': 10,
                        'local_as_as_no': 200,
                        'local_dual_as': True,
                        'local_no_prepend': True,
                        'local_replace_as': True,
                        'password_text': '094F471A1A0A464058',
                        'remote_as': 333,
                        'shutdown': True,
                        'suppress_four_byte_as_capability': True,
                        'transport_connection_mode': 'active-only',
                        'update_source': 'loopback0'}},
                'protocol_state': 'RUNNING',
                'vrf': 
                    {'default': 
                        {'neighbor': 
                            {'10.16.2.2': 
                                {'bgp_neighbor_counters': 
                                    {'messages': 
                                        {'received': 
                                            {'notifications': 0,
                                            'updates': 0},
                                        'sent': 
                                            {'notifications': 0,
                                            'updates': 0}}},
                                'bgp_session_transport': 
                                    {'transport': 
                                        {'foreign_host': '0',
                                        'foreign_port': '10.16.2.2',
                                        'local_host': 'Loopback0',
                                        'local_port': '0'}},
                                'holdtime': 180,
                                'remote_as': 100,
                                'session_state': 'idle'}},
                        'router_id': '10.4.1.1'}}},
            'test': 
                {'bgp_id': 333},
            'test1': 
                {'bgp_id': 333},
            'test2': 
                {'bgp_id': 333}}}

    BgpTable = {
        'instance': 
            {'default': 
                {'vrf': 
                    {'VRF1': 
                        {'address_family': 
                            {'vpnv4 unicast': 
                                {'bgp_table_version': 47,
                                'local_as': 100},
                            'vpnv4 unicast RD 200:1': 
                                {'default_vrf': 'vrf1',
                                'prefixes': 
                                    {'10.1.1.0/24': 
                                        {'index': 
                                            {1: 
                                                {'metric': '2219',
                                                'next_hop': '10.1.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*>',
                                                'weight': '0'},
                                            2: {'metric': '2219',
                                                'next_hop': '10.186.5.5',
                                                'origin_codes': 'e',
                                                'path': '200 '
                                                        '33299 '
                                                        '51178 '
                                                        '47751 '
                                                        '{27016}',
                                                'status_codes': '*',
                                                'weight': '0'}}},
                                    '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                        'next_hop': '10.1.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>',
                                                                        'weight': '0'},
                                                                    2: {'metric': '2219',
                                                                        'next_hop': '10.186.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*',
                                                                        'weight': '0'}}},
                                          '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                        'next_hop': '10.1.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>',
                                                                        'weight': '0'},
                                                                    2: {'metric': '2219',
                                                                        'next_hop': '10.186.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*',
                                                                        'weight': '0'}}},
                                          '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                        'next_hop': '10.1.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>',
                                                                        'weight': '0'},
                                                                    2: {'metric': '2219',
                                                                        'next_hop': '10.186.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*',
                                                                        'weight': '0'}}},
                                          '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                        'next_hop': '10.1.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>',
                                                                        'weight': '0'},
                                                                    2: {'metric': '2219',
                                                                        'next_hop': '10.186.5.5',
                                                                        'origin_codes': 'e',
                                                                        'path': '200 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*',
                                                                        'weight': '0'}}},
                                          '10.205.1.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '400 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.205.2.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '400 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.205.3.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '400 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.205.4.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '400 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.205.5.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '400 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '300 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '300 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '300 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '300 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}},
                                          '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                        'metric': '2219',
                                                                        'next_hop': '10.64.4.4',
                                                                        'origin_codes': 'e',
                                                                        'path': '300 '
                                                                                '33299 '
                                                                                '51178 '
                                                                                '47751 '
                                                                                '{27016}',
                                                                        'status_codes': '*>i',
                                                                        'weight': '0'}}}},
                                                                                         'route_distinguisher': '200:1'}}},
                                  'VRF2': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 47,
                                                                                'local_as': 100},
                                                              'vpnv4 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                         'prefixes': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                    'next_hop': '10.186.5.5',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '200 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                    'next_hop': '10.186.5.5',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '200 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                    'next_hop': '10.186.5.5',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '200 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                    'next_hop': '10.186.5.5',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '200 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                    'next_hop': '10.186.5.5',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '200 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.205.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '400 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.205.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '400 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.205.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '400 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.205.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '400 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.205.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '400 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '300 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '300 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '300 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '300 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}},
                                                                                                      '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                    'metric': '2219',
                                                                                                                                    'next_hop': '10.64.4.4',
                                                                                                                                    'origin_codes': 'e',
                                                                                                                                    'path': '300 '
                                                                                                                                            '33299 '
                                                                                                                                            '51178 '
                                                                                                                                            '47751 '
                                                                                                                                            '{27016}',
                                                                                                                                    'status_codes': '*>i',
                                                                                                                                    'weight': '0'}}}},
                                                                                         'route_distinguisher': '200:2'}}},
                                  'default': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 47,
                                                                                   'local_as': 100},
                                                                 'vpnv4 unicast RD 200:1': {'default_vrf': 'vrf1',
                                                                                            'prefixes': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.1.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.1.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.1.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.1.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.1.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:1'},
                                                                 'vpnv4 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                            'prefixes': {'10.1.1.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.2.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.3.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.4.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.1.5.0/24': {'index': {1: {'metric': '2219',
                                                                                                                                       'next_hop': '10.186.5.5',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '200 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:2'},
                                                                 'vpnv4 unicast RD 300:1': {'default_vrf': 'none',
                                                                                            'prefixes': {'10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.169.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '300 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}}},
                                                                                            'route_distinguisher': '300:1'},
                                                                 'vpnv4 unicast RD 400:1': {'default_vrf': 'none',
                                                                                            'prefixes': {'10.205.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.3.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.4.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}},
                                                                                                         '10.205.5.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*>i',
                                                                                                                                       'weight': '0'},
                                                                                                                                   2: {'locprf': '100',
                                                                                                                                       'metric': '2219',
                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                       'origin_codes': 'e',
                                                                                                                                       'path': '400 '
                                                                                                                                               '33299 '
                                                                                                                                               '51178 '
                                                                                                                                               '47751 '
                                                                                                                                               '{27016}',
                                                                                                                                       'status_codes': '*i',
                                                                                                                                       'weight': '0'}}}},
                                                                                            'route_distinguisher': '400:1'},
                                                                 'vpnv6 unicast': {'bgp_table_version': 32,
                                                                                   'local_as': 100},
                                                                 'vpnv6 unicast RD 200:1': {'default_vrf': 'vrf1',
                                                                                            'prefixes': {'2001:db8:cdc9:144::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:169::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:190::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:1b9::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:121::/64': {'index': {1: {'metric': '2219',
                                                                                                                                          'next_hop': '2001:db8:1:5::5',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '200 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>',
                                                                                                                                          'weight': '0'}}},
                                                                                                         '2001:db8:31b9:144::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:169::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:190::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:1b9::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:121::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:1'},
                                                                 'vpnv6 unicast RD 200:2': {'default_vrf': 'vrf2',
                                                                                            'prefixes': {'2001:db8:cdc9:144::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:169::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:190::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:1b9::/64': {'index': {1: {'metric': '2219',
                                                                                                                                            'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '200 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:cdc9:121::/64': {'index': {1: {'metric': '2219',
                                                                                                                                          'next_hop': '2001:db8:20:1:5::5',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '200 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>',
                                                                                                                                          'weight': '0'}}},
                                                                                                         '2001:db8:31b9:144::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:169::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:190::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:1b9::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:121::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'}}}},
                                                                                            'route_distinguisher': '200:2'},
                                                                 'vpnv6 unicast RD 300:1': {'default_vrf': 'none',
                                                                                            'prefixes': {'2001:db8:31b9:144::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'},
                                                                                                                                        2: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:169::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'},
                                                                                                                                        2: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:190::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'},
                                                                                                                                        2: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:1b9::/64': {'index': {1: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*>i',
                                                                                                                                            'weight': '0'},
                                                                                                                                        2: {'locprf': '100',
                                                                                                                                            'metric': '2219',
                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                            'origin_codes': 'e',
                                                                                                                                            'path': '300 '
                                                                                                                                                    '33299 '
                                                                                                                                                    '51178 '
                                                                                                                                                    '47751 '
                                                                                                                                                    '{27016}',
                                                                                                                                            'status_codes': '*i',
                                                                                                                                            'weight': '0'}}},
                                                                                                         '2001:db8:31b9:121::/64': {'index': {1: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*>i',
                                                                                                                                          'weight': '0'},
                                                                                                                                      2: {'locprf': '100',
                                                                                                                                          'metric': '2219',
                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                          'origin_codes': 'e',
                                                                                                                                          'path': '300 '
                                                                                                                                                  '33299 '
                                                                                                                                                  '51178 '
                                                                                                                                                  '47751 '
                                                                                                                                                  '{27016}',
                                                                                                                                          'status_codes': '*i',
                                                                                                                                          'weight': '0'}}}},
                                                                                            'route_distinguisher': '300:1'}}}}}}}

    BgpRoutesPerPeer = {
        'instance': {'default': {'vrf': {'VRF1': {'neighbor': {'10.1.5.5': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                          'msg_rcvd': 11858,
                                                                                                          'msg_sent': 11864,
                                                                                                          'output_queue': 0,
                                                                                                          'route_distinguisher': '200:1',
                                                                                                          'state_pfxrcd': '5',
                                                                                                          'tbl_ver': 47,
                                                                                                          'up_down': '1w1d'}},
                                                                     'remote_as': 200}}},
                                  'VRF2': {'neighbor': {'2001:db8:20:1:5::5': {'address_family': {'vpnv6 unicast': {'input_queue': 0,
                                                                                                                    'msg_rcvd': 11858,
                                                                                                                    'msg_sent': 11864,
                                                                                                                    'output_queue': 0,
                                                                                                                    'route_distinguisher': '300:1',
                                                                                                                    'state_pfxrcd': '5',
                                                                                                                    'tbl_ver': 47,
                                                                                                                    'up_down': '1w1d'}},
                                                                               'remote_as': 200}}},
                                  'default': {'neighbor': {'10.16.2.2': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 11875,
                                                                                                            'msg_sent': 11874,
                                                                                                            'output_queue': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 47,
                                                                                                            'up_down': '1w1d'},
                                                                                          'vpnv4 unicast RD 200:1': {'advertised': {'10.1.1.0/24': {'index': {1: {'froms': '10.186.5.5',
                                                                                                                                                                  'next_hop': '10.4.1.1',
                                                                                                                                                                  'origin_code': 'e',
                                                                                                                                                                  'path': '200 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}'}}},
                                                                                                                                    '10.1.2.0/24': {'index': {1: {'froms': '10.186.5.5',
                                                                                                                                                                  'next_hop': '10.4.1.1',
                                                                                                                                                                  'origin_code': 'e',
                                                                                                                                                                  'path': '200 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}'}}}}},
                                                                                          'vpnv4 unicast RD 300:1': {'received_routes': {'10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                                                       'metric': '2219',
                                                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*i',
                                                                                                                                                                       'weight': '0'}}}},
                                                                                                                     'routes': {'10.169.1.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                                              'metric': '2219',
                                                                                                                                                              'next_hop': '10.64.4.4',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '300 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*i',
                                                                                                                                                              'weight': '0'}}}}},
                                                                                          'vpnv4 unicast RD 400:1': {'received_routes': {'10.9.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                                                       'metric': '2219',
                                                                                                                                                                       'next_hop': '10.64.4.4',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '400 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*i',
                                                                                                                                                                       'weight': '0'}}}},
                                                                                                                     'routes': {'10.9.2.0/24': {'index': {1: {'locprf': '100',
                                                                                                                                                              'metric': '2219',
                                                                                                                                                              'next_hop': '10.64.4.4',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '400 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*i',
                                                                                                                                                              'weight': '0'}}}}},
                                                                                          'vpnv6 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 11875,
                                                                                                            'msg_sent': 11874,
                                                                                                            'output_queue': 0,
                                                                                                            'state_pfxrcd': '5',
                                                                                                            'tbl_ver': 32,
                                                                                                            'up_down': '1w1d'},
                                                                                          'vpnv6 unicast RD 200:1': {'advertised': {'2001:db8:cdc9:144::/64': {'index': {1: {'froms': '2001:db8:20:1:5::5',
                                                                                                                                                                       'next_hop': '10.4.1.1',
                                                                                                                                                                       'origin_code': 'e',
                                                                                                                                                                       'path': '200 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}'}}},
                                                                                                                                    '2001:db8:cdc9:121::/64': {'index': {1: {'froms': '2001:db8:20:1:5::5',
                                                                                                                                                                     'next_hop': '10.4.1.1',
                                                                                                                                                                     'origin_code': 'e',
                                                                                                                                                                     'path': '200 '
                                                                                                                                                                             '33299 '
                                                                                                                                                                             '51178 '
                                                                                                                                                                             '47751 '
                                                                                                                                                                             '{27017}'}}}}},
                                                                                          'vpnv6 unicast RD 300:1': {'received_routes': {'2001:db8:31b9:1b9::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                            'metric': '2219',
                                                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                                                            'origin_codes': 'e',
                                                                                                                                                                            'path': '300 '
                                                                                                                                                                                    '33299 '
                                                                                                                                                                                    '51178 '
                                                                                                                                                                                    '47751 '
                                                                                                                                                                                    '{27016}',
                                                                                                                                                                            'status_codes': '*i',
                                                                                                                                                                            'weight': '0'}}},
                                                                                                                                         '2001:db8:31b9:121::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                          'metric': '2219',
                                                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                                                          'origin_codes': 'e',
                                                                                                                                                                          'path': '300 '
                                                                                                                                                                                  '33299 '
                                                                                                                                                                                  '51178 '
                                                                                                                                                                                  '47751 '
                                                                                                                                                                                  '{27016}',
                                                                                                                                                                          'status_codes': '*i',
                                                                                                                                                                          'weight': '0'}}}},
                                                                                                                     'routes': {'2001:db8:31b9:144::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                   'metric': '2219',
                                                                                                                                                                   'next_hop': '10.64.4.4',
                                                                                                                                                                   'origin_codes': 'e',
                                                                                                                                                                   'path': '300 '
                                                                                                                                                                           '33299 '
                                                                                                                                                                           '51178 '
                                                                                                                                                                           '47751 '
                                                                                                                                                                           '{27016}',
                                                                                                                                                                   'status_codes': '*i',
                                                                                                                                                                   'weight': '0'}}},
                                                                                                                                '2001:db8:31b9:121::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                 'metric': '2219',
                                                                                                                                                                 'next_hop': '10.64.4.4',
                                                                                                                                                                 'origin_codes': 'e',
                                                                                                                                                                 'path': '300 '
                                                                                                                                                                         '33299 '
                                                                                                                                                                         '51178 '
                                                                                                                                                                         '47751 '
                                                                                                                                                                         '{27016}',
                                                                                                                                                                 'status_codes': '*i',
                                                                                                                                                                 'weight': '0'}}}}},
                                                                                          'vpnv6 unicast RD 400:1': {'received_routes': {'2001:db8:a69:4c9::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                            'metric': '2219',
                                                                                                                                                                            'next_hop': '10.64.4.4',
                                                                                                                                                                            'origin_codes': 'e',
                                                                                                                                                                            'path': '400 '
                                                                                                                                                                                    '33299 '
                                                                                                                                                                                    '51178 '
                                                                                                                                                                                    '47751 '
                                                                                                                                                                                    '{27016}',
                                                                                                                                                                            'status_codes': '*i',
                                                                                                                                                                            'weight': '0'}}},
                                                                                                                                         '2001:db8:a69:484::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                          'metric': '2219',
                                                                                                                                                                          'next_hop': '10.64.4.4',
                                                                                                                                                                          'origin_codes': 'e',
                                                                                                                                                                          'path': '400 '
                                                                                                                                                                                  '33299 '
                                                                                                                                                                                  '51178 '
                                                                                                                                                                                  '47751 '
                                                                                                                                                                                  '{27016}',
                                                                                                                                                                          'status_codes': '*i',
                                                                                                                                                                          'weight': '0'}}}},
                                                                                                                     'routes': {'2001:db8:a69:484::/64': {'index': {1: {'locprf': '100',
                                                                                                                                                                 'metric': '2219',
                                                                                                                                                                 'next_hop': '10.64.4.4',
                                                                                                                                                                 'origin_codes': 'e',
                                                                                                                                                                 'path': '400 '
                                                                                                                                                                         '33299 '
                                                                                                                                                                         '51178 '
                                                                                                                                                                         '47751 '
                                                                                                                                                                         '{27016}',
                                                                                                                                                                 'status_codes': '*i',
                                                                                                                                                                 'weight': '0'}}}}}},
                                                                       'remote_as': 100}}}}}}}

    # ============
    # GET OPER RPC
    # ============

    class etree_holder():
        def __init__(self):
            self.data_ele = ET.fromstring('''
            <data>
              <bgp xmlns="http://openconfig.net/yang/bgp">
               <global>
                <config>
                 <as>100</as>
                 <router-id>10.4.1.1</router-id>
                </config>
                <state>
                 <as>100</as>
                 <router-id>10.4.1.1</router-id>
                 <total-paths>0</total-paths>
                 <total-prefixes>0</total-prefixes>
                </state>
                <afi-safis>
                 <afi-safi>
                  <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                  <config>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                   <enabled>true</enabled>
                  </config>
                  <state>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                   <enabled>true</enabled>
                   <total-paths>0</total-paths>
                   <total-prefixes>0</total-prefixes>
                  </state>
                 </afi-safi>
                 <afi-safi>
                  <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                  <config>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                   <enabled>true</enabled>
                  </config>
                  <state>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                   <enabled>true</enabled>
                   <total-paths>0</total-paths>
                   <total-prefixes>0</total-prefixes>
                  </state>
                 </afi-safi>
                </afi-safis>
               </global>
               <neighbors>
                <neighbor>
                 <neighbor-address>10.16.2.2</neighbor-address>
                 <config>
                  <neighbor-address>10.16.2.2</neighbor-address>
                  <peer-as>100</peer-as>
                 </config>
                 <state>
                  <neighbor-address>10.16.2.2</neighbor-address>
                  <peer-as>100</peer-as>
                  <queues>
                   <input>0</input>
                   <output>0</output>
                  </queues>
                  <session-state>IDLE</session-state>
                  <messages>
                   <sent>
                    <NOTIFICATION>0</NOTIFICATION>
                    <UPDATE>0</UPDATE>
                   </sent>
                   <received>
                    <NOTIFICATION>0</NOTIFICATION>
                    <UPDATE>0</UPDATE>
                   </received>
                  </messages>
                 </state>
                 <transport>
                  <config>
                   <local-address>Loopback0</local-address>
                  </config>
                  <state>
                   <local-address>Loopback0</local-address>
                   <local-port>0</local-port>
                   <remote-address>10.16.2.2</remote-address>
                   <remote-port>0</remote-port>
                  </state>
                 </transport>
                 <afi-safis>
                  <afi-safi>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                   <config>
                    <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                    <enabled>true</enabled>
                   </config>
                   <state>
                    <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv4-unicast</afi-safi-name>
                    <enabled>true</enabled>
                    <active>false</active>
                    <prefixes>
                     <received>0</received>
                     <sent>0</sent>
                    </prefixes>
                   </state>
                  </afi-safi>
                  <afi-safi>
                   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                   <config>
                    <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                    <enabled>true</enabled>
                   </config>
                   <state>
                    <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:l3vpn-ipv6-unicast</afi-safi-name>
                    <enabled>true</enabled>
                    <active>false</active>
                    <prefixes>
                     <received>0</received>
                     <sent>0</sent>
                    </prefixes>
                   </state>
                  </afi-safi>
                 </afi-safis>
                 <timers>
                  <state>
                   <negotiated-hold-time>180</negotiated-hold-time>
                  </state>
                 </timers>
                 <graceful-restart>
                  <state>
                   <peer-restart-time>120</peer-restart-time>
                  </state>
                 </graceful-restart>
                </neighbor>
               </neighbors>
              </bgp>
             </data>
            ''')

    yang_output = etree_holder()
