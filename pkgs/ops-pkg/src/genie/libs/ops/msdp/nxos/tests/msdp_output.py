'''
 Msdp Genie Ops Object Outputs for NXOS.
'''

class MsdpOutput(object):
    # 'show ip msdp peer vrf all' output
    showIpMsdpPeerVrf = '''\
    R3_titatnium# show ip msdp peer vrf all
    MSDP peer 10.4.1.1 for VRF "default"
    AS 100, local address: 10.36.3.3 (loopback0)
      Description: R1
      Connection status: Established
        Uptime(Downtime): 01:27:25
        Last reset reason: Keepalive timer expired
        Password: not set
      Keepalive Interval: 60 sec
      Keepalive Timeout: 90 sec
      Reconnection Interval: 33 sec
      Policies:
        SA in: none, SA out: none
        SA limit: 111
      Member of mesh-group: 1
      Statistics (in/out):
        Last messaged received: 00:00:22
        SAs: 0/0, SA-Requests: 0/0, SA-Responses: 0/0
        In/Out Ctrl Msgs: 0/0, In/Out Data Msgs: 0/0
        Remote/Local Port 26743/639
        Keepalives: 92/119, Notifications: 0/6
        RPF check failures: 0
        Cache Lifetime: 00:03:30
        Established Transitions: 6
        Connection Attempts: 0
        Discontinuity Time: 01:27:25

    MSDP peer 10.94.44.44 for VRF "VRF1"
    AS 200, local address: 10.21.33.34 (loopback3)
      Description: R4
      Connection status: Inactive, Connecting in: 00:00:23
        Uptime(Downtime): 01:03:22
        Password: not set
      Keepalive Interval: 60 sec
      Keepalive Timeout: 90 sec
      Reconnection Interval: 44 sec
      Policies:
        SA in: none, SA out: none
        SA limit: 44
      Member of mesh-group: 2
      Statistics (in/out):
        Last messaged received: never
        SAs: 0/0, SA-Requests: 0/0, SA-Responses: 0/0
        In/Out Ctrl Msgs: 0/0, In/Out Data Msgs: 0/0
        Remote/Local Port 0/0
        Keepalives: 0/0, Notifications: 0/0
        RPF check failures: 0
        Cache Lifetime: 00:03:30
        Established Transitions: 0
        Connection Attempts: 88
        Discontinuity Time: 00:00:20
    '''
    # 'show ip msdp sa-cache detail vrf' output
    showIpMsdpSaCacheDetailVrf = '''\

    nexus# show ip msdp sa-cache detail vrf all
    MSDP SA Route Cache for VRF "default" - 1 entries
    Source          Group            RP               ASN         Uptime
    172.16.25.2       228.1.1.1        10.106.106.106   100         00:02:43
        Peer: 10.106.106.106, Expires: 00:02:32
    '''

    # show ip msdp policy statistics sa-policy 10.4.1.1 in
    ShowIpMsdpPolicyStatisticsSaPolicyIn = '''\
    N95_2_R2# show ip msdp policy statistics sa-policy 10.4.1.1 in 
    C: No. of comparisions, M: No. of matches

    route-map filtera permit 10
      match ip address mcast-all-groups                          C: 0      M: 0     
    route-map filtera permit 20
      match ip address mcast-all-groups2                         C: 0      M: 0     

    Total accept count for policy: 0     
    Total reject count for policy: 0  
     '''

    # show ip msdp policy statistics sa-policy 10.4.1.1 in Vrf VRF1
    ShowIpMsdpPolicyStatisticsSaPolicyInVRF1 = '''\
        R4# show ip msdp policy statistics sa-policy 10.94.44.44 in Vrf VRF1
        No SA input policy set for this peer
     '''

    # show ip msdp policy statistics sa-policy 10.4.1.1 out
    ShowIpMsdpPolicyStatisticsSaPolicyOut = '''\
    N95_2_R2# show ip msdp policy statistics sa-policy 10.4.1.1 out
    C: No. of comparisions, M: No. of matches

    route-map filtera permit 10
      match ip address mcast-all-groups                          C: 0      M: 0     
    route-map filtera permit 20
      match ip address mcast-all-groups2                         C: 0      M: 0     

    Total accept count for policy: 0     
    Total reject count for policy: 0
     '''

    # show ip msdp policy statistics sa-policy 10.4.1.1 out Vrf VRF1
    ShowIpMsdpPolicyStatisticsSaPolicyOutVRF1 = '''\
        R4# show ip msdp policy statistics sa-policy 10.94.44.44 out Vrf VRF1
        No SA input policy set for this peer
     '''

    # show ip msdp summary
    ShowIpMsdpSummary = '''\
    N95_2_R2# show ip msdp summary vrf all
    MSDP Peer Status Summary for VRF "default"
    Local ASN: 0, originator-id: 10.16.2.2

    Number of configured peers:  1
    Number of established peers: 1
    Number of shutdown peers:    0

    Peer            Peer        Connection      Uptime/   Last msg  (S,G)s
    Address         ASN         State           Downtime  Received  Received
    10.4.1.1         0           Established     05:46:19  00:00:51  1
     '''

    # show ip msdp summary Vrf VRF1
    ShowIpMsdpSummaryVRF1 = '''\
    N95_2_R2# show ip msdp summary 

    MSDP Peer Status Summary for VRF "VRF1"
    Local ASN: 0, originator-id: 10.16.2.2

    Number of configured peers:  1
    Number of established peers: 1
    Number of shutdown peers:    0

    Peer            Peer        Connection      Uptime/   Last msg  (S,G)s
    Address         ASN         State           Downtime  Received  Received
    10.94.44.44     0           Established     05:46:18  00:00:55  0
     '''

    showOpsOutput={
        "vrf": {
          "VRF1": {
               "global": {
                    "originator_id": "10.16.2.2",
                    "statistics": {
                         "num_of_configured_peers": 1,
                         "num_of_established_peers": 1,
                         "num_of_shutdown_peers": 0
                    },
                    "local_as": 0
               },
               "peer": {
                    "10.94.44.44": {
                         "timer": {
                              "holdtime_interval": 90,
                              "connect_retry_interval": 44,
                              "keepalive_interval": 60
                         },
                         "statistics": {
                              "last_message_received": "00:00:55",
                              "error": {
                                   "rpf_failure": "0"
                              },
                              "discontinuity_time": "00:00:20",
                              "num_of_sg_received": 0,
                              "sent": {
                                   "keepalive": 0,
                                   "total": 0,
                                   "sa_request": 0,
                                   "sa_response": 0,
                                   "notification": 0
                              },
                              "received": {
                                   "keepalive": 0,
                                   "total": 0,
                                   "sa_request": 0,
                                   "sa_response": 0,
                                   "notification": 0
                              }
                         },
                         "sa_limit": "44",
                         "enable": False,
                         "description": "R4",
                         "session_state": "inactive",
                         "peer_as": "200",
                         "elapsed_time": "01:03:22",
                         "mesh_group": "2",
                         "connect_source": "loopback3"
                    }
               }
          },
          "default": {
               "sa_cache": {
                    "228.1.1.1 172.16.25.2": {
                         "up_time": "00:02:43",
                         "group": "228.1.1.1",
                         "peer_learned_from": "10.106.106.106",
                         "source_addr": "172.16.25.2",
                         "expire": "00:02:32",
                         "origin_rp": {
                              "10.106.106.106": {
                                   "rp_address": "10.106.106.106"
                              }
                         }
                    }
               },
               "global": {
                    "originator_id": "10.16.2.2",
                    "statistics": {
                         "num_of_configured_peers": 1,
                         "num_of_established_peers": 1,
                         "num_of_shutdown_peers": 0
                    },
                    "local_as": 0
               },
               "peer": {
                    "10.4.1.1": {
                         "timer": {
                              "holdtime_interval": 90,
                              "connect_retry_interval": 33,
                              "keepalive_interval": 60
                         },
                         "statistics": {
                              "last_message_received": "00:00:51",
                              "error": {
                                   "rpf_failure": "0"
                              },
                              "discontinuity_time": "01:27:25",
                              "num_of_sg_received": 1,
                              "sa_policy": {
                                   "in": {
                                        "total_reject_count": 0,
                                        "total_accept_count": 0,
                                        "filtera": {
                                             "route-map filtera permit 10 match ip address mcast-all-groups": {
                                                  "num_of_comparison": 0,
                                                  "num_of_matches": 0
                                             },
                                             "route-map filtera permit 20 match ip address mcast-all-groups2": {
                                                  "num_of_comparison": 0,
                                                  "num_of_matches": 0
                                             }
                                        }
                                   },
                                   "out": {
                                        "total_reject_count": 0,
                                        "total_accept_count": 0,
                                        "filtera": {
                                             "route-map filtera permit 10 match ip address mcast-all-groups": {
                                                  "num_of_comparison": 0,
                                                  "num_of_matches": 0
                                             },
                                             "route-map filtera permit 20 match ip address mcast-all-groups2": {
                                                  "num_of_comparison": 0,
                                                  "num_of_matches": 0
                                             }
                                        }
                                   }
                              },
                              "sent": {
                                   "keepalive": 119,
                                   "total": 0,
                                   "sa_request": 0,
                                   "sa_response": 0,
                                   "notification": 6
                              },
                              "received": {
                                   "keepalive": 92,
                                   "total": 0,
                                   "sa_request": 0,
                                   "sa_response": 0,
                                   "notification": 0
                              }
                         },
                         "sa_limit": "111",
                         "enable": True,
                         "description": "R1",
                         "session_state": "established",
                         "peer_as": "100",
                         "elapsed_time": "01:27:25",
                         "mesh_group": "1",
                         "connect_source": "loopback0"
                    }
               }
          }
        }
    }


