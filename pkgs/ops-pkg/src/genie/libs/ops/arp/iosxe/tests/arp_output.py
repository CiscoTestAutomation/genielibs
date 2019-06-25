''' 
Arp Genie Ops Object Outputs for IOSXE.
'''


class ArpOutput(object):

	ShowArp = {
		'interfaces': {
			'Vlan100': {
				'ipv4': {
					'neighbors': {
						'192.168.234.1': {
							'age': '-',
							'ip': '192.168.234.1',
							'link_layer_address': '58bf.eab6.2f51',
							'origin': 'static',
							'protocol': 'Internet',
							'type': 'ARPA'},
						'192.168.234.2': {'age': '29',
							'ip': '192.168.234.2',
							'link_layer_address': '3820.5672.fc51',
							'origin': 'dynamic',
							'protocol': 'Internet',
							'type': 'ARPA'}
					}
				}
			},
			'Vlan200': {
				'ipv4': {
					'neighbors': {
						'192.168.70.1': {
							'age': '-',
							'ip': '192.168.70.1',
							'link_layer_address': '58bf.eab6.2f62',
							'origin': 'static',
							'protocol': 'Internet',
							'type': 'ARPA'}
					}
				}
			}
		}
	}
	ShowIpArp_all='''
			Protocol  Address          Age (min)  Hardware Addr   Type   Interface
			Internet  192.168.234.1           -   58bf.eab6.2f51  ARPA   Vlan100
			Internet  192.168.234.2          29   3820.5672.fc51  ARPA   Vlan100
			Internet  192.168.70.1            -   58bf.eab6.2f62  ARPA   Vlan200
			'''
	ShowIpArp_vrf1='''
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.12.90.1              -   fa16.3e24.787a  ARPA   GigabitEthernet2.390
Internet  10.12.90.2            139   fa16.3e8a.cfeb  ARPA   GigabitEthernet2.390
Internet  10.12.110.1             -   fa16.3e24.787a  ARPA   GigabitEthernet2.410
	'''
	ShowIpArp={
        'interfaces': {
            'GigabitEthernet2.390': {
                'ipv4': {
                    'neighbors': {
                        '10.12.90.1': {
                            'age': '-',
                            'ip': '10.12.90.1',
                            'link_layer_address': 'fa16.3e24.787a',
                            'origin': 'static',
                            'protocol': 'Internet',
                            'type': 'ARPA'},
                        '10.12.90.2':
                            {'age': '139',
                             'ip': '10.12.90.2',
                             'link_layer_address': 'fa16.3e8a.cfeb',
                             'origin': 'dynamic',
                             'protocol': 'Internet',
                             'type': 'ARPA'}
                    }
                }
            },
            'GigabitEthernet2.410': {
                'ipv4': {
                    'neighbors': {
                        '10.12.110.1': {
                            'age': '-',
                            'ip': '10.12.110.1',
                            'link_layer_address': 'fa16.3e24.787a',
                            'origin': 'static',
                            'protocol': 'Internet',
                            'type': 'ARPA'}
                    }
                }
            }
        }
    }
	ShowVrf={
        'vrf': {
            'VRF1': {
                'route_distinguisher': '65000:1',
                'protocols': ['ipv4', 'ipv6'],
                'interfaces': ['GigabitEthernet2.390',
                               'GigabitEthernet2.410'],
            }
        }
    }
	ShowIpArpSummary = {
		  'incomp_entries': 0,
		  'total_entries': 8}

	ShowIpTraffic = {
		'arp_statistics': {
			'arp_drops_input_full': 0,
			'arp_in_other': 0,
			'arp_in_replies': 764,
			'arp_in_requests': 2020,
			'arp_in_reverse': 0,
			'arp_out_proxy': 2,
			'arp_out_replies': 126,
			'arp_out_requests': 29,
			'arp_out_reverse': 0},
			'ip_statistics': {
				'ip_bcast_received': 33324,
			'ip_bcast_sent': 5,
			'ip_drop_encap_failed': 8,
			'ip_drop_forced_drop': 0,
			'ip_drop_no_adj': 20,
			'ip_drop_no_route': 19,
			'ip_drop_opts_denied': 0,
			'ip_drop_src_ip': 0,
			'ip_drop_unicast_rpf': 0,
			'ip_drop_unresolved': 0,
			'ip_drop_unsupp_address': 0,
			'ip_frags_fragmented': 1,
			'ip_frags_fragments': 5,
			'ip_frags_invalid_hole': 0,
			'ip_frags_no_fragmented': 0,
			'ip_frags_no_reassembled': 0,
			'ip_frags_reassembled': 0,
			'ip_frags_timeouts': 0,
			'ip_mcast_received': 144833,
			'ip_mcast_sent': 66274,
			'ip_opts_alert': 12717,
			'ip_opts_basic_security': 0,
			'ip_opts_cipso': 0,
			'ip_opts_end': 0,
			'ip_opts_extended_security': 0,
			'ip_opts_ignored': 0,
			'ip_opts_loose_src_route': 0,
			'ip_opts_nop': 0,
			'ip_opts_other': 0,
			'ip_opts_record_route': 0,
			'ip_opts_strct_src_route': 0,
			'ip_opts_strm_id': 0,
			'ip_opts_timestamp': 0,
			'ip_opts_ump': 0,
			'ip_rcvd_bad_hop': 0,
			'ip_rcvd_bad_optns': 0,
			'ip_rcvd_checksum_errors': 0,
			'ip_rcvd_format_errors': 0,
			'ip_rcvd_local_destination': 110596,
			'ip_rcvd_not_gateway': 5,
			'ip_rcvd_sec_failures': 0,
			'ip_rcvd_total': 17780,
			'ip_rcvd_unknwn_protocol': 0,
			'ip_rcvd_with_optns': 12717,
			'ip_sent_forwarded': 1654728,
			'ip_sent_generated': 85543},
		'icmp_statistics': {
			'icmp_received_checksum_errors': 0,
			'icmp_received_echo': 284,
			'icmp_received_echo_reply': 9,
			'icmp_received_format_errors': 0,
			'icmp_received_info_replies': 0,
			'icmp_received_info_request': 0,
			'icmp_received_irdp_advertisements': 0,
			'icmp_received_irdp_solicitations': 0,
			'icmp_received_mask_replies': 0,
			'icmp_received_mask_requests': 0,
			'icmp_received_other': 0,
			'icmp_received_parameter': 0,
			'icmp_received_quench': 0,
			'icmp_received_redirects': 0,
			'icmp_received_time_exceeded': 0,
			'icmp_received_timestamp': 0,
			'icmp_received_timestamp_replies': 0,
			'icmp_received_unreachable': 0,
			'icmp_sent_echo': 9,
			'icmp_sent_echo_reply': 134,
			'icmp_sent_info_reply': 0,
			'icmp_sent_irdp_advertisements': 0,
			'icmp_sent_irdp_solicitations': 0,
			'icmp_sent_mask_replies': 0,
			'icmp_sent_mask_requests': 0,
			'icmp_sent_parameter_problem': 0,
			'icmp_sent_quench': 0,
			'icmp_sent_redirects': 0,
			'icmp_sent_time_exceeded': 0,
			'icmp_sent_timestamp': 0,
			'icmp_sent_timestamp_replies': 0,
			'icmp_sent_unreachable': 14},
		'udp_statistics': {
			'udp_received_finput': 0,
			'udp_received_no_port': 15906,
			'udp_received_total': 62515,
			'udp_received_udp_checksum_errors': 0,
			'udp_sent_fwd_broadcasts': 0,
			'udp_sent_total': 41486},
		'pimv2_statistics': {
			'pimv2_asserts': '0/697',
			'pimv2_bootstraps': '2088/2438',
			'pimv2_candidate_rp_advs': '350/0',
			'pimv2_checksum_errors': 0,
			'pimv2_format_errors': 0,
			'pimv2_grafts': '0/2',
			'pimv2_hellos': '5011/5008',
			'pimv2_join_prunes': '5/712',
			'pimv2_non_rp': 0,
			'pimv2_non_sm_group': 0,
			'pimv2_queue_drops': 0,
			'pimv2_registers': '1/1',
			'pimv2_registers_stops': '1/1',
			'pimv2_state_refresh': '0/0',
			'pimv2_total': '7458/8859'},
		'ospf_statistics': {
			'ospf_received_checksum_errors': 0,
			'ospf_received_database_desc': 20,
			'ospf_received_hello': 15153,
			'ospf_received_link_state_req': 2,
			'ospf_received_lnk_st_acks': 688,
			'ospf_received_lnk_st_updates': 359,
			'ospf_received_total': 16222,
			'ospf_sent_database_desc': 30,
			'ospf_sent_hello': 8887,
			'ospf_sent_lnk_st_acks': 239,
			'ospf_sent_lnk_st_updates': 299,
			'ospf_sent_total': 9456,
			'ospf_traffic_cntrs_clear': 'never'},
		'igmp_statistics': {
			'igmp_checksum_errors': '0/0',
			'igmp_dvmrp': '0/0',
			'igmp_format_errors': '0/0',
			'igmp_host_leaves': '0/5',
			'igmp_host_queries': '2475/1414',
			'igmp_host_reports': '357/3525',
			'igmp_pim': '0/0',
			'igmp_queue_drops': 0,
			'igmp_total': '2832/4946'},
		'tcp_statistics': {
			'tcp_received_checksum_errors': 0,
			'tcp_received_no_port': 0,
			'tcp_received_total': 15396,
			'tcp_sent_total': 19552},
		'eigrp_ipv4_statistics': {
			'eigrp_ipv4_received_total': 4612,
			'eigrp_ipv4_sent_total': 4611},
		'bgp_statistics': {
			'bgp_received_keepalives': 2167,
			'bgp_received_notifications': 0,
			'bgp_received_opens': 6,
			'bgp_received_route_refresh': 0,
			'bgp_received_total': 2185,
			'bgp_received_unrecognized': 0,
			'bgp_received_updates': 12,
			'bgp_sent_keepalives': 2296,
			'bgp_sent_notifications': 2,
			'bgp_sent_opens': 6,
			'bgp_sent_route_refresh': 0,
			'bgp_sent_total': 2304,
			'bgp_sent_updates': 0},
	}

	ShowIpInterface = {
		"Vlan211": {
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
				 "192.168.76.1/24": {
					  "prefix_length": "24",
					  "ip": "192.168.76.1",
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

	Arp_info = {
		'interfaces': {
			'GigabitEthernet0/0': {
				'arp_dynamic_learning': {
					'local_proxy_enable': False,
					'proxy_enable': True}
			},
			'GigabitEthernet1/0/1': {
				'arp_dynamic_learning': {
					'local_proxy_enable': False,
					'proxy_enable': True}
			},
			'Vlan100': {
				'ipv4': {
					'neighbors': {
						'192.168.234.1': {
							'ip': '192.168.234.1',
							'link_layer_address': '58bf.eab6.2f51',
							'origin': 'static'},
						'192.168.234.2': {
							'ip': '192.168.234.2',
							'link_layer_address': '3820.5672.fc51',
							'origin': 'dynamic'}
					}
				}
			},
			'Vlan200': {
				'ipv4': {
					'neighbors': {
						'192.168.70.1': {
							'ip': '192.168.70.1',
							'link_layer_address': '58bf.eab6.2f62',
							'origin': 'static'}
					}
				}
			},
			'Vlan211': {
				'arp_dynamic_learning': {
					'local_proxy_enable': False,
					'proxy_enable': True}
			},
			'GigabitEthernet2.390': {
				'ipv4': {
					'neighbors': {
						'10.12.90.1': {
							'ip': '10.12.90.1',
							'link_layer_address': 'fa16.3e24.787a',
							'origin': 'static',
						},
						'10.12.90.2':
							{
							 'ip': '10.12.90.2',
							 'link_layer_address': 'fa16.3e8a.cfeb',
							 'origin': 'dynamic',
							}
					}
				}
			},
			'GigabitEthernet2.410': {
				'ipv4': {
					'neighbors': {
						'10.12.110.1': {
							'ip': '10.12.110.1',
							'link_layer_address': 'fa16.3e24.787a',
							'origin': 'static',
							}
					}
				}
		},
		},
		'statistics': {
			'entries_total': 8,
			'in_drops': 0,
			'in_replies_pkts': 764,
			'in_requests_pkts': 2020,
			'incomplete_total': 0,
			'out_replies_pkts': 126,
			'out_requests_pkts': 29}}
