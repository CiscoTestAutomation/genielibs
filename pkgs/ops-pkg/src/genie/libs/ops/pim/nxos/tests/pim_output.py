''' 
Pim Genie Ops Object Outputs for NXOS.
'''


class PimOutput(object):

    ShowFeature = {
        'feature':
            {'bash-shell':
                {'instance':
                    {'1':
                        {'state': 'disabled',}}},
            'bgp':
                {'instance':
                    {'1':
                        {'state': 'enabled',}}},
            'pim':
                {'instance':
                    {'1':
                        {'state': 'enabled',}}},
            'pim6':
                {'instance':
                    {'1':
                        {'state': 'enabled',}}},
            'eigrp':
                {'instance':
                    {'1':
                        {'state': 'enabled',},
                    '2':
                        {'state': 'enabled',
                         'running': 'no',},
                    '3':
                        {'state': 'enabled',
                         'running': 'no',},
                    '4':
                        {'state': 'enabled',
                         'running': 'no',}, }}}
    }

    ShowIpPimInterfaceVrfAll = {
        'vrf':{
            'VRF1':{
                'interfaces':{
                    'Ethernet2/2':{
                        'address_family':{
                            'ipv4':{
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['10.11.33.11', '10.229.11.11'],
                                'ip_subnet': '10.11.33.0/24',
                                'dr_address': '10.11.33.11' ,
                                'dr_priority': 144,
                                'neighbor_count': 1,
                                'hello_interval': 45,
                                'hello_expiration': '00:00:05',
                                'neighbor_holdtime': 159,
                                'configured_dr_priority': 144,
                                'dr_delay': 3 ,
                                'bsr_border': True,
                                'genid': '0x26fae674',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'v4neighbor-policy',
                                'jp_inbound_policy': 'v4jp-policy',
                                'jp_outbound_policy': 'v4jp-policy',
                                'jp_interval': 60,
                                'jp_next_sending': 60,
                                'bfd': {
                                    'enable': False,
                                },
                               'sm': {
                                    'passive': False,
                                },
                               'vpc_svi': False,
                               'auto_enabled': False,
                               'statistics': {
                                    'general': {
                                        'hellos': '360/474',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                        },
                    },
                    'Ethernet2/3':{
                        'address_family': {
                            'ipv4': {
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['10.11.66.11', '192.168.64.2'],
                                'ip_subnet': '10.11.66.0/24',
                                'dr_address': '10.11.66.11',
                                'dr_priority': 1,
                                'neighbor_count': 0,
                                'hello_interval': 30,
                                'hello_expiration': '00:00:14',
                                'neighbor_holdtime': 105,
                                'configured_dr_priority': 1,
                                'dr_delay': 3,
                                'bsr_border': False,
                                'genid': '0x2737c18b',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'none configured',
                                'jp_inbound_policy': 'none configured',
                                'jp_outbound_policy': 'none configured',
                                'jp_interval': 60,
                                'jp_next_sending': 60,
                                'bfd': {
                                    'enable': False,
                                },
                                'sm': {
                                    'passive': False,
                                },
                                'vpc_svi': False,
                                'auto_enabled': False,
                                'statistics': {
                                    'general': {
                                        'hellos': '489/0',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                            },
                        },
                    },
                },
            'default':{
                'interfaces': {
                    'Ethernet2/1': {
                        'address_family': {
                            'ipv4': {
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['10.1.5.1'],
                                'ip_subnet': '10.1.5.0/24',
                                'dr_address': '10.1.5.1',
                                'dr_priority': 1,
                                'neighbor_count': 0,
                                'hello_interval': 30,
                                'hello_expiration': '00:00:13',
                                'neighbor_holdtime': 105,
                                'configured_dr_priority': 1,
                                'dr_delay': 3,
                                'bsr_border': False,
                                'genid': '0x3148ed16',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'none configured',
                                'jp_inbound_policy': 'none configured',
                                'jp_outbound_policy': 'none configured',
                                'jp_interval': 60,
                                'jp_next_sending': 60,
                                'bfd': {
                                    'enable': False,
                                },
                                'sm': {
                                    'passive': False,
                                },
                                'vpc_svi': False,
                                'auto_enabled': False,
                                'statistics': {
                                    'general': {
                                        'hellos': '243/0',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }
    }

    ShowIpv6PimInterfaceVrfAll = {
        'vrf':{
            'default':{
                'interfaces':{
                    'Ethernet2/1':{
                        'address_family':{
                            'ipv6':{
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['2001:db8:1:5::1/64'],
                                'dr_address': 'fe80::5054:ff:fe89:740c' ,
                                'dr_priority': 1,
                                'neighbor_count': 0,
                                'hello_interval': 30,
                                'hello_expiration': '00:00:13',
                                'neighbor_holdtime': 105,
                                'configured_dr_priority': 1,
                                'bsr_border': False,
                                'genid': '0x25f72e3c',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'none configured',
                                'jp_inbound_policy': 'none configured',
                                'jp_outbound_policy': 'none configured',
                                'bfd': {
                                    'enable': False,
                                },
                               'sm': {
                                    'passive': False,
                                },
                               'auto_enabled': False,
                               'statistics': {
                                    'last_reset': 'never',
                                    'general': {
                                        'hellos': '240/0',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                        },
                    },
                    'Ethernet2/4':{
                        'address_family': {
                            'ipv6': {
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['2001:db8:1:2::1/64','2001:db8:1:2::2/64'],
                                'dr_address': 'fe80::5054:ff:fe89:740c',
                                'dr_priority': 1,
                                'neighbor_count': 0,
                                'hello_interval': 30,
                                'hello_expiration': '00:00:07',
                                'neighbor_holdtime': 105,
                                'configured_dr_priority': 1,
                                'bsr_border': False,
                                'genid': '0x30a2ad71',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'none configured',
                                'jp_inbound_policy': 'none configured',
                                'jp_outbound_policy': 'none configured',
                                'bfd': {
                                    'enable': False,
                                },
                                'sm': {
                                    'passive': False,
                                },
                                'auto_enabled': False,
                                'statistics': {
                                    'last_reset': 'never',
                                    'general': {
                                        'hellos': '489/0',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                            },
                        },
                    },
                },
            'VRF1':{
                'interfaces': {
                    'Ethernet2/2': {
                        'address_family': {
                            'ipv6': {
                                'oper_status': 'up',
                                'link_status': 'up',
                                'admin_status': 'up',
                                'address': ['2001:db8:11:33::11/64'],
                                'dr_address': 'fe80::5054:ff:fe89:740c',
                                'dr_priority': 166,
                                'neighbor_count': 1,
                                'hello_interval': 67,
                                'hello_expiration': '00:00:34',
                                'neighbor_holdtime': 236,
                                'configured_dr_priority': 166,
                                'bsr_border': True,
                                'genid': '0x08f0f420',
                                'hello_md5_ah_authentication': 'disabled',
                                'neighbor_filter': 'v6neighbor-policy',
                                'jp_inbound_policy': 'v6jp-policy',
                                'jp_outbound_policy': 'v6jp-policy',
                                'bfd': {
                                    'enable': False,
                                },
                                'sm': {
                                    'passive': False,
                                },
                                'auto_enabled': False,
                                'statistics': {
                                    'last_reset': 'never',
                                    'general': {
                                        'hellos': '274/477',
                                        'jps': '0/0',
                                        'asserts': '0/0',
                                        'grafts': '0/0',
                                        'graft_acks': '0/0',
                                        'df_offers': '0/0',
                                        'df_winners': '0/0',
                                        'df_backoffs': '0/0',
                                        'df_passes': '0/0',
                                    },
                                    'errors': {
                                        'checksum': 0,
                                        'invalid_packet_types': 0,
                                        'invalid_df_subtypes': 0,
                                        'authentication_failed': 0,
                                        'packet_length_errors': 0,
                                        'bad_version_packets': 0,
                                        'packets_from_self': 0,
                                        'packets_from_non_neighbors': 0,
                                        'packets_received_on_passiveinterface': 0,
                                        'jps_received_on_rpf_interface': 0,
                                        'joins_received_with_no_rp': 0,
                                        'joins_received_with_wrong_rp': 0,
                                        'joins_received_with_ssm_groups': 0,
                                        'joins_received_with_bidir_groups': 0,
                                        'jps_filtered_by_inbound_policy': 0,
                                        'jps_filtered_by_outbound_policy': 0,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }

    }

    ShowIpPimRpVrfAll = {
        "vrf": {
            "default": {
                 "address_family": {
                      "ipv4": {
                           "rp": {
                                "autorp": {
                                     "address": "10.1.5.1",
                                     "bsr_next_discovery": "00:00:42"
                                },
                                "static_rp": {
                                     "10.111.111.111": {
                                          "sm": {
                                               "policy_name": "224.0.0.0/4"
                                          }
                                     },
                                     "10.16.2.2": {
                                          "sm": {
                                               "policy_name": "224.0.0.0/4"
                                          }
                                     },
                                     "10.66.12.12": {
                                          "bidir": {
                                               "policy_name": "233.0.0.0/24"
                                          }
                                     }
                                },
                                "rp_list": {
                                     "10.111.111.111 SM static": {
                                          "mode": "SM",
                                          "group_ranges": "224.0.0.0/4",
                                          "df_ordinal": 0,
                                          "expiration": "never",
                                          "up_time": "00:01:06",
                                          "address": "10.111.111.111",
                                          "info_source_type": "static"
                                     },
                                     "10.16.2.2 SM static": {
                                          "mode": "SM",
                                          "group_ranges": "224.0.0.0/4",
                                          "df_ordinal": 0,
                                          "expiration": "never",
                                          "up_time": "03:52:52",
                                          "address": "10.16.2.2",
                                          "info_source_type": "static"
                                     },
                                     "10.66.12.12 BIDIR static": {
                                          "mode": "BIDIR",
                                          "group_ranges": "233.0.0.0/24",
                                          "df_ordinal": 1,
                                          "expiration": "never",
                                          "up_time": "00:00:54",
                                          "address": "10.66.12.12",
                                          "info_source_type": "static"
                                     },
                                     "10.1.5.1 SM bootstrap": {
                                          "mode": "SM",
                                          "group_ranges": "224.0.0.0/5",
                                          "df_ordinal": 0,
                                          "expiration": "00:02:05",
                                          "up_time": "01:56:07",
                                          "priority": 92,
                                          "address": "10.1.5.1",
                                          "info_source_address": "10.1.5.1",
                                          "info_source_type": "bootstrap"
                                     }
                                },
                                "rp_mappings": {
                                     "224.0.0.0/4 10.16.2.2 static": {
                                          "group": "224.0.0.0/4",
                                          "protocol": "static",
                                          "rp_address": "10.16.2.2",
                                          "up_time": "03:52:52",
                                          "expiration": "never"
                                     },
                                     "224.0.0.0/4 10.111.111.111 static": {
                                          "group": "224.0.0.0/4",
                                          "protocol": "static",
                                          "rp_address": "10.111.111.111",
                                          "up_time": "00:01:06",
                                          "expiration": "never"
                                     },
                                     "224.0.0.0/5 10.1.5.1 bootstrap": {
                                          "group": "224.0.0.0/5",
                                          "protocol": "bootstrap",
                                          "rp_address": "10.1.5.1",
                                          "up_time": "01:56:07",
                                          "expiration": "00:02:05"
                                     },
                                     "233.0.0.0/24 10.66.12.12 static": {
                                          "group": "233.0.0.0/24",
                                          "protocol": "static",
                                          "rp_address": "10.66.12.12",
                                          "up_time": "00:00:54",
                                          "expiration": "never"
                                     }
                                },
                                "bsr": {
                                     "bsr_candidate": {
                                          "hash_mask_length": 30,
                                          "priority": 111,
                                          "address": "10.1.5.1"
                                     },
                                     "rp": {
                                          "up_time": "01:56:07",
                                          "rp_address": "10.1.5.1",
                                          "group_policy": "224.0.0.0/5"
                                     },
                                     "bsr_next_bootstrap": "00:00:01",
                                     'rp_candidate_next_advertisement': '00:02:05',
                                     "bsr_address": {
                                          "10.1.5.1": {
                                               "mode": "SM",
                                               "priority": 92,
                                               "address": "10.1.5.1",
                                               "policy": "224.0.0.0/5"
                                          }
                                     },
                                     "bsr": {
                                          "hash_mask_length": 30,
                                          "priority": 111,
                                          "address": "10.1.5.1"
                                     }
                                }
                           },
                           "sm": {
                                "asm": {
                                     "anycast_rp": {
                                          "10.111.111.111 10.1.5.1": {
                                               "anycast_address": "10.111.111.111"
                                          },
                                          "10.111.111.111 10.1.2.1": {
                                               "anycast_address": "10.111.111.111"
                                          }
                                     }
                                }
                           }
                      }
                 }
            },
            "VRF1": {
                 "address_family": {
                      "ipv4": {
                           "rp": {
                                "autorp": {
                                     "send_rp_announce": {
                                          "rp_source": "192.168.64.2",
                                          "bidir": True,
                                          "scope": 0,
                                          "group_list": "226.0.0.0/8",
                                          "group": "226.0.0.0"
                                     },
                                     "address": "10.229.11.11",
                                     "bsr_next_discovery": "00:00:15"
                                },
                                "static_rp": {
                                     "10.21.33.33": {
                                          "sm": {
                                               "policy_name": "224.0.0.0/4"
                                          }
                                     }
                                },
                                "rp_list": {
                                     "192.168.64.2 BIDIR autorp": {
                                          "mode": "BIDIR",
                                          "group_ranges": "226.0.0.0/8",
                                          "df_ordinal": 0,
                                          "expiration": "never",
                                          "up_time": "04:30:45",
                                          "priority": 255,
                                          "address": "192.168.64.2",
                                          "info_source_address": "192.168.64.2",
                                          "info_source_type": "autorp"
                                     },
                                     "10.21.33.33 SM static": {
                                          "mode": "SM",
                                          "group_ranges": "224.0.0.0/4",
                                          "df_ordinal": 0,
                                          "expiration": "never",
                                          "up_time": "03:52:52",
                                          "address": "10.21.33.33",
                                          "info_source_type": "static"
                                     }
                                },
                                "rp_mappings": {
                                     "224.0.0.0/4 10.21.33.33 static": {
                                          "group": "224.0.0.0/4",
                                          "protocol": "static",
                                          "rp_address": "10.21.33.33",
                                          "up_time": "03:52:52",
                                          "expiration": "never"
                                     },
                                     "226.0.0.0/8 192.168.64.2 autorp": {
                                          "group": "226.0.0.0/8",
                                          "protocol": "autorp",
                                          "rp_address": "192.168.64.2",
                                          "up_time": "04:30:45",
                                          "expiration": "never"
                                     }
                                }
                           }
                      }
                 }
            }
       }
    }

    ShowIpv6PimRpVrfAll = {
        "vrf": {
            "VRF1": {
                 "address_family": {
                      "ipv6": {
                           "rp": {
                                "rp_list": {
                                     "2001:db8:1:1::1 SM bootstrap": {
                                          "df_ordinal": 0,
                                          "info_source_address": "2001:db8:1:1::1",
                                          "info_source_type": "bootstrap",
                                          "mode": "SM",
                                          "group_ranges": "ff05::1/8",
                                          "expiration": "00:02:20",
                                          "priority": 192,
                                          "up_time": "03:29:13",
                                          "address": "2001:db8:1:1::1"
                                     }
                                },
                                "rp_mappings": {
                                     "ff05::1/8 2001:db8:1:1::1 bootstrap": {
                                          "group": "ff05::1/8",
                                          "rp_address": "2001:db8:1:1::1",
                                          "expiration": "00:02:20",
                                          "protocol": "bootstrap",
                                          "up_time": "03:29:13"
                                     }
                                },
                                "bsr": {
                                     "bsr_address": {
                                          "2001:db8:1:1::1": {
                                               "mode": "SM",
                                               "policy": "ff05::1/8",
                                               "priority": 192,
                                               "address": "2001:db8:1:1::1"
                                          }
                                     },
                                     "bsr": {
                                          "priority": 99,
                                          "hash_mask_length": 128,
                                          "expires": "00:01:37",
                                          "address": "2001:db8:1:1::1",
                                          "up_time": "00:09:14"
                                     },
                                     "bsr_candidate": {
                                          "hash_mask_length": 128,
                                          "priority": 99,
                                          "address": "2001:db8:1:1::1"
                                     },
                                     "rp": {
                                          "rp_address": "2001:db8:1:1::1",
                                          "group_policy": "ff05::1/8",
                                          "up_time": "03:29:13"
                                     },
                                     "rp_candidate_next_advertisement": "00:02:20"
                                }
                           },
                           "sm": {
                                "asm": {
                                     "anycast_rp": {
                                          "2001:db8:111:111::111 2001:db8:3:4::5": {
                                               "anycast_address": "2001:db8:111:111::111"
                                          },
                                          "2001:db8:111:111::111 2001:db8:1:2::2": {
                                               "anycast_address": "2001:db8:111:111::111"
                                          }
                                     }
                                }
                           }
                      }
                 }
            },
            "default": {
                 "address_family": {
                      "ipv6": {
                           "rp": {
                                "rp_list": {
                                     "2001:db8:1:1::1 SM bootstrap": {
                                          "df_ordinal": 0,
                                          "info_source_address": "2001:db8:1:1::1",
                                          "info_source_type": "bootstrap",
                                          "mode": "SM",
                                          "group_ranges": "ff05::1/8",
                                          "expiration": "00:02:20",
                                          "priority": 192,
                                          "up_time": "03:29:13",
                                          "address": "2001:db8:1:1::1"
                                     },
                                     "2001:db8:504::1 SM static": {
                                          "expiration": "0.000000",
                                          "info_source_type": "static",
                                          "mode": "SM",
                                          "group_ranges": "ff1e::3002/128 ff1e::3001/128",
                                          "df_ordinal": 0,
                                          "up_time": "00:00:02",
                                          "address": "2001:db8:504::1"
                                     },
                                     "2001:db8:12:12::12 BIDIR static": {
                                          "expiration": "0.000000",
                                          "info_source_type": "static",
                                          "mode": "BIDIR",
                                          "group_ranges": "ff08::/16",
                                          "df_ordinal": 7,
                                          "up_time": "00:58:17",
                                          "address": "2001:db8:12:12::12"
                                     },
                                     "2001:db8:111:111::111 SM static": {
                                          "expiration": "0.000000",
                                          "info_source_type": "static",
                                          "mode": "SM",
                                          "group_ranges": "ff09::/16",
                                          "df_ordinal": 0,
                                          "up_time": "00:00:52",
                                          "address": "2001:db8:111:111::111"
                                     }
                                },
                                "rp_mappings": {
                                     "ff09::/16 2001:db8:111:111::111 static": {
                                          "group": "ff09::/16",
                                          "rp_address": "2001:db8:111:111::111",
                                          "expiration": "0.000000",
                                          "protocol": "static",
                                          "up_time": "00:00:52"
                                     },
                                     "ff05::1/8 2001:db8:1:1::1 bootstrap": {
                                          "group": "ff05::1/8",
                                          "rp_address": "2001:db8:1:1::1",
                                          "expiration": "00:02:20",
                                          "protocol": "bootstrap",
                                          "up_time": "03:29:13"
                                     },
                                     "ff08::/16 2001:db8:12:12::12 static": {
                                          "group": "ff08::/16",
                                          "rp_address": "2001:db8:12:12::12",
                                          "expiration": "0.000000",
                                          "protocol": "static",
                                          "up_time": "00:58:17"
                                     },
                                     "ff1e::3002/128 ff1e::3001/128 2001:db8:504::1 static": {
                                          "group": "ff1e::3002/128 ff1e::3001/128",
                                          "rp_address": "2001:db8:504::1",
                                          "expiration": "0.000000",
                                          "protocol": "static",
                                          "up_time": "00:00:02"
                                     }
                                },
                                "static_rp": {
                                     "2001:db8:111:111::111": {
                                          "sm": {
                                               "policy_name": "ff09::/16"
                                          }
                                     },
                                     "2001:db8:504::1": {
                                          "sm": {
                                               "route_map": "PIM6-STATIC-RP",
                                               "policy_name": "ff1e::3002/128 ff1e::3001/128"
                                          }
                                     },
                                     "2001:db8:12:12::12": {
                                          "bidir": {
                                               "policy_name": "ff08::/16"
                                          }
                                     }
                                },
                                "bsr": {
                                     "bsr_address": {
                                          "2001:db8:1:1::1": {
                                               "mode": "SM",
                                               "policy": "ff05::1/8",
                                               "priority": 192,
                                               "address": "2001:db8:1:1::1"
                                          }
                                     },
                                     "bsr": {
                                          "hash_mask_length": 128,
                                          "priority": 99,
                                          "address": "2001:db8:1:1::1"
                                     },
                                     "bsr_candidate": {
                                          "hash_mask_length": 128,
                                          "priority": 99,
                                          "address": "2001:db8:1:1::1"
                                     },
                                     "rp": {
                                          "rp_address": "2001:db8:1:1::1",
                                          "group_policy": "ff05::1/8",
                                          "up_time": "03:29:13"
                                     },
                                     "bsr_next_bootstrap": "00:00:15",
                                     "rp_candidate_next_advertisement": "00:02:20"
                                }
                           },
                           "sm": {
                                "asm": {
                                     "anycast_rp": {
                                          "2001:db8:111:111::111 2001:db8:3:4::5": {
                                               "anycast_address": "2001:db8:111:111::111"
                                          },
                                          "2001:db8:111:111::111 2001:db8:1:2::2": {
                                               "anycast_address": "2001:db8:111:111::111"
                                          }
                                     }
                                }
                           }
                      }
                 }
            }
       }
    }

    ShowIpPimDfVrfAll = {
        'vrf':{
            'default':
                {
                'address_family':
                    {'ipv4':
                        {
                        'rp':{
                            'bidir':{
                                'interface_df_election':{
                                    '10.16.2.2 Loopback0':{
                                        'address': '10.16.2.2',
                                        'interface_name': 'Loopback0',
                                        'df_bits': '00000002 (1)',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': '224.128.0.0/9',
                                        'df_address': '10.4.1.1',
                                        'interface_state': 'win',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '00:28:14',
                                        'df_ordinal': 2,

                                    },
                                    '10.16.2.2 Ethernet2/2': {
                                        'address': '10.16.2.2',
                                        'interface_name': 'Ethernet2/2',
                                        'df_bits': '00000002 (1)',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': '224.128.0.0/9',
                                        'df_address': '10.2.0.2',
                                        'interface_state': 'lose',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '00:28:14',
                                        'df_ordinal': 2,
                                        'is_rpf': True,

                                    },
                               },
                            },
                        },
                    },
                },
            },
            'VRF1':
                {
                'address_family':
                    {'ipv4':
                        {
                        'rp': {
                            'bidir': {
                                'interface_df_election': {
                                    '10.66.12.12 Loopback1': {
                                        'address': '10.66.12.12',
                                        'interface_name': 'Loopback1',
                                        'df_bits': '00000002 (1)',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': '224.128.0.0/9',
                                        'df_address': '10.4.1.1',
                                        'interface_state': 'win',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '02:28:14',
                                        'df_ordinal': 3,

                                    },
                                },
                            },
                        },
                    },
                },
            },
        },

    }

    ShowIpv6PimDfVrfAll = {
        'vrf':{
            'default':
                {
                'address_family':
                    {'ipv6':
                        {
                        'rp':{
                            'bidir':{
                                'interface_df_election':{
                                    '2001:db8:1:1::1 Ethernet2/1':{
                                        'address': '2001:db8:1:1::1',
                                        'interface_name': 'Ethernet2/1',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': 'ff09::/16',
                                        'df_address': 'fe80::5054:ff:fe89:740c',
                                        'interface_state': 'win',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '00:00:48',
                                        'df_ordinal': 8,

                                    },
                                    '2001:db8:1:1::1 Ethernet2/5': {
                                        'address': '2001:db8:1:1::1',
                                        'interface_name': 'Ethernet2/5',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': 'ff09::/16',
                                        'df_address': 'fe80::5054:ff:fe89:740c',
                                        'interface_state': 'win',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '00:00:48',
                                        'df_ordinal': 8,

                                    },
                                    '2001:db8:1:1::1 Loopback0': {
                                        'address': '2001:db8:1:1::1',
                                        'interface_name': 'Loopback0',
                                        'metric_pref': 0,
                                        'metric': 0,
                                        'group_range': 'ff09::/16',
                                        'df_address': '0::',
                                        'interface_state': 'lose',
                                        'winner_metric_pref': 0,
                                        'winner_metric': 0,
                                        'df_uptime': '00:00:48',
                                        'df_ordinal': 8,

                                    },
                                    '2001:db8:12:12::12 Ethernet2/1': {
                                        'address': '2001:db8:12:12::12',
                                        'interface_name': 'Ethernet2/1',
                                        'metric_pref': -1,
                                        'metric': -1,
                                        'group_range': 'ff08::/16',
                                        'df_address': '0::',
                                        'interface_state': 'lose',
                                        'winner_metric_pref': -1,
                                        'winner_metric': -1,
                                        'df_uptime': '00:01:27',
                                        'df_ordinal': 7,
                                    },
                                    '2001:db8:12:12::12 Ethernet2/5': {
                                        'address': '2001:db8:12:12::12',
                                        'interface_name': 'Ethernet2/5',
                                        'metric_pref': -1,
                                        'metric': -1,
                                        'group_range': 'ff08::/16',
                                        'df_address': '0::',
                                        'interface_state': 'lose',
                                        'winner_metric_pref': -1,
                                        'winner_metric': -1,
                                        'df_uptime': '00:01:27',
                                        'df_ordinal': 7,
                                    },
                                    '2001:db8:12:12::12 Loopback0': {
                                        'address': '2001:db8:12:12::12',
                                        'interface_name': 'Loopback0',
                                        'metric_pref': -1,
                                        'metric': -1,
                                        'group_range': 'ff08::/16',
                                        'df_address': '0::',
                                        'interface_state': 'lose',
                                        'winner_metric_pref': -1,
                                        'winner_metric': -1,
                                        'df_uptime': '00:01:27',
                                        'df_ordinal': 7,
                                    },

                               },
                            },
                        },
                    },
                },
            },
        },    
    }

    ShowIpPimVrfVallDetail = {
        'vrf':{
            'default':
                {
                'address_family':
                    {'ipv4':
                        {
                        'sm':{
                            'asm':{
                                'register_source': 'loopback0',
                                'register_source_address': '10.4.1.1',
                                'sg_expiry_timer': {
                                    'sg_list': 'sg-expiry-timer-sg-list',
                                    'infinity': True,
                                    'sg_expiry_timer_configured': True,
                                    'config_version': 1,
                                    'active_version': 1,
                                },
                            },
                        },
                        'vrf_id': 1,
                        'table_id': '0x00000001',
                        'interface_count': 3,
                        'bfd': {
                            'enable': False,
                        },
                        'mvpn': {
                            'enable': False,
                        },
                        'state_limit': 'none',
                        'register_rate_limit': 'none',
                        'pre_build_spt': 'disabled',
                        'cli_vrf_done': True,
                        'cibtype_auto_enabled': True,
                        'vxlan_vni_id': 0,
                        'shared_tree_ranges':'none',
                        },
                    },
                },
            'VRF1':
                {
                'address_family':
                    {'ipv4':
                        {
                        'sm': {
                            'asm': {
                                'register_source': 'loopback1',
                                'register_source_address': '10.229.11.11',
                                'sg_expiry_timer': {
                                    'sg_list': 'none',
                                    'sg_expiry_timer': 1200,
                                    'sg_expiry_timer_configured': True,
                                    'config_version': 1,
                                    'active_version': 1,
                                },
                            },
                        },
                        'vrf_id': 3,
                        'table_id': '0x00000003',
                        'interface_count': 3,
                        'bfd': {
                            'enable': False,
                        },
                        'mvpn': {
                            'enable': False,
                        },
                        'state_limit': 'none',
                        'register_rate_limit': 'none',

                        'pre_build_spt': 'disabled',
                        'cli_vrf_done': True,
                        'cibtype_auto_enabled': True,
                        'vxlan_vni_id': 0,
                        'shared_tree_ranges': 'none',
                    },
                },
            },
        },
    }

    ShowIpv6PimVrfAllDetail = {
        'vrf':{
            'default':
                {
                'address_family':
                    {'ipv6':
                        {
                        'vrf_id': 1,
                        'table_id': '0x80000001',
                        'interface_count': 3,
                        'bfd': {
                            'enable': False,
                        },

                        'state_limit': 'none',
                        'register_rate_limit': 'none',
                        'shared_tree_route_map':'v6spt-threshold-group-list',
                        },
                    },
                },
            'VRF1':
                {
                'address_family':
                    {'ipv6':
                        {
                        'vrf_id': 3,
                        'table_id': '0x80000003',
                        'interface_count': 3,
                        'bfd': {
                            'enable': False,
                        },

                        'state_limit': 'none',
                        'register_rate_limit': 'none',
                        'shared_tree_ranges': 'none',
                    },
                },
            },
        },
    }

    ShowIpPimGroupRangeVrfAll = {
        'vrf':{
            'VRF1':
                {
                'address_family':{
                    'ipv4':{
                        'sm':{
                            'ssm':{
                               '232.0.0.0/8':{
                                   'action': 'accept',
                                   'mode': 'ssm',
                                   'range': 'local',
                                },
                            },
                            'asm':{
                                '224.0.0.0/4': {
                                    'mode': 'asm',
                                    'rp_address': '10.21.33.33',
                                },
                            },
                        },
                    },
                },
            },
            'default':{
                'address_family': {
                    'ipv4': {
                        'sm': {
                            'ssm': {
                                '232.0.0.0/8': {
                                    'action': 'accept',
                                    'mode': 'ssm',
                                    'range': 'local',
                                },
                            },
                            'asm':{
                                '224.0.0.0/4': {
                                    'mode': 'asm',
                                    'rp_address': '10.16.2.2',
                                },
                                '224.0.0.0/5': {
                                    'mode': 'asm',
                                    'rp_address': '10.1.5.1',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    ShowIpv6PimGroupRangeVrfAll = {
        'vrf':{
            'default':
                {
                'address_family':{
                    'ipv6':{
                        'sm':{
                            'ssm':{
                               'ff3x::/32':{
                                   'mode': 'ssm',
                                    },
                                },
                            'asm':{
                                'ff05::1/8': {
                                'mode': 'asm',
                                'rp_address': '2001:db8:1:1::1',
                                    },
                                },
                            },
                        },
                    },
                },
            'VRF1':{
                'address_family': {
                    'ipv6': {
                        'sm': {
                            'ssm': {
                                'ff3x::/32': {
                                    'mode': 'ssm',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    ShowIpPimNeighborVrfAll = {
        'vrf':{
            'VRF1':
                {
                'interfaces':{
                    'Ethernet2/2':{
                        'address_family':{
                            'ipv4':{
                                'neighbors':{
                                   '10.11.33.33':{
                                       'bfd_status': False,
                                       'expiration': '00:01:25',
                                       'dr_priority': 1,
                                       'up_time': '07:31:30',
                                       'interface': 'Ethernet2/2',
                                       'bidir_capable': True,

                                    },
                                    '10.11.33.43': {
                                        'bfd_status': False,
                                        'expiration': '00:01:25',
                                        'dr_priority': 1,
                                        'up_time': '07:31:30',
                                        'interface': 'Ethernet2/2',
                                        'bidir_capable': True,

                                    },
                                },
                            },
                        },

                    },
                },
            },
        },
    }

    ShowIpv6PimNeighborVrfAll = {
        'vrf':{
            'VRF1':
                {
                'interfaces':{
                    'Ethernet2/2':{
                        'address_family':{
                            'ipv6':{
                                'neighbors':{
                                   'fe80::5054:ff:fe5b:aa80':{
                                       'bfd_status': False,
                                       'expiration': '00:01:28',
                                       'dr_priority': 1,
                                       'up_time': '07:31:36',
                                       'interface': 'Ethernet2/2',
                                       'bidir_capable': True,

                                    },
                                    'secondary_address':['2001:db8:11:33::33','2001:db8:1:3::3']
                                },
                            },
                        },

                    },
                },
            },
            'default':
                {
                    'interfaces': {
                        'Ethernet2/4': {
                            'address_family': {
                                'ipv6': {
                                    'neighbors': {
                                        'fe80::5054:ff:fec2:b74f': {
                                            'bfd_status': False,
                                            'expiration': '00:01:21',
                                            'dr_priority': 1,
                                            'up_time': '6d19h',
                                            'interface': 'Ethernet2/4',
                                            'bidir_capable': True,

                                        },
                                        'secondary_address': ['2001:10:1:2::2']
                                    },
                                },
                            },

                        },
                    },
                },
        },
    }

    ShowIpPimRouteVrfAll = {
        'vrf':{
            'VRF1':
                {
                'address_family':
                    {'ipv4':
                         {
                         'topology_tree_info': {
                                '232.0.0.0/8 * True': {
                                    'group': '232.0.0.0/8',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'expiration': '00:00:01',
                                    'incoming_interface': 'Null',
                                    'rpf_neighbor': '0.0.0.0',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'immediate': '00000000',
                                    'immediate_count': 0,
                                    'immediate_timeout_count': 0,
                                    'immediate_timeout': '00000000',
                                    'timeout_interval': 3,
                                    'sgr_prune_count': 0,
                                    'sgr_prune': '00000000',
                                },
                         },
                    },
                },
            },
            'default':
                {
                'address_family':
                    {'ipv4':
                         {
                         'topology_tree_info': {
                                '231.0.0.1/24 * True': {
                                    'group': '231.0.0.1/24',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'expiration': '00:00:01',
                                    'incoming_interface': 'Null0',
                                    'rpf_neighbor': '0.0.0.0',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'immediate': '00000000',
                                    'immediate_count': 0,
                                    'immediate_timeout_count': 0,
                                    'immediate_timeout': '00000000',
                                    'timeout_interval': 3,
                                    'sgr_prune_count': 0,
                                    'sgr_prune': '00000000',
                                    },
                                '233.0.0.0/24 * True': {
                                    'group': '233.0.0.0/24',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'rp_bit': True,
                                    'expiration': '00:01:58',
                                    'incoming_interface': 'Null',
                                    'rpf_neighbor': '0.0.0.0',
                                    'rp_address':'10.66.12.12',
                                    'mode':'bidir',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'timeout_interval': 2,
                                    },
                                '238.0.0.0/24 * True': {
                                    'group': '238.0.0.0/24',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'rp_bit': True,
                                    'mode': 'bidir',
                                    'expiration': '00:01:58',
                                    'incoming_interface': 'loopback0',
                                    'rpf_neighbor': '10.4.1.1',
                                    'rp_address': '10.4.1.1',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'timeout_interval': 2,
                             },
                         },
                    },
                },
            },
        },
    }

    ShowIpv6PimRouteVrfAll = {
        'vrf':{
            'VRF1':
                {
                'address_family':
                    {'ipv6':
                         {
                         'topology_tree_info': {
                                'ff30::/12 * True': {
                                    'group': 'ff30::/12',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'expiration': '00:00:27',
                                    'incoming_interface': 'Null',
                                    'rpf_neighbor': '0::',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'immediate': '00000000',
                                    'immediate_count': 0,
                                    'immediate_timeout_count': 0,
                                    'immediate_timeout': '00000000',
                                    'timeout_interval': 3,
                                    'route_fabric_owned': False,
                                },
                         },
                    },
                },
            },
            'default':
                {
                'address_family':
                    {'ipv6':
                         {
                         'topology_tree_info': {
                                'ff08::/16 * True': {
                                    'group': 'ff08::/16',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'rp_bit': True,
                                    'expiration': '00:02:31',
                                    'incoming_interface': 'Null',
                                    'rpf_neighbor': '0::',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'timeout_interval': 2,
                                    'mode': 'bidir',
                                    'rp_address': '2001:db8:12:12::12',
                                    'route_fabric_owned': False,
                                    },
                                'ff30::/12 * True': {
                                    'group': 'ff30::/12',
                                    'source_address': '*',
                                    'is_rpt': True,
                                    'expiration': '00:02:31',
                                    'incoming_interface': 'Null0',
                                    'rpf_neighbor': '0::',
                                    'jp_holdtime_roundup': 3,
                                    'oif': '00000000',
                                    'oif_count': 0,
                                    'oif_timeout_count': 0,
                                    'oif_timeout': '00000000',
                                    'timeout_interval': 3,
                                    'route_fabric_owned': False,
                                    'immediate': '00000000',
                                    'immediate_count': 0,
                                    'immediate_timeout_count': 0,
                                    'immediate_timeout': '00000000',
                                 },
                         },
                    },
                },
            },
        },
    }

    ShowIpMrouteVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'232.0.0.0/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'ip msdp pim',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'oil_count': 0,
                                        'uptime': '3d11h'}}},
                            '239.5.5.5/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp msdp '
                                                 'ip '
                                                 'pim',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'oil_count': 1,
                                        'outgoing_interface_list': 
                                            {'loopback1': 
                                                {'oil_flags': 'igmp',
                                                'oil_uptime': '3d11h'}},
                                        'uptime': '3d11h'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'233.0.0.0/24': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim msdp '
                                                  'ip',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'oil_count': 0,
                                        'uptime': '00:41:05'}}},
                            '238.0.0.0/24': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp '
                                                  'pim msdp '
                                                  'ip',
                                        'incoming_interface_list': 
                                            {'Ethernet9/13': 
                                                {'rpf_nbr': '10.2.3.2'}},
                                        'oil_count': 1,
                                        'outgoing_interface_list': 
                                            {'loopback2': 
                                                {'oil_flags': 'igmp',
                                                'oil_uptime': '3d11h'}},
                                        'uptime': '3d11h'}}}}}}}}}

    ShowIpv6MrouteVrfAll = {
        'vrf': 
            {
            'VRF1': 
                {'address_family': 
                    {'ipv6': 
                        {'multicast_group': 
                            {'ff30::/12': 
                                {'source_address': 
                                    {
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234, internal'}},
                                        'oil_count': '3',
                                        'uptime': '00:04:03'},
                                    '*': {'flags': 'ipv6 pim6 m6rib msdp',
                                           'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234, '
                                                                                                      'internal'}},
                                           'oil_count': '2',
                                           'outgoing_interface_list': {'Ethernet1/33.11': {'oif_rpf': True,
                                                                                           'oil_flags': 'm6rib',
                                                                                           'oil_uptime': '00:04:03'}},
                                           'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': {'flags': 'pim6 m6rib ipv6',
                                                               'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10, '
                                                                                                                       'internal'}},
                                                               'oil_count': '1',
                                                               'uptime': '00:04:03'},
                                    '2001::222:2:44:1234/128': {'flags': 'pim6 m6rib ipv6',
                                                                'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10, '
                                                                                                                        'internal'}},
                                                                'oil_count': '1',
                                                                'uptime': '00:04:03'}}},
                            'ff1e:2222:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'oil_count': '1',
                                        'uptime': '00:04:03'},
                                    '2001::222:2:44:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                                'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                                                'oil_count': '1',
                                                                'uptime': '00:04:02'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv6': 
                        {'multicast_group': 
                            {'ff30::/12': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim6 ipv6',
                                        'incoming_interface_list': {'Null': {'rpf_nbr': '0::'}},
                                        'oil_count': '0',
                                        'uptime': '00:11:23'}}}}}}}}}

    ShowIpPimPolicyStaticticsRegisterPolicyVrfAll = {
        'vrf': {
            'VRF1':
                {
                'address_family':
                    {'ipv4':{
                        'sm': {
                            'asm': {
                                'accept_register': 'pim_register_vrf',
                                'register_policy': {
                                    'pim_register_vrf': {
                                        'match ip multicast group 239.2.2.2/32': {
                                            'compare_count': 0,
                                            'match_count': 0,
                                            },
                                        'total_accept_count': 0,
                                        'total_reject_count': 0,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            'default':
                {
                'address_family':
                    {'ipv4':
                        {
                        'sm':{
                            'asm':{
                                'accept_register': 'pim_register_p',
                                'register_policy':{
                                    'pim_register_p':{
                                            'ip prefix-list pim_register_p seq 5 permit 239.3.3.3/32':{
                                                  'match_count':0,
                                            },
                                            'total_accept_count':0,
                                            'total_reject_count':0,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            }


    Pim_info = {
         "feature_pim": True,
         "feature_pim6": True,
         "vrf": {
              "VRF1": {
                   "address_family": {
                        "ipv4": {
                             "sm": {
                                  "ssm": {
                                       "232.0.0.0/8": {
                                            "action": "accept",
                                            "mode": "ssm",
                                            "range": "local"
                                       }
                                  },
                                  "asm": {
                                       "accept_register": "pim_register_vrf",
                                       "sg_expiry_timer": {
                                            "sg_list": "none"
                                       },
                                       "register_source": "loopback1"
                                  }
                             },
                             "topology_tree_info": {
                                  "232.0.0.0/8 * True": {
                                       "source_address": "*",
                                       "rpf_neighbor": "0.0.0.0",
                                       "msdp_learned": True,
                                       "is_rpt": True,
                                       "expiration": "00:00:01",
                                       "incoming_interface": "Null",
                                       "up_time": "3d11h",
                                       "group": "232.0.0.0/8"
                                  }
                             },
                             "bidir": True,
                             "rp": {
                                  "rp_mappings": {
                                       "226.0.0.0/8 192.168.64.2 autorp": {
                                            "up_time": "04:30:45",
                                            "expiration": "never",
                                            "protocol": "autorp",
                                            "group": "226.0.0.0/8",
                                            "rp_address": "192.168.64.2"
                                       },
                                       "224.0.0.0/4 10.21.33.33 static": {
                                            "up_time": "03:52:52",
                                            "expiration": "never",
                                            "protocol": "static",
                                            "group": "224.0.0.0/4",
                                            "rp_address": "10.21.33.33"
                                       }
                                  },
                                  "autorp": {
                                       "send_rp_announce": {
                                            "bidir": True,
                                            "scope": 0,
                                            "group_list": "226.0.0.0/8",
                                            "interface": "Ethernet2/3",
                                            "group": "226.0.0.0"
                                       },
                                       "send_rp_discovery": {
                                            "interface": "Ethernet2/2"
                                       }
                                  },
                                  "static_rp": {
                                       "10.21.33.33": {
                                            "sm": {
                                                 "policy_name": "224.0.0.0/4"
                                            }
                                       }
                                  },
                                  "rp_list": {
                                       "10.21.33.33 SM static": {
                                            "info_source_type": "static",
                                            "mode": "SM",
                                            "address": "10.21.33.33",
                                            "up_time": "03:52:52",
                                            "expiration": "never"
                                       },
                                       "192.168.64.2 BIDIR autorp": {
                                            "info_source_type": "autorp",
                                            "address": "192.168.64.2",
                                            "info_source_address": "192.168.64.2",
                                            "up_time": "04:30:45",
                                            "expiration": "never",
                                            "mode": "BIDIR"
                                       }
                                  }
                             }
                        },
                        "ipv6": {
                             "sm": {
                                  "ssm": {
                                       "ff3x::/32": {
                                            "mode": "ssm"
                                       }
                                  },
                                  "asm": {
                                       "anycast_rp": {
                                            "2001:db8:111:111::111 2001:db8:1:2::2": {
                                                 "anycast_address": "2001:db8:111:111::111"
                                            },
                                            "2001:db8:111:111::111 2001:db8:3:4::5": {
                                                 "anycast_address": "2001:db8:111:111::111"
                                            }
                                       }
                                  }
                             },
                             "topology_tree_info": {
                                  "ff30::/12 * True": {
                                       "source_address": "*",
                                       "outgoing_interface": {
                                            "Ethernet1/33.11": {
                                                 "up_time": "00:04:03"
                                            }
                                       },
                                       "rpf_neighbor": "0::",
                                       "msdp_learned": True,
                                       "is_rpt": True,
                                       "expiration": "00:00:27",
                                       "incoming_interface": "Null",
                                       "up_time": "00:04:03",
                                       "group": "ff30::/12"
                                  }
                             },
                             "rp": {
                                  "rp_mappings": {
                                       "ff05::1/8 2001:db8:1:1::1 bootstrap": {
                                            "up_time": "03:29:13",
                                            "expiration": "00:02:20",
                                            "protocol": "bootstrap",
                                            "group": "ff05::1/8",
                                            "rp_address": "2001:db8:1:1::1"
                                       }
                                  },
                                  "bsr": {
                                       "2001:db8:1:1::1": {
                                            "policy": "ff05::1/8",
                                            "mode": "SM",
                                            "address": "2001:db8:1:1::1",
                                            "priority": 192
                                       },
                                       "bsr_candidate": {
                                            "address": "2001:db8:1:1::1",
                                            "priority": 99,
                                            "hash_mask_length": 128
                                       },
                                       "rp_candidate_next_advertisement": "00:02:20",
                                       "bsr": {
                                            "expires": "00:01:37",
                                            "up_time": "00:09:14",
                                            "address": "2001:db8:1:1::1",
                                            "priority": 99,
                                            "hash_mask_length": 128
                                       },
                                       "rp": {
                                            "up_time": "03:29:13",
                                            "rp_address": "2001:db8:1:1::1",
                                            "group_policy": "ff05::1/8"
                                       }
                                  },
                                  "rp_list": {
                                       "2001:db8:1:1::1 SM bootstrap": {
                                            "info_source_type": "bootstrap",
                                            "address": "2001:db8:1:1::1",
                                            "info_source_address": "2001:db8:1:1::1",
                                            "up_time": "03:29:13",
                                            "expiration": "00:02:20",
                                            "mode": "SM"
                                       }
                                  }
                             }
                        }
                   },
                   "interfaces": {
                        "Ethernet2/2": {
                             "address_family": {
                                  "ipv4": {
                                       "jp_interval": 60,
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "10.11.33.11",
                                            "10.229.11.11"
                                       ],
                                       "neighbors": {
                                            "10.11.33.43": {
                                                 "dr_priority": 1,
                                                 "bfd_status": False,
                                                 "bidir_capable": True,
                                                 "up_time": "07:31:30",
                                                 "expiration": "00:01:25",
                                                 "interface": "Ethernet2/2",
                                                 "gen_id": "0x26fae674"
                                            },
                                            "10.11.33.33": {
                                                 "dr_priority": 1,
                                                 "bfd_status": False,
                                                 "bidir_capable": True,
                                                 "up_time": "07:31:30",
                                                 "expiration": "00:01:25",
                                                 "interface": "Ethernet2/2",
                                                 "gen_id": "0x26fae674"
                                            }
                                       },
                                       "oper_status": "up",
                                       "dr_priority": 144,
                                       "bsr_border": True,
                                       "neighbor_filter": "v4neighbor-policy",
                                       "dr_address": "10.11.33.11",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 45,
                                       "hello_expiration": "00:00:05"
                                  },
                                  "ipv6": {
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "2001:db8:11:33::11/64"
                                       ],
                                       "neighbors": {
                                            "fe80::5054:ff:fe5b:aa80": {
                                                 "dr_priority": 1,
                                                 "bfd_status": False,
                                                 "bidir_capable": True,
                                                 "up_time": "07:31:36",
                                                 "expiration": "00:01:28",
                                                 "interface": "Ethernet2/2",
                                                 "gen_id": "0x08f0f420"
                                            }
                                       },
                                       "oper_status": "up",
                                       "dr_priority": 166,
                                       "bsr_border": True,
                                       "neighbor_filter": "v6neighbor-policy",
                                       "dr_address": "fe80::5054:ff:fe89:740c",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 67,
                                       "hello_expiration": "00:00:34"
                                  }
                             }
                        },
                        "Ethernet2/3": {
                             "address_family": {
                                  "ipv4": {
                                       "jp_interval": 60,
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "10.11.66.11",
                                            "192.168.64.2"
                                       ],
                                       "oper_status": "up",
                                       "dr_priority": 1,
                                       "bsr_border": False,
                                       "genid": "0x2737c18b",
                                       "neighbor_filter": "none configured",
                                       "dr_address": "10.11.66.11",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 30,
                                       "hello_expiration": "00:00:14"
                                  }
                             }
                        }
                   }
              },
              "default": {
                   "address_family": {
                        "ipv4": {
                             "sm": {
                                  "ssm": {
                                       "232.0.0.0/8": {
                                            "action": "accept",
                                            "mode": "ssm",
                                            "range": "local"
                                       }
                                  },
                                  "asm": {
                                       "accept_register": "pim_register_p",
                                       "anycast_rp": {
                                            "10.111.111.111 10.1.2.1": {
                                                 "anycast_address": "10.111.111.111"
                                            },
                                            "10.111.111.111 10.1.5.1": {
                                                 "anycast_address": "10.111.111.111"
                                            }
                                       },
                                       "register_source": "loopback0",
                                       "sg_expiry_timer": {
                                            "infinity": True,
                                            "sg_list": "sg-expiry-timer-sg-list"
                                       }
                                  }
                             },
                             "topology_tree_info": {
                                  "238.0.0.0/24 * True": {
                                       "group": "238.0.0.0/24",
                                       "source_address": "*",
                                       "outgoing_interface": {
                                            "loopback2": {
                                                 "up_time": "3d11h"
                                            }
                                       },
                                       "rpf_neighbor": "10.4.1.1",
                                       "msdp_learned": True,
                                       "up_time": "3d11h",
                                       "expiration": "00:01:58",
                                       "incoming_interface": "loopback0",
                                       "is_rpt": True,
                                       "mode": "bidir",
                                       "rp_address": "10.4.1.1"
                                  },
                                  "233.0.0.0/24 * True": {
                                       "group": "233.0.0.0/24",
                                       "source_address": "*",
                                       "rp_address": "10.66.12.12",
                                       "rpf_neighbor": "0.0.0.0",
                                       "msdp_learned": True,
                                       "up_time": "00:41:05",
                                       "expiration": "00:01:58",
                                       "incoming_interface": "Null",
                                       "is_rpt": True,
                                       "mode": "bidir"
                                  },
                                  "231.0.0.1/24 * True": {
                                       "source_address": "*",
                                       "rpf_neighbor": "0.0.0.0",
                                       "is_rpt": True,
                                       "expiration": "00:00:01",
                                       "incoming_interface": "Null0",
                                       "group": "231.0.0.1/24"
                                  }
                             },
                             "bidir": True,
                             "rp": {
                                  "rp_mappings": {
                                       "224.0.0.0/4 10.16.2.2 static": {
                                            "up_time": "03:52:52",
                                            "expiration": "never",
                                            "protocol": "static",
                                            "group": "224.0.0.0/4",
                                            "rp_address": "10.16.2.2"
                                       },
                                       "224.0.0.0/5 10.1.5.1 bootstrap": {
                                            "up_time": "01:56:07",
                                            "expiration": "00:02:05",
                                            "protocol": "bootstrap",
                                            "group": "224.0.0.0/5",
                                            "rp_address": "10.1.5.1"
                                       },
                                       "224.0.0.0/4 10.111.111.111 static": {
                                            "up_time": "00:01:06",
                                            "expiration": "never",
                                            "protocol": "static",
                                            "group": "224.0.0.0/4",
                                            "rp_address": "10.111.111.111"
                                       },
                                       "233.0.0.0/24 10.66.12.12 static": {
                                            "up_time": "00:00:54",
                                            "expiration": "never",
                                            "protocol": "static",
                                            "group": "233.0.0.0/24",
                                            "rp_address": "10.66.12.12"
                                       }
                                  },
                                  "autorp": {
                                       "send_rp_discovery": {
                                            "interface": "Ethernet2/1"
                                       }
                                  },
                                  "static_rp": {
                                       "10.111.111.111": {
                                            "sm": {
                                                 "policy_name": "224.0.0.0/4"
                                            }
                                       },
                                       "10.16.2.2": {
                                            "sm": {
                                                 "policy_name": "224.0.0.0/4"
                                            }
                                       },
                                       "10.66.12.12": {
                                            "bidir": {
                                                 "policy_name": "233.0.0.0/24"
                                            }
                                       }
                                  },
                                  "bsr": {
                                       "bsr_next_bootstrap": "00:00:01",
                                       "bsr": {
                                            "address": "10.1.5.1",
                                            "priority": 111,
                                            "hash_mask_length": 30
                                       },
                                       "bsr_candidate": {
                                            "address": "10.1.5.1",
                                            "priority": 111,
                                            "hash_mask_length": 30
                                       },
                                       "rp_candidate_next_advertisement": "00:02:05",
                                       "10.1.5.1": {
                                            "policy": "224.0.0.0/5",
                                            "mode": "SM",
                                            "address": "10.1.5.1",
                                            "priority": 92
                                       },
                                       "rp": {
                                            "up_time": "01:56:07",
                                            "rp_address": "10.1.5.1",
                                            "group_policy": "224.0.0.0/5"
                                       }
                                  },
                                  "rp_list": {
                                       "10.66.12.12 BIDIR static": {
                                            "info_source_type": "static",
                                            "mode": "BIDIR",
                                            "address": "10.66.12.12",
                                            "up_time": "00:00:54",
                                            "expiration": "never"
                                       },
                                       "10.16.2.2 SM static": {
                                            "info_source_type": "static",
                                            "mode": "SM",
                                            "address": "10.16.2.2",
                                            "up_time": "03:52:52",
                                            "expiration": "never"
                                       },
                                       "10.111.111.111 SM static": {
                                            "info_source_type": "static",
                                            "mode": "SM",
                                            "address": "10.111.111.111",
                                            "up_time": "00:01:06",
                                            "expiration": "never"
                                       },
                                       "10.1.5.1 SM bootstrap": {
                                            "info_source_type": "bootstrap",
                                            "address": "10.1.5.1",
                                            "info_source_address": "10.1.5.1",
                                            "up_time": "01:56:07",
                                            "expiration": "00:02:05",
                                            "mode": "SM"
                                       }
                                  }
                             }
                        },
                        "ipv6": {
                             "sm": {
                                  "ssm": {
                                       "ff3x::/32": {
                                            "mode": "ssm"
                                       }
                                  },
                                  "asm": {
                                       "anycast_rp": {
                                            "2001:db8:111:111::111 2001:db8:1:2::2": {
                                                 "anycast_address": "2001:db8:111:111::111"
                                            },
                                            "2001:db8:111:111::111 2001:db8:3:4::5": {
                                                 "anycast_address": "2001:db8:111:111::111"
                                            }
                                       }
                                  }
                             },
                             "rp": {
                                  "rp_mappings": {
                                       "ff05::1/8 2001:db8:1:1::1 bootstrap": {
                                            "up_time": "03:29:13",
                                            "expiration": "00:02:20",
                                            "protocol": "bootstrap",
                                            "group": "ff05::1/8",
                                            "rp_address": "2001:db8:1:1::1"
                                       },
                                       "ff09::/16 2001:db8:111:111::111 static": {
                                            "up_time": "00:00:52",
                                            "expiration": "0.000000",
                                            "protocol": "static",
                                            "group": "ff09::/16",
                                            "rp_address": "2001:db8:111:111::111"
                                       },
                                       "ff1e::3002/128 ff1e::3001/128 2001:db8:504::1 static": {
                                            "up_time": "00:00:02",
                                            "expiration": "0.000000",
                                            "protocol": "static",
                                            "group": "ff1e::3002/128 ff1e::3001/128",
                                            "rp_address": "2001:db8:504::1"
                                       },
                                       "ff08::/16 2001:db8:12:12::12 static": {
                                            "up_time": "00:58:17",
                                            "expiration": "0.000000",
                                            "protocol": "static",
                                            "group": "ff08::/16",
                                            "rp_address": "2001:db8:12:12::12"
                                       }
                                  },
                                  "bsr": {
                                       "bsr_next_bootstrap": "00:00:15",
                                       "bsr": {
                                            "address": "2001:db8:1:1::1",
                                            "priority": 99,
                                            "hash_mask_length": 128
                                       },
                                       "2001:db8:1:1::1": {
                                            "policy": "ff05::1/8",
                                            "mode": "SM",
                                            "address": "2001:db8:1:1::1",
                                            "priority": 192
                                       },
                                       "bsr_candidate": {
                                            "address": "2001:db8:1:1::1",
                                            "priority": 99,
                                            "hash_mask_length": 128
                                       },
                                       "rp_candidate_next_advertisement": "00:02:20",
                                       "rp": {
                                            "up_time": "03:29:13",
                                            "rp_address": "2001:db8:1:1::1",
                                            "group_policy": "ff05::1/8"
                                       }
                                  },
                                  "static_rp": {
                                       "2001:db8:504::1": {
                                            "sm": {
                                                 "policy_name": "ff1e::3002/128 ff1e::3001/128",
                                                 "route_map": "PIM6-STATIC-RP"
                                            }
                                       },
                                       "2001:db8:12:12::12": {
                                            "bidir": {
                                                 "policy_name": "ff08::/16"
                                            }
                                       },
                                       "2001:db8:111:111::111": {
                                            "sm": {
                                                 "policy_name": "ff09::/16"
                                            }
                                       }
                                  },
                                  "bidir": {
                                       "interface_df_election": {
                                            "2001:db8:12:12::12 Ethernet2/5": {
                                                 "interface_name": "Ethernet2/5",
                                                 "address": "2001:db8:12:12::12",
                                                 "interface_state": "lose",
                                                 "df_address": "0::"
                                            },
                                            "2001:db8:1:1::1 Ethernet2/1": {
                                                 "interface_name": "Ethernet2/1",
                                                 "address": "2001:db8:1:1::1",
                                                 "interface_state": "win",
                                                 "df_address": "fe80::5054:ff:fe89:740c"
                                            },
                                            "2001:db8:12:12::12 Ethernet2/1": {
                                                 "interface_name": "Ethernet2/1",
                                                 "address": "2001:db8:12:12::12",
                                                 "interface_state": "lose",
                                                 "df_address": "0::"
                                            },
                                            "2001:db8:1:1::1 Ethernet2/5": {
                                                 "interface_name": "Ethernet2/5",
                                                 "address": "2001:db8:1:1::1",
                                                 "interface_state": "win",
                                                 "df_address": "fe80::5054:ff:fe89:740c"
                                            },
                                            "2001:db8:12:12::12 Loopback0": {
                                                 "interface_name": "Loopback0",
                                                 "address": "2001:db8:12:12::12",
                                                 "interface_state": "lose",
                                                 "df_address": "0::"
                                            },
                                            "2001:db8:1:1::1 Loopback0": {
                                                 "interface_name": "Loopback0",
                                                 "address": "2001:db8:1:1::1",
                                                 "interface_state": "lose",
                                                 "df_address": "0::"
                                            }
                                       }
                                  },
                                  "rp_list": {
                                       "2001:db8:12:12::12 BIDIR static": {
                                            "info_source_type": "static",
                                            "mode": "BIDIR",
                                            "address": "2001:db8:12:12::12",
                                            "up_time": "00:58:17",
                                            "expiration": "0.000000"
                                       },
                                       "2001:db8:504::1 SM static": {
                                            "info_source_type": "static",
                                            "mode": "SM",
                                            "address": "2001:db8:504::1",
                                            "up_time": "00:00:02",
                                            "expiration": "0.000000"
                                       },
                                       "2001:db8:111:111::111 SM static": {
                                            "info_source_type": "static",
                                            "mode": "SM",
                                            "address": "2001:db8:111:111::111",
                                            "up_time": "00:00:52",
                                            "expiration": "0.000000"
                                       },
                                       "2001:db8:1:1::1 SM bootstrap": {
                                            "info_source_type": "bootstrap",
                                            "address": "2001:db8:1:1::1",
                                            "info_source_address": "2001:db8:1:1::1",
                                            "up_time": "03:29:13",
                                            "expiration": "00:02:20",
                                            "mode": "SM"
                                       }
                                  }
                             },
                             "topology_tree_info": {
                                  "ff30::/12 * True": {
                                       "source_address": "*",
                                       "rpf_neighbor": "0::",
                                       "msdp_learned": False,
                                       "is_rpt": True,
                                       "expiration": "00:02:31",
                                       "incoming_interface": "Null0",
                                       "up_time": "00:11:23",
                                       "group": "ff30::/12"
                                  },
                                  "ff08::/16 * True": {
                                       "source_address": "*",
                                       "rp_address": "2001:db8:12:12::12",
                                       "rpf_neighbor": "0::",
                                       "is_rpt": True,
                                       "expiration": "00:02:31",
                                       "incoming_interface": "Null",
                                       "mode": "bidir",
                                       "group": "ff08::/16"
                                  }
                             },
                             "bidir": True
                        }
                   },
                   "interfaces": {
                        "Ethernet2/1": {
                             "address_family": {
                                  "ipv4": {
                                       "jp_interval": 60,
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "10.1.5.1"
                                       ],
                                       "oper_status": "up",
                                       "dr_priority": 1,
                                       "bsr_border": False,
                                       "genid": "0x3148ed16",
                                       "neighbor_filter": "none configured",
                                       "dr_address": "10.1.5.1",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 30,
                                       "hello_expiration": "00:00:13"
                                  },
                                  "ipv6": {
                                       "dr_priority": 1,
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "2001:db8:1:5::1/64"
                                       ],
                                       "oper_status": "up",
                                       "genid": "0x25f72e3c",
                                       "bsr_border": False,
                                       "neighbor_filter": "none configured",
                                       "dr_address": "fe80::5054:ff:fe89:740c",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 30,
                                       "hello_expiration": "00:00:13"
                                  }
                             }
                        },
                        "Ethernet2/4": {
                             "address_family": {
                                  "ipv6": {
                                       "bfd": {
                                            "enable": False
                                       },
                                       "address": [
                                            "2001:db8:1:2::1/64",
                                            "2001:db8:1:2::2/64"
                                       ],
                                       "neighbors": {
                                            "fe80::5054:ff:fec2:b74f": {
                                                 "dr_priority": 1,
                                                 "bfd_status": False,
                                                 "bidir_capable": True,
                                                 "up_time": "6d19h",
                                                 "expiration": "00:01:21",
                                                 "interface": "Ethernet2/4",
                                                 "gen_id": "0x30a2ad71"
                                            }
                                       },
                                       "oper_status": "up",
                                       "dr_priority": 1,
                                       "bsr_border": False,
                                       "neighbor_filter": "none configured",
                                       "dr_address": "fe80::5054:ff:fe89:740c",
                                       "sm": {
                                            "passive": False
                                       },
                                       "hello_interval": 30,
                                       "hello_expiration": "00:00:07"
                                  }
                             }
                        }
                   }
              }
         }
    }
