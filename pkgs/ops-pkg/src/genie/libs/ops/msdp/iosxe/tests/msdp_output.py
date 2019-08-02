'''
MSDP Genie Ops Object Outputs for IOSXE

'''

class MsdpOutput(object):

    # 'show ip msdp peer'
    ShowIpMsdpPeer =   {
        'vrf': {
            'default': {
                'peer': {
                    '10.1.100.4': {
                        'session_state': 'Up',
                        'peer_as': 1,
                        'resets': '0',
                        'connect_source': 'Loopback0',
                        'connect_source_address': '10.1.100.2',
                        'elapsed_time': '00:41:18',
                        'statistics': {
                            'queue': {
                                'size_in': 0,
                                'size_out': 0
                            },
                            'sent': {
                                'data_message': 42,
                                'sa_message': 0,
                                'sa_response': 0,
                                'data_packets': 0
                            },
                            'received': {
                                'data_message': 50,
                                'sa_message': 27,
                                'sa_request': 0,
                                'data_packets': 6
                            },
                            'established_transitions': 1,
                            'output_msg_discarded': 0,
                            'error': {
                                'rpf_failure': 27
                            }
                        },
                        'conn_count_cleared': '00:43:22',
                        'sa_filter': {
                            'in': {
                                '(S,G)': {
                                    'filter': 'none',
                                    'route_map': 'none'
                                },
                                'RP': {
                                    'filter': 'none',
                                    'route_map': 'none'
                                }
                            },
                            'out': {
                                '(S,G)': {
                                    'filter': 'none',
                                    'route_map': 'none'
                                },
                                'RP': {
                                    'filter': 'none',
                                    'route_map': 'none'
                                }
                            }
                        },
                        'sa_request': {
                            'input_filter': 'none'
                        },
                        'ttl_threshold': 0,
                        'sa_learned_from': 0,
                        'signature_protection': False}}}}}

    # 'show ip msdp sa-cache'
    ShowIpMsdpSaCache =  {
        'vrf': {
            'default': {
                'num_of_sa_cache': 1,
                'sa_cache': {
                    '225.1.1.1 10.3.3.18': {
                        'group': '225.1.1.1',
                        'source_addr': '10.3.3.18',
                        'up_time': '00:00:10',
                        'expire': '00:05:49',
                        'peer_as': 3,
                        'peer': '10.1.100.4',
                        'origin_rp': {
                            '10.3.100.8': {
                                'rp_address': '10.3.100.8'}},
                        'peer_learned_from': '10.1.100.4',
                        'rpf_peer': '10.1.100.4',
                        'statistics': {
                            'received': {
                                'sa': 1,
                                'encapsulated_data_received': 1}}}}}}}

    MsdpInfo = {
        'vrf': {
            'default': {
                'peer': {
                    '10.1.100.4': {
                        'connect_source': 'Loopback0',
                        'elapsed_time': '00:41:18',
                        'peer_as': 1,
                        'session_state': 'established',
                        'statistics': {
                            'error': {
                                'rpf_failure': 27},
                            'queue': {
                                'size_in': 0,
                                'size_out': 0},
                            'received': {
                                'sa_message': 27,
                                'sa_request': 0},
                            'sent': {
                                'sa_message': 0,
                                'sa_response': 0}},
                        'ttl_threshold': 0}},
                'sa_cache': {
                    '225.1.1.1 10.3.3.18': {
                        'expire': '00:05:49',
                        'group': '225.1.1.1',
                        'origin_rp': {
                            '10.3.100.8': {
                                'rp_address': '10.3.100.8'}},
                        'peer_learned_from': '10.1.100.4',
                        'rpf_peer': '10.1.100.4',
                        'source_addr': '10.3.3.18',
                        'up_time': '00:00:10'}}}}}
