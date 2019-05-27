''' 
Interface Genie Ops Object Outputs for IOS.
'''


class InterfaceOutput(object):

    ShowInterfaces = '''\
        Vlan1 is up, line protocol is up 
          Hardware is EtherSVI, address is 843d.c638.b9c0 (bia 843d.c638.b9c0)
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive not supported
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 2d13h, output 6w1d, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             353484 packets input, 100219974 bytes, 0 no buffer
             Received 0 broadcasts (0 IP multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             117 packets output, 7488 bytes, 0 underruns
             0 output errors, 2 interface resets
             0 output buffer failures, 0 output buffers swapped out
        Vlan99 is up, line protocol is down 
          Hardware is EtherSVI, address is 843d.c638.b9c1 (bia 843d.c638.b9c1)
          Internet address is 18.0.1.2/24
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive not supported
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 9w0d, output 6w1d, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             286 packets input, 22592 bytes, 0 no buffer
             Received 0 broadcasts (0 IP multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             307 packets output, 24544 bytes, 0 underruns
             0 output errors, 9 interface resets
             0 output buffer failures, 0 output buffers swapped out
        FastEthernet0 is up, line protocol is up 
          Hardware is PowerPC405 FastEthernet, address is 843d.c638.b9b7 (bia 843d.c638.b9b7)
          Internet address is 10.1.8.146/24
          MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive not set
          Full-duplex, 100Mb/s, MII
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 00:00:00, output 00:00:00, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/0 (size/max)
          5 minute input rate 2000 bits/sec, 3 packets/sec
          5 minute output rate 1000 bits/sec, 1 packets/sec
             5750392 packets input, 592470159 bytes
             Received 505096 broadcasts (6 IP multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog
             0 input packets with dribble condition detected
             267622 packets output, 58024476 bytes, 0 underruns
             0 output errors, 0 collisions, 1 interface resets
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier
             0 output buffer failures, 0 output buffers swapped out
        GigabitEthernet1/0/1 is up, line protocol is up (connected) 
          Hardware is Gigabit Ethernet, address is 843d.c638.b981 (bia 843d.c638.b981)
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 00:00:29, output 00:00:01, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             5391746 packets input, 1396754269 bytes, 0 no buffer
             Received 4814991 broadcasts (1399945 multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 1399945 multicast, 0 pause input
             0 input packets with dribble condition detected
             2871210 packets output, 227369424 bytes, 0 underruns
             0 output errors, 0 collisions, 1 interface resets
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 PAUSE output
             0 output buffer failures, 0 output buffers swapped out
        GigabitEthernet1/0/2 is up, line protocol is up (connected) 
          Hardware is Gigabit Ethernet, address is 843d.c638.b982 (bia 843d.c638.b982)
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 00:00:17, output 00:00:01, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             5380657 packets input, 1395777395 bytes, 0 no buffer
             Received 4805330 broadcasts (1390555 multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 1390555 multicast, 0 pause input
             0 input packets with dribble condition detected
             2858192 packets output, 226262568 bytes, 0 underruns
             0 output errors, 0 collisions, 1 interface resets
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 PAUSE output
             0 output buffer failures, 0 output buffers swapped out
        GigabitEthernet1/0/3 is up, line protocol is up (connected) 
          Hardware is Gigabit Ethernet, address is 843d.c638.b9c5 (bia 843d.c638.b9c5)
          MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input 00:00:00, output 00:00:01, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             7282676 packets input, 1517788828 bytes, 0 no buffer
             Received 6706223 broadcasts (0 IP multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 3291045 multicast, 0 pause input
             0 input packets with dribble condition detected
             800134 packets output, 92023448 bytes, 0 underruns
             0 output errors, 0 collisions, 1 interface resets
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 PAUSE output
             0 output buffer failures, 0 output buffers swapped out
        GigabitEthernet1/0/4 is down, line protocol is down (notconnect) 
          Hardware is Gigabit Ethernet, address is 843d.c638.b984 (bia 843d.c638.b984)
          MTU 1500 bytes, BW 10000 Kbit, DLY 1000 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Auto-duplex, Auto-speed, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input never, output never, output hang never
          Last clearing of "show interface" counters never
          Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 0 bits/sec, 0 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             250974 packets input, 25264740 bytes, 0 no buffer
             Received 215432 broadcasts (202521 multicasts)
             0 runts, 0 giants, 0 throttles
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 202521 multicast, 0 pause input
             0 input packets with dribble condition detected
             64338 packets output, 8655637 bytes, 0 underruns
             0 output errors, 0 collisions, 1 interface resets
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 PAUSE output
             0 output buffer failures, 0 output buffers swapped out
    '''


    ShowIpInterface = '''\
        Vlan1 is up, line protocol is up
          Internet protocol processing disabled
        Vlan99 is up, line protocol is down
          Internet address is 18.0.1.2/24
          Broadcast address is 255.255.255.255
          Address determined by setup command
          MTU is 1500 bytes
          Helper address is not set
          Directed broadcast forwarding is disabled
          Outgoing access list is not set
          Inbound  access list is not set
          Proxy ARP is enabled
          Local Proxy ARP is disabled
          Security level is default
          Split horizon is enabled
          ICMP redirects are always sent
          ICMP unreachables are always sent
          ICMP mask replies are never sent
          IP fast switching is enabled
          IP CEF switching is enabled
          IP CEF switching turbo vector
          IP Null turbo vector
          IP multicast fast switching is enabled
          IP multicast distributed fast switching is disabled
          IP route-cache flags are Fast, CEF
          Router Discovery is disabled
          IP output packet accounting is disabled
          IP access violation accounting is disabled
          TCP/IP header compression is disabled
          RTP/IP header compression is disabled
          Probe proxy name replies are disabled
          Policy routing is disabled
          Network address translation is disabled
          BGP Policy Mapping is disabled
          Input features: MCI Check
          Output features: Input interface drop, Check hwidb
          WCCP Redirect outbound is disabled
          WCCP Redirect inbound is disabled
          WCCP Redirect exclude is disabled
        FastEthernet0 is up, line protocol is up
          Internet address is 10.1.8.146/24
          Broadcast address is 255.255.255.255
          Address determined by non-volatile memory
          MTU is 1500 bytes
          Helper address is not set
          Directed broadcast forwarding is disabled
          Outgoing access list is not set
          Inbound  access list is not set
          Proxy ARP is enabled
          Local Proxy ARP is disabled
          Security level is default
          Split horizon is enabled
          ICMP redirects are always sent
          ICMP unreachables are always sent
          ICMP mask replies are never sent
          IP fast switching is disabled
          IP CEF switching is disabled
          IP Null turbo vector
          IP Null turbo vector
          IP multicast fast switching is disabled
          IP multicast distributed fast switching is disabled
          IP route-cache flags are No CEF, No Distributed
          Router Discovery is disabled
          IP output packet accounting is disabled
          IP access violation accounting is disabled
          TCP/IP header compression is disabled
          RTP/IP header compression is disabled
          Probe proxy name replies are disabled
          Policy routing is disabled
          Network address translation is disabled
          BGP Policy Mapping is disabled
          Input features: MCI Check
          Output features: Input interface drop, Check hwidb
          WCCP Redirect outbound is disabled
          WCCP Redirect inbound is disabled
          WCCP Redirect exclude is disabled
        GigabitEthernet1/0/1 is up, line protocol is up
          Inbound  access list is not set
        GigabitEthernet1/0/2 is up, line protocol is up
          Inbound  access list is not set
    '''

    ShowIpv6Interface = '''\
        Vlan99 is up, line protocol is down
          IPv6 is tentative, link-local address is FE80::863D:C6FF:FE38:B9C1 [TEN]
          No Virtual link-local address(es):
          Global unicast address(es):
            2001:ABAD:BEEF::2, subnet is 2001:ABAD:BEEF::/64 [TEN]
          Joined group address(es):
            FF02::1
          MTU is 1500 bytes
          ICMP error messages limited to one every 100 milliseconds
          ICMP redirects are enabled
          ICMP unreachables are sent
          Output features: Check hwidb
          ND DAD is enabled, number of DAD attempts: 1
          ND reachable time is 30000 milliseconds (using 30000)
    '''

    ShowVrfDetail = '''\
        VRF ABCD; default RD <not set>; default VPNID <not set>
          No interfaces
        Address family ipv4 (Table ID = 0x14):
          Connected addresses are not in global routing table
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 not active.

        VRF Mgmt-vrf; default RD <not set>; default VPNID <not set>
          No interfaces
        Address family ipv4 (Table ID = 0x1):
          Connected addresses are not in global routing table
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 not active.

        VRF vrf1; default RD 1:1; default VPNID <not set>
          No interfaces
        Address family ipv4 (Table ID = 0x19):
          Connected addresses are not in global routing table
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 not active.

        VRF vrf2; default RD 1:2; default VPNID <not set>
          No interfaces
        Address family ipv4 (Table ID = 0x1A):
          Connected addresses are not in global routing table
          No Export VPN route-target communities
          No Import VPN route-target communities
          No import route-map
          No export route-map
          VRF label distribution protocol: not configured
          VRF label allocation mode: per-prefix
        Address family ipv6 not active.
    '''

    ShowInterfacesAccounting = '''\
        Vlan1 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                              IP         60      20640          0          0
                             ARP      75108    4506480        117       7020
        Vlan99 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                              IP        232      18096        222      17284
                             ARP         10        600         51       3060
                            IPv6         44       3896         34       2972
        FastEthernet0 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                           Other      96510    7430556       8085    2647942
                              IP     616665  211824128     162892   13686898
                   Spanning Tree    5782786  300705452          0          0
                             ARP      30996    1863060        407      24420
                             CDP      96607   37290302      96420   41730360
        GigabitEthernet1/0/1 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                           Other          0          0     555425   34912532
                   Spanning Tree       1630      97800    1874087  112452188
                             CDP      70133   32751715      62957   28711360
        GigabitEthernet1/0/2 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                           Other          0          0     555426   34912592
                   Spanning Tree       1617      97020    1874089  112452308
                             CDP      70124   32747512      62957   28711360
        GigabitEthernet1/0/3 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                           Other          0          0     378675   22828938
                   Spanning Tree    3788586  227315160          0          0
                             ARP          9        540          3        180
                             CDP      70249   32805887      63079   27754760
        GigabitEthernet1/0/4 
                        Protocol    Pkts In   Chars In   Pkts Out  Chars Out
    '''

    InterfaceOpsOutput_info = {
        'FastEthernet0': {'accounting': {'arp': {'chars_in': 1863060,
                                                 'chars_out': 24420,
                                                 'pkts_in': 30996,
                                                 'pkts_out': 407},
                                         'cdp': {'chars_in': 37290302,
                                                 'chars_out': 41730360,
                                                 'pkts_in': 96607,
                                                 'pkts_out': 96420},
                                         'ip': {'chars_in': 211824128,
                                                 'chars_out': 13686898,
                                                 'pkts_in': 616665,
                                                 'pkts_out': 162892},
                                         'other': {'chars_in': 7430556,
                                                 'chars_out': 2647942,
                                                 'pkts_in': 96510,
                                                 'pkts_out': 8085},
                                         'spanning tree': {'chars_in': 300705452,
                                                         'chars_out': 0,
                                                         'pkts_in': 5782786,
                                                         'pkts_out': 0}},
                         'bandwidth': 100000,
                         'counters': {'in_broadcast_pkts': 6,
                                     'in_crc_errors': 0,
                                     'in_errors': 0,
                                     'in_multicast_pkts': 505096,
                                     'last_clear': 'never',
                                     'out_errors': 0,
                                     'out_octets': 58024476,
                                     'out_pkts': 267622,
                                     'rate': {'in_rate': 2000,
                                                 'in_rate_pkts': 3,
                                                 'load_interval': 300,
                                                 'out_rate': 1000,
                                                 'out_rate_pkts': 1}},
                         'delay': 100,
                         'enabled': True,
                         'encapsulation': {'encapsulation': 'arpa'},
                         'ipv4': {'10.1.8.146/24': {'ip': '10.1.8.146',
                                                     'prefix_length': '24',
                                                     'secondary': False}},
                         'mac_address': '843d.c638.b9b7',
                         'mtu': 1500,
                         'oper_status': 'up',
                         'phys_address': '843d.c638.b9b7',
                         'port_channel': {'port_channel_member': False},
                         'switchport_enable': False,
                         'type': 'PowerPC405 FastEthernet'},
         'GigabitEthernet1/0/1': {'accounting': {'cdp': {'chars_in': 32751715,
                                                         'chars_out': 28711360,
                                                         'pkts_in': 70133,
                                                         'pkts_out': 62957},
                                                 'other': {'chars_in': 0,
                                                         'chars_out': 34912532,
                                                         'pkts_in': 0,
                                                         'pkts_out': 555425},
                                                 'spanning tree': {'chars_in': 97800,
                                                                 'chars_out': 112452188,
                                                                 'pkts_in': 1630,
                                                                 'pkts_out': 1874087}},
                                 'bandwidth': 1000000,
                                 'counters': {'in_broadcast_pkts': 1399945,
                                             'in_crc_errors': 0,
                                             'in_errors': 0,
                                             'in_mac_pause_frames': 0,
                                             'in_multicast_pkts': 1399945,
                                             'in_octets': 1396754269,
                                             'in_pkts': 5391746,
                                             'last_clear': 'never',
                                             'out_errors': 0,
                                             'out_octets': 227369424,
                                             'out_pkts': 2871210,
                                             'rate': {'in_rate': 0,
                                                     'in_rate_pkts': 0,
                                                     'load_interval': 300,
                                                     'out_rate': 0,
                                                     'out_rate_pkts': 0}},
                                 'delay': 10,
                                 'duplex_mode': 'full',
                                 'enabled': True,
                                 'encapsulation': {'encapsulation': 'arpa'},
                                 'flow_control': {'receive': False, 'send': False},
                                 'mac_address': '843d.c638.b981',
                                 'mtu': 1500,
                                 'oper_status': 'up',
                                 'phys_address': '843d.c638.b981',
                                 'port_channel': {'port_channel_member': False},
                                 'port_speed': '1000',
                                 'switchport_enable': False,
                                 'type': 'Gigabit Ethernet'},
         'GigabitEthernet1/0/2': {'accounting': {'cdp': {'chars_in': 32747512,
                                                         'chars_out': 28711360,
                                                         'pkts_in': 70124,
                                                         'pkts_out': 62957},
                                                 'other': {'chars_in': 0,
                                                         'chars_out': 34912592,
                                                         'pkts_in': 0,
                                                         'pkts_out': 555426},
                                                 'spanning tree': {'chars_in': 97020,
                                                                 'chars_out': 112452308,
                                                                 'pkts_in': 1617,
                                                                 'pkts_out': 1874089}},
                                 'bandwidth': 1000000,
                                 'counters': {'in_broadcast_pkts': 1390555,
                                             'in_crc_errors': 0,
                                             'in_errors': 0,
                                             'in_mac_pause_frames': 0,
                                             'in_multicast_pkts': 1390555,
                                             'in_octets': 1395777395,
                                             'in_pkts': 5380657,
                                             'last_clear': 'never',
                                             'out_errors': 0,
                                             'out_octets': 226262568,
                                             'out_pkts': 2858192,
                                             'rate': {'in_rate': 0,
                                                     'in_rate_pkts': 0,
                                                     'load_interval': 300,
                                                     'out_rate': 0,
                                                     'out_rate_pkts': 0}},
                                 'delay': 10,
                                 'duplex_mode': 'full',
                                 'enabled': True,
                                 'encapsulation': {'encapsulation': 'arpa'},
                                 'flow_control': {'receive': False, 'send': False},
                                 'mac_address': '843d.c638.b982',
                                 'mtu': 1500,
                                 'oper_status': 'up',
                                 'phys_address': '843d.c638.b982',
                                 'port_channel': {'port_channel_member': False},
                                 'port_speed': '1000',
                                 'switchport_enable': False,
                                 'type': 'Gigabit Ethernet'},
         'GigabitEthernet1/0/3': {'accounting': {'arp': {'chars_in': 540,
                                                         'chars_out': 180,
                                                         'pkts_in': 9,
                                                         'pkts_out': 3},
                                                 'cdp': {'chars_in': 32805887,
                                                         'chars_out': 27754760,
                                                         'pkts_in': 70249,
                                                         'pkts_out': 63079},
                                                 'other': {'chars_in': 0,
                                                         'chars_out': 22828938,
                                                         'pkts_in': 0,
                                                         'pkts_out': 378675},
                                                 'spanning tree': {'chars_in': 227315160,
                                                                 'chars_out': 0,
                                                                 'pkts_in': 3788586,
                                                                 'pkts_out': 0}},
                                 'bandwidth': 1000000,
                                 'counters': {'in_broadcast_pkts': 0,
                                             'in_crc_errors': 0,
                                             'in_errors': 0,
                                             'in_mac_pause_frames': 0,
                                             'in_multicast_pkts': 3291045,
                                             'in_octets': 1517788828,
                                             'in_pkts': 7282676,
                                             'last_clear': 'never',
                                             'out_errors': 0,
                                             'out_octets': 92023448,
                                             'out_pkts': 800134,
                                             'rate': {'in_rate': 0,
                                                     'in_rate_pkts': 0,
                                                     'load_interval': 300,
                                                     'out_rate': 0,
                                                     'out_rate_pkts': 0}},
                                 'delay': 10,
                                 'duplex_mode': 'full',
                                 'enabled': True,
                                 'encapsulation': {'encapsulation': 'arpa'},
                                 'flow_control': {'receive': False, 'send': False},
                                 'mac_address': '843d.c638.b9c5',
                                 'mtu': 1500,
                                 'oper_status': 'up',
                                 'phys_address': '843d.c638.b9c5',
                                 'port_channel': {'port_channel_member': False},
                                 'port_speed': '1000',
                                 'switchport_enable': False,
                                 'type': 'Gigabit Ethernet'},
         'GigabitEthernet1/0/4': {'bandwidth': 10000,
                                 'counters': {'in_broadcast_pkts': 202521,
                                             'in_crc_errors': 0,
                                             'in_errors': 0,
                                             'in_mac_pause_frames': 0,
                                             'in_multicast_pkts': 202521,
                                             'in_octets': 25264740,
                                             'in_pkts': 250974,
                                             'last_clear': 'never',
                                             'out_errors': 0,
                                             'out_octets': 8655637,
                                             'out_pkts': 64338,
                                             'rate': {'in_rate': 0,
                                                     'in_rate_pkts': 0,
                                                     'load_interval': 300,
                                                     'out_rate': 0,
                                                     'out_rate_pkts': 0}},
                                 'delay': 1000,
                                 'duplex_mode': 'auto',
                                 'enabled': True,
                                 'encapsulation': {'encapsulation': 'arpa'},
                                 'flow_control': {'receive': False, 'send': False},
                                 'mac_address': '843d.c638.b984',
                                 'mtu': 1500,
                                 'oper_status': 'down',
                                 'phys_address': '843d.c638.b984',
                                 'port_channel': {'port_channel_member': False},
                                 'port_speed': 'auto',
                                 'switchport_enable': False,
                                 'type': 'Gigabit Ethernet'},
         'Vlan1': {'accounting': {'arp': {'chars_in': 4506480,
                                         'chars_out': 7020,
                                         'pkts_in': 75108,
                                         'pkts_out': 117},
                                 'ip': {'chars_in': 20640,
                                         'chars_out': 0,
                                         'pkts_in': 60,
                                         'pkts_out': 0}},
                 'bandwidth': 1000000,
                 'counters': {'in_broadcast_pkts': 0,
                             'in_crc_errors': 0,
                             'in_errors': 0,
                             'in_multicast_pkts': 0,
                             'in_octets': 100219974,
                             'in_pkts': 353484,
                             'last_clear': 'never',
                             'out_errors': 0,
                             'out_octets': 7488,
                             'out_pkts': 117,
                             'rate': {'in_rate': 0,
                                         'in_rate_pkts': 0,
                                         'load_interval': 300,
                                         'out_rate': 0,
                                         'out_rate_pkts': 0}},
                 'delay': 10,
                 'enabled': True,
                 'encapsulation': {'encapsulation': 'arpa'},
                 'mac_address': '843d.c638.b9c0',
                 'mtu': 1500,
                 'oper_status': 'up',
                 'phys_address': '843d.c638.b9c0',
                 'port_channel': {'port_channel_member': False},
                 'switchport_enable': False,
                 'type': 'EtherSVI'},
         'Vlan99': {'accounting': {'arp': {'chars_in': 600,
                                         'chars_out': 3060,
                                         'pkts_in': 10,
                                         'pkts_out': 51},
                                 'ip': {'chars_in': 18096,
                                         'chars_out': 17284,
                                         'pkts_in': 232,
                                         'pkts_out': 222},
                                 'ipv6': {'chars_in': 3896,
                                         'chars_out': 2972,
                                         'pkts_in': 44,
                                         'pkts_out': 34}},
                 'bandwidth': 1000000,
                 'counters': {'in_broadcast_pkts': 0,
                                 'in_crc_errors': 0,
                                 'in_errors': 0,
                                 'in_multicast_pkts': 0,
                                 'in_octets': 22592,
                                 'in_pkts': 286,
                                 'last_clear': 'never',
                                 'out_errors': 0,
                                 'out_octets': 24544,
                                 'out_pkts': 307,
                                 'rate': {'in_rate': 0,
                                         'in_rate_pkts': 0,
                                         'load_interval': 300,
                                         'out_rate': 0,
                                         'out_rate_pkts': 0}},
                 'delay': 10,
                 'enabled': True,
                 'encapsulation': {'encapsulation': 'arpa'},
                 'ipv4': {'18.0.1.2/24': {'ip': '18.0.1.2',
                                             'prefix_length': '24',
                                             'secondary': False}},
                 'ipv6': {'2001:ABAD:BEEF::2/64': {'ip': '2001:ABAD:BEEF::2',
                                                     'prefix_length': '64',
                                                     'status': 'tentative'},
                             'FE80::863D:C6FF:FE38:B9C1': {'ip': 'FE80::863D:C6FF:FE38:B9C1',
                                                         'origin': 'link_layer',
                                                         'status': 'tentative'}},
                 'mac_address': '843d.c638.b9c1',
                 'mtu': 1500,
                 'oper_status': 'down',
                 'phys_address': '843d.c638.b9c1',
                 'port_channel': {'port_channel_member': False},
                 'switchport_enable': False,
                 'type': 'EtherSVI'}
    }
