''' 
Arp Genie Ops Object Outputs for NXOS.
'''


class ArpOutput(object):

	ShowIpArpDetailVrfAll = {
          'interfaces': {
               'Ethernet1/1': {
                    'ipv4': {
                         'neighbors': {
                              '10.1.3.5': {
                                   'age': '-',
                                   'ip': '10.1.3.5',
                                   'link_layer_address': 'aaaa.bbbb.cccc',
                                   'origin': 'static',
                                   'physical_interface': 'Ethernet1/1'}
                         }
                    }
               },
               'Ethernet1/1.1': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.4.2': {
                                   'age': '00:01:53',
                                   'ip': '192.168.4.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/1.1'}
                         }
                    }
               },
               'Ethernet1/1.2': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.154.2': {
                                   'age': '00:00:47',
                                   'ip': '192.168.154.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/1.2'}
                         }
                    }
               },
               'Ethernet1/1.4': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.106.2': {
                                   'age': '00:08:42',
                                   'ip': '192.168.106.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/1.4'}
                         }
                    }
               },
               'Ethernet1/2.1': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.154.2': {
                                   'age': '00:18:24',
                                   'ip': '192.168.154.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/2.1'}
                         }
                    }
               },
               'Ethernet1/2.2': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.51.2': {
                                   'age': '00:05:21',
                                   'ip': '192.168.51.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/2.2'}
                         }
                    }
               },
               'Ethernet1/2.4': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.9.2': {
                                   'age': '00:10:51',
                                   'ip': '192.168.9.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/2.4'}
                         }
                    }
               },
               'Ethernet1/4.100': {
                    'ipv4': {
                         'neighbors': {
                              '10.51.1.101': {
                                   'age': '00:01:28',
                                   'ip': '10.51.1.101',
                                   'link_layer_address': '0000.71c7.6e61',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/4.100'}
                         }
                    }
               },
               'Ethernet1/4.101': {
                    'ipv4': {
                         'neighbors': {
                              '10.154.1.101': {
                                   'age': '00:01:28',
                                   'ip': '10.154.1.101',
                                   'link_layer_address': '0000.71c7.75c1',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/4.101'}
                         }
                    }
               },
               'Ethernet1/4.200': {
                    'ipv4': {
                         'neighbors': {
                              '10.76.1.101': {
                                   'age': '00:01:28',
                                   'ip': '10.76.1.101',
                                   'link_layer_address': '0000.0068.ce6f',
                                   'origin': 'dynamic',
                                   'physical_interface': 'Ethernet1/4.200'}
                         }
                    }
               },
               'mgmt0': {
                    'ipv4': {
                         'neighbors': {
                              '10.1.7.1': {
                                   'age': '00:17:15',
                                   'ip': '10.1.7.1',
                                   'link_layer_address': '0012.7f57.ac80',
                                   'origin': 'dynamic',
                                   'physical_interface': 'mgmt0'},
                              '10.1.7.250': {
                                   'age': '00:14:24',
                                   'ip': '10.1.7.250',
                                   'link_layer_address': '0050.5682.7915',
                                   'origin': 'dynamic',
                                   'physical_interface': 'mgmt0'},
                              '10.1.7.253': {
                                   'age': '00:10:22',
                                   'ip': '10.1.7.253',
                                   'link_layer_address': '0050.56a4.a9fc',
                                   'origin': 'dynamic',
                                   'physical_interface': 'mgmt0'}
                         }
                    }
               }
          }
     }

	ShowIpArpSummaryVrfAll = {
          'incomplete': 0,
          'throttled': 0,
          'resolved': 12,
          'total': 12,
          'unknown': 0}

	ShowIpArpstatisticsVrfAll = {
          'statistics': {
               'adjacency': {
                    'adjacency_adds': 43,
                    'adjacency_deletes': 12,
                    'adjacency_timeouts': 12,
                    'failed_due_to_limits': 0},
               'received': {
                    'anycast_proxy_arp': 0,
                    'dropped': 28218,
                    'dropped_server_port': 0,
                    'drops_details': {
                         'appeared_on_a_wrong_interface': 0,
                         'arp_refresh_requests_received_from_clients': 0,
                         'context_not_created': 0,
                         'directed_broadcast_source': 0,
                         'dropping_due_to_tunneling_failures': 0,
                         'glean_requests_recv_count': 71,
                         'grat_arp_received_on_proxy': 0,
                         'incorrect_length': 0,
                         'invalid_context': 0,
                         'invalid_destination_ip_address': 0,
                         'invalid_hardwaretype': 0,
                         'invalid_layer2_address_length': 0,
                         'invalid_layer3_address_length': 0,
                         'invalid_protocol_packet': 0,
                         'invalid_source_ip_address': 28,
                         'invalid_source_mac_address': 0,
                         'l2_packet_on_untrusted_l2_port': 0,
                         'l2fm_query_failed_for_a_l2address': 0,
                         'no_mem_to_create_per_intf_structure': 0,
                         'non_active_fhrp_dest_ip': 0,
                         'non_local_destination_ip_address': 20421,
                         'number_of_signals_received_from_l2rib': 0,
                         'packet_with_vip_on_standby_fhrp': 0,
                         'received_before_arp_initialization': 0,
                         'requests_came_for_exising_entries': 15,
                         'requests_came_on_a_l2_interface': 0,
                         'source_address_mismatch_with_subnet': 0,
                         'source_mac_address_is_our_own': 0},
                    'enhanced_proxy_arp': 0,
                    'fastpath': 0,
                    'l2_port_track_proxy_arp': 0,
                    'l2_replies': 0,
                    'l2_requests': 0,
                    'local_proxy_arp': 0,
                    'proxy_arp': 0,
                    'replies': 6582,
                    'requests': 22632,
                    'snooped': 0,
                    'total': 0,
                    'tunneled': 0},
               'sent': {
                    'dropped': 0,
                    'drops_details': {
                         'adjacency_couldnt_be_added': 0,
                         'arp_refresh_skipped_over_core_and_flooded': 0,
                         'client_enqueue_failed': 0,
                         'context_not_created': 0,
                         'dest_not_reachable_for_proxy_arp': 0,
                         'dest_unreachable_for_enhanced_proxy': 0,
                         'destnination_is_our_own_ip': 26,
                         'destnination_on_l2_port_tracked': 0,
                         'invalid_context': 0,
                         'invalid_dest_ip': 0,
                         'invalid_ifindex': 0,
                         'invalid_local_proxy_arp': 0,
                         'invalid_proxy_arp': 0,
                         'invalid_src_ip': 0,
                         'mbuf_operation_failed': 0,
                         'null_source_ip': 0,
                         'null_source_mac': 0,
                         'unattached_ip': 0,
                         'vip_is_not_active': 0},
                    'gratuitous': 58,
                    'l2_replies': 0,
                    'l2_requests': 0,
                    'replies': 998,
                    'requests': 2102,
                    'total': 3158,
                    'tunneled': 0}
          }
     }

	ShowIpInterfaceVrfAll = {
          "Ethernet2/11": {
               "icmp_port_unreachable": "enabled",
               "multicast_groups_address": "none",
               "proxy_arp": "disabled",
               "interface_status": "protocol-down/link-down/admin-down",
               "load_sharing": "none",
               "ipv4": {
                    "counters": {
                         "multicast_bytes_received": 0,
                         "labeled_packets_forwarded": 0,
                         "multicast_bytes_sent": 0,
                         "unicast_bytes_sent": 0,
                         "labeled_packets_received": 0,
                         "labeled_packets_originated": 0,
                         "multicast_bytes_consumed": 0,
                         "multicast_packets_sent": 0,
                         "unicast_bytes_consumed": 0,
                         "broadcast_packets_originated": 0,
                         "multicast_packets_originated": 0,
                         "multicast_bytes_originated": 0,
                         "multicast_packets_received": 0,
                         "multicast_packets_consumed": 0,
                         "broadcast_packets_forwarded": 0,
                         "broadcast_bytes_originated": 0,
                         "labeled_bytes_originated": 0,
                         "broadcast_bytes_consumed": 0,
                         "broadcast_packets_sent": 0,
                         "labeled_packets_consumed": 0,
                         "unicast_packets_consumed": 0,
                         "labeled_bytes_forwarded": 0,
                         "broadcast_packets_consumed": 0,
                         "unicast_packets_sent": 0,
                         "broadcast_bytes_received": 0,
                         "labeled_packets_sent": 0,
                         "labeled_bytes_consumed": 0,
                         "unicast_bytes_received": 0,
                         "multicast_bytes_forwarded": 0,
                         "multicast_packets_forwarded": 0,
                         "unicast_packets_forwarded": 0,
                         "unicast_packets_received": 0,
                         "broadcast_packets_received": 0,
                         "broadcast_bytes_sent": 0,
                         "broadcast_bytes_forwarded": 0,
                         "labeled_bytes_sent": 0,
                         "unicast_bytes_forwarded": 0,
                         "unicast_packets_originated": 0,
                         "labeled_bytes_received": 0,
                         "unicast_bytes_originated": 0
                    },
                    "10.64.4.4/24": {
                         "ip": "10.64.4.4",
                         "prefix_length": "24",
                         "broadcast_address": "255.255.255.255",
                         "secondary": False,
                         "ip_subnet": "10.64.4.0"
                    },
                    "unnumbered": {
                         "interface_ref": "loopback0"
                    }
               },
               "icmp_unreachable": "disabled",
               "wccp_redirect_inbound": "disabled",
               "unicast_reverse_path": "none",
               "icmp_redirects": "enabled",
               "multicast_routing": "disabled",
               "wccp_redirect_outbound": "disabled",
               "iod": 46,
               "directed_broadcast": "disabled",
               "ip_mtu": 1500,
               "vrf": "default",
               "local_proxy_arp": "disabled",
               "ip_forwarding": "disabled",
               "int_stat_last_reset": "never",
               "wccp_redirect_exclude": "disabled"
          },
          "loopback0": {
               "icmp_port_unreachable": "enabled",
               "multicast_groups_address": "none",
               "proxy_arp": "disabled",
               "interface_status": "protocol-up/link-up/admin-up",
               "load_sharing": "none",
               "ipv4": {
                    "counters": {
                         "multicast_bytes_received": 0,
                         "labeled_packets_forwarded": 0,
                         "multicast_bytes_sent": 0,
                         "unicast_bytes_sent": 0,
                         "labeled_packets_received": 0,
                         "labeled_packets_originated": 0,
                         "multicast_bytes_consumed": 0,
                         "multicast_packets_sent": 0,
                         "unicast_bytes_consumed": 5612014,
                         "broadcast_packets_originated": 0,
                         "multicast_packets_originated": 0,
                         "multicast_bytes_originated": 0,
                         "multicast_packets_received": 0,
                         "multicast_packets_consumed": 0,
                         "broadcast_packets_forwarded": 0,
                         "broadcast_bytes_originated": 0,
                         "labeled_bytes_originated": 0,
                         "broadcast_bytes_consumed": 0,
                         "broadcast_packets_sent": 0,
                         "labeled_packets_consumed": 0,
                         "unicast_packets_consumed": 92391,
                         "labeled_bytes_forwarded": 0,
                         "broadcast_packets_consumed": 0,
                         "unicast_packets_sent": 0,
                         "broadcast_bytes_received": 0,
                         "labeled_packets_sent": 0,
                         "labeled_bytes_consumed": 0,
                         "unicast_bytes_received": 0,
                         "multicast_bytes_forwarded": 0,
                         "multicast_packets_forwarded": 0,
                         "unicast_packets_forwarded": 0,
                         "unicast_packets_received": 0,
                         "broadcast_packets_received": 0,
                         "broadcast_bytes_sent": 0,
                         "broadcast_bytes_forwarded": 0,
                         "labeled_bytes_sent": 0,
                         "unicast_bytes_forwarded": 0,
                         "unicast_packets_originated": 0,
                         "labeled_bytes_received": 0,
                         "unicast_bytes_originated": 0
                    },
                    "10.64.4.4/24": {
                         "route_preference": "0",
                         "prefix_length": "24",
                         "broadcast_address": "255.255.255.255",
                         "ip_subnet": "10.64.4.0",
                         "ip": "10.64.4.4",
                         "secondary": False,
                         "route_tag": "0"
                    }
               },
               "icmp_unreachable": "disabled",
               "wccp_redirect_inbound": "disabled",
               "unicast_reverse_path": "none",
               "icmp_redirects": "enabled",
               "multicast_routing": "disabled",
               "wccp_redirect_outbound": "disabled",
               "iod": 180,
               "directed_broadcast": "disabled",
               "ip_mtu": 1500,
               "vrf": "default",
               "local_proxy_arp": "disabled",
               "ip_forwarding": "disabled",
               "int_stat_last_reset": "never",
               "wccp_redirect_exclude": "disabled"
          },
          "Ethernet2/1": {
               "icmp_port_unreachable": "enabled",
               "load_sharing": "none",
               "proxy_arp": "disabled",
               "interface_status": "protocol-up/link-up/admin-up",
               "ipv4": {
                    "counters": {
                         "multicast_bytes_received": 13421700,
                         "labeled_packets_forwarded": 0,
                         "multicast_bytes_sent": 17167084,
                         "unicast_bytes_sent": 9499793,
                         "labeled_packets_received": 0,
                         "labeled_packets_originated": 0,
                         "multicast_bytes_consumed": 13421700,
                         "multicast_packets_sent": 208673,
                         "unicast_bytes_consumed": 2804558,
                         "broadcast_packets_originated": 0,
                         "multicast_packets_originated": 208673,
                         "multicast_bytes_originated": 17167084,
                         "multicast_packets_received": 208601,
                         "multicast_packets_consumed": 417202,
                         "broadcast_packets_forwarded": 0,
                         "broadcast_bytes_originated": 0,
                         "labeled_bytes_originated": 0,
                         "broadcast_bytes_consumed": 0,
                         "broadcast_packets_sent": 0,
                         "labeled_packets_consumed": 0,
                         "unicast_packets_consumed": 46150,
                         "labeled_bytes_forwarded": 0,
                         "broadcast_packets_consumed": 0,
                         "unicast_packets_sent": 53942,
                         "broadcast_bytes_received": 0,
                         "labeled_packets_sent": 0,
                         "labeled_bytes_consumed": 0,
                         "unicast_bytes_received": 2803426,
                         "multicast_bytes_forwarded": 0,
                         "multicast_packets_forwarded": 0,
                         "unicast_packets_forwarded": 0,
                         "unicast_packets_received": 46139,
                         "broadcast_packets_received": 0,
                         "broadcast_bytes_sent": 0,
                         "broadcast_bytes_forwarded": 0,
                         "labeled_bytes_sent": 0,
                         "unicast_bytes_forwarded": 0,
                         "unicast_packets_originated": 53942,
                         "labeled_bytes_received": 0,
                         "unicast_bytes_originated": 9499793
                    },
                    "10.3.4.4/24": {
                         "route_preference": "0",
                         "prefix_length": "24",
                         "broadcast_address": "255.255.255.255",
                         "ip_subnet": "10.3.4.0",
                         "ip": "10.3.4.4",
                         "secondary": False,
                         "route_tag": "0"
                    }
               },
               "icmp_unreachable": "disabled",
               "wccp_redirect_inbound": "disabled",
               "unicast_reverse_path": "none",
               "icmp_redirects": "enabled",
               "multicast_routing": "disabled",
               "wccp_redirect_outbound": "disabled",
               "iod": 36,
               "directed_broadcast": "disabled",
               "ip_mtu": 1500,
               "vrf": "default",
               "local_proxy_arp": "disabled",
               "wccp_redirect_exclude": "disabled",
               "ip_forwarding": "disabled",
               "int_stat_last_reset": "never",
               "multicast_groups": [
                    "224.0.0.2",
                    "224.0.0.5",
                    "224.0.0.6"
               ]
          },
          "Ethernet2/10.12": {
               "icmp_port_unreachable": "enabled",
               "multicast_groups_address": "none",
               "proxy_arp": "disabled",
               "interface_status": "protocol-down/link-down/admin-down",
               "load_sharing": "none",
               "ipv4": {
                    "counters": {
                         "multicast_bytes_received": 0,
                         "labeled_packets_forwarded": 0,
                         "multicast_bytes_sent": 0,
                         "unicast_bytes_sent": 0,
                         "labeled_packets_received": 0,
                         "labeled_packets_originated": 0,
                         "multicast_bytes_consumed": 0,
                         "multicast_packets_sent": 0,
                         "unicast_bytes_consumed": 0,
                         "broadcast_packets_originated": 0,
                         "multicast_packets_originated": 0,
                         "multicast_bytes_originated": 0,
                         "multicast_packets_received": 0,
                         "multicast_packets_consumed": 0,
                         "broadcast_packets_forwarded": 0,
                         "broadcast_bytes_originated": 0,
                         "labeled_bytes_originated": 0,
                         "broadcast_bytes_consumed": 0,
                         "broadcast_packets_sent": 0,
                         "labeled_packets_consumed": 0,
                         "unicast_packets_consumed": 0,
                         "labeled_bytes_forwarded": 0,
                         "broadcast_packets_consumed": 0,
                         "unicast_packets_sent": 0,
                         "broadcast_bytes_received": 0,
                         "labeled_packets_sent": 0,
                         "labeled_bytes_consumed": 0,
                         "unicast_bytes_received": 0,
                         "multicast_bytes_forwarded": 0,
                         "multicast_packets_forwarded": 0,
                         "unicast_packets_forwarded": 0,
                         "unicast_packets_received": 0,
                         "broadcast_packets_received": 0,
                         "broadcast_bytes_sent": 0,
                         "broadcast_bytes_forwarded": 0,
                         "labeled_bytes_sent": 0,
                         "unicast_bytes_forwarded": 0,
                         "unicast_packets_originated": 0,
                         "labeled_bytes_received": 0,
                         "unicast_bytes_originated": 0
                    },
                    "10.66.12.12/24": {
                         "route_preference": "0",
                         "prefix_length": "24",
                         "broadcast_address": "255.255.255.255",
                         "ip_subnet": "10.66.12.0",
                         "ip": "10.66.12.12",
                         "secondary": False,
                         "route_tag": "0"
                    }
               },
               "icmp_unreachable": "disabled",
               "wccp_redirect_inbound": "disabled",
               "unicast_reverse_path": "none",
               "icmp_redirects": "enabled",
               "multicast_routing": "disabled",
               "wccp_redirect_outbound": "disabled",
               "iod": 184,
               "directed_broadcast": "disabled",
               "ip_mtu": 1500,
               "vrf": "default",
               "local_proxy_arp": "disabled",
               "ip_forwarding": "disabled",
               "int_stat_last_reset": "never",
               "wccp_redirect_exclude": "disabled"
          },
          "Ethernet2/12": {
               "icmp_port_unreachable": "enabled",
               "multicast_groups_address": "none",
               "proxy_arp": "disabled",
               "interface_status": "protocol-down/link-down/admin-down",
               "load_sharing": "none",
               "ipv4": {
                    "counters": {
                         "multicast_bytes_received": 0,
                         "labeled_packets_forwarded": 0,
                         "multicast_bytes_sent": 0,
                         "unicast_bytes_sent": 0,
                         "labeled_packets_received": 0,
                         "labeled_packets_originated": 0,
                         "multicast_bytes_consumed": 0,
                         "multicast_packets_sent": 0,
                         "unicast_bytes_consumed": 0,
                         "broadcast_packets_originated": 0,
                         "multicast_packets_originated": 0,
                         "multicast_bytes_originated": 0,
                         "multicast_packets_received": 0,
                         "multicast_packets_consumed": 0,
                         "broadcast_packets_forwarded": 0,
                         "broadcast_bytes_originated": 0,
                         "labeled_bytes_originated": 0,
                         "broadcast_bytes_consumed": 0,
                         "broadcast_packets_sent": 0,
                         "labeled_packets_consumed": 0,
                         "unicast_packets_consumed": 0,
                         "labeled_bytes_forwarded": 0,
                         "broadcast_packets_consumed": 0,
                         "unicast_packets_sent": 0,
                         "broadcast_bytes_received": 0,
                         "labeled_packets_sent": 0,
                         "labeled_bytes_consumed": 0,
                         "unicast_bytes_received": 0,
                         "multicast_bytes_forwarded": 0,
                         "multicast_packets_forwarded": 0,
                         "unicast_packets_forwarded": 0,
                         "unicast_packets_received": 0,
                         "broadcast_packets_received": 0,
                         "broadcast_bytes_sent": 0,
                         "broadcast_bytes_forwarded": 0,
                         "labeled_bytes_sent": 0,
                         "unicast_bytes_forwarded": 0,
                         "unicast_packets_originated": 0,
                         "labeled_bytes_received": 0,
                         "unicast_bytes_originated": 0
                    },
                    "10.66.12.12/24": {
                         "ip": "10.66.12.12",
                         "prefix_length": "24",
                         "broadcast_address": "255.255.255.255",
                         "secondary": False,
                         "ip_subnet": "10.66.12.0"
                    },
                    "unnumbered": {
                         "interface_ref": "Ethernet2/10.12"
                    }
               },
               "icmp_unreachable": "disabled",
               "wccp_redirect_inbound": "disabled",
               "unicast_reverse_path": "none",
               "icmp_redirects": "enabled",
               "multicast_routing": "disabled",
               "wccp_redirect_outbound": "disabled",
               "iod": 47,
               "directed_broadcast": "disabled",
               "ip_mtu": 1500,
               "vrf": "default",
               "local_proxy_arp": "disabled",
               "ip_forwarding": "disabled",
               "int_stat_last_reset": "never",
               "wccp_redirect_exclude": "disabled"}
          }

	Arp_info = {
          'interfaces': {
               'Ethernet1/1': {
                    'ipv4': {
                         'neighbors': {
                              '10.1.3.5': {
                                   'ip': '10.1.3.5',
                                   'link_layer_address': 'aaaa.bbbb.cccc',
                                   'origin': 'static'}
                         }
                    }
               },
               'Ethernet1/1.1': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.4.2': {
                                   'ip': '192.168.4.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/1.2': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.154.2': {
                                   'ip': '192.168.154.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/1.4': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.106.2': {
                                   'ip': '192.168.106.2',
                                   'link_layer_address': '000c.292a.1eaf',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/2.1': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.154.2': {
                                   'ip': '192.168.154.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/2.2': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.51.2': {
                                   'ip': '192.168.51.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/2.4': {
                    'ipv4': {
                         'neighbors': {
                              '192.168.9.2': {
                                   'ip': '192.168.9.2',
                                   'link_layer_address': '000c.2904.5840',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/4.100': {
                    'ipv4': {
                         'neighbors': {
                              '10.51.1.101': {
                                   'ip': '10.51.1.101',
                                   'link_layer_address': '0000.71c7.6e61',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/4.101': {
                    'ipv4': {
                         'neighbors': {
                              '10.154.1.101': {
                                   'ip': '10.154.1.101',
                                   'link_layer_address': '0000.71c7.75c1',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet1/4.200': {
                    'ipv4': {
                         'neighbors': {
                              '10.76.1.101': {
                                   'ip': '10.76.1.101',
                                   'link_layer_address': '0000.0068.ce6f',
                                   'origin': 'dynamic'}
                         }
                    }
               },
               'Ethernet2/1': {
                    'arp_dynamic_learning': {
                         'local_proxy_enable': False,
                         'proxy_enable': False}
               },
               'Ethernet2/10.12': {
                    'arp_dynamic_learning': {
                         'local_proxy_enable': False,
                         'proxy_enable': False}
               },
               'Ethernet2/11': {
                    'arp_dynamic_learning': {
                         'local_proxy_enable': False,
                         'proxy_enable': False}
               },
               'Ethernet2/12': {
                    'arp_dynamic_learning': {
                         'local_proxy_enable': False,
                         'proxy_enable': False}
               },
               'loopback0': {
                    'arp_dynamic_learning': {
                         'local_proxy_enable': False,
                         'proxy_enable': False}
               },
               'mgmt0': {
                    'ipv4': {
                         'neighbors': {
                              '10.1.7.1': {
                                   'ip': '10.1.7.1',
                                   'link_layer_address': '0012.7f57.ac80',
                                   'origin': 'dynamic'},
                              '10.1.7.250': {
                                   'ip': '10.1.7.250',
                                   'link_layer_address': '0050.5682.7915',
                                   'origin': 'dynamic'},
                              '10.1.7.253': {
                                   'ip': '10.1.7.253',
                                   'link_layer_address': '0050.56a4.a9fc',
                                   'origin': 'dynamic'}
                         }
                    }
               }
          },
          'statistics': {
               'entries_total': 12,
               'in_drops': 28218,
               'in_replies_pkts': 6582,
               'in_requests_pkts': 22632,
               'in_total': 0,
               'incomplete_total': 0,
               'out_drops': 0,
               'out_gratuitous_pkts': 58,
               'out_replies_pkts': 998,
               'out_requests_pkts': 2102,
               'out_total': 3158}
          }