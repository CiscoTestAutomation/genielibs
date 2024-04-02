'''
Interface Genie Ops Object Outputs for CHEETAH.
'''

class InterfaceOutput(object):

    showInterfaceWired_0 = '''
     wired0    Link encap:Ethernet  HWaddr 00:EA:BD:12:8E:70 eMac Status: UP
      	  inet addr: 9.6.64.181  Bcast: 9.6.64.255  Mask: 255.255.255.0
                UP BROADCAST RUNNING PROMISC MULTICAST  MTU:2400  Metric:1
                collisions:0 txqueuelen:80 
      	  full Duplex, 1000 Mb/s

      	  5 minute input rate 719323 bits/sec, 87 packets/sec
      	  5 minute output rate 2042 bits/sec, 0 packets/sec
      Wired0 Port Statistics:
      ID         :               2             TYPE       :               0
      RX PKTS    :        24172648/514         TX PKTS    :          262068/1         
      RX OCTETS  :     16727171905/637415      TX OCTETS  :       123668457/318       
      RX ERR     :             236/0           TX ERR     :               0/0
    '''

    showInterfaceWired_1 = '''
    wired1    Link encap:Ethernet  HWaddr 00:EA:BD:12:8E:70 eMac Status: DOWN
      	  inet addr: unassigned  Bcast: 9.6.64.255  Mask: 255.255.255.0
      DOWN BROADCAST RUNNING PROMISC MULTICAST  MTU:0  Metric:0

      	  half Duplex, 0 Mb/s

      	  5 minute input rate n/a bits/sec, n/a packets/sec
      	  5 minute output rate n/a bits/sec, n/a packets/sec
      Wired1 Port Statistics:
      ID         :               1             TYPE       :               0
      RX PKTS    :               0/0           TX PKTS    :            7844/0
      RX OCTETS  :               0/0           TX OCTETS  :         3121792/0
      RX ERR     :               0/0           TX ERR     :               0/0
    '''

    showInterfaceWired_2 = '''
      Invalid interface number, does not exist on AP !
    '''

    showInterfaceWired_3 = '''
        Invalid interface number, does not exist on AP !
    '''

    showInterfaceDot11Radio_0 = '''
    Dot11Radio0 is UP, line protocol is UP
      Hardware is 802.11 2.4G Radio, channel is 11
      Radio MAC is 70:6D:15:C0:87:60

      Dot11Radio0     Link encap:Ethernet  HWaddr 70:6D:15:C0:87:60  
                UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
                RX packets:33456202 errors:0 dropped:0 overruns:0 frame:0
                TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                collisions:0 txqueuelen:1000 
                RX bytes:446267363 (425.5 MiB)  TX bytes:0 (0.0 B)
                Interrupt:65 Memory:f8000000-f8200000 

      ML_TYPE: NON_ML	DOT11 Statistics (Cumulative Total/Last 5 Seconds):
      RECEIVER                                TRANSMITTER
      Host Rx K Bytes:             0/0        Host Tx K Bytes:             0/0
      Unicasts Rx:                 0/0        Unicasts Tx:                 0/0
      Broadcasts Rx:               0/0        Broadcasts Tx:               0/0
      Beacons Rx:          130342074/1508     Beacons Tx:              15565/0
      Probes Rx:             1266699/35       Probes Tx:                   0/0
      Multicasts Rx:               0/0        Multicasts Tx:             147/0
      Mgmt Packets Rx:     131608769/1543     Mgmt Packets Tx:             0/0
      Ctrl Frames Rx:         495955/8        Ctrl Frames Tx:              0/0
      RTS received:            44130/0        RTS transmitted:             0/0
      Duplicate frames:            0/0        CTS not received:            0/0
      MIC errors:                  0/0        WEP errors:                  0/0
      FCS errors:           17607735/305      Retries:                     0/0
      Key Index errors:            0/0        Tx Failures:                 0/0
                                              Tx Drops:                    0/0
      Rate Statistics for Radio::
      ML_TYPE: ML	DOT11 Statistics (Cumulative Total/Last 5 Seconds):
      RECEIVER                                TRANSMITTER
      Host Rx K Bytes:             0/0        Host Tx K Bytes:             0/0
      Unicasts Rx:                 0/0        Unicasts Tx:                 0/0
      Broadcasts Rx:               0/0        Broadcasts Tx:               0/0
      Beacons Rx:          130342074/1508     Beacons Tx:              15565/0
      Probes Rx:             1266699/35       Probes Tx:                   0/0
      Multicasts Rx:               0/0        Multicasts Tx:               0/0
      Mgmt Packets Rx:     131608769/1543     Mgmt Packets Tx:             0/0
      Ctrl Frames Rx:         495955/8        Ctrl Frames Tx:              0/0
      RTS received:            44130/0        RTS transmitted:             0/0
      Duplicate frames:            0/0        CTS not received:            0/0
      MIC errors:                  0/0        WEP errors:                  0/0
      FCS errors:           17607735/305      Retries:                     0/0
      Key Index errors:            0/0        Tx Failures:                 0/0
                                              Tx Drops:                    0/0
      Rate Statistics for Radio::


      Beacons missed: 0-30s 31-60s 61-90s 90s+
                           0      0      0    0
    '''

    showInterfaceDot11Radio_1 = '''
    Dot11Radio1 is DOWN, line protocol is DOWN
      Hardware is 802.11 5.0G Radio, channel is 149
      Radio MAC is 70:6D:15:C0:87:60

      Dot11Radio1     Link encap:Ethernet  HWaddr 70:6D:15:C0:87:60  
                BROADCAST MULTICAST  MTU:1500  Metric:1
                RX packets:3 errors:0 dropped:0 overruns:0 frame:0
                TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
                collisions:0 txqueuelen:1000 
                RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
                Interrupt:102 Memory:f8400000-f8600000 

      ML_TYPE: NON_ML	DOT11 Statistics (Cumulative Total/Last 5 Seconds):
      RECEIVER                                TRANSMITTER
      Host Rx K Bytes:             0/0        Host Tx K Bytes:             0/0
      Unicasts Rx:                 0/0        Unicasts Tx:                 0/0
      Broadcasts Rx:               0/0        Broadcasts Tx:               0/0
      Beacons Rx:                  0/0        Beacons Tx:                  0/0
      Probes Rx:                   0/0        Probes Tx:                   0/0
      Multicasts Rx:               0/0        Multicasts Tx:               0/0
      Mgmt Packets Rx:             0/0        Mgmt Packets Tx:             0/0
      Ctrl Frames Rx:              0/0        Ctrl Frames Tx:              0/0
      RTS received:                0/0        RTS transmitted:             0/0
      Duplicate frames:            0/0        CTS not received:            0/0
      MIC errors:                  0/0        WEP errors:                  0/0
      FCS errors:                  0/0        Retries:                     0/0
      Key Index errors:            0/0        Tx Failures:                 0/0
                                              Tx Drops:                    0/0
      Rate Statistics for Radio::
      ML_TYPE: ML	DOT11 Statistics (Cumulative Total/Last 5 Seconds):
      RECEIVER                                TRANSMITTER
      Host Rx K Bytes:             0/0        Host Tx K Bytes:             0/0
      Unicasts Rx:                 0/0        Unicasts Tx:                 0/0
      Broadcasts Rx:               0/0        Broadcasts Tx:               0/0
      Beacons Rx:                  0/0        Beacons Tx:                  0/0
      Probes Rx:                   0/0        Probes Tx:                   0/0
      Multicasts Rx:               0/0        Multicasts Tx:               0/0
      Mgmt Packets Rx:             0/0        Mgmt Packets Tx:             0/0
      Ctrl Frames Rx:              0/0        Ctrl Frames Tx:              0/0
      RTS received:                0/0        RTS transmitted:             0/0
      Duplicate frames:            0/0        CTS not received:            0/0
      MIC errors:                  0/0        WEP errors:                  0/0
      FCS errors:                  0/0        Retries:                     0/0
      Key Index errors:            0/0        Tx Failures:                 0/0
                                              Tx Drops:                    0/0
      Rate Statistics for Radio::


      Beacons missed: 0-30s 31-60s 61-90s 90s+
                           0      0      0    0
    '''

    showInterfaceDot11Radio_2 = '''
        Error: Device not found
    '''

    showinterface_ops_output = {
        'interface': {
            'wired0': {
                'type': 'ethernet',
                'enabled': 'up',
                'mac_address': '00:EA:BD:12:8E:70',
                'bandwidth': 1000,
                'duplex_mode': 'full',
                'counters': {
                    'in_pkts': 24172648,
                    'in_octets': 16727171905,
                    'in_errors': 236,
                    'out_pkts': 262068,
                    'out_octets': 123668457,
                    'out_errors': 0,
                    'rate': {
                        'in_rate': '719323',
                        'in_rate_pkts': '87',
                        'out_rate': '2042',
                        'out_rate_pkts': '0'
                    }
                }
            },
            'wired1': {
                'type': 'ethernet',
                'enabled': 'down',
                'mac_address': '00:EA:BD:12:8E:70',
                'bandwidth': 0,
                'duplex_mode': 'half',
                'counters': {
                    'in_pkts': 0,
                    'in_octets': 0,
                    'in_errors': 0,
                    'out_pkts': 7844,
                    'out_octets': 3121792,
                    'out_errors': 0,
                    'rate': {
                        'in_rate': 'n/a',
                        'in_rate_pkts': 'n/a',
                        'out_rate': 'n/a',
                        'out_rate_pkts': 'n/a'
                    }
                }
            },
            'Dot11Radio0': {
                'type': '802.11 2.4G Radio',
                'oper_status': 'up',
                'mac_address': '70:6D:15:C0:87:60',
                'enabled': 'up',
                'counters': {
                    'rate': {
                        'in_rate_pkts': 33456202,
                        'out_rate_pkts': 33456202,
                        'in_pkts': 446267363,
                        'out_pkts': 0
                    },
                    'in_unicast_pkts': 0,
                    'in_broadcast_pkts': 0,
                    'in_multicast_pkts': 0,
                    'in_mac_control_frames': 495955,
                    'out_unicast_pkts': 0,
                    'out_broadcast_pkts': 0,
                    'out_multicast_pkts': 0,
                    'out_mac_control_frames': 0
                }
            },
            'Dot11Radio1': {
                'type': '802.11 5.0G Radio',
                'oper_status': 'down',
                'mac_address': '70:6D:15:C0:87:60',
                'enabled': 'down',
                'counters': {
                    'rate': {
                        'in_rate_pkts': 3,
                        'out_rate_pkts': 3,
                        'in_pkts': 0,
                        'out_pkts': 0
                    },
                    'in_unicast_pkts': 0,
                    'in_broadcast_pkts': 0,
                    'in_multicast_pkts': 0,
                    'in_mac_control_frames': 0,
                    'out_unicast_pkts': 0,
                    'out_broadcast_pkts': 0,
                    'out_multicast_pkts': 0,
                    'out_mac_control_frames': 0
                }
            }
        }
    }