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


    ShowInterfacesSwitchport = {
        "GigabitEthernet1/0/1": {
            "switchport_mode": "trunk",
            "pruning_vlans": "2-1001",
            'operational_mode': 'trunk',
            "switchport_enable": True,
            "trunk_vlans": "200-211",
            "capture_mode": False,
            "private_vlan": {
                 "native_vlan_tagging": True,
                 "encapsulation": "dot1q"
            },
            "access_vlan": "1",
            "unknown_unicast_blocked": False,
            "native_vlan_tagging": True,
            "unknown_multicast_blocked": False,
            "protected": False,
            "negotiation_of_trunk": True,
            "capture_vlans": "all",
            "encapsulation": {
                 "operational_encapsulation": "dot1q",
                 "native_vlan": "1",
                 "administrative_encapsulation": "dot1q"
            }
       },
       "GigabitEthernet1/0/2": {
            "pruning_vlans": "2-1001",
            "switchport_enable": True,
            "unknown_multicast_blocked": False,
            "trunk_vlans": "100-110",
            "port_channel": {
                "port_channel_int": "Port-channel12",
                "port_channel_member": True
            },
            "access_vlan": "1",
            "operational_mode": "trunk",
            "unknown_unicast_blocked": False,
            "capture_mode": False,
            "private_vlan": {
                 "native_vlan_tagging": True,
                 "encapsulation": "dot1q",
                 "operational": "10 (VLAN0010) 100 (VLAN0100)",
                 "trunk_mappings": "10 (VLAN0010) 100 (VLAN0100)"
            },
            "encapsulation": {
                 "operational_encapsulation": "dot1q",
                 "native_vlan": "1",
                 "administrative_encapsulation": "dot1q"
            },
            "protected": False,
            "native_vlan_tagging": True,
            "negotiation_of_trunk": True,
            "capture_vlans": "all",
            "switchport_mode": "trunk"
       },
       "GigabitEthernet1/0/5": {
            "switchport_mode": "static access",
            "pruning_vlans": "2-1001",
            "switchport_enable": True,
            "trunk_vlans": "all",
            'operational_mode': 'down',
            "capture_mode": False,
            "private_vlan": {
                 "native_vlan_tagging": True,
                 "encapsulation": "dot1q"
            },
            "access_vlan": "1",
            "unknown_unicast_blocked": False,
            "native_vlan_tagging": True,
            "unknown_multicast_blocked": False,
            "protected": False,
            "negotiation_of_trunk": False,
            "capture_vlans": "all",
            "encapsulation": {
                 "native_vlan": "1",
                 "administrative_encapsulation": "dot1q"
            }
       },
       "GigabitEthernet1/1/1": {
            "switchport_enable": True,
            "switchport_mode": "dynamic auto"
       }
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
        'GigabitEthernet1/0/1': {
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
        "GigabitEthernet3": {
              "phys_address": "5254.0072.9b0c",
              "encapsulation": {
                   "encapsulation": "arpa"
              },
              "port_channel": {
                   "port_channel_member": False
              },
              "oper_status": "up",
              "mac_address": "5254.0072.9b0c",
              "enabled": True,
              "bandwidth": 1000000,
              "mtu": 1500,
              "duplex_mode": "full",
              "flow_control": {
                   "receive": False,
                   "send": False
              },
              "auto_negotiate": True,
              "port_speed": "1000",
              "counters": {
                   "in_octets": 480,
                   "out_mac_pause_frames": 0,
                   "in_errors": 0,
                   "in_crc_errors": 0,
                   "in_pkts": 6,
                   "out_errors": 0,
                   "out_octets": 7820,
                   "in_mac_pause_frames": 0,
                   "last_clear": "never",
                   "in_multicast_pkts": 0,
                   "rate": {
                        "load_interval": 300,
                        "in_rate_pkts": 0,
                        "out_rate": 0,
                        "in_rate": 0,
                        "out_rate_pkts": 0
                   },
                   "in_broadcast_pkts": 0,
                   "out_pkts": 28
              },
              "ipv4": {
                   "unnumbered": {
                        "interface_ref": "Loopback0"
                   }
              },
              "switchport_enable": False,
              "ipv6": {
                   "FE80::5054:FF:FE1E:4F2": {
                        "ip": "FE80::5054:FF:FE1E:4F2",
                        "origin": "link_layer",
                        "status": "valid"
                   }
              },
              "delay": 10,
              "type": "CSR vNIC"
         },
         "Vlan100": {
              "phys_address": "0057.d228.1a51",
              "port_channel": {
                   "port_channel_member": False
              },
              "oper_status": "up",
              "mac_address": "0057.d228.1a51",
              "enabled": True,
              "encapsulation": {
                   "encapsulation": "arpa"
              },
              "ipv4": {
                   "201.11.14.1/24": {
                        "prefix_length": "24",
                        "ip": "201.11.14.1",
                        "secondary": False
                   }
              },
              "bandwidth": 1000000,
              "counters": {
                   "in_pkts": 50790,
                   "in_errors": 0,
                   "out_octets": 5526,
                   "in_octets": 3657594,
                   "last_clear": "1d04h",
                   "in_multicast_pkts": 0,
                   "out_errors": 0,
                   "rate": {
                        "load_interval": 300,
                        "in_rate_pkts": 0,
                        "out_rate": 0,
                        "in_rate": 0,
                        "out_rate_pkts": 0
                   },
                   "in_crc_errors": 0,
                   "in_broadcast_pkts": 0,
                   "out_pkts": 72
              },
              "type": "Ethernet SVI",
              "switchport_enable": False,
              "mtu": 1500,
              "delay": 10
         },
         "Vlan211": {
              "ipv6": {
                   "FE80::257:D2FF:FE28:1A71": {
                        "ip": "FE80::257:D2FF:FE28:1A71",
                        "origin": "link_layer",
                        "status": "valid"
                   },
                   "2001:10::14:1/112": {
                        "prefix_length": "112",
                        "status": "valid",
                        "ip": "2001:10::14:1",
                        "autoconf": {
                             "preferred_lifetime": 604711,
                             "valid_lifetime": 2591911
                        }
                   }
              },
              "switchport_enable": False
         },
         "GigabitEthernet1/1/1": {
              "switchport_mode": "dynamic auto",
              "switchport_enable": False
         },
         "Port-channel12": {
              "phys_address": "0057.d228.1a02",
              "encapsulation": {
                   "encapsulation": "qinq virtual lan",
                   "first_dot1q": "10",
                   "second_dot1q": "20"
              },
              "port_channel": {
                   "port_channel_member_intfs": [
                        "GigabitEthernet1/0/2"
                   ],
                   "port_channel_member": True
              },
              "oper_status": "up",
              "mac_address": "0057.d228.1a02",
              "enabled": True,
              "bandwidth": 1000000,
              "duplex_mode": "full",
              "flow_control": {
                   "receive": False,
                   "send": False
              },
              "auto_negotiate": True,
              "port_speed": "1000",
              "counters": {
                   "in_octets": 72614643,
                   "out_mac_pause_frames": 0,
                   "in_errors": 0,
                   "in_crc_errors": 0,
                   "in_pkts": 961622,
                   "out_errors": 0,
                   "out_octets": 6235318,
                   "in_mac_pause_frames": 0,
                   "last_clear": "1d23h",
                   "in_multicast_pkts": 4286699522,
                   "rate": {
                        "load_interval": 300,
                        "in_rate_pkts": 2,
                        "out_rate": 0,
                        "in_rate": 2000,
                        "out_rate_pkts": 0
                   },
                   "in_broadcast_pkts": 944788,
                   "out_pkts": 39281
              },
              "type": "EtherChannel",
              "switchport_enable": False,
              "mtu": 1500,
              "delay": 10
         },
         "Loopback0": {
              "encapsulation": {
                   "encapsulation": "loopback"
              },
              "bandwidth": 8000000,
              "switchport_enable": False,
              "port_channel": {
                   "port_channel_member": False
              },
              "counters": {
                   "in_pkts": 0,
                   "in_errors": 0,
                   "out_octets": 5760,
                   "in_octets": 0,
                   "last_clear": "1d04h",
                   "in_multicast_pkts": 0,
                   "out_errors": 0,
                   "rate": {
                        "load_interval": 300,
                        "in_rate_pkts": 0,
                        "out_rate": 0,
                        "in_rate": 0,
                        "out_rate_pkts": 0
                   },
                   "in_crc_errors": 0,
                   "in_broadcast_pkts": 0,
                   "out_pkts": 72
              },
              "type": "Loopback",
              "oper_status": "up",
              "enabled": True,
              "delay": 5000,
              "mtu": 1514
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
              "phys_address": "0057.d228.1a64",
              "enabled": False,
              "access_vlan": "1",
              "trunk_vlans": "200-211",
              "switchport_mode": "trunk",
              "type": "Gigabit Ethernet",
              "mtu": 1500,
              "duplex_mode": "auto",
              "port_channel": {
                   "port_channel_member": False
              },
              "oper_status": "down",
              "mac_address": "0057.d228.1a64",
              "ipv6": {
                   "2001:DB8:4:4:257:D2FF:FE28:1A64/64": {
                        "prefix_length": "64",
                        "ip": "2001:DB8:4:4:257:D2FF:FE28:1A64",
                        "eui_64": True,
                        "status": "tentative"
                   },
                   "2001:DB8:1:1::1/64": {
                        "prefix_length": "64",
                        "ip": "2001:DB8:1:1::1",
                        "status": "tentative"
                   },
                   "2001:DB8:3:3::3/64": {
                        "prefix_length": "64",
                        "ip": "2001:DB8:3:3::3",
                        "anycast": True,
                        "status": "tentative"
                   },
                   "FE80::257:D2FF:FE28:1A64": {
                        "ip": "FE80::257:D2FF:FE28:1A64",
                        "origin": "link_layer",
                        "status": "tentative"
                   },
                   "2001:DB8:2:2::2/64": {
                        "prefix_length": "64",
                        "ip": "2001:DB8:2:2::2",
                        "status": "tentative"
                   },
                   "2000::1/126": {
                        "prefix_length": "126",
                        "ip": "2000::1",
                        "status": "tentative"
                   }
              },
              "encapsulation": {
                   "encapsulation": "arpa",
                   "native_vlan": "1"
              },
              "flow_control": {
                   "receive": False,
                   "send": False
              },
              "bandwidth": 768,
              "port_speed": "1000",
              "counters": {
                   "in_octets": 2297417,
                   "out_mac_pause_frames": 0,
                   "in_errors": 0,
                   "in_crc_errors": 0,
                   "in_pkts": 12127,
                   "out_errors": 0,
                   "out_octets": 2321107,
                   "in_mac_pause_frames": 0,
                   "last_clear": "1d02h",
                   "in_multicast_pkts": 4171,
                   "rate": {
                        "load_interval": 30,
                        "in_rate_pkts": 0,
                        "out_rate": 0,
                        "in_rate": 0,
                        "out_rate_pkts": 0
                   },
                   "in_broadcast_pkts": 0,
                   "out_pkts": 12229
              },
              "vlan_id": "1",
              "ipv4": {
                   "10.1.1.1/24": {
                        "prefix_length": "24",
                        "ip": "10.1.1.1",
                        "secondary": False
                   },
                   "10.2.2.2/24": {
                        "prefix_length": "24",
                        "ip": "10.2.2.2",
                        "secondary": True
                   }
              },
              "switchport_enable": True,
              "description": "desc",
              "delay": 3330
         },
         "GigabitEthernet1/0/2": {
              "phys_address": "0057.d228.1a02",
              "encapsulation": {
                   "encapsulation": "arpa",
                   "native_vlan": "1"
              },
              "port_channel": {
                   "port_channel_int": "Port-channel12",
                   "port_channel_member": True
              },
              "flow_control": {
                   "receive": False,
                   "send": False
              },
              "oper_status": "up",
              "mac_address": "0057.d228.1a02",
              "enabled": True,
              "access_vlan": "1",
              "trunk_vlans": "100-110",
              "duplex_mode": "full",
              "switchport_mode": "trunk",
              "bandwidth": 1000000,
              "port_speed": "1000",
              "counters": {
                   "in_octets": 41210298,
                   "out_mac_pause_frames": 0,
                   "in_errors": 0,
                   "in_crc_errors": 0,
                   "in_pkts": 545526,
                   "out_errors": 0,
                   "out_octets": 3642296,
                   "in_mac_pause_frames": 0,
                   "last_clear": "1d02h",
                   "in_multicast_pkts": 535961,
                   "rate": {
                        "load_interval": 300,
                        "in_rate_pkts": 5,
                        "out_rate": 0,
                        "in_rate": 3000,
                        "out_rate_pkts": 0
                   },
                   "in_broadcast_pkts": 535961,
                   "out_pkts": 23376
              },
              "vlan_id": "1",
              "type": "Gigabit Ethernet",
              "switchport_enable": True,
              "mtu": 1500,
              'vrf': 'VRF1',
              "delay": 10
         },
         "GigabitEthernet1/0/5": {
              "encapsulation": {
                   "native_vlan": "1"
              },
              "switchport_mode": "static access",
              "access_vlan": "1",
              "vlan_id": "1",
              "switchport_enable": False,
              "trunk_vlans": "all"
         },
         "GigabitEthernet0/0": {
              "ipv4": {
                   "10.1.8.134/24": {
                        "prefix_length": "24",
                        "ip": "10.1.8.134",
                        "secondary": False
                   }
              },
              "vrf": "Mgmt-vrf",
              "switchport_enable": False
         }
    }
