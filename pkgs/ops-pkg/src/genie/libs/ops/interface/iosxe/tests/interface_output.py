''' 
Interface Genie Ops Object Outputs for IOSXE.
'''


class InterfaceOutput(object):

    ShowInterfaces = {
        "GigabitEthernet1/0/1": {
            "flow_control": {
                 "send": False,
                 "receive": False
            },
            "type": "Gigabit Ethernet",
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "1d02h",
                 "out_interface_resets": 2,
                 "in_mac_pause_frames": 0,
                 "out_collision": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 30,
                      "out_rate": 0,
                      "in_rate": 0,
                      "in_rate_pkts": 0
                 },
                 "in_watchdog": 0,
                 "out_deferred": 0,
                 "out_mac_pause_frames": 0,
                 "in_pkts": 12127,
                 "in_multicast_pkts": 4171,
                 "in_runts": 0,
                 "out_unknown_protocl_drops": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_lost_carrier": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 2297417,
                 "in_crc_errors": 0,
                 "out_no_carrier": 0,
                 "in_with_dribble": 0,
                 "in_broadcast_pkts": 0,
                 "out_pkts": 12229,
                 "out_late_collision": 0,
                 "out_octets": 2321107,
                 "in_overrun": 0,
                 "out_babble": 0
            },
            "phys_address": "0057.d228.1a64",
            "keepalive": 10,
            "output_hang": "never",
            "txload": "1/255",
            "description": "desc",
            "oper_status": "down",
            "arp_type": "arpa",
            "rxload": "1/255",
            "duplex_mode": "auto",
            "queues": {
                 "input_queue_size": 0,
                 "total_output_drop": 0,
                 "input_queue_drops": 0,
                 "input_queue_max": 375,
                 "output_queue_size": 0,
                 "input_queue_flushes": 0,
                 "output_queue_max": 40,
                 "queue_strategy": "fifo"
            },
            "ipv4": {
                 "10.1.1.1/24": {
                      "prefix_length": "24",
                      "ip": "10.1.1.1"
                 }
            },
            "encapsulations": {
                 "encapsulation": "arpa"
            },
            "last_input": "never",
            "last_output": "04:39:18",
            "line_protocol": "down",
            "mac_address": "0057.d228.1a64",
            "connected": False,
            "port_channel": {
                 "port_channel_member": False
            },
            "media_type": "10/100/1000BaseTX",
            "bandwidth": 768,
            'port_speed': '1000mb/s',
            "enabled": False,
            "arp_timeout": "04:00:00",
            "mtu": 1500,
            "delay": 3330,
            "reliability": "255/255"
        },
        "GigabitEthernet1/0/2": {
            "flow_control": {
                 "send": False,
                 "receive": False
            },
            "type": "Gigabit Ethernet",
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "1d02h",
                 "out_interface_resets": 5,
                 "in_mac_pause_frames": 0,
                 "out_collision": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 300,
                      "out_rate": 0,
                      "in_rate": 3000,
                      "in_rate_pkts": 5
                 },
                 "in_watchdog": 0,
                 "out_deferred": 0,
                 "out_mac_pause_frames": 0,
                 "in_pkts": 545526,
                 "in_multicast_pkts": 535961,
                 "in_runts": 0,
                 "out_unknown_protocl_drops": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_lost_carrier": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 41210298,
                 "in_crc_errors": 0,
                 "out_no_carrier": 0,
                 "in_with_dribble": 0,
                 "in_broadcast_pkts": 535961,
                 "out_pkts": 23376,
                 "out_late_collision": 0,
                 "out_octets": 3642296,
                 "in_overrun": 0,
                 "out_babble": 0
            },
            "phys_address": "0057.d228.1a02",
            "keepalive": 10,
            "output_hang": "never",
            "txload": "1/255",
            "oper_status": "up",
            "arp_type": "arpa",
            "media_type": "10/100/1000BaseTX",
            "rxload": "1/255",
            "duplex_mode": "full",
            "queues": {
                 "input_queue_size": 0,
                 "total_output_drop": 0,
                 "input_queue_drops": 0,
                 "input_queue_max": 2000,
                 "output_queue_size": 0,
                 "input_queue_flushes": 0,
                 "output_queue_max": 40,
                 "queue_strategy": "fifo"
            },
            "encapsulations": {
                 "encapsulation": "arpa"
            },
            "last_input": "never",
            "last_output": "00:00:02",
            "line_protocol": "up",
            "mac_address": "0057.d228.1a02",
            "connected": True,
            "port_channel": {
                 "port_channel_member": False
            },
            "arp_timeout": "04:00:00",
            "bandwidth": 1000000,
            'port_speed': '1000mb/s',
            "enabled": True,
            "mtu": 1500,
            "delay": 10,
            "reliability": "255/255"
       }
    }


    ShowEtherchannelSummary = {
        'number_of_lag_in_use': 2,
        'number_of_aggregators': 2,
        'interfaces': {
            'Port-channel2': {
                'name': 'Port-channel2',
                'bundle_id': 2,
                'protocol': 'lacp',
                'flags': 'RU',
                'oper_status': 'up',
                'members': {
                    'GigabitEthernet0/0/0': {
                        'interface': 'GigabitEthernet0/0/0',
                        'flags': 'bndl',
                        'bundled': True,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel2"
                        },
                    },
                    'GigabitEthernet0/0/1': {
                        'interface': 'GigabitEthernet0/0/1',
                        'flags': 'hot-sby',
                        'bundled': False,
                        'port_channel': {
                           "port_channel_member": True,
                           "port_channel_int": "Port-channel2"
                        },
                    },
                },
                'port_channel': {
                    'port_channel_member': True,
                    'port_channel_member_intfs': ['GigabitEthernet0/0/0',
                                                  'GigabitEthernet0/0/1'],

                }
            },
        },
    }

    ShowIpInterface = {
        "GigabitEthernet1/0/1": {
            "sevurity_level": "default",
            'address_determined_by': 'setup command',
            "ip_route_cache_flags": [
                 "CEF",
                 "Fast"
            ],
            "enabled": False,
            "oper_status": "down",
            "router_discovery": False,
            "ip_multicast_fast_switching": False,
            "split_horizon": True,
            "bgp_policy_mapping": False,
            "ip_output_packet_accounting": False,
            "mtu": 1500,
            "policy_routing": False,
            "local_proxy_arp": False,
            "proxy_arp": True,
            "network_address_translation": False,
            "ip_cef_switching_turbo_vector": True,
            "icmp": {
                "redirects": "always sent",
                "mask_replies": "never sent",
                "unreachables": "always sent",
            },
            "ipv4": {
                 "10.1.1.1/24": {
                      "prefix_length": "24",
                      "ip": "10.1.1.1",
                      "secondary": False,
                      "broadcase_address": "255.255.255.255"
                 },
                 "10.2.2.2/24": {
                      "prefix_length": "24",
                      "ip": "10.2.2.2",
                      "secondary": True
                 },
            },
            "ip_access_violation_accounting": False,
            "ip_cef_switching": True,
            "unicast_routing_topologies": {
                 "topology": {
                     "base": {
                         "status": "up"
                      }
                  },
            },
            'wccp': {
              'redirect_outbound': False,
              'redirect_inbound': False,
              'redirect_exclude': False,
            },
            "ip_null_turbo_vector": True,
            "probe_proxy_name_replies": False,
            "ip_fast_switching": True,
            "ip_multicast_distributed_fast_switching": False,
            "tcp_ip_header_compression": False,
            "rtp_ip_header_compression": False,
            "directed_broadcast_forwarding": False,
            "ip_flow_switching": False,
            "input_features": ["MCI Check", "QoS Classification", "QoS Marking"],
        }
    }

    ShowIpv6Interface = {
        "GigabitEthernet1/0/1": {
            "joined_group_addresses": [
                 "FF02::1"
            ],
            "ipv6": {
                 "2001:DB8:2:2::2/64": {
                      "ip": "2001:DB8:2:2::2",
                      "prefix_length": "64",
                      "status": "tentative"
                 },
                 "2001:db8:400::1/126": {
                      "ip": "2001:db8:400::1",
                      "prefix_length": "126",
                      "status": "tentative"
                 },
                 "2001:DB8:1:1::1/64": {
                      "ip": "2001:DB8:1:1::1",
                      "prefix_length": "64",
                      "status": "tentative"
                 },
                 "2001:DB8:4:4:257:D2FF:FE28:1A64/64": {
                      "ip": "2001:DB8:4:4:257:D2FF:FE28:1A64",
                      "prefix_length": "64",
                      "status": "tentative",
                      "eui_64": True
                 },
                 "2001:DB8:3:3::3/64": {
                      "ip": "2001:DB8:3:3::3",
                      "prefix_length": "64",
                      "status": "tentative",
                      "anycast": True
                 },
                 "FE80::257:D2FF:FE28:1A64": {
                      "ip": "FE80::257:D2FF:FE28:1A64",
                      "status": "tentative",
                      "origin": "link_layer",
                 },
                 "enabled": True,
                 "nd": {
                      "dad_attempts": 1,
                      "ns_retransmit_interval": 1000,
                      "dad_enabled": True,
                      "reachable_time": 30000,
                      "using_time": 30000
                 },
                 "icmp": {
                      "error_messages_limited": 100,
                      "redirects": True,
                      "unreachables": "sent"
                 },
            },
            "oper_status": "down",
            "enabled": False,
            "mtu": 1500
        },
    }

    ShowVrf = {
        'vrf': {
            'Mgmt-intf': {
                'protocols': ['ipv4', 'ipv6'],
                'interfaces': ['GigabitEthernet1/0/2'],
            },
            'VRF1': {
                'route_distinguisher': '65000:1',
                'protocols': ['ipv4', 'ipv6'],
                'interfaces': ['GigabitEthernet1/0/1'],
            }
        }
    }

    ShowInterfacesAccounting = {
        "GigabitEthernet1/0/1": {
            "accounting": {
                "arp": {
                    "chars_in": 4590030,
                    "chars_out": 120,
                    "pkts_in": 109280,
                    "pkts_out": 2
                },
                "ip": {
                    "chars_in": 2173570,
                    "chars_out": 2167858,
                    "pkts_in": 22150,
                    "pkts_out": 22121
                },
                "ipv6": {
                    "chars_in": 1944,
                    "chars_out": 0,
                    "pkts_in": 24,
                    "pkts_out": 0
                },
                "other": {
                    "chars_in": 5306164,
                    "chars_out": 120,
                    "pkts_in": 112674,
                    "pkts_out": 2
                }
            }
        },
        "GigabitEthernet1/0/2": {
            "accounting": {
                "arp": {
                    "chars_in": 5460,
                    "chars_out": 5520,
                    "pkts_in": 91,
                    "pkts_out": 92
                },
                "ip": {
                    "chars_in": 968690,
                    "chars_out": 1148402,
                    "pkts_in": 11745,
                    "pkts_out": 10821
                },
                "ipv6": {
                    "chars_in": 70,
                    "chars_out": 0,
                    "pkts_in": 1,
                    "pkts_out": 0
                },
                "other": {
                    "chars_in": 741524,
                    "chars_out": 5520,
                    "pkts_in": 3483,
                    "pkts_out": 92
                }
            }
        }
    }
    ShowInterfaces_gi1 = '''
    GigabitEthernet1/0/1 is administratively down, line protocol is down (disabled) 
          Hardware is Gigabit Ethernet, address is 0057.d228.1a64 (bia 0057.d228.1a64)
          Description: desc
          Internet address is 10.1.1.1/24
          MTU 1500 bytes, BW 768 Kbit/sec, DLY 3330 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Auto-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input never, output 04:39:18, output hang never
          Last clearing of "show interface" counters 1d02h
          Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          30 second input rate 0 bits/sec, 0 packets/sec
          30 second output rate 0 bits/sec, 0 packets/sec
             12127 packets input, 2297417 bytes, 0 no buffer
             Received 4173 broadcasts (0 IP multicasts)
             0 runts, 0 giants, 0 throttles 
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 4171 multicast, 0 pause input
             0 input packets with dribble condition detected
             12229 packets output, 2321107 bytes, 0 underruns
             0 output errors, 0 collisions, 2 interface resets
             0 unknown protocol drops
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 pause output
             0 output buffer failures, 0 output buffers swapped out
    '''

    ShowInterfacesAccounting_gi1 = '''
     GigabitEthernet1/0/1 
                Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                   Other     112674    5306164          2        120
                      IP      22150    2173570      22121    2167858
                     ARP     109280    4590030          2        120
                    IPv6         24       1944          0          0
     '''
    ShowIpInterfaces_gi1 = '''
    GigabitEthernet1/0/1 is administratively down, line protocol is down
        Internet address is 10.1.1.1/24
        Broadcast address is 255.255.255.255
        Address determined by setup command
        MTU is 1500 bytes
        Helper address is not set
        Directed broadcast forwarding is disabled
        Secondary address 10.2.2.2/24
        Outgoing Common access list is not set 
        Outgoing access list is not set
        Inbound Common access list is not set 
        Inbound  access list is not set
        Proxy ARP is enabled
        Local Proxy ARP is disabled
        Security level is default
        Split horizon is enabled
        ICMP redirects are always sent
        ICMP unreachables are always sent
        ICMP mask replies are never sent
        IP fast switching is enabled
        IP Flow switching is disabled
        IP CEF switching is enabled
        IP CEF switching turbo vector
        IP Null turbo vector
        Associated unicast routing topologies:
              Topology "base", operation state is UP
        IP multicast fast switching is disabled
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
        Input features: QoS Classification, QoS Marking, MCI Check
        IPv4 WCCP Redirect outbound is disabled
        IPv4 WCCP Redirect inbound is disabled
        IPv4 WCCP Redirect exclude is disabled
    '''
    ShowIpv6Interfaces_gi1='''
    GigabitEthernet1/0/1 is administratively down, line protocol is down
        IPv6 is tentative, link-local address is FE80::257:D2FF:FE28:1A64 [TEN]
        No Virtual link-local address(es):
        Description: desc
        Global unicast address(es):
          2001:db8:400::1, subnet is 2001:db8:400::/126 [TEN]
          2001:DB8:1:1::1, subnet is 2001:DB8:1:1::/64 [TEN]
          2001:DB8:2:2::2, subnet is 2001:DB8:2:2::/64 [TEN]
          2001:DB8:3:3::3, subnet is 2001:DB8:3:3::/64 [ANY/TEN]
          2001:DB8:4:4:257:D2FF:FE28:1A64, subnet is 2001:DB8:4:4::/64 [EUI/TEN]
        Joined group address(es):
          FF02::1
        MTU is 1500 bytes
        ICMP error messages limited to one every 100 milliseconds
        ICMP redirects are enabled
        ICMP unreachables are sent
        ND DAD is enabled, number of DAD attempts: 1
        ND reachable time is 30000 milliseconds (using 30000)
        ND NS retransmit interval is 1000 milliseconds
    '''
    ShowVrf_all = '''
        Name                             Default RD            Protocols   Interfaces
        Mgmt-intf                        <not set>             ipv4,ipv6    GigabitEthernet1/0/2
        VRF1                             65000:1               ipv4,ipv6    GigabitEthernet1/0/1

    '''
    ShowVrf_vrf1 = '''
            Name                             Default RD            Protocols   Interfaces
            VRF1                             65000:1               ipv4,ipv6    GigabitEthernet1/0/1
            '''
    ShowInterfaces_all='''
        GigabitEthernet1/0/1 is administratively down, line protocol is down (disabled) 
          Hardware is Gigabit Ethernet, address is 0057.d228.1a64 (bia 0057.d228.1a64)
          Description: desc
          Internet address is 10.1.1.1/24
          MTU 1500 bytes, BW 768 Kbit/sec, DLY 3330 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Auto-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input never, output 04:39:18, output hang never
          Last clearing of "show interface" counters 1d02h
          Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          30 second input rate 0 bits/sec, 0 packets/sec
          30 second output rate 0 bits/sec, 0 packets/sec
             12127 packets input, 2297417 bytes, 0 no buffer
             Received 4173 broadcasts (0 IP multicasts)
             0 runts, 0 giants, 0 throttles 
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 4171 multicast, 0 pause input
             0 input packets with dribble condition detected
             12229 packets output, 2321107 bytes, 0 underruns
             0 output errors, 0 collisions, 2 interface resets
             0 unknown protocol drops
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 pause output
             0 output buffer failures, 0 output buffers swapped out
        GigabitEthernet1/0/2 is up, line protocol is up (connected) 
          Hardware is Gigabit Ethernet, address is 0057.d228.1a02 (bia 0057.d228.1a02)
          MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
             reliability 255/255, txload 1/255, rxload 1/255
          Encapsulation ARPA, loopback not set
          Keepalive set (10 sec)
          Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
          input flow-control is off, output flow-control is unsupported 
          ARP type: ARPA, ARP Timeout 04:00:00
          Last input never, output 00:00:02, output hang never
          Last clearing of "show interface" counters 1d02h
          Input queue: 0/2000/0/0 (size/max/drops/flushes); Total output drops: 0
          Queueing strategy: fifo
          Output queue: 0/40 (size/max)
          5 minute input rate 3000 bits/sec, 5 packets/sec
          5 minute output rate 0 bits/sec, 0 packets/sec
             545526 packets input, 41210298 bytes, 0 no buffer
             Received 535996 broadcasts (535961 multicasts)
             0 runts, 0 giants, 0 throttles 
             0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
             0 watchdog, 535961 multicast, 0 pause input
             0 input packets with dribble condition detected
             23376 packets output, 3642296 bytes, 0 underruns
             0 output errors, 0 collisions, 5 interface resets
             0 unknown protocol drops
             0 babbles, 0 late collision, 0 deferred
             0 lost carrier, 0 no carrier, 0 pause output
             0 output buffer failures, 0 output buffers swapped out
    '''
    ShowIpInterfaces_all = '''
        GigabitEthernet1/0/1 is administratively down, line protocol is down
        Internet address is 10.1.1.1/24
        Broadcast address is 255.255.255.255
        Address determined by setup command
        MTU is 1500 bytes
        Helper address is not set
        Directed broadcast forwarding is disabled
        Secondary address 10.2.2.2/24
        Outgoing Common access list is not set 
        Outgoing access list is not set
        Inbound Common access list is not set 
        Inbound  access list is not set
        Proxy ARP is enabled
        Local Proxy ARP is disabled
        Security level is default
        Split horizon is enabled
        ICMP redirects are always sent
        ICMP unreachables are always sent
        ICMP mask replies are never sent
        IP fast switching is enabled
        IP Flow switching is disabled
        IP CEF switching is enabled
        IP CEF switching turbo vector
        IP Null turbo vector
        Associated unicast routing topologies:
              Topology "base", operation state is UP
        IP multicast fast switching is disabled
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
        Input features: QoS Classification, QoS Marking, MCI Check
        IPv4 WCCP Redirect outbound is disabled
        IPv4 WCCP Redirect inbound is disabled
        IPv4 WCCP Redirect exclude is disabled

    '''
    ShowIpv6Interfaces_all='''
        GigabitEthernet1/0/1 is administratively down, line protocol is down
        IPv6 is tentative, link-local address is FE80::257:D2FF:FE28:1A64 [TEN]
        No Virtual link-local address(es):
        Description: desc
        Global unicast address(es):
          2001:db8:400::1, subnet is 2001:db8:400::/126 [TEN]
          2001:DB8:1:1::1, subnet is 2001:DB8:1:1::/64 [TEN]
          2001:DB8:2:2::2, subnet is 2001:DB8:2:2::/64 [TEN]
          2001:DB8:3:3::3, subnet is 2001:DB8:3:3::/64 [ANY/TEN]
          2001:DB8:4:4:257:D2FF:FE28:1A64, subnet is 2001:DB8:4:4::/64 [EUI/TEN]
        Joined group address(es):
          FF02::1
        MTU is 1500 bytes
        ICMP error messages limited to one every 100 milliseconds
        ICMP redirects are enabled
        ICMP unreachables are sent
        ND DAD is enabled, number of DAD attempts: 1
        ND reachable time is 30000 milliseconds (using 30000)
        ND NS retransmit interval is 1000 milliseconds
    '''
    ShowInterfacesAccounting_all='''
    GigabitEthernet1/0/1
                Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                   Other     112674    5306164          2        120
                      IP      22150    2173570      22121    2167858
                     ARP     109280    4590030          2        120
                    IPv6         24       1944          0          0
    GigabitEthernet1/0/2 
                Protocol    Pkts In   Chars In   Pkts Out  Chars Out
                   Other       3483     741524         92       5520
                      IP      11745     968690      10821    1148402
                     ARP         91       5460         92       5520
                    IPv6          1         70          0          0

    '''

    ShowInterfacesAccountingCustom = {
        "GigabitEthernet1/0/1": {
            "accounting": {
                "arp": {
                    "chars_in": 4590030,
                    "chars_out": 120,
                    "pkts_in": 109280,
                    "pkts_out": 2
                },
                "ip": {
                    "chars_in": 2173570,
                    "chars_out": 2167858,
                    "pkts_in": 22150,
                    "pkts_out": 22121
                },
                "ipv6": {
                    "chars_in": 1944,
                    "chars_out": 0,
                    "pkts_in": 24,
                    "pkts_out": 0
                },
                "other": {
                    "chars_in": 5306164,
                    "chars_out": 120,
                    "pkts_in": 112674,
                    "pkts_out": 2
                }
            }
        }
    }

    interfaceOpsOutput_custom_info={
        "GigabitEthernet1/0/1": {
            "accounting": {
                "arp": {
                    "chars_in": 4590030,
                    "chars_out": 120,
                    "pkts_in": 109280,
                    "pkts_out": 2
                },
                "ip": {
                    "chars_in": 2173570,
                    "chars_out": 2167858,
                    "pkts_in": 22150,
                    "pkts_out": 22121
                },
                "ipv6": {
                    "chars_in": 1944,
                    "chars_out": 0,
                    "pkts_in": 24,
                    "pkts_out": 0
                },
                "other": {
                    "chars_in": 5306164,
                    "chars_out": 120,
                    "pkts_in": 112674,
                    "pkts_out": 2
                }
            },
            "type": "Gigabit Ethernet",
            "oper_status": "down",
            'vrf': 'VRF1',
            "ipv4": {
                "10.2.2.2/24": {
                    "secondary": True,
                    "ip": "10.2.2.2",
                    "prefix_length": "24"
                },
                "10.1.1.1/24": {
                    "secondary": False,
                    "ip": "10.1.1.1",
                    "prefix_length": "24"
                }
            },
            "mac_address": "0057.d228.1a64",
            "duplex_mode": "auto",
            'port_speed': '1000mb/s',
            "delay": 3330,
            "phys_address": "0057.d228.1a64",
            "port_channel": {
                "port_channel_member": False
            },
            "encapsulation": {
                "encapsulation": "arpa"
            },
            "mtu": 1500,
            "description": "desc",
            "flow_control": {
                "receive": False,
                "send": False
            },
            "enabled": False,
            "counters": {
                "last_clear": "1d02h",
                "in_pkts": 12127,
                "out_errors": 0,
                "in_octets": 2297417,
                "out_octets": 2321107,
                "in_broadcast_pkts": 4173,
                "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 30,
                    "in_rate": 0,
                    "in_rate_pkts": 0
                },
                "out_pkts": 12229,
                "in_multicast_pkts": 4171,
                "in_crc_errors": 0,
                "in_mac_pause_frames": 0,
                "in_errors": 0,
                "out_mac_pause_frames": 0
            },
            "bandwidth": 768,
            "switchport_enable": False
        },

    }
    InterfaceOpsOutput_info = {
        "GigabitEthernet1/0/1": {
            "accounting": {
              "arp": {
                "chars_in": 4590030,
                "chars_out": 120,
                "pkts_in": 109280,
                "pkts_out": 2
              },
              "ip": {
                "chars_in": 2173570,
                "chars_out": 2167858,
                "pkts_in": 22150,
                "pkts_out": 22121
              },
              "ipv6": {
                "chars_in": 1944,
                "chars_out": 0,
                "pkts_in": 24,
                "pkts_out": 0
              },
              "other": {
                "chars_in": 5306164,
                "chars_out": 120,
                "pkts_in": 112674,
                "pkts_out": 2
              }
            },
            "type": "Gigabit Ethernet",
            "oper_status": "down",
            "ipv4": {
               "10.2.2.2/24": {
                    "secondary": True,
                    "ip": "10.2.2.2",
                    "prefix_length": "24"
               },
               "10.1.1.1/24": {
                    "secondary": False,
                    "ip": "10.1.1.1",
                    "prefix_length": "24"
               }
            },
            'vrf':'VRF1',
            "mac_address": "0057.d228.1a64",
            "duplex_mode": "auto",
            'port_speed': '1000mb/s',
            "delay": 3330,
            "phys_address": "0057.d228.1a64",
            "port_channel": {
               "port_channel_member": False
            },
            "encapsulation": {
               "encapsulation": "arpa"
            },
            "mtu": 1500,
            "description": "desc",
            "flow_control": {
               "receive": False,
               "send": False
            },
            "enabled": False,
            "counters": {
               "last_clear": "1d02h",
               "in_pkts": 12127,
               "out_errors": 0,
               "in_octets": 2297417,
               "out_octets": 2321107,
               "in_broadcast_pkts": 4173,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 30,
                    "in_rate": 0,
                    "in_rate_pkts": 0
               },
               "out_pkts": 12229,
               "in_multicast_pkts": 4171,
               "in_crc_errors": 0,
               "in_mac_pause_frames": 0,
               "in_errors": 0,
               "out_mac_pause_frames": 0
            },
            "bandwidth": 768,
            "ipv6": {
               "FE80::257:D2FF:FE28:1A64": {
                    "origin": "link_layer",
                    "ip": "FE80::257:D2FF:FE28:1A64",
                    "status": "tentative"
               },
               "2001:DB8:4:4:257:D2FF:FE28:1A64/64": {
                    "ip": "2001:DB8:4:4:257:D2FF:FE28:1A64",
                    "eui_64": True,
                    "prefix_length": "64",
                    "status": "tentative"
               },
               "2001:db8:400::1/126": {
                    "ip": "2001:db8:400::1",
                    "prefix_length": "126",
                    "status": "tentative"
               },
               "2001:DB8:1:1::1/64": {
                    "ip": "2001:DB8:1:1::1",
                    "prefix_length": "64",
                    "status": "tentative"
               },
               "2001:DB8:2:2::2/64": {
                    "ip": "2001:DB8:2:2::2",
                    "prefix_length": "64",
                    "status": "tentative"
               },
               "2001:DB8:3:3::3/64": {
                    "ip": "2001:DB8:3:3::3",
                    "anycast": True,
                    "prefix_length": "64",
                    "status": "tentative"
               }
            },
            "switchport_enable": False
            },
        "GigabitEthernet1/0/2": {
            "accounting": {
              "arp": {
                "chars_in": 5460,
                "chars_out": 5520,
                "pkts_in": 91,
                "pkts_out": 92
              },
              "ip": {
                "chars_in": 968690,
                "chars_out": 1148402,
                "pkts_in": 11745,
                "pkts_out": 10821
              },
              "ipv6": {
                "chars_in": 70,
                "chars_out": 0,
                "pkts_in": 1,
                "pkts_out": 0
              },
              "other": {
                "chars_in": 741524,
                "chars_out": 5520,
                "pkts_in": 3483,
                "pkts_out": 92
              }
            },
            "type": "Gigabit Ethernet",
            "oper_status": "up",
            "mac_address": "0057.d228.1a02",
            "duplex_mode": "full",
            "vrf": "Mgmt-intf",
            "delay": 10,
            "phys_address": "0057.d228.1a02",
            "port_channel": {
               "port_channel_member": False
            },
            'port_speed': '1000mb/s',
            "encapsulation": {
               "encapsulation": "arpa"
            },
            "mtu": 1500,
            "flow_control": {
               "receive": False,
               "send": False
            },
            "enabled": True,
            "counters": {
               "last_clear": "1d02h",
               "in_pkts": 545526,
               "out_errors": 0,
               "in_octets": 41210298,
               "out_octets": 3642296,
               "in_broadcast_pkts": 535996,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 300,
                    "in_rate": 3000,
                    "in_rate_pkts": 5
               },
               "out_pkts": 23376,
               "in_multicast_pkts": 535961,
               "in_crc_errors": 0,
               "in_mac_pause_frames": 0,
               "in_errors": 0,
               "out_mac_pause_frames": 0
            },
            'switchport_enable': False,
            "bandwidth": 1000000
        },
    }
