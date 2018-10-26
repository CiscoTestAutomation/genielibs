'''
 VxlanConsistency Genie Ops Object Outputs for NXOS.
'''

class VxlanConsistencyOutput(object):

    interface_detail_output = '''\
        CH-P2-TOR-1# sh nve interface nve 1 detail
        Interface: nve1, State: Up, encapsulation: VXLAN
         VPC Capability: VPC-VIP-Only [not-notified]
         Local Router MAC: 00f2.8b7a.f8ff
         Host Learning Mode: Control-Plane
         Source-Interface: loopback1 (primary: 3.0.0.1, secondary: 0.0.0.0)
         Source Interface State: Up
         IR Capability Mode: No
         Virtual RMAC Advertisement: No
         NVE Flags:
         Interface Handle: 0x49000001
         Source Interface hold-down-time: 180
         Source Interface hold-up-time: 30
         Remaining hold-down time: 0 seconds
         Virtual Router MAC: N/A
         Interface state: nve-intf-add-complete
         unknown-peer-forwarding: disable
         down-stream vni config mode: n/a
        Nve Src node last notif sent: None
        Nve Mcast Src node last notif sent: None
        Nve MultiSite Src node last notif sent: None
    '''

    run_config_interface_output = '''\
        CH-P2-TOR-1# sh run int nve 1

        !Command: show running-config interface nve1
        !Time: Wed May 30 07:34:20 2018

        version 7.0(3)I7(4)

        interface nve1
          no shutdown
          host-reachability protocol bgp
          source-interface loopback1
          member vni 2001001
            mcast-group 225.0.1.11
    '''

    run_config_interface_output_empty = '''\
        CH-P2-TOR-1# sh run int nve 1
    '''

    mac_address_table_output = '''\
        CH-P2-TOR-1# show mac address-table vni 2001001 | grep nve1 
        C 1001     0000.0191.0000   dynamic  0         F      F    nve1(4.0.0.3)
    '''

    l2_route_output = '''\
        CH-P2-TOR-1# sh l2route evpn mac evi 1001  mac 0000.0191.0000

        Flags -(Rmac):Router MAC (Stt):Static (L):Local (R):Remote (V):vPC link 
        (Dup):Duplicate (Spl):Split (Rcv):Recv (AD):Auto-Delete (D):Del Pending
        (S):Stale (C):Clear, (Ps):Peer Sync (O):Re-Originated (Nho):NH-Override
        (Pf):Permanently-Frozen

        Topology    Mac Address    Prod   Flags         Seq No     Next-Hops      
        ----------- -------------- ------ ------------- ---------- ----------------
        1001        0000.0191.0000 BGP    SplRcv        19         4.0.0.3    
    '''

    bgp_l2vpn_output = '''\
        CH-P2-TOR-1# sh bgp l2vpn evpn 0000.04b1.0000 | be "best path, in rib"   n 10
          Path type: internal, path is valid, is best path, in rib
                     Imported from 2.0.0.101:33768:[2]:[0]:[0]:[48]:[0000.04b1.0000]:[0]:[0.0.0.0]/216 
          AS-Path: NONE, path sourced internal to AS
            4.0.0.3 (metric 9) from 2.0.0.66 (2.0.0.66)
              Origin IGP, MED not set, localpref 100, weight 0
              Received label 2001001
              Extcommunity: RT:2:2001001 ENCAP:8 MAC Mobility Sequence:00:19
              Originator: 2.0.0.101 Cluster list: 2.0.0.66 

          Path-id 1 not advertised to any peer
        BGP routing table entry for [2]:[0]:[0]:[48]:[0000.04b1.0000]:[32]:[4.32.102.2]/272, version 6768199
        --
          Path type: internal, path is valid, is best path, in rib
                     Imported from 2.0.0.101:33768:[2]:[0]:[0]:[48]:[0000.04b1.0000]:[32]:[4.32.102.2]/272 
          AS-Path: NONE, path sourced internal to AS
            4.0.0.3 (metric 9) from 2.0.0.66 (2.0.0.66)
              Origin IGP, MED not set, localpref 100, weight 0
              Received label 2001001 3003802
              Extcommunity: RT:2:2001001 RT:2:3003802 ENCAP:8 MAC Mobility Sequence:00:2
                  Router MAC:00de.fbdc.5f87
              Originator: 2.0.0.101 Cluster list: 2.0.0.66 

          Path-id 1 not advertised to any peer
    '''

    local_mac_address_table_output = '''\
        CH-P2-TOR-1# sh mac address-table local vni 2001001 
        Legend: 
                * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
                age - seconds since last seen,+ - primary entry using vPC Peer-Link,
                (T) - True, (F) - False, C - ControlPlane MAC, ~ - vsan
           VLAN     MAC Address      Type      age     Secure NTFY Ports
        ---------+-----------------+--------+---------+------+----+------------------
        * 1001     0000.0191.0001   dynamic  0         F      F    Po1
    '''

    local_l2_route_output = '''\
        CH-P2-TOR-1# sh l2route evpn mac evi 1001  mac 0000.0191.0000

        Flags -(Rmac):Router MAC (Stt):Static (L):Local (R):Remote (V):vPC link 
        (Dup):Duplicate (Spl):Split (Rcv):Recv (AD):Auto-Delete (D):Del Pending
        (S):Stale (C):Clear, (Ps):Peer Sync (O):Re-Originated (Nho):NH-Override
        (Pf):Permanently-Frozen

        Topology    Mac Address    Prod   Flags         Seq No     Next-Hops      
        ----------- -------------- ------ ------------- ---------- ----------------
        1001        0000.0191.0001 Local  L,            5          Po1    
    '''

    local_nve_interface_output = '''\
        CH-P2-TOR-1# sh nve interface nve 1 detail | grep Source-Interface
         Source-Interface: loopback0 (primary: 0.0.0.0, secondary: 2.0.0.1)
    '''

    local_bgp_l2vpn_output = '''\
        CH-P2-TOR-1# sh bgp l2vpn evpn 0000.0191.0000 | grep -b 8  -a 10  "best path" 
        BGP routing table information for VRF default, address family L2VPN EVPN
        Route Distinguisher: 2.0.0.1:33768    (L2VNI 2001001)
        BGP routing table entry for [2]:[0]:[0]:[48]:[0000.0191.0000]:[0]:[0.0.0.0]/216, version 6956047
        Paths: (1 available, best #1)
        Flags: (0x000302) (high32 00000000) on xmit-list, is not in l2rib/evpn

          Advertised path-id 1
          Path type: local, path is valid, is best path
          AS-Path: NONE, path locally originated
            2.0.0.1 (metric 0) from 0.0.0.0 (2.0.0.1)
              Origin IGP, MED not set, localpref 100, weight 32768
              Received label 2001001
              Extcommunity: RT:2:2001001 ENCAP:8 MAC Mobility Sequence:00:1

          Path-id 1 advertised to peers:
            2.0.0.66       
        BGP routing table entry for [2]:[0]:[0]:[48]:[0000.0191.0000]:[32]:[4.32.101.2]/272, version 6956019
        Paths: (1 available, best #1)
        Flags: (0x000302) (high32 00000000) on xmit-list, is not in l2rib/evpn

          Advertised path-id 1
          Path type: local, path is valid, is best path
          AS-Path: NONE, path locally originated
            2.0.0.1 (metric 0) from 0.0.0.0 (2.0.0.1)
              Origin IGP, MED not set, localpref 100, weight 32768
              Received label 2001001 3003802
              Extcommunity: RT:2:2001001 RT:2:3003802 ENCAP:8 MAC Mobility Sequence:00:1
                  Router MAC:00f2.8b7a.f8ff

          Path-id 1 advertised to peers:
            2.0.0.66  
    '''

    vxlanConsistencyOutput = {
        'interface': {
            'nve1': {
                'member_vni': {
                    '2001001': {
                        'local': {
                            'mac_address': {
                                '0000.0191.0001': {
                                    'evi': '1001',
                                    'next_hop': 'Po1',
                                    'topology': {
                                        '1001': {
                                            'next_hop': 'Po1',
                                            'prod': 'Local'}
                                    }
                                }
                            },
                            'verified_structure': {
                                'mac_address': {
                                    '0000.0191.0001': {
                                        'next_hop': '2.0.0.1',
                                        'received_label': '2001001'}
                                },
                                'source_interface': {
                                    'loopback1': {
                                        'primary': '3.0.0.1',
                                        'secondary': '0.0.0.0'}
                                },
                                'vpc_capability': {
                                    'VPC-VIP-Only': {'notified': False}
                                }
                            }
                        },
                        'mcast_group': '225.0.1.11',
                        'remote': {
                            'mac_address': {
                                '0000.0191.0000': {
                                    'evi': '1001',
                                    'next_hop': '4.0.0.3',
                                    'topology': {
                                        '1001': {
                                            'next_hop': '4.0.0.3',
                                            'prod': 'BGP'}
                                    }
                                }
                            },
                            'verified_structure': {
                                'mac_address': {
                                    '0000.0191.0000': {
                                        'next_hop': '4.0.0.3',
                                        'received_label': '2001001'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }