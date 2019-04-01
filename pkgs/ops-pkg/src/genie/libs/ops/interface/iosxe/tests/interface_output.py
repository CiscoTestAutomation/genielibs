''' 
Interface Genie Ops Object Outputs for IOSXE.
'''


class InterfaceOutput(object):

    ShowInterfaces = {
        "Port-channel12": {
            "flow_control": {
                 "send": False,
                 "receive": False
            },
            "type": "EtherChannel",
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "1d23h",
                 "out_interface_resets": 2,
                 "in_mac_pause_frames": 0,
                 "out_collision": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 300,
                      "out_rate": 0,
                      "in_rate": 2000,
                      "in_rate_pkts": 2
                 },
                 "in_watchdog": 0,
                 "out_deferred": 0,
                 "out_mac_pause_frames": 0,
                 "in_pkts": 961622,
                 "in_multicast_pkts": 4286699522,
                 "in_runts": 0,
                 "out_unknown_protocl_drops": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_lost_carrier": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 72614643,
                 "in_crc_errors": 0,
                 "out_no_carrier": 0,
                 "in_with_dribble": 0,
                 "in_broadcast_pkts": 944788,
                 "out_pkts": 39281,
                 "out_late_collision": 0,
                 "out_octets": 6235318,
                 "in_overrun": 0,
                 "out_babble": 0
            },
            "auto_negotiate": True,
            "phys_address": "0057.d228.1a02",
            "keepalive": 10,
            "output_hang": "never",
            "txload": "1/255",
            "oper_status": "up",
            "arp_type": "arpa",
            "rxload": "1/255",
            "duplex_mode": "full",
            "link_type": "auto",
            "queues": {
                 "input_queue_size": 0,
                 "total_output_drop": 0,
                 "input_queue_drops": 0,
                 "input_queue_max": 2000,
                 "output_queue_size": 0,
                 "input_queue_flushes": 0,
                 "output_queue_max": 0,
                 "queue_strategy": "fifo"
            },
            "encapsulations": {
                 "encapsulation": "qinq virtual lan",
                 "first_dot1q": "10",
                 "second_dot1q": "20",
            },
            "last_input": "never",
            "last_output": "1d22h",
            "line_protocol": "up",
            "mac_address": "0057.d228.1a02",
            "connected": True,
            "port_channel": {
                 "port_channel_member": True,
                 "port_channel_member_intfs": ['GigabitEthernet1/0/2'],
            },
            "arp_timeout": "04:00:00",
            "bandwidth": 1000000,
            "port_speed": "1000",
            "enabled": True,
            "mtu": 1500,
            "delay": 10,
            "reliability": "255/255"
       },
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
            "port_speed": "1000",
            "enabled": False,
            "arp_timeout": "04:00:00",
            "mtu": 1500,
            "delay": 3330,
            "reliability": "255/255"
       },
       "GigabitEthernet3": {
            "flow_control": {
                 "send": False,
                 "receive": False
            },
            "type": "CSR vNIC",
            'auto_negotiate': True,
            'duplex_mode': 'full',
            'link_type': 'auto',
            'media_type': 'RJ45',
            'port_speed': '1000',
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "never",
                 "out_interface_resets": 1,
                 "in_mac_pause_frames": 0,
                 "out_collision": 0,
                 "in_crc_errors": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 300,
                      "out_rate": 0,
                      "in_rate": 0,
                      "in_rate_pkts": 0
                 },
                 "in_watchdog": 0,
                 "out_deferred": 0,
                 "out_mac_pause_frames": 0,
                 "in_pkts": 6,
                 "in_multicast_pkts": 0,
                 "in_runts": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 480,
                 "out_unknown_protocl_drops": 0,
                 "out_no_carrier": 0,
                 "out_lost_carrier": 0,
                 "in_broadcast_pkts": 0,
                 "out_pkts": 28,
                 "out_late_collision": 0,
                 "out_octets": 7820,
                 "in_overrun": 0,
                 "out_babble": 0
            },
            "phys_address": "5254.0072.9b0c",
            "keepalive": 10,
            "output_hang": "never",
            "txload": "1/255",
            "reliability": "255/255",
            "arp_type": "arpa",
            "rxload": "1/255",
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
                 "200.2.1.1/24": {
                      "prefix_length": "24",
                      "ip": "200.2.1.1"
                 },
                 "unnumbered": {
                      "interface_ref": "Loopback0"
                 }
            },
            "encapsulations": {
                 "encapsulation": "arpa"
            },
            "last_output": "00:00:27",
            "line_protocol": "up",
            "mac_address": "5254.0072.9b0c",
            "oper_status": "up",
            "port_channel": {
                 "port_channel_member": False
            },
            "arp_timeout": "04:00:00",
            "bandwidth": 1000000,
            "enabled": True,
            "mtu": 1500,
            "delay": 10,
            "last_input": "never"
       },
       "Loopback0": {
            "queues": {
                 "input_queue_size": 0,
                 "total_output_drop": 0,
                 "input_queue_drops": 0,
                 "input_queue_max": 75,
                 "output_queue_size": 0,
                 "input_queue_flushes": 0,
                 "output_queue_max": 0,
                 "queue_strategy": "fifo"
            },
            "mtu": 1514,
            "encapsulations": {
                 "encapsulation": "loopback"
            },
            "last_output": "never",
            "type": "Loopback",
            "line_protocol": "up",
            "oper_status": "up",
            "keepalive": 10,
            "output_hang": "never",
            "txload": "1/255",
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "1d04h",
                 "out_interface_resets": 0,
                 "out_collision": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 300,
                      "out_rate": 0,
                      "in_rate": 0,
                      "in_rate_pkts": 0
                 },
                 "in_pkts": 0,
                 "in_multicast_pkts": 0,
                 "in_runts": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 0,
                 "in_crc_errors": 0,
                 "out_unknown_protocl_drops": 0,
                 "in_broadcast_pkts": 0,
                 "out_pkts": 72,
                 "out_octets": 5760,
                 "in_overrun": 0,
                 "in_abort": 0
            },
            "reliability": "255/255",
            "bandwidth": 8000000,
            "port_channel": {
                 "port_channel_member": False
            },
            "enabled": True,
            "ipv4": {
                 "200.2.1.1/24": {
                      "prefix_length": "24",
                      "ip": "200.2.1.1"
                 }
            },
            "rxload": "1/255",
            "delay": 5000,
            "last_input": "1d02h"
       },
       "Vlan100": {
            "type": "Ethernet SVI",
            "counters": {
                 "out_buffer_failure": 0,
                 "out_underruns": 0,
                 "in_giants": 0,
                 "in_throttles": 0,
                 "in_frame": 0,
                 "in_ignored": 0,
                 "last_clear": "1d04h",
                 "out_interface_resets": 0,
                 "rate": {
                      "out_rate_pkts": 0,
                      "load_interval": 300,
                      "out_rate": 0,
                      "in_rate": 0,
                      "in_rate_pkts": 0
                 },
                 "in_pkts": 50790,
                 "in_multicast_pkts": 0,
                 "in_runts": 0,
                 "in_no_buffer": 0,
                 "out_buffers_swapped": 0,
                 "out_errors": 0,
                 "in_errors": 0,
                 "in_octets": 3657594,
                 "in_crc_errors": 0,
                 "out_unknown_protocl_drops": 0,
                 "in_broadcast_pkts": 0,
                 "out_pkts": 72,
                 "out_octets": 5526,
                 "in_overrun": 0
            },
            "phys_address": "0057.d228.1a51",
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
            "txload": "1/255",
            "reliability": "255/255",
            "arp_type": "arpa",
            "rxload": "1/255",
            "output_hang": "never",
            "ipv4": {
                 "201.0.12.1/24": {
                      "prefix_length": "24",
                      "ip": "201.0.12.1"
                 }
            },
            "encapsulations": {
                 "encapsulation": "arpa"
            },
            "last_output": "1d03h",
            "line_protocol": "up",
            "mac_address": "0057.d228.1a51",
            "oper_status": "up",
            "port_channel": {
                 "port_channel_member": False
            },
            "arp_timeout": "04:00:00",
            "bandwidth": 1000000,
            "enabled": True,
            "mtu": 1500,
            "delay": 10,
            "last_input": "never"
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
            "port_speed": "1000",
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
                    'port_channel_member_intfs': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
                }
            },
        },
    }

    ShowIpInterface = {
        "Vlan100": {
            "sevurity_level": "default",
            "ip_route_cache_flags": [
                 "CEF",
                 "Fast"
            ],
            "enabled": True,
            "oper_status": "up",
            "address_determined_by": "configuration file",
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
                 "201.11.14.1/24": {
                      "prefix_length": "24",
                      "ip": "201.11.14.1",
                      "secondary": False,
                      "broadcase_address": "255.255.255.255"
                 }
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
            "ip_null_turbo_vector": True,
            "probe_proxy_name_replies": False,
            "ip_fast_switching": True,
            "ip_multicast_distributed_fast_switching": False,
            "tcp_ip_header_compression": False,
            "rtp_ip_header_compression": False,
            "input_features": ["MCI Check"],
            "directed_broadcast_forwarding": False,
            "ip_flow_switching": False
       },
       "GigabitEthernet0/0": {
            "sevurity_level": "default",
            'address_determined_by': 'setup command',
            "ip_route_cache_flags": [
                 "CEF",
                 "Fast"
            ],
            "enabled": True,
            "oper_status": "up",
            "router_discovery": False,
            "ip_multicast_fast_switching": False,
            "split_horizon": True,
            "bgp_policy_mapping": False,
            "ip_output_packet_accounting": False,
            "mtu": 1500,
            "policy_routing": False,
            "local_proxy_arp": False,
            "vrf": "Mgmt-vrf",
            "proxy_arp": True,
            "network_address_translation": False,
            "ip_cef_switching_turbo_vector": True,
            "icmp": {
                "redirects": "always sent",
                "mask_replies": "never sent",
                "unreachables": "always sent",
            },
            "ipv4": {
                 "10.1.8.134/24": {
                      "prefix_length": "24",
                      "ip": "10.1.8.134",
                      "secondary": False,
                      "broadcase_address": "255.255.255.255"
                 }
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
            "ip_null_turbo_vector": True,
            "probe_proxy_name_replies": False,
            "ip_fast_switching": True,
            "ip_multicast_distributed_fast_switching": False,
            "tcp_ip_header_compression": False,
            "rtp_ip_header_compression": False,
            "input_features": ["MCI Check"],
            "directed_broadcast_forwarding": False,
            "ip_flow_switching": False
       },
       "GigabitEthernet2": {
            "enabled": False,
            "oper_status": "down"
       },
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
                 "2000::1/126": {
                      "ip": "2000::1",
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
       "Vlan211": {
            "joined_group_addresses": [
                 "FF02::1",
                 "FF02::1:FF14:1",
                 "FF02::1:FF28:1A71"
            ],
            "ipv6": {
                 "2001:10::14:1/112": {
                      "ip": "2001:10::14:1",
                      "prefix_length": "112",
                      "status": "valid",
                      'autoconf': {
                          'preferred_lifetime': 604711,
                          'valid_lifetime': 2591911,
                      },
                 },
                 "FE80::257:D2FF:FE28:1A71": {
                      "ip": "FE80::257:D2FF:FE28:1A71",
                      "status": "valid",
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
            "oper_status": "up",
            "enabled": True,
            "autoconf": True,
            "mtu": 1500
       },
       "GigabitEthernet3": {
            "enabled": True,
            "joined_group_addresses": [
                 "FF02::1",
                 "FF02::1:FF1E:4F2",
                 "FF02::2"
            ],
            "ipv6": {
                 "enabled": False,
                 "FE80::5054:FF:FE1E:4F2": {
                      "ip": "FE80::5054:FF:FE1E:4F2",
                      "status": "valid",
                      "origin": "link_layer",
                 },
                 "unnumbered": {
                      "interface_ref": "Loopback0",
                 },
                 "nd": {
                      "dad_attempts": 1,
                      "reachable_time": 30000,
                      "using_time": 30000,
                      "dad_enabled": True
                 },
                 "icmp": {
                      "unreachables": "sent",
                      "redirects": True,
                      "error_messages_limited": 100
                 },
                 "nd": {
                      "dad_attempts": 1,
                      "dad_enabled": True,
                      "reachable_time": 30000,
                      "using_time": 30000,
                      "advertised_reachable_time": 0,
                      "advertised_retransmit_interval": 0,
                      "router_advertisements_interval": 200,
                      "router_advertisements_live": 1800,
                      "advertised_default_router_preference": 'Medium',
                      "advertised_reachable_time_unspecified": False,
                      "advertised_retransmit_interval_unspecified": False,
                 },
            },
            "oper_status": "up",
            "mtu": 1500,
            "addresses_config_method": 'stateless autoconfig',
       }
    }

    ShowVrfDetail = {
        "Mgmt-vrf": {
              "vrf_id": 1,
              "interfaces": [
                   "GigabitEthernet0/0"
              ],
              "interface": {
                   "GigabitEthernet0/0": {'vrf': 'Mgmt-vrf'}
              },
              "address_family": {
                   "ipv4 unicast": {
                        "table_id": "0x1"
                   },
                   "ipv6 unicast": {
                        "table_id": "0x1E000001"
                   }
              },
              "flags": "0x0"
         },
        "VRF1": {
              "interfaces": [
                   "GigabitEthernet1/0/2"
              ],
              "interface": {
                   "GigabitEthernet1/0/2": {'vrf': 'VRF1'}
              },
              "address_family": {
                   "ipv4 unicast": {
                        "export_to_global": {
                             "export_to_global_map": "export_to_global_map",
                             "prefix_limit": 1000
                        },
                        "import_from_global": {
                             "prefix_limit": 1000,
                             "import_from_global_map": "import_from_global_map"
                        },
                        "table_id": "0x1",
                        "routing_table_limit": {
                             "routing_table_limit_action": {
                                  "enable_alert_percent": {
                                       "alert_percent_value": 10000
                                  }
                             }
                        },
                        "route_target": {
                             "200:1": {
                                  "rt_type": "both",
                                  "route_target": "200:1"
                             },
                             "100:1": {
                                  "rt_type": "both",
                                  "route_target": "100:1"
                             }
                        }
                   },
                   "ipv6 unicast": {
                        "export_to_global": {
                             "export_to_global_map": "export_to_global_map",
                             "prefix_limit": 1000
                        },
                        "table_id": "0x1E000001",
                        "routing_table_limit": {
                             "routing_table_limit_action": {
                                  "enable_alert_percent": {
                                       "alert_percent_value": 7000
                                  }
                             },
                             "routing_table_limit_number": 10000
                        },
                        "route_target": {
                             "200:1": {
                                  "rt_type": "import",
                                  "route_target": "200:1"
                             },
                             "400:1": {
                                  "rt_type": "import",
                                  "route_target": "400:1"
                             },
                             "300:1": {
                                  "rt_type": "export",
                                  "route_target": "300:1"
                             },
                             "100:1": {
                                  "rt_type": "export",
                                  "route_target": "100:1"
                             }
                        }
                   }
              },
              "flags": "0x100",
              "route_distinguisher": "100:1",
              "vrf_id": 1
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

    InterfaceOpsOutput_info = {
        "Port-channel12": {
            "type": "EtherChannel",
            "switchport_enable": False,
            "oper_status": "up",
            "mac_address": "0057.d228.1a02",
            "duplex_mode": "full",
            "port_speed": "1000",
            "delay": 10,
            "phys_address": "0057.d228.1a02",
            "port_channel": {
               "port_channel_member": True,
               "port_channel_member_intfs": [
                    "GigabitEthernet1/0/2"
               ]
            },
            "auto_negotiate": True,
            "mtu": 1500,
            "flow_control": {
               "receive": False,
               "send": False
            },
            "enabled": True,
            "counters": {
               "last_clear": "1d23h",
               "in_pkts": 961622,
               "out_errors": 0,
               "in_octets": 72614643,
               "out_octets": 6235318,
               "in_broadcast_pkts": 944788,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 300,
                    "in_rate": 2000,
                    "in_rate_pkts": 2
               },
               "out_pkts": 39281,
               "in_multicast_pkts": 4286699522,
               "in_crc_errors": 0,
               "in_mac_pause_frames": 0,
               "in_errors": 0,
               "out_mac_pause_frames": 0
            },
            "bandwidth": 1000000,
            "encapsulation": {
               "second_dot1q": "20",
               "first_dot1q": "10",
               "encapsulation": "qinq virtual lan"
            }
            },
        "Loopback0": {
            "type": "Loopback",
            "oper_status": "up",
            "encapsulation": {
               "encapsulation": "loopback"
            },
            "mtu": 1514,
            "port_channel": {
               "port_channel_member": False
            },
            "enabled": True,
            "counters": {
               "out_errors": 0,
               "last_clear": "1d04h",
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 300,
                    "in_rate": 0,
                    "in_rate_pkts": 0
               },
               "in_pkts": 0,
               "out_pkts": 72,
               "in_errors": 0,
               "out_octets": 5760,
               "in_multicast_pkts": 0,
               "in_crc_errors": 0,
               "in_octets": 0
            },
            "bandwidth": 8000000,
            "delay": 5000,
            "switchport_enable": False
            },
        "Vlan211": {
            "ipv6": {
               "2001:10::14:1/112": {
                    "ip": "2001:10::14:1",
                    "autoconf": {
                         "valid_lifetime": 2591911,
                         "preferred_lifetime": 604711
                    },
                    "prefix_length": "112",
                    "status": "valid"
               },
               "FE80::257:D2FF:FE28:1A71": {
                    "origin": "link_layer",
                    "ip": "FE80::257:D2FF:FE28:1A71",
                    "status": "valid"
               }
            },
             'switchport_enable': False
            },
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
            "mac_address": "0057.d228.1a64",
            "duplex_mode": "auto",
            "port_speed": "1000",
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
               "in_broadcast_pkts": 0,
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
               "2000::1/126": {
                    "ip": "2000::1",
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
            "vrf": "VRF1",
            "delay": 10,
            "phys_address": "0057.d228.1a02",
            "port_channel": {
               "port_channel_member": False
            },
            "port_speed": "1000",
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
               "in_broadcast_pkts": 535961,
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
        "Vlan100": {
            "type": "Ethernet SVI",
            "oper_status": "up",
            "ipv4": {
               "201.11.14.1/24": {
                    "secondary": False,
                    "ip": "201.11.14.1",
                    "prefix_length": "24"
               }
            },
            "mac_address": "0057.d228.1a51",
            "delay": 10,
            "phys_address": "0057.d228.1a51",
            "port_channel": {
               "port_channel_member": False
            },
            "encapsulation": {
               "encapsulation": "arpa"
            },
            "mtu": 1500,
            "enabled": True,
            "counters": {
               "out_errors": 0,
               "last_clear": "1d04h",
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 300,
                    "in_rate": 0,
                    "in_rate_pkts": 0
               },
               "in_pkts": 50790,
               "out_pkts": 72,
               "in_errors": 0,
               "out_octets": 5526,
               "in_multicast_pkts": 0,
               "in_crc_errors": 0,
               "in_octets": 3657594
            },
            "switchport_enable": False,
            "bandwidth": 1000000
            },
        "GigabitEthernet0/0": {
            "ipv4": {
               "10.1.8.134/24": {
                    "secondary": False,
                    "ip": "10.1.8.134",
                    "prefix_length": "24"
               }
            },
            "vrf": "Mgmt-vrf",
            'switchport_enable': False
            },
        "GigabitEthernet3": {
            "type": "CSR vNIC",
            "oper_status": "up",
            "ipv4": {
               "unnumbered": {
                    "interface_ref": "Loopback0"
               }
            },
            "mac_address": "5254.0072.9b0c",
            "duplex_mode": "full",
            "port_speed": "1000",
            "delay": 10,
            "phys_address": "5254.0072.9b0c",
            "port_channel": {
               "port_channel_member": False
            },
            "ipv6": {
               "FE80::5054:FF:FE1E:4F2": {
                    "origin": "link_layer",
                    "ip": "FE80::5054:FF:FE1E:4F2",
                    "status": "valid"
               }
            },
            "auto_negotiate": True,
            "mtu": 1500,
            "flow_control": {
               "receive": False,
               "send": False
            },
            "enabled": True,
            "counters": {
               "last_clear": "never",
               "in_pkts": 6,
               "out_errors": 0,
               "in_octets": 480,
               "out_octets": 7820,
               "in_broadcast_pkts": 0,
               "rate": {
                    "out_rate_pkts": 0,
                    "out_rate": 0,
                    "load_interval": 300,
                    "in_rate": 0,
                    "in_rate_pkts": 0
               },
               "out_pkts": 28,
               "in_multicast_pkts": 0,
               "in_crc_errors": 0,
               "in_mac_pause_frames": 0,
               "in_errors": 0,
               "out_mac_pause_frames": 0
            },
            "bandwidth": 1000000,
            "switchport_enable": False,
            "encapsulation": {
               "encapsulation": "arpa"
            }
        },
    }
