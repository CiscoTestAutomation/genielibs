''' 
Interface Genie Ops Object Outputs for NXOS.
'''


class InterfaceOutput(object):

    ShowInterface_all = '''
        mgmt0 is up
          admin state is up
          Hardware: Ethernet, address: 5254.00c9.d26e (bia 5254.00c9.d26e)
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec
          reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, medium is broadcast
          Port mode is routed
          full-duplex, 1000 Mb/s
          Auto-Negotiation is turned on
          Auto-mdix is turned off
          EtherType is 0x0000 
          1 minute input rate 0 bits/sec, 0 packets/sec
          1 minute output rate 24 bits/sec, 0 packets/sec
          Rx
            2 input packets 0 unicast packets 2 multicast packets
            0 broadcast packets 168 bytes
          Tx
            22 output packets 0 unicast packets 18 multicast packets
            4 broadcast packets 4726 bytes
        Ethernet2/1 is up
            admin state is up, Dedicated Interface
              Hardware: 10/100/1000 Ethernet, address: aaaa.bbbb.cccc (bia 5254.003b.4aca)
              Description: desc
              Internet Address is 10.4.4.4/24 secondary tag 10
              MTU 1600 bytes, BW 768 Kbit, DLY 3330 usec
              reliability 255/255, txload 1/255, rxload 1/255
              Encapsulation ARPA, medium is broadcast
              Port mode is routed
              full-duplex, 1000 Mb/s
              Beacon is turned off
              Auto-Negotiation is turned off
              Input flow-control is off, output flow-control is off
              Auto-mdix is turned off
              Switchport monitor is off 
              EtherType is 0x8100 
              Members in this channel: Po1
              EEE (efficient-ethernet) : n/a
              Last link flapped 00:00:29
              Last clearing of "show interface" counters never
              1 interface resets
              Load-Interval #1: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              Load-Interval #2: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              RX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 input packets  0 bytes
                0 jumbo packets  0 storm suppression packets
                0 runts  0 giants  0 CRC/FCS  0 no buffer
                0 input error  0 short frame  0 overrun   0 underrun  0 ignored
                0 watchdog  0 bad etype drop  0 bad proto drop  0 if down drop
                0 input with dribble  0 input discard
                0 Rx pause
              TX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 output packets  0 bytes
                0 jumbo packets
                0 output error  0 collision  0 deferred  0 late collision
                0 lost carrier  0 no carrier  0 babble  0 output discard
                0 Tx pause
        Ethernet2/1.10 is down (Administratively down)
            admin state is down, Dedicated Interface, [parent interface is Ethernet2/1]
              Hardware: 10/100/1000 Ethernet, address: 5254.003b.4af8 (bia 5254.003b.4aca)
              MTU 1600 bytes, BW 768 Kbit, DLY 10 usec
              reliability 255/255, txload 1/255, rxload 1/255
              Encapsulation 802.1Q Virtual LAN, Vlan ID 10, medium is broadcast
              Port mode is routed
              Auto-mdix is turned off
              EtherType is 0x8100 
        Ethernet2/1.20 is up
            admin state is up, Dedicated Interface, [parent interface is Ethernet2/1]
              Hardware: 10/100/1000 Ethernet, address: 5254.003b.4af8 (bia 5254.003b.4aca)
              MTU 1600 bytes, BW 768 Kbit, DLY 10 usec
              reliability 255/255, txload 1/255, rxload 1/255
              Encapsulation 802.1Q Virtual LAN, Vlan ID 20, medium is p2p
              Port mode is routed
              Auto-mdix is turned off
              EtherType is 0x8100 
        Ethernet2/2 is up
            admin state is up, Dedicated Interface
              Hardware: 10/100/1000 Ethernet, address: 5254.00ac.b52e (bia 5254.00ac.b52e)
              MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec
              reliability 255/255, txload 1/255, rxload 1/255
              Encapsulation ARPA, medium is broadcast
              Port mode is trunk
              full-duplex, 1000 Mb/s
              Beacon is turned off
              Auto-Negotiation is turned off
              Input flow-control is off, output flow-control is off
              Auto-mdix is turned off
              Switchport monitor is off 
              EtherType is 0x8100
                Members in this channel: Po1
              EEE (efficient-ethernet) : n/a
              Last link flapped 00:07:28
              Last clearing of "show interface" counters never
              1 interface resets
              Load-Interval #1: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              Load-Interval #2: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              RX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 input packets  0 bytes
                0 jumbo packets  0 storm suppression packets
                0 runts  0 giants  0 CRC/FCS  0 no buffer
                0 input error  0 short frame  0 overrun   0 underrun  0 ignored
                0 watchdog  0 bad etype drop  0 bad proto drop  0 if down drop
                0 input with dribble  0 input discard
                0 Rx pause
              TX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 output packets  0 bytes
                0 jumbo packets
                0 output error  0 collision  0 deferred  0 late collision
                0 lost carrier  0 no carrier  0 babble  0 output discard
                0 Tx pause
        '''

    ShowInterface_eth2 = '''
        Ethernet2/1 is up
            admin state is up, Dedicated Interface
              Hardware: 10/100/1000 Ethernet, address: aaaa.bbbb.cccc (bia 5254.003b.4aca)
              Description: desc
              Internet Address is 10.4.4.4/24 secondary tag 10
              MTU 1600 bytes, BW 768 Kbit, DLY 3330 usec
              reliability 255/255, txload 1/255, rxload 1/255
              Encapsulation ARPA, medium is broadcast
              Port mode is routed
              full-duplex, 1000 Mb/s
              Beacon is turned off
              Auto-Negotiation is turned off
              Input flow-control is off, output flow-control is off
              Auto-mdix is turned off
              Switchport monitor is off 
              EtherType is 0x8100 
              Members in this channel: Po1
              EEE (efficient-ethernet) : n/a
              Last link flapped 00:00:29
              Last clearing of "show interface" counters never
              1 interface resets
              Load-Interval #1: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              Load-Interval #2: 0 seconds
                0 seconds input rate 0 bits/sec, 0 packets/sec
                0 seconds output rate 0 bits/sec, 0 packets/sec
                input rate 0 bps, 0 pps; output rate 0 bps, 0 pps
              RX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 input packets  0 bytes
                0 jumbo packets  0 storm suppression packets
                0 runts  0 giants  0 CRC/FCS  0 no buffer
                0 input error  0 short frame  0 overrun   0 underrun  0 ignored
                0 watchdog  0 bad etype drop  0 bad proto drop  0 if down drop
                0 input with dribble  0 input discard
                0 Rx pause
              TX
                0 unicast packets  0 multicast packets  0 broadcast packets
                0 output packets  0 bytes
                0 jumbo packets
                0 output error  0 collision  0 deferred  0 late collision
                0 lost carrier  0 no carrier  0 babble  0 output discard
                0 Tx pause'''
    ShowIpInterfaceVrfAll = {
        'Ethernet2/1': {'directed_broadcast': 'disabled',
                 'icmp_port_unreachable': 'enabled',
                 'icmp_redirects': 'disabled',
                 'icmp_unreachable': 'disabled',
                 'int_stat_last_reset': 'never',
                 'interface_status': 'protocol-up/link-up/admin-up',
                 'iod': 36,
                 'ip_forwarding': 'disabled',
                 'ip_mtu': 1600,
                 'ipv4': {'10.2.2.2/24': {'ip': '10.2.2.2',
                                          'ip_subnet': '10.2.2.0',
                                          'prefix_length': '24',
                                          'secondary': True},
                          '10.3.3.3/24': {'broadcast_address': '255.255.255.255',
                                          'ip': '10.3.3.3',
                                          'ip_subnet': '10.3.3.0',
                                          'prefix_length': '24',
                                          'route_preference': '0',
                                          'route_tag': '0',
                                          'secondary': True},
                          '10.4.4.4/24': {'ip': '10.4.4.4',
                                          'ip_subnet': '10.4.4.0',
                                          'prefix_length': '24',
                                          'route_preference': 'None',
                                          'route_tag': 'None'},
                          'unnumbered':{'interface_ref': 'loopback0'},
                          'counters': {'broadcast_bytes_consumed': 0,
                                       'broadcast_bytes_forwarded': 0,
                                       'broadcast_bytes_originated': 0,
                                       'broadcast_bytes_received': 0,
                                       'broadcast_bytes_sent': 0,
                                       'broadcast_packets_consumed': 0,
                                       'broadcast_packets_forwarded': 0,
                                       'broadcast_packets_originated': 0,
                                       'broadcast_packets_received': 0,
                                       'broadcast_packets_sent': 0,
                                       'labeled_bytes_consumed': 0,
                                       'labeled_bytes_forwarded': 0,
                                       'labeled_bytes_originated': 0,
                                       'labeled_bytes_received': 0,
                                       'labeled_bytes_sent': 0,
                                       'labeled_packets_consumed': 0,
                                       'labeled_packets_forwarded': 0,
                                       'labeled_packets_originated': 0,
                                       'labeled_packets_received': 0,
                                       'labeled_packets_sent': 0,
                                       'multicast_bytes_consumed': 0,
                                       'multicast_bytes_forwarded': 0,
                                       'multicast_bytes_originated': 0,
                                       'multicast_bytes_received': 0,
                                       'multicast_bytes_sent': 0,
                                       'multicast_packets_consumed': 0,
                                       'multicast_packets_forwarded': 0,
                                       'multicast_packets_originated': 0,
                                       'multicast_packets_received': 0,
                                       'multicast_packets_sent': 0,
                                       'unicast_bytes_consumed': 0,
                                       'unicast_bytes_forwarded': 0,
                                       'unicast_bytes_originated': 0,
                                       'unicast_bytes_received': 0,
                                       'unicast_bytes_sent': 0,
                                       'unicast_packets_consumed': 0,
                                       'unicast_packets_forwarded': 0,
                                       'unicast_packets_originated': 0,
                                       'unicast_packets_received': 0,
                                       'unicast_packets_sent': 0}},
                 'load_sharing': 'none',
                 'local_proxy_arp': 'disabled',
                 'multicast_groups': ['224.0.0.6', '224.0.0.5', '224.0.0.2'],
                 'multicast_routing': 'disabled',
                 'proxy_arp': 'disabled',
                 'unicast_reverse_path': 'none',
                 'vrf': 'VRF1',
                 'wccp_redirect_exclude': 'disabled',
                 'wccp_redirect_inbound': 'disabled',
                 'wccp_redirect_outbound': 'disabled'}
    }
    ShowIpInterfaceVrfAll_all = '''
            IP Interface Status for VRF "default"

            IP Interface Status for VRF "management"

            IP Interface Status for VRF "VRF1"
            Ethernet2/1, Interface status: protocol-up/link-up/admin-up, iod: 36,
              IP address: 10.4.4.4, IP subnet: 10.4.4.0/24 secondary
              IP address: 10.2.2.2, IP subnet: 10.2.2.0/24 secondary
              IP address: 10.3.3.3, IP subnet: 10.3.3.0/24 secondary
              IP broadcast address: 255.255.255.255
              IP multicast groups locally joined: 
                 224.0.0.6  224.0.0.5  224.0.0.2
              IP MTU: 1600 bytes (using link MTU)
              IP primary address route-preference: 0, tag: 0
              IP unnumbered interface (loopback0)
              IP proxy ARP : disabled
              IP Local Proxy ARP : disabled
              IP multicast routing: disabled
              IP icmp redirects: disabled
              IP directed-broadcast: disabled 
              IP Forwarding: disabled 
              IP icmp unreachables (except port): disabled
              IP icmp port-unreachable: enabled
              IP unicast reverse path forwarding: none
              IP load sharing: none 
              IP interface statistics last reset: never
              IP interface software stats: (sent/received/forwarded/originated/consumed)
                Unicast packets    : 0/0/0/0/0
                Unicast bytes      : 0/0/0/0/0
                Multicast packets  : 0/0/0/0/0
                Multicast bytes    : 0/0/0/0/0
                Broadcast packets  : 0/0/0/0/0
                Broadcast bytes    : 0/0/0/0/0
                Labeled packets    : 0/0/0/0/0
                Labeled bytes      : 0/0/0/0/0
              WCCP Redirect outbound: disabled
              WCCP Redirect inbound: disabled
              WCCP Redirect exclude: disabled
          '''
    ShowIpInterfaceVrfAll_vrf1_eth2='''
        IP Interface Status for VRF "VRF1"
            Ethernet2/1, Interface status: protocol-up/link-up/admin-up, iod: 36,
              IP address: 10.4.4.4, IP subnet: 10.4.4.0/24 secondary
              IP address: 10.2.2.2, IP subnet: 10.2.2.0/24 secondary
              IP address: 10.3.3.3, IP subnet: 10.3.3.0/24 secondary
              IP broadcast address: 255.255.255.255
              IP multicast groups locally joined: 
                 224.0.0.6  224.0.0.5  224.0.0.2
              IP MTU: 1600 bytes (using link MTU)
              IP primary address route-preference: 0, tag: 0
              IP unnumbered interface (loopback0)
              IP proxy ARP : disabled
              IP Local Proxy ARP : disabled
              IP multicast routing: disabled
              IP icmp redirects: disabled
              IP directed-broadcast: disabled 
              IP Forwarding: disabled 
              IP icmp unreachables (except port): disabled
              IP icmp port-unreachable: enabled
              IP unicast reverse path forwarding: none
              IP load sharing: none 
              IP interface statistics last reset: never
              IP interface software stats: (sent/received/forwarded/originated/consumed)
                Unicast packets    : 0/0/0/0/0
                Unicast bytes      : 0/0/0/0/0
                Multicast packets  : 0/0/0/0/0
                Multicast bytes    : 0/0/0/0/0
                Broadcast packets  : 0/0/0/0/0
                Broadcast bytes    : 0/0/0/0/0
                Labeled packets    : 0/0/0/0/0
                Labeled bytes      : 0/0/0/0/0
              WCCP Redirect outbound: disabled
              WCCP Redirect inbound: disabled
              WCCP Redirect exclude: disabled
    '''
    ShowVrfAllInterface = {
        'Ethernet2/1': {'site_of_origin': '--', 'vrf': 'VRF1', 'vrf_id': 3},
        'Ethernet2/1.10': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/1.20': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/10': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/11': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/12': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/13': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/14': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/15': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/16': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/17': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/18': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/19': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/20': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/21': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/22': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/23': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/24': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/25': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/26': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/27': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/28': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/29': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/30': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/31': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/32': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/33': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/34': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/35': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/36': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/37': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/38': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/39': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/4': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/40': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/41': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/42': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/43': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/44': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/45': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/46': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/47': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/48': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/5': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/6': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/7': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/8': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet2/9': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/1': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/10': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/11': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/12': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/13': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/14': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/15': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/16': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/17': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/18': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/19': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/2': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/20': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/21': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/22': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/23': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/24': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/25': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/26': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/27': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/28': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/29': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/3': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/30': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/31': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/32': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/33': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/34': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/35': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/36': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/37': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/38': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/39': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/4': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/40': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/41': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/42': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/43': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/44': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/45': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/46': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/47': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/48': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/5': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/6': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/7': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/8': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet3/9': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/1': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/10': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/11': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/12': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/13': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/14': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/15': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/16': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/17': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/18': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/19': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/2': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/20': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/21': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/22': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/23': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/24': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/25': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/26': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/27': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/28': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/29': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/3': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/30': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/31': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/32': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/33': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/34': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/35': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/36': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/37': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/38': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/39': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/4': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/40': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/41': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/42': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/43': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/44': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/45': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/46': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/47': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/48': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/5': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/6': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/7': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/8': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Ethernet4/9': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'Null0': {'site_of_origin': '--', 'vrf': 'default', 'vrf_id': 1},
        'mgmt0': {'site_of_origin': '--', 'vrf': 'management', 'vrf_id': 2}
    }
    ShowVrfAllInterface_all = '''

    Interface                 VRF-Name                        VRF-ID  Site-of-Origin
    Ethernet2/1               VRF1                                 3  --
    Null0                     default                              1  --
    Ethernet2/1.10            default                              1  --
    Ethernet2/1.20            default                              1  --
    Ethernet2/4               default                              1  --
    Ethernet2/5               default                              1  --
    Ethernet2/6               default                              1  --
    Ethernet2/7               default                              1  --
    Ethernet2/8               default                              1  --
    Ethernet2/9               default                              1  --
    Ethernet2/10              default                              1  --
    Ethernet2/11              default                              1  --
    Ethernet2/12              default                              1  --
    Ethernet2/13              default                              1  --
    Ethernet2/14              default                              1  --
    Ethernet2/15              default                              1  --
    Ethernet2/16              default                              1  --
    Ethernet2/17              default                              1  --
    Ethernet2/18              default                              1  --
    Ethernet2/19              default                              1  --
    Ethernet2/20              default                              1  --
    Ethernet2/21              default                              1  --
    Ethernet2/22              default                              1  --
    Ethernet2/23              default                              1  --
    Ethernet2/24              default                              1  --
    Ethernet2/25              default                              1  --
    Ethernet2/26              default                              1  --
    Ethernet2/27              default                              1  --
    Ethernet2/28              default                              1  --
    Ethernet2/29              default                              1  --
    Ethernet2/30              default                              1  --
    Ethernet2/31              default                              1  --
    Ethernet2/32              default                              1  --
    Ethernet2/33              default                              1  --
    Ethernet2/34              default                              1  --
    Ethernet2/35              default                              1  --
    Ethernet2/36              default                              1  --
    Ethernet2/37              default                              1  --
    Ethernet2/38              default                              1  --
    Ethernet2/39              default                              1  --
    Ethernet2/40              default                              1  --
    Ethernet2/41              default                              1  --
    Ethernet2/42              default                              1  --
    Ethernet2/43              default                              1  --
    Ethernet2/44              default                              1  --
    Ethernet2/45              default                              1  --
    Ethernet2/46              default                              1  --
    Ethernet2/47              default                              1  --
    Ethernet2/48              default                              1  --
    Ethernet3/1               default                              1  --
    Ethernet3/2               default                              1  --
    Ethernet3/3               default                              1  --
    Ethernet3/4               default                              1  --
    Ethernet3/5               default                              1  --
    Ethernet3/6               default                              1  --
    Ethernet3/7               default                              1  --
    Ethernet3/8               default                              1  --
    Ethernet3/9               default                              1  --
    Ethernet3/10              default                              1  --
    Ethernet3/11              default                              1  --
    Ethernet3/12              default                              1  --
    Ethernet3/13              default                              1  --
    Ethernet3/14              default                              1  --
    Ethernet3/15              default                              1  --
    Ethernet3/16              default                              1  --
    Ethernet3/17              default                              1  --
    Ethernet3/18              default                              1  --
    Ethernet3/19              default                              1  --
    Ethernet3/20              default                              1  --
    Ethernet3/21              default                              1  --
    Ethernet3/22              default                              1  --
    Ethernet3/23              default                              1  --
    Ethernet3/24              default                              1  --
    Ethernet3/25              default                              1  --
    Ethernet3/26              default                              1  --
    Ethernet3/27              default                              1  --
    Ethernet3/28              default                              1  --
    Ethernet3/29              default                              1  --
    Ethernet3/30              default                              1  --
    Ethernet3/31              default                              1  --
    Ethernet3/32              default                              1  --
    Ethernet3/33              default                              1  --
    Ethernet3/34              default                              1  --
    Ethernet3/35              default                              1  --
    Ethernet3/36              default                              1  --
    Ethernet3/37              default                              1  --
    Ethernet3/38              default                              1  --
    Ethernet3/39              default                              1  --
    Ethernet3/40              default                              1  --
    Ethernet3/41              default                              1  --
    Ethernet3/42              default                              1  --
    Ethernet3/43              default                              1  --
    Ethernet3/44              default                              1  --
    Ethernet3/45              default                              1  --
    Ethernet3/46              default                              1  --
    Ethernet3/47              default                              1  --
    Ethernet3/48              default                              1  --
    Ethernet4/1               default                              1  --
    Ethernet4/2               default                              1  --
    Ethernet4/3               default                              1  --
    Ethernet4/4               default                              1  --
    Ethernet4/5               default                              1  --
    Ethernet4/6               default                              1  --
    Ethernet4/7               default                              1  --
    Ethernet4/8               default                              1  --
    Ethernet4/9               default                              1  --
    Ethernet4/10              default                              1  --
    Ethernet4/11              default                              1  --
    Ethernet4/12              default                              1  --
    Ethernet4/13              default                              1  --
    Ethernet4/14              default                              1  --
    Ethernet4/15              default                              1  --
    Ethernet4/16              default                              1  --
    Ethernet4/17              default                              1  --
    Ethernet4/18              default                              1  --
    Ethernet4/19              default                              1  --
    Ethernet4/20              default                              1  --
    Ethernet4/21              default                              1  --
    Ethernet4/22              default                              1  --
    Ethernet4/23              default                              1  --
    Ethernet4/24              default                              1  --
    Ethernet4/25              default                              1  --
    Ethernet4/26              default                              1  --
    Ethernet4/27              default                              1  --
    Ethernet4/28              default                              1  --
    Ethernet4/29              default                              1  --
    Ethernet4/30              default                              1  --
    Ethernet4/31              default                              1  --
    Ethernet4/32              default                              1  --
    Ethernet4/33              default                              1  --
    Ethernet4/34              default                              1  --
    Ethernet4/35              default                              1  --
    Ethernet4/36              default                              1  --
    Ethernet4/37              default                              1  --
    Ethernet4/38              default                              1  --
    Ethernet4/39              default                              1  --
    Ethernet4/40              default                              1  --
    Ethernet4/41              default                              1  --
    Ethernet4/42              default                              1  --
    Ethernet4/43              default                              1  --
    Ethernet4/44              default                              1  --
    Ethernet4/45              default                              1  --
    Ethernet4/46              default                              1  --
    Ethernet4/47              default                              1  --
    Ethernet4/48              default                              1  --
    mgmt0                     management                           2  --

        '''
    ShowVrfAllInterface_vrf1_eth2='''
    Interface                 VRF-Name                        VRF-ID  Site-of-Origin
    Ethernet2/1               VRF1                                 3  --
    '''
    ShowInterfaceSwitchport = {
        'Ethernet2/2': {'access_vlan': 1,
                         'access_vlan_mode': 'default',
                         'admin_priv_vlan_primary_host_assoc': 'none',
                         'admin_priv_vlan_primary_mapping': 'none',
                         'admin_priv_vlan_secondary_host_assoc': 'none',
                         'admin_priv_vlan_secondary_mapping': 'none',
                         'admin_priv_vlan_trunk_encapsulation': 'dot1q',
                         'admin_priv_vlan_trunk_native_vlan': 'none',
                         'admin_priv_vlan_trunk_normal_vlans': 'none',
                         'admin_priv_vlan_trunk_private_vlans': 'none',
                         'native_vlan': 1,
                         'native_vlan_mode': 'default',
                         'operational_private_vlan': 'none',
                         'switchport_mode': 'trunk',
                         'switchport_monitor': 'Not enabled',
                         'switchport_status': 'enabled',
                         'switchport_enable': True,
                         'trunk_vlans': '100,300'},
            'Ethernet2/3': {'access_vlan': 100,
                         'access_vlan_mode': 'Vlan not created',
                         'admin_priv_vlan_primary_host_assoc': 'none',
                         'admin_priv_vlan_primary_mapping': 'none',
                         'admin_priv_vlan_secondary_host_assoc': 'none',
                         'admin_priv_vlan_secondary_mapping': 'none',
                         'admin_priv_vlan_trunk_encapsulation': 'dot1q',
                         'admin_priv_vlan_trunk_native_vlan': 'none',
                         'admin_priv_vlan_trunk_normal_vlans': 'none',
                         'admin_priv_vlan_trunk_private_vlans': 'none',
                         'native_vlan': 1,
                         'native_vlan_mode': 'default',
                         'operational_private_vlan': 'none',
                         'switchport_mode': 'access',
                         'switchport_monitor': 'Not enabled',
                         'switchport_status': 'enabled',
                         'switchport_enable': True,
                         'trunk_vlans': '1-4094'}
    }
    ShowInterfaceSwitchport_all = '''
            Name: Ethernet2/2
              Switchport: Enabled
              Switchport Monitor: Not enabled 
              Operational Mode: trunk
              Access Mode VLAN: 1 (default)
              Trunking Native Mode VLAN: 1 (default)
              Trunking VLANs Allowed: 100,300
              Administrative private-vlan primary host-association: none
              Administrative private-vlan secondary host-association: none
              Administrative private-vlan primary mapping: none
              Administrative private-vlan secondary mapping: none
              Administrative private-vlan trunk native VLAN: none
              Administrative private-vlan trunk encapsulation: dot1q
              Administrative private-vlan trunk normal VLANs: none
              Administrative private-vlan trunk private VLANs: none
              Operational private-vlan: none
            Name: Ethernet2/3
              Switchport: Enabled
              Switchport Monitor: Not enabled 
              Operational Mode: access
              Access Mode VLAN: 100 (Vlan not created)
              Trunking Native Mode VLAN: 1 (default)
              Trunking VLANs Allowed: 1-4094
              Administrative private-vlan primary host-association: none
              Administrative private-vlan secondary host-association: none
              Administrative private-vlan primary mapping: none
              Administrative private-vlan secondary mapping: none
              Administrative private-vlan trunk native VLAN: none
              Administrative private-vlan trunk encapsulation: dot1q
              Administrative private-vlan trunk normal VLANs: none
              Administrative private-vlan trunk private VLANs: none
              Operational private-vlan: none  
          '''
    ShowInterfaceSwitchport_eth2='''
        Name: Ethernet2/1
              Switchport: Enabled
              Switchport Monitor: Not enabled 
              Operational Mode: trunk
              Access Mode VLAN: 1 (default)
              Trunking Native Mode VLAN: 1 (default)
              Trunking VLANs Allowed: 100,300
              Administrative private-vlan primary host-association: none
              Administrative private-vlan secondary host-association: none
              Administrative private-vlan primary mapping: none
              Administrative private-vlan secondary mapping: none
              Administrative private-vlan trunk native VLAN: none
              Administrative private-vlan trunk encapsulation: dot1q
              Administrative private-vlan trunk normal VLANs: none
              Administrative private-vlan trunk private VLANs: none
              Operational private-vlan: none
    '''
    ShowIpv6InterfaceVrfAll = {
        'Ethernet2/1': {'enabled': True,
                 'interface_status': 'protocol-up/link-up/admin-up',
                 'iod': 36,
                 'ipv6': {'2001:db8:1:1::1/64': {'ip': '2001:db8:1:1::1',
                                                 'prefix_length': '64',
                                                 'status': 'valid'},
                          '2001:db8:2:2::2/64': {'anycast': True,
                                                 'ip': '2001:db8:2:2::2',
                                                 'prefix_length': '64',
                                                 'status': 'valid'},
                          '2001:db8:3:3::3/64': {'ip': '2001:db8:3:3::3',
                                                 'prefix_length': '64',
                                                 'status': 'valid'},
                          '2001:db8:4:4:a8aa:bbff:febb:cccc/64': {'ip': '2001:db8:4:4:a8aa:bbff:febb:cccc',
                                                                  'prefix_length': '64',
                                                                  'status': 'valid'},
                          'counters': {'multicast_bytes_consumed': 640,
                                       'multicast_bytes_forwarded': 0,
                                       'multicast_bytes_originated': 1144,
                                       'multicast_packets_consumed': 9,
                                       'multicast_packets_forwarded': 0,
                                       'multicast_packets_originated': 12,
                                       'unicast_bytes_consumed': 0,
                                       'unicast_bytes_forwarded': 0,
                                       'unicast_bytes_originated': 0,
                                       'unicast_packets_consumed': 0,
                                       'unicast_packets_forwarded': 0,
                                       'unicast_packets_originated': 0},
                          'ipv6_forwarding_feature': 'disabled',
                          'ipv6_last_reset': 'never',
                          'ipv6_link_local': 'fe80::a8aa:bbff:febb:cccc ',
                          'ipv6_link_local_state': 'default',
                          'ipv6_ll_state': 'valid',
                          'ipv6_load_sharing': 'none',
                          'ipv6_mtu': 1600,
                          'ipv6_multicast_entries': 'none',
                          'ipv6_multicast_groups': ['ff02::1:ffbb:cccc',
                                                    'ff02::1:ff00:3',
                                                    'ff02::1:ff00:2',
                                                    'ff02::2',
                                                    'ff02::1',
                                                    'ff02::1:ff00:1',
                                                    'ff02::1:ffbb:cccc',
                                                    'ff02::1:ff00:0'],
                          'ipv6_multicast_routing': 'disabled',
                          'ipv6_report_link_local': 'disabled',
                          'ipv6_subnet': '2001:db8:1:1::/64',
                          'ipv6_unicast_rev_path_forwarding': 'none',
                          'ipv6_virtual_add': 'none',
                          'multicast_groups': True},
                 'vrf': 'VRF1'}
    }
    ShowIpv6InterfaceVrfAll_all = '''
        IPv6 Interface Status for VRF "default"

        IPv6 Interface Status for VRF "management"

        IPv6 Interface Status for VRF "VRF1"
        Ethernet2/1, Interface status: protocol-up/link-up/admin-up, iod: 36
          IPv6 address: 
            2001:db8:1:1::1/64 [VALID]
            2001:db8:3:3::3/64 [VALID]
            2001:db8:4:4:a8aa:bbff:febb:cccc/64 [VALID]
            2001:db8:2:2::2/64 [VALID]
          IPv6 subnet:  2001:db8:1:1::/64
          Anycast configured addresses:
            2001:db8:2:2::2/64 [VALID]
          IPv6 link-local address: fe80::a8aa:bbff:febb:cccc (default) [VALID]
          IPv6 virtual addresses configured: none
          IPv6 multicast routing: disabled
          IPv6 report link local: disabled
          IPv6 Forwarding feature: disabled
          IPv6 multicast groups locally joined:   
              ff02::1:ffbb:cccc  ff02::1:ff00:3  ff02::1:ff00:2  ff02::2   
              ff02::1  ff02::1:ff00:1  ff02::1:ffbb:cccc  ff02::1:ff00:0  
          IPv6 multicast (S,G) entries joined: none
          IPv6 MTU: 1600 (using link MTU)
          IPv6 unicast reverse path forwarding: none
          IPv6 load sharing: none 
          IPv6 interface statistics last reset: never
          IPv6 interface RP-traffic statistics: (forwarded/originated/consumed)
            Unicast packets:      0/0/0
            Unicast bytes:        0/0/0
            Multicast packets:    0/12/9
            Multicast bytes:      0/1144/640
      '''
    ShowIpv6InterfaceVrfAll_eth1='''
     IPv6 Interface Status for VRF "VRF1"
        Ethernet2/1, Interface status: protocol-up/link-up/admin-up, iod: 36
          IPv6 address: 
            2001:db8:1:1::1/64 [VALID]
            2001:db8:3:3::3/64 [VALID]
            2001:db8:4:4:a8aa:bbff:febb:cccc/64 [VALID]
            2001:db8:2:2::2/64 [VALID]
          IPv6 subnet:  2001:db8:1:1::/64
          Anycast configured addresses:
            2001:db8:2:2::2/64 [VALID]
          IPv6 link-local address: fe80::a8aa:bbff:febb:cccc (default) [VALID]
          IPv6 virtual addresses configured: none
          IPv6 multicast routing: disabled
          IPv6 report link local: disabled
          IPv6 Forwarding feature: disabled
          IPv6 multicast groups locally joined:   
              ff02::1:ffbb:cccc  ff02::1:ff00:3  ff02::1:ff00:2  ff02::2   
              ff02::1  ff02::1:ff00:1  ff02::1:ffbb:cccc  ff02::1:ff00:0  
          IPv6 multicast (S,G) entries joined: none
          IPv6 MTU: 1600 (using link MTU)
          IPv6 unicast reverse path forwarding: none
          IPv6 load sharing: none 
          IPv6 interface statistics last reset: never
          IPv6 interface RP-traffic statistics: (forwarded/originated/consumed)
            Unicast packets:      0/0/0
            Unicast bytes:        0/0/0
            Multicast packets:    0/12/9
            Multicast bytes:      0/1144/640
    '''
    ShowRoutingVrfAll = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'vpnv4 unicast':
                           {'bgp_distance_internal_as': 33,
                            'bgp_distance_local': 55,
                            'ip':
                                {'10.2.2.2/24':
                                     {'ubest_num': '1',
                                      'mbest_num': '0',
                                      'best_route':
                                          {'unicast':
                                               {'nexthop':
                                                    {'Null0':
                                                         {'protocol':
                                                              {'bgp':
                                                                   {'uptime': '5w0d',
                                                                    'preference': '55',
                                                                    'metric': '0',
                                                                    'protocol_id': '100',
                                                                    'interface':
                                                                        'Ethernet2/1',
                                                                    'attribute':
                                                                        'discard',
                                                                    'tag':
                                                                        '100'}}}}}}}}}}},
             'default':
                 {'address_family':
                      {'ipv4 unicast':
                           {'bgp_distance_internal_as': 33,
                            'bgp_distance_local': 55,
                            'ip':
                                {'10.169.2.2/24':
                                     {'ubest_num': '1',
                                      'mbest_num': '0',
                                      'best_route':
                                          {'unicast':
                                               {'nexthop':
                                                    {'Null0':
                                                         {'protocol':
                                                              {'bgp':
                                                                   {'uptime': '5w0d',
                                                                    'preference': '55',
                                                                    'metric': '0',
                                                                    'protocol_id': '100',
                                                                    'interface': 'Ethernet2/1',
                                                                    'attribute': 'discard',
                                                                    'tag': '100'}}}}}}}}}}}}}
    ShowRoutingVrfAll_vrf1 = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'vpnv4 unicast':
                           {'bgp_distance_internal_as': 33,
                            'bgp_distance_local': 55,
                            'ip':
                                {'10.2.2.2/24':
                                     {'ubest_num': '1',
                                      'mbest_num': '0',
                                      'best_route':
                                          {'unicast':
                                               {'nexthop':
                                                    {'Null0':
                                                         {'protocol':
                                                              {'bgp':
                                                                   {'uptime': '5w0d',
                                                                    'preference': '55',
                                                                    'metric': '0',
                                                                    'protocol_id': '100',
                                                                    'interface':
                                                                        'Ethernet2/1',
                                                                    'attribute':
                                                                        'discard',
                                                                    'tag':
                                                                        '100'}}}}}}}}}}}, }}
    ShowRoutingIpv6VrfAll = {
        "vrf": {
            "VRF1": {
               "address_family": {
                    "ipv6 unicast": {
                         "ip": {
                              "2001:db8:1:1::1/128": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8:1:1::1": {
                                                       "protocol": {
                                                            "local": {
                                                                 "interface": "Ethernet1/1",
                                                                 "metric": "0",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              },
                              "2001:db8:1:1::/64": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8:1:1::1": {
                                                       "protocol": {
                                                            "direct": {
                                                                 "interface": "Ethernet1/1",
                                                                 "metric": "0",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              },
                              "2001:db8:2:2::2/128": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8:2:2::2": {
                                                       "protocol": {
                                                            "local": {
                                                                 "interface": "Ethernet1/1",
                                                                 "metric": "0",
                                                                 "tag": "222",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              },
                              "2001:db8:4:4:a8aa:bbff:febb:cccc/64": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8::5054:ff:fed5:63f9": {
                                                       "protocol": {
                                                            "local": {
                                                                 "interface": "Ethernet2/1",
                                                                 "metric": "0",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              },
                              "2001:db8::/64": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8::5054:ff:fed5:63f9": {
                                                       "protocol": {
                                                            "direct": {
                                                                 "interface": "Ethernet1/1",
                                                                 "metric": "0",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              },
                              "2001:db8:3:3::3/64": {
                                   "attach": "attached",
                                   "best_route": {
                                        "unicast": {
                                             "nexthop": {
                                                  "2001:db8:2:2::2": {
                                                       "protocol": {
                                                            "direct": {
                                                                 "interface": "Ethernet2/1",
                                                                 "metric": "0",
                                                                 "tag": "222",
                                                                 "uptime": "00:15:46",
                                                                 "preference": "0"
                                                            }
                                                       }
                                                  }
                                             }
                                        }
                                   },
                                   "mbest_num": "0",
                                   "ubest_num": "1"
                              }}}}}}
    }
    InterfaceOpsOutput_custom_info = {
        'Ethernet2/1': {'access_vlan': 1,
                        'native_vlan': 1,
                        'auto_negotiate': False,
                        'bandwidth': 768,
                        'counters': {'in_broadcast_pkts': 0,
                                     'in_crc_errors': 0,
                                     'in_errors': 0,
                                     'in_mac_pause_frames': 0,
                                     'in_multicast_pkts': 0,
                                     'in_octets': 0,
                                     'in_pkts': 0,
                                     'in_unicast_pkts': 0,
                                     'in_unknown_protos': 0,
                                     'last_clear': 'never',
                                     'out_broadcast_pkts': 0,
                                     'out_discard': 0,
                                     'out_errors': 0,
                                     'out_mac_pause_frames': 0,
                                     'out_multicast_pkts': 0,
                                     'out_octets': 0,
                                     'out_pkts': 0,
                                     'out_unicast_pkts': 0,
                                     'rate': {'in_rate': 0,
                                              'in_rate_pkts': 0,
                                              'load_interval': 0,
                                              'out_rate': 0,
                                              'out_rate_pkts': 0}},
                        'delay': 3330,
                        'description': 'desc',
                        'duplex_mode': 'full',
                        'enabled': True,
                        'encapsulation': {'encapsulation': 'arpa'},
                        'flow_control': {'receive': False, 'send': False},
                         'port_channel': {'port_channel_member': True,
                        'port_channel_member_intfs': ['Port-channel1']},
                        'ipv4': {'10.2.2.2/24': {'ip': '10.2.2.2',
                                                 'prefix_length': '24',
                                                 'origin': 'bgp',
                                                 'route_tag': '100',
                                                 'secondary': True},
                                 '10.3.3.3/24': {'ip': '10.3.3.3',
                                                 'prefix_length': '24',
                                                 'secondary': True},
                                 '10.4.4.4/24': {'ip': '10.4.4.4',
                                                 'prefix_length': '24',
                                                 'route_tag': '10',
                                                 'secondary': True},
                                 'unnumbered': {'interface_ref': 'loopback0'}},
                        'mac_address': 'aaaa.bbbb.cccc',
                        'medium': 'broadcast',
                        'mtu': 1600,
                        'oper_status': 'up',
                        'port_speed': '1000',
                        'last_change': '00:00:29',
                        'phys_address': '5254.003b.4aca',
                        'switchport_mode': 'trunk',
                        'switchport_enable': True,
                        'trunk_vlans': '100,300',
                        'type': '10/100/1000 Ethernet',
                        'vrf': 'VRF1'}, }

    InterfaceOpsOutput_info = {
        'Ethernet2/1': {'auto_negotiate': False,
                 'bandwidth': 768,
                 'counters': {'in_broadcast_pkts': 0,
                              'in_crc_errors': 0,
                              'in_errors': 0,
                              'in_mac_pause_frames': 0,
                              'in_multicast_pkts': 0,
                              'in_octets': 0,
                              'in_pkts': 0,
                              'in_unicast_pkts': 0,
                              'in_unknown_protos': 0,
                              'last_clear': 'never',
                              'out_broadcast_pkts': 0,
                              'out_discard': 0,
                              'out_errors': 0,
                              'out_mac_pause_frames': 0,
                              'out_multicast_pkts': 0,
                              'out_octets': 0,
                              'out_pkts': 0,
                              'out_unicast_pkts': 0,
                              'rate': {'in_rate': 0,
                                       'in_rate_pkts': 0,
                                       'load_interval': 0,
                                       'out_rate': 0,
                                       'out_rate_pkts': 0}},
                 'delay': 3330,
                 'description': 'desc',
                 'duplex_mode': 'full',
                 'enabled': True,
                 'encapsulation': {'encapsulation': 'arpa'},
                 'flow_control': {'receive': False, 'send': False},
                  'port_channel': {'port_channel_member': True,
                        'port_channel_member_intfs': ['Port-channel1']},
                 'ipv4': {'10.2.2.2/24': {'ip': '10.2.2.2',
                                          'prefix_length': '24',
                                          'origin': 'bgp',
                                          'route_tag': '100',
                                          'secondary': True},
                          '10.3.3.3/24': {'ip': '10.3.3.3',
                                          'prefix_length': '24',
                                          'secondary': True},
                          '10.4.4.4/24': {'ip': '10.4.4.4',
                                          'prefix_length': '24',
                                          'route_tag': '10',
                                          'secondary': True},
                          'unnumbered':{'interface_ref': 'loopback0'}},
                 'ipv6': {'2001:db8:1:1::1/64': {'ip': '2001:db8:1:1::1',
                                                 'prefix_length': '64',
                                                 'status': 'valid'},
                          '2001:db8:2:2::2/64': {'anycast': True,
                                                 'ip': '2001:db8:2:2::2',
                                                 'prefix_length': '64',
                                                 'status': 'valid'},
                          '2001:db8:3:3::3/64': {'ip': '2001:db8:3:3::3',
                                                 'prefix_length': '64',
                                                 'origin': 'direct',
                                                 'route_tag': '222',
                                                 'status': 'valid'},
                          '2001:db8:4:4:a8aa:bbff:febb:cccc/64': {'ip': '2001:db8:4:4:a8aa:bbff:febb:cccc',
                                                                  'prefix_length': '64',
                                                                  'eui_64': True,
                                                                  'origin': 'local',
                                                                  'status': 'valid'}},
                 'mac_address': 'aaaa.bbbb.cccc',
                 'medium': 'broadcast',
                 'mtu': 1600,
                 'oper_status': 'up',
                 'port_speed': '1000',
                 'last_change': '00:00:29',
                 'phys_address': '5254.003b.4aca',
                 'type': '10/100/1000 Ethernet',
                 'vrf': 'VRF1'},
        'Ethernet2/1.10': {'bandwidth': 768,
                        'delay': 10,
                        'enabled': False,
                        'encapsulation': {'encapsulation': 'dot1q',
                                          'first_dot1q': '10'},
                        'mac_address': '5254.003b.4af8',
                        'medium': 'broadcast',
                        'mtu': 1600,
                        'oper_status': 'down',
                        'phys_address': '5254.003b.4aca',
                        'port_channel': {'port_channel_member': False},
                        'type': '10/100/1000 Ethernet',
                        'vlan_id': '10',
                        'vrf': 'default'},
        'Ethernet2/1.20': {'bandwidth': 768,
                        'delay': 10,
                        'enabled': True,
                        'encapsulation': {'encapsulation': 'dot1q',
                                          'first_dot1q': '20'},
                        'mac_address': '5254.003b.4af8',
                        'medium': 'p2p',
                        'mtu': 1600,
                        'oper_status': 'up',
                        'phys_address': '5254.003b.4aca',
                        'port_channel': {'port_channel_member': False},
                        'type': '10/100/1000 Ethernet',
                        'vlan_id': '20',
                        'vrf': 'default'},
        'Ethernet2/10': {'vrf': 'default'},
        'Ethernet2/11': {'vrf': 'default'},
        'Ethernet2/12': {'vrf': 'default'},
        'Ethernet2/13': {'vrf': 'default'},
        'Ethernet2/14': {'vrf': 'default'},
        'Ethernet2/15': {'vrf': 'default'},
        'Ethernet2/16': {'vrf': 'default'},
        'Ethernet2/17': {'vrf': 'default'},
        'Ethernet2/18': {'vrf': 'default'},
        'Ethernet2/19': {'vrf': 'default'},
        'Ethernet2/2': {'access_vlan': 1,
                     'native_vlan': 1,
                     'auto_negotiate': False,
                     'bandwidth': 1000000,
                     'counters': {'in_broadcast_pkts': 0,
                                  'in_crc_errors': 0,
                                  'in_errors': 0,
                                  'in_mac_pause_frames': 0,
                                  'in_multicast_pkts': 0,
                                  'in_octets': 0,
                                  'in_pkts': 0,
                                  'in_unicast_pkts': 0,
                                  'in_unknown_protos': 0,
                                  'last_clear': 'never',
                                  'out_broadcast_pkts': 0,
                                  'out_discard': 0,
                                  'out_errors': 0,
                                  'out_mac_pause_frames': 0,
                                  'out_multicast_pkts': 0,
                                  'out_octets': 0,
                                  'out_pkts': 0,
                                  'out_unicast_pkts': 0,
                                  'rate': {'in_rate': 0,
                                           'in_rate_pkts': 0,
                                           'load_interval': 0,
                                           'out_rate': 0,
                                           'out_rate_pkts': 0}},
                     'delay': 10,
                     'duplex_mode': 'full',
                     'enabled': True,
                     'encapsulation': {'encapsulation': 'arpa'},
                     'flow_control': {'receive': False, 'send': False},
                        'port_channel': {'port_channel_member': True,
                        'port_channel_member_intfs': ['Port-channel1']},
                     'mac_address': '5254.00ac.b52e',
                     'medium': 'broadcast',
                     'mtu': 1500,
                     'oper_status': 'up',
                     'phys_address': '5254.00ac.b52e',
                     'port_speed': '1000',
                     'last_change': '00:07:28',
                     'switchport_mode': 'trunk',
                     'switchport_enable': True,
                     'trunk_vlans': '100,300',
                     'type': '10/100/1000 Ethernet'},
        'Ethernet2/20': {'vrf': 'default'},
        'Ethernet2/21': {'vrf': 'default'},
        'Ethernet2/22': {'vrf': 'default'},
        'Ethernet2/23': {'vrf': 'default'},
        'Ethernet2/24': {'vrf': 'default'},
        'Ethernet2/25': {'vrf': 'default'},
        'Ethernet2/26': {'vrf': 'default'},
        'Ethernet2/27': {'vrf': 'default'},
        'Ethernet2/28': {'vrf': 'default'},
        'Ethernet2/29': {'vrf': 'default'},
        'Ethernet2/3': {'access_vlan': 100,
                         'native_vlan': 1,
                     'switchport_mode': 'access',
                     'switchport_enable': True,
                     'trunk_vlans': '1-4094'},
        'Ethernet2/30': {'vrf': 'default'},
        'Ethernet2/31': {'vrf': 'default'},
        'Ethernet2/32': {'vrf': 'default'},
        'Ethernet2/33': {'vrf': 'default'},
        'Ethernet2/34': {'vrf': 'default'},
        'Ethernet2/35': {'vrf': 'default'},
        'Ethernet2/36': {'vrf': 'default'},
        'Ethernet2/37': {'vrf': 'default'},
        'Ethernet2/38': {'vrf': 'default'},
        'Ethernet2/39': {'vrf': 'default'},
        'Ethernet2/4': {'vrf': 'default'},
        'Ethernet2/40': {'vrf': 'default'},
        'Ethernet2/41': {'vrf': 'default'},
        'Ethernet2/42': {'vrf': 'default'},
        'Ethernet2/43': {'vrf': 'default'},
        'Ethernet2/44': {'vrf': 'default'},
        'Ethernet2/45': {'vrf': 'default'},
        'Ethernet2/46': {'vrf': 'default'},
        'Ethernet2/47': {'vrf': 'default'},
        'Ethernet2/48': {'vrf': 'default'},
        'Ethernet2/5': {'vrf': 'default'},
        'Ethernet2/6': {'vrf': 'default'},
        'Ethernet2/7': {'vrf': 'default'},
        'Ethernet2/8': {'vrf': 'default'},
        'Ethernet2/9': {'vrf': 'default'},
        'Ethernet3/1': {'vrf': 'default'},
        'Ethernet3/10': {'vrf': 'default'},
        'Ethernet3/11': {'vrf': 'default'},
        'Ethernet3/12': {'vrf': 'default'},
        'Ethernet3/13': {'vrf': 'default'},
        'Ethernet3/14': {'vrf': 'default'},
        'Ethernet3/15': {'vrf': 'default'},
        'Ethernet3/16': {'vrf': 'default'},
        'Ethernet3/17': {'vrf': 'default'},
        'Ethernet3/18': {'vrf': 'default'},
        'Ethernet3/19': {'vrf': 'default'},
        'Ethernet3/2': {'vrf': 'default'},
        'Ethernet3/20': {'vrf': 'default'},
        'Ethernet3/21': {'vrf': 'default'},
        'Ethernet3/22': {'vrf': 'default'},
        'Ethernet3/23': {'vrf': 'default'},
        'Ethernet3/24': {'vrf': 'default'},
        'Ethernet3/25': {'vrf': 'default'},
        'Ethernet3/26': {'vrf': 'default'},
        'Ethernet3/27': {'vrf': 'default'},
        'Ethernet3/28': {'vrf': 'default'},
        'Ethernet3/29': {'vrf': 'default'},
        'Ethernet3/3': {'vrf': 'default'},
        'Ethernet3/30': {'vrf': 'default'},
        'Ethernet3/31': {'vrf': 'default'},
        'Ethernet3/32': {'vrf': 'default'},
        'Ethernet3/33': {'vrf': 'default'},
        'Ethernet3/34': {'vrf': 'default'},
        'Ethernet3/35': {'vrf': 'default'},
        'Ethernet3/36': {'vrf': 'default'},
        'Ethernet3/37': {'vrf': 'default'},
        'Ethernet3/38': {'vrf': 'default'},
        'Ethernet3/39': {'vrf': 'default'},
        'Ethernet3/4': {'vrf': 'default'},
        'Ethernet3/40': {'vrf': 'default'},
        'Ethernet3/41': {'vrf': 'default'},
        'Ethernet3/42': {'vrf': 'default'},
        'Ethernet3/43': {'vrf': 'default'},
        'Ethernet3/44': {'vrf': 'default'},
        'Ethernet3/45': {'vrf': 'default'},
        'Ethernet3/46': {'vrf': 'default'},
        'Ethernet3/47': {'vrf': 'default'},
        'Ethernet3/48': {'vrf': 'default'},
        'Ethernet3/5': {'vrf': 'default'},
        'Ethernet3/6': {'vrf': 'default'},
        'Ethernet3/7': {'vrf': 'default'},
        'Ethernet3/8': {'vrf': 'default'},
        'Ethernet3/9': {'vrf': 'default'},
        'Ethernet4/1': {'vrf': 'default'},
        'Ethernet4/10': {'vrf': 'default'},
        'Ethernet4/11': {'vrf': 'default'},
        'Ethernet4/12': {'vrf': 'default'},
        'Ethernet4/13': {'vrf': 'default'},
        'Ethernet4/14': {'vrf': 'default'},
        'Ethernet4/15': {'vrf': 'default'},
        'Ethernet4/16': {'vrf': 'default'},
        'Ethernet4/17': {'vrf': 'default'},
        'Ethernet4/18': {'vrf': 'default'},
        'Ethernet4/19': {'vrf': 'default'},
        'Ethernet4/2': {'vrf': 'default'},
        'Ethernet4/20': {'vrf': 'default'},
        'Ethernet4/21': {'vrf': 'default'},
        'Ethernet4/22': {'vrf': 'default'},
        'Ethernet4/23': {'vrf': 'default'},
        'Ethernet4/24': {'vrf': 'default'},
        'Ethernet4/25': {'vrf': 'default'},
        'Ethernet4/26': {'vrf': 'default'},
        'Ethernet4/27': {'vrf': 'default'},
        'Ethernet4/28': {'vrf': 'default'},
        'Ethernet4/29': {'vrf': 'default'},
        'Ethernet4/3': {'vrf': 'default'},
        'Ethernet4/30': {'vrf': 'default'},
        'Ethernet4/31': {'vrf': 'default'},
        'Ethernet4/32': {'vrf': 'default'},
        'Ethernet4/33': {'vrf': 'default'},
        'Ethernet4/34': {'vrf': 'default'},
        'Ethernet4/35': {'vrf': 'default'},
        'Ethernet4/36': {'vrf': 'default'},
        'Ethernet4/37': {'vrf': 'default'},
        'Ethernet4/38': {'vrf': 'default'},
        'Ethernet4/39': {'vrf': 'default'},
        'Ethernet4/4': {'vrf': 'default'},
        'Ethernet4/40': {'vrf': 'default'},
        'Ethernet4/41': {'vrf': 'default'},
        'Ethernet4/42': {'vrf': 'default'},
        'Ethernet4/43': {'vrf': 'default'},
        'Ethernet4/44': {'vrf': 'default'},
        'Ethernet4/45': {'vrf': 'default'},
        'Ethernet4/46': {'vrf': 'default'},
        'Ethernet4/47': {'vrf': 'default'},
        'Ethernet4/48': {'vrf': 'default'},
        'Ethernet4/5': {'vrf': 'default'},
        'Ethernet4/6': {'vrf': 'default'},
        'Ethernet4/7': {'vrf': 'default'},
        'Ethernet4/8': {'vrf': 'default'},
        'Ethernet4/9': {'vrf': 'default'},
        'Null0': {'vrf': 'default'},
        'Mgmt0': 
            {'auto_negotiate': True,
            'bandwidth': 1000000,
            'counters': 
                {'in_broadcast_pkts': 4,
                'in_multicast_pkts': 2,
                'in_octets': 4726,
                'in_pkts': 2,
                'in_unicast_pkts': 0,
                'rate':
                    {'in_rate': 0,
                    'in_rate_pkts': 0,
                    'load_interval': 1,
                    'out_rate': 24,
                    'out_rate_pkts': 0}},
                'delay': 10,
                'duplex_mode': 'full',
                'enabled': True,
                'encapsulation': {'encapsulation': 'arpa'},
                'mac_address': '5254.00c9.d26e',
                'medium': 'broadcast',
                'mtu': 1500,
                'oper_status': 'up',
                'phys_address': '5254.00c9.d26e',
                'port_channel': {'port_channel_member': False},
                'port_speed': '1000',
                'type': 'Ethernet',
                'vrf': 'management'}}
