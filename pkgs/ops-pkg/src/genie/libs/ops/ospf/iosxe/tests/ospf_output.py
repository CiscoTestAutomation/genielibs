''' 
OSPF Genie Ops Object Outputs for IOSXE.
'''


class OspfOutput(object):

    ############################################################################
    #                           OSPF INFO OUTPUTS
    ############################################################################

    # 'show ip protocols'
    ShowIpProtocols = {
        'protocols': 
            {'application': 
                {'flushed': 0,
                'holddown': 0,
                'incoming_filter_list': 'not set',
                'invalid': 0,
                'maximum_path': 32,
                'outgoing_filter_list': 'not set',
                'preference': 
                    {'single_value': 
                        {'all': 4}},
                'update_frequency': 0},
            'bgp': 
                {'instance': 
                    {'default': 
                        {'bgp_id': 100,
                        'vrf': 
                            {'default': 
                                {'address_family': 
                                    {'ipv4': 
                                        {'automatic_route_summarization': False,
                                        'igp_sync': False,
                                        'incoming_filter_list': 'not set',
                                        'maximum_path': 1,
                                        'neighbor': 
                                            {'10.64.4.4': 
                                                {'distance': 200,
                                                'last_update': '03:34:58',
                                                'neighbor_id': '10.64.4.4'}},
                                        'outgoing_filter_list': 'not set',
                                        'preference': 
                                            {'multi_values': 
                                                {'external': 20,
                                                'internal': 200,
                                                'local': 200}}}}}}}}},
            'ospf': 
                {'vrf': 
                    {'default': 
                        {'address_family': 
                            {'ipv4': 
                                {'instance': 
                                    {'1': 
                                        {'areas': 
                                            {'0.0.0.0': 
                                                {'configured_interfaces': ['Loopback0', 'GigabitEthernet2', 'GigabitEthernet1']}},
                                        'incoming_filter_list': 'not set',
                                        'outgoing_filter_list': 'not set',
                                        'preference': 
                                            {'multi_values': 
                                                {'external': 114,
                                                'granularity': 
                                                    {'detail': 
                                                        {'inter_area': 113,
                                                        'intra_area': 112}}},
                                            'single_value': 
                                                {'all': 110}},
                                        'router_id': '10.4.1.1',
                                        'routing_information_sources': 
                                            {'gateway': 
                                                {'10.16.2.2': 
                                                    {'distance': 110,
                                                    'last_update': '07:33:00'},
                                                '10.36.3.3': 
                                                    {'distance': 110,
                                                    'last_update': '07:33:00'},
                                                '10.64.4.4': 
                                                    {'distance': 110,
                                                    'last_update': '00:19:15'}}},
                                        'spf_control': 
                                            {'paths': 4},
                                        'total_areas': 1,
                                        'total_normal_area': 1,
                                        'total_nssa_area': 0,
                                        'total_stub_area': 0}}}}}}}}}

    # 'show ip ospf'
    ShowIpOspf = {
        'vrf': 
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'2': 
                                {'adjacency_stagger': 
                                    {'initial_number': 300,
                                     'maximum_number': 300},
                                'area_transit': True,
                                'areas': 
                                    {'0.0.0.1': 
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'normal',
                                        'authentication': False,
                                        'ranges': 
                                            {'10.4.1.0/24': 
                                                {'advertise': True,
                                                'prefix': '10.4.1.0/24'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x053FED',
                                            'area_scope_lsa_count': 11,
                                            'area_scope_opaque_lsa_cksum_sum': '0x000000',
                                            'area_scope_opaque_lsa_count': 0,
                                            'dcbitless_lsa_count': 1,
                                            'donotage_lsa_count': 0,
                                            'flood_list_length': 0,
                                            'indication_lsa_count': 0,
                                            'interfaces_count': 2,
                                            'spf_last_executed': '03:26:37.769',
                                            'spf_runs_count': 97}}},
                                'auto_cost': 
                                    {'bandwidth_unit': 'mbps',
                                    'enable': False,
                                    'reference_bandwidth': 100},
                                'bfd': 
                                    {'enable': True},
                                'db_exchange_summary_list_optimization': True,
                                'domain_id_type': '0x0005',
                                'domain_id_value': '0.0.0.2',
                                'elapsed_time': '23:34:42.224',
                                'external_flood_list_length': 0,
                                'flags': 
                                    {'abr': True,
                                    'asbr': True},
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': False,
                                        'helper_enable': True,
                                        'type': 'cisco'},
                                    'ietf': 
                                        {'enable': False,
                                        'helper_enable': True,
                                        'type': 'ietf'}},
                                'incremental_spf': False,
                                'lls': True,
                                'lsa_group_pacing_timer': 240,
                                'nsr': 
                                    {'enable': True},
                                'nssa': True,
                                'numbers': 
                                    {'dc_bitless': 0,
                                    'do_not_age': 0,
                                    'external_lsa': 0,
                                    'external_lsa_checksum': '0x000000',
                                    'opaque_as_lsa': 0,
                                    'opaque_as_lsa_checksum': '0x000000'},
                                'opqaue_lsa': True,
                                'redistribution': 
                                    {'bgp': 
                                        {'bgp_id': 100,
                                        'subnets': 'subnets'
                                        }},
                                'retransmission_pacing_timer': 66,
                                'router_id': '10.229.11.11',
                                'spf_control': 
                                    {'throttle': 
                                        {'lsa': 
                                            {'arrival': 100,
                                            'hold': 200,
                                            'maximum': 5000,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'start_time': '02:17:25.010',
                                'stub_router': 
                                    {'always': 
                                        {'always': False,
                                        'external_lsa': False,
                                        'include_stub': False,
                                        'summary_lsa': False}},
                                'total_areas': 1,
                                'total_areas_transit_capable': 0,
                                'total_normal_areas': 1,
                                'total_nssa_areas': 0,
                                'total_stub_areas': 0}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'adjacency_stagger': 
                                    {'initial_number': 300,
                                    'maximum_number': 300},
                                'area_transit': True,
                                'areas': 
                                    {'0.0.0.0': 
                                        {'area_id': '0.0.0.0',
                                        'area_type': 'normal',
                                        'authentication': False,
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': True,
                                                'cost': 10,
                                                'prefix': '10.4.0.0/16'}},
                                        'rrr_enabled': True,
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x07CF20',
                                            'area_scope_lsa_count': 19,
                                            'area_scope_opaque_lsa_cksum_sum': '0x000000',
                                            'area_scope_opaque_lsa_count': 0,
                                            'dcbitless_lsa_count': 5,
                                            'donotage_lsa_count': 0,
                                            'flood_list_length': 0,
                                            'indication_lsa_count': 0,
                                            'interfaces_count': 3,
                                            'loopback_count': 1,
                                            'spf_last_executed': '00:19:54.849',
                                            'spf_runs_count': 41}}},
                                'auto_cost': 
                                    {'bandwidth_unit': 'mbps',
                                    'enable': False,
                                    'reference_bandwidth': 100},
                                'bfd': 
                                    {'enable': True,
                                    'strict_mode': True},
                                'database_control': 
                                    {'max_lsa': 123},
                                'db_exchange_summary_list_optimization': True,
                                'elapsed_time': '1d01h',
                                'event_log': 
                                    {'enable': True,
                                    'max_events': 1000,
                                    'mode': 'cyclic'},
                                'external_flood_list_length': 0,
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': False,
                                        'helper_enable': True,
                                        'type': 'cisco'},
                                    'ietf': 
                                        {'enable': False,
                                        'helper_enable': True,
                                        'type': 'ietf'}},
                                'incremental_spf': False,
                                'lls': True,
                                'lsa_group_pacing_timer': 240,
                                'nsr': 
                                    {'enable': False},
                                'nssa': True,
                                'numbers': 
                                    {'dc_bitless': 0,
                                    'do_not_age': 0,
                                    'external_lsa': 1,
                                    'external_lsa_checksum': '0x007F60',
                                    'opaque_as_lsa': 0,
                                    'opaque_as_lsa_checksum': '0x000000'},
                                'opqaue_lsa': True,
                                'retransmission_pacing_timer': 66,
                                'router_id': '10.4.1.1',
                                'spf_control': 
                                    {'throttle': 
                                        {'lsa': 
                                            {'arrival': 100,
                                            'hold': 200,
                                            'maximum': 5000,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'start_time': '00:23:49.050',
                                'stub_router': 
                                    {'always': 
                                        {'always': False,
                                        'external_lsa': False,
                                        'include_stub': False,
                                        'summary_lsa': False}},
                                'total_areas': 1,
                                'total_areas_transit_capable': 0,
                                'total_normal_areas': 1,
                                'total_nssa_areas': 0,
                                'total_stub_areas': 0}}}}}}}

    # 'show ip ospf interface'
    ShowIpOspfInterface = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces': 
                                            {'GigabitEthernet3': 
                                                {'attached': 'interface enable',
                                                'bdr_ip_addr': '10.186.5.5',
                                                'bdr_router_id': '10.115.55.55',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.186.5.1',
                                                'dr_router_id': '10.229.11.11',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'frr_enabled': True,
                                                'frr_protected': True,
                                                'graceful_restart': 
                                                    {'cisco': 
                                                        {'helper': True,
                                                        'type': 'cisco'},
                                                    'ietf': 
                                                        {'helper': True,
                                                        'type': 'ietf'}},
                                                'lls': True,
                                                'oob_resync_timeout': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'if_cfg': True,
                                                'index': '1/1/1',
                                                'interface_id': 9,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.186.5.1/24',
                                                'last_flood_scan_length': 0,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'max_flood_scan_length': 7,
                                                'max_flood_scan_time_msec': 1,
                                                'name': 'GigabitEthernet3',
                                                'neighbors': 
                                                    {'10.115.55.55': 
                                                        {'bdr_router_id': '10.115.55.55'}},
                                                'next': '0x0(0)/0x0(0)/0x0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'router_id': '10.229.11.11',
                                                'state': 'dr',
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0},
                                                'ti_lfa_protected': False,
                                                'ttl_security': 
                                                    {'enable': True,
                                                    'hops': 30},
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}},
                                        'sham_links': 
                                            {'10.229.11.11 10.151.22.22': 
                                                {'attached': 'not attached',
                                                'bfd': 
                                                    {'enable': False},
                                                'bdr_ip_addr': '10.186.7.7',
                                                'bdr_router_id': '10.246.57.57',
                                                'cost': 111,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'dr_ip_addr': '10.1.2.2',
                                                'dr_router_id': '10.229.11.11',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'graceful_restart': 
                                                    {'cisco': 
                                                        {'helper': True,
                                                        'type': 'cisco'},
                                                    'ietf': 
                                                        {'helper': True,
                                                        'type': 'ietf'}},
                                                'lls': True,
                                                'oob_resync_timeout': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'index': '1/2/2',
                                                'interface_id': 14,
                                                'interface_type': 'sham-link',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'max_flood_scan_length': 5,
                                                'max_flood_scan_time_msec': 1,
                                                'name': 'SL0',
                                                'next': '0x0(0)/0x0(0)/0x0(0)',
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'router_id': '10.229.11.11',
                                                'state': 'point-to-point',
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0},
                                                'ti_lfa_protected': False,
                                                'ttl_security': 
                                                    {'enable': True,
                                                    'hops': 3},
                                                'topology': 
                                                    {0: 
                                                        {'cost': 111,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}},
                                        'virtual_links': 
                                            {'0.0.0.1 10.36.3.3': 
                                                {'attached': 'not attached',
                                                'bfd': 
                                                    {'enable': False},
                                                'bdr_ip_addr': '10.196.6.6',
                                                'bdr_router_id': '10.49.56.56',
                                                'cost': 1,
                                                'dead_interval': 44,
                                                'demand_circuit': True,
                                                'dr_ip_addr': '10.1.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'graceful_restart': 
                                                    {'cisco': 
                                                        {'helper': True,
                                                        'type': 'cisco'},
                                                    'ietf': 
                                                        {'helper': True,
                                                        'type': 'ietf'}},
                                                'hello_interval': 4,
                                                'hello_timer': '00:00:02',
                                                'index': '2/6',
                                                'interface_type': 'virtual-link',
                                                'ip_address': '10.19.4.4/24',
                                                'last_flood_scan_length': 2,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'lls': True,
                                                'max_flood_scan_length': 8,
                                                'max_flood_scan_time_msec': 0,
                                                'name': 'VL0',
                                                'next': '0x0(0)/0x0(0)',
                                                'oob_resync_timeout': 44,
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0},
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'interfaces': 
                                            {'GigabitEthernet1': 
                                                {'attached': 'interface enable',
                                                'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'md5',
                                                        'youngest_key_id': 2}},
                                                'bdr_ip_addr': '10.1.4.1',
                                                'bdr_router_id': '10.4.1.1',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.1.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'frr_enabled': True,
                                                'frr_protected': True,
                                                'graceful_restart': 
                                                    {'cisco': 
                                                        {'helper': True,
                                                        'type': 'cisco'},
                                                    'ietf': 
                                                        {'helper': True,
                                                        'type': 'ietf'}},
                                                'lls': True,
                                                'oob_resync_timeout': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'if_cfg': True,
                                                'index': '1/2/2',
                                                'interface_id': 7,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.1.4.1/24',
                                                'last_flood_scan_length': 3,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'max_flood_scan_length': 3,
                                                'max_flood_scan_time_msec': 1,
                                                'name': 'GigabitEthernet1',
                                                'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'dr_router_id': '10.64.4.4'}},
                                                'next': '0x0(0)/0x0(0)/0x0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'router_id': '10.4.1.1',
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0},
                                                'ti_lfa_protected': False,
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            'GigabitEthernet2': 
                                                {'attached': 'interface enable',
                                                'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'simple'}},
                                                'bdr_ip_addr': '10.1.2.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.1.2.1',
                                                'dr_router_id': '10.4.1.1',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'frr_enabled': True,
                                                'frr_protected': True,
                                                'graceful_restart': 
                                                    {'cisco': 
                                                        {'helper': True,
                                                        'type': 'cisco'},
                                                    'ietf': 
                                                        {'helper': True,
                                                        'type': 'ietf'}},
                                                'lls': True,
                                                'oob_resync_timeout': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:05',
                                                'if_cfg': True,
                                                'index': '1/3/3',
                                                'interface_id': 8,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.1.2.1/24',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'max_flood_scan_length': 3,
                                                'max_flood_scan_time_msec': 1,
                                                'name': 'GigabitEthernet2',
                                                'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'bdr_router_id': '10.16.2.2'}},
                                                'next': '0x0(0)/0x0(0)/0x0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'router_id': '10.4.1.1',
                                                'state': 'dr',
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0},
                                                'ti_lfa_protected': False,
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            'Loopback0': 
                                                {'attached': 'interface enable',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'demand_circuit': False,
                                                'enable': True,
                                                'if_cfg': True,
                                                'interface_id': 11,
                                                'interface_type': 'loopback',
                                                'ip_address': '10.4.1.1/32',
                                                'line_protocol': True,
                                                'name': 'Loopback0',
                                                'router_id': '10.4.1.1',
                                                'stub_host': True,
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}}}}}}}}}}}}}
    ShowIpOspfInterface_custom = {
        'vrf':{
             'default':
                 {'address_family':
                      {'ipv4':
                           {'instance':
                                {'1':
                                     {'areas':
                                          {'0.0.0.0':
                                               {'interfaces':
                                                    {'GigabitEthernet1':
                                                         {'attached': 'interface enable',
                                                          'authentication':
                                                              {'auth_trailer_key':
                                                                   {
                                                                       'crypto_algorithm': 'md5',
                                                                       'youngest_key_id': 2}},
                                                          'bdr_ip_addr': '10.1.4.1',
                                                          'bdr_router_id': '10.4.1.1',
                                                          'bfd':
                                                              {'enable': False},
                                                          'cost': 1,
                                                          'dead_interval': 40,
                                                          'demand_circuit': False,
                                                          'dr_ip_addr': '10.1.4.4',
                                                          'dr_router_id': '10.64.4.4',
                                                          'enable': True,
                                                          'flood_queue_length': 0,
                                                          'frr_enabled': True,
                                                          'frr_protected': True,
                                                          'graceful_restart':
                                                              {'cisco':
                                                                   {'helper': True,
                                                                    'type': 'cisco'},
                                                               'ietf':
                                                                   {'helper': True,
                                                                    'type': 'ietf'}},
                                                          'lls': True,
                                                          'oob_resync_timeout': 40,
                                                          'hello_interval': 10,
                                                          'hello_timer': '00:00:08',
                                                          'if_cfg': True,
                                                          'index': '1/2/2',
                                                          'interface_id': 7,
                                                          'interface_type': 'broadcast',
                                                          'ip_address': '10.1.4.1/24',
                                                          'last_flood_scan_length': 3,
                                                          'last_flood_scan_time_msec': 0,
                                                          'line_protocol': True,
                                                          'max_flood_scan_length': 3,
                                                          'max_flood_scan_time_msec': 1,
                                                          'name': 'GigabitEthernet1',
                                                          'neighbors':
                                                              {'10.64.4.4':
                                                                   {
                                                                       'dr_router_id':
                                                                           '10.64.4.4'}},
                                                          'next': '0x0(0)/0x0(0)/0x0(0)',
                                                          'passive': False,
                                                          'priority': 1,
                                                          'retransmit_interval': 5,
                                                          'router_id': '10.4.1.1',
                                                          'state': 'bdr',
                                                          'statistics':
                                                              {'adj_nbr_count': 1,
                                                               'nbr_count': 1,
                                                               'num_nbrs_suppress_hello': 0},
                                                          'ti_lfa_protected': False,
                                                          'topology':
                                                              {0:
                                                                   {'cost': 1,
                                                                    'disabled': False,
                                                                    'name': 'Base',
                                                                    'shutdown': False}},
                                                          'transmit_delay': 1,
                                                          'wait_interval': 40},}}}}}}}}}}

    # 'show ip ospf neighbor detail'
    ShowIpOspfNeighborDetail = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces': 
                                            {'GigabitEthernet3': 
                                                {'neighbors': 
                                                    {'10.115.55.55': 
                                                        {'address': '10.186.5.5',
                                                        'bdr_ip_addr': '10.186.5.5',
                                                        'dead_timer': '00:00:34',
                                                        'dr_ip_addr': '10.186.5.1',
                                                        'first': '0x0(0)/0x0(0)/0x0(0)',
                                                        'index': '1/1/1,',
                                                        'interface': 'GigabitEthernet3',
                                                        'neighbor_router_id': '10.115.55.55',
                                                        'neighbor_uptime': '15:47:14',
                                                        'next': '0x0(0)/0x0(0)/0x0(0)',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'last_retrans_max_scan_length': 6,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 1,
                                                            'last_retrans_scan_time_msec': 0,
                                                            'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 6}}}}},
                                        'virtual_links': 
                                            {'0.0.0.1 10.36.3.3': 
                                                {'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'address': '10.229.3.3',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:41',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'first': '0x0(0)/0x0(0)',
                                                        'hello_options': '0x2',
                                                        'index': '1/3,',
                                                        'interface': 'OSPF_VL1',
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'neighbor_uptime': '05:07:21',
                                                        'next': '0x0(0)/0x0(0)',
                                                        'priority': 0,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'last_retrans_max_scan_length': 1,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 1,
                                                            'last_retrans_scan_time_msec': 0,
                                                            'nbr_event_count': 12,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 3}}}}},
                                        'sham_links': 
                                            {'10.229.11.11 10.151.22.22': 
                                                {'neighbors': 
                                                    {'10.151.22.22': 
                                                        {'address': '10.151.22.22',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'first': '0x0(0)/0x0(0)/0x0(0)',
                                                        'hello_options': '0x2',
                                                        'index': '1/2/2,',
                                                        'interface': 'OSPF_SL1',
                                                        'neighbor_router_id': '10.151.22.22',
                                                        'neighbor_uptime': '07:41:59',
                                                        'next': '0x0(0)/0x0(0)/0x0(0)',
                                                        'priority': 0,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'last_retrans_max_scan_length': 1,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 1,
                                                            'last_retrans_scan_time_msec': 0,
                                                            'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 2}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'interfaces': 
                                            {'GigabitEthernet1': 
                                                {'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'address': '10.1.4.4',
                                                        'bdr_ip_addr': '10.1.4.1',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '10.1.4.4',
                                                        'first': '0x0(0)/0x0(0)/0x0(0)',
                                                        'index': '1/1/1,',
                                                        'interface': 'GigabitEthernet1',
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'neighbor_uptime': '1d01h',
                                                        'next': '0x0(0)/0x0(0)/0x0(0)',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'last_retrans_max_scan_length': 1,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0,
                                                            'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 1}}}},
                                            'GigabitEthernet2': 
                                                {'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'address': '10.1.2.2',
                                                        'bdr_ip_addr': '10.1.2.2',
                                                        'dead_timer': '00:00:33',
                                                        'dr_ip_addr': '10.1.2.1',
                                                        'first': '0x0(0)/0x0(0)/0x0(0)',
                                                        'hello_options': '0x2',
                                                        'index': '1/2/2,',
                                                        'interface': 'GigabitEthernet2',
                                                        'neighbor_router_id': '10.16.2.2',
                                                        'neighbor_uptime': '08:04:20',
                                                        'next': '0x0(0)/0x0(0)/0x0(0)',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'last_retrans_max_scan_length': 0,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0,
                                                            'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 0}}}}}}}}}}}}}}
    ShowIpOspfNeighborDetail_custom = {
        'vrf':
            {'default':
                 {'address_family':
                      {'ipv4':
                           {'instance':
                                {'1':
                                     {'areas':
                                          {'0.0.0.0':
                                               {'interfaces':
                                                    {'GigabitEthernet1':
                                                         {'neighbors':
                                                              {'10.64.4.4':
                                                                   {'address': '10.1.4.4',
                                                                    'bdr_ip_addr':
                                                                        '10.1.4.1',
                                                                    'dead_timer':
                                                                        '00:00:35',
                                                                    'dr_ip_addr':
                                                                        '10.1.4.4',
                                                                    'first': '0x0('
                                                                             '0)/0x0(0)/0x0(0)',
                                                                    'index': '1/1/1,',
                                                                    'interface':
                                                                        'GigabitEthernet1',
                                                                    'neighbor_router_id': '10.64.4.4',
                                                                    'neighbor_uptime':
                                                                        '1d01h',
                                                                    'next': '0x0('
                                                                            '0)/0x0(0)/0x0(0)',
                                                                    'priority': 1,
                                                                    'state': 'full',
                                                                    'statistics':
                                                                        {
                                                                            'last_retrans_max_scan_length': 1,
                                                                            'last_retrans_max_scan_time_msec': 0,
                                                                            'last_retrans_scan_length': 0,
                                                                            'last_retrans_scan_time_msec': 0,
                                                                            'nbr_event_count': 6,
                                                                            'nbr_retrans_qlen': 0,
                                                                            'total_retransmission': 1}}}}}}}}}}}}}}

    # 'show ip ospf sham-links'
    ShowIpOspfShamLinks = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'sham_links': 
                                            {'10.229.11.11 10.151.22.22': 
                                                {'adjacency_state': 'full',
                                                'cost': 111,
                                                'dcbitless_lsa_count': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'donotage_lsa': 'not allowed',
                                                'first': '0x0(0)/0x0(0)/0x0(0)',
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'index': '1/2/2',
                                                'last_retransmission_max_length': 1,
                                                'last_retransmission_max_scan': 0,
                                                'last_retransmission_scan_length': 1,
                                                'last_retransmission_scan_time': 0,
                                                'link_state': 'up',
                                                'local_id': '10.229.11.11',
                                                'name': 'SL0',
                                                'remote_id': '10.151.22.22',
                                                'retrans_qlen': 0,
                                                'state': 'point_to_point',
                                                'strict_ttl_check': True,
                                                'strict_ttl_max_hops': 3,
                                                'total_retransmission': 2,
                                                'transit_area_id': '0.0.0.1',
                                                'wait_interval': 40}}}}}}}}}}}

    # 'show ip ospf virutal-links'
    ShowIpOspfVirtualLinks = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'virtual_links': 
                                            {'0.0.0.1 10.36.3.3': 
                                                {'adjacency_state': 'full',
                                                'dcbitless_lsa_count': 7,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'donotage_lsa': 'not allowed',
                                                'first': '0x0(0)/0x0(0)',
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'index': '1/3',
                                                'interface': 'GigabitEthernet0/1',
                                                'last_retransmission_max_length': 0,
                                                'last_retransmission_max_scan': 0,
                                                'last_retransmission_scan_length': 0,
                                                'last_retransmission_scan_time': 0,
                                                'link_state': 'up',
                                                'name': 'VL0',
                                                'retrans_qlen': 0,
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'strict_ttl_check': True,
                                                'strict_ttl_max_hops': 3,
                                                'topology': 
                                                    {0: 
                                                        {'cost': 1,
                                                        'disabled': False,
                                                        'name': 'Base',
                                                        'shutdown': False}},
                                                'total_retransmission': 0,
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1,
                                                'wait_interval': 40}}}}}}}}}}}

    # 'show ip ospf database router'
    ShowIpOspfDatabaseRouter = {
        'vrf': 
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                     'lsas': 
                                                        {'10.1.77.77 10.1.77.77': 
                                                            {'adv_router': '10.1.77.77',
                                                            'lsa_id': '10.1.77.77',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.19.7.7': 
                                                                                {'link_data': '10.19.7.7',
                                                                                'link_id': '10.19.7.7',
                                                                                'num_mtid_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.166.7.6': 
                                                                                {'link_data': '10.166.7.7',
                                                                                'link_id': '10.166.7.6',
                                                                                'num_mtid_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 30,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.77.77': 
                                                                                {'link_data': '255.255.255.255',
                                                                                'link_id': '10.1.77.77',
                                                                                'num_mtid_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'stub network'}},
                                                                        'num_of_links': 3}},
                                                                'header': 
                                                                    {'adv_router': '10.1.77.77',
                                                                    'age': 288,
                                                                    'checksum': '0x1379',
                                                                    'length': 60,
                                                                    'lsa_id': '10.1.77.77',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '80000030',
                                                                    'type': 1}}}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                    'lsas': 
                                                        {'10.4.1.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.4.1.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.4.1.1': 
                                                                                {'link_data': '255.255.255.255',
                                                                                'link_id': '10.4.1.1',
                                                                                'num_mtid_metrics': 2,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0},
                                                                                    32: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 32},
                                                                                    33: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 33}},
                                                                                'type': 'stub network'},
                                                                            '10.1.2.1': 
                                                                                {'link_data': '10.1.2.1',
                                                                                'link_id': '10.1.2.1',
                                                                                'num_mtid_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.4.4': 
                                                                                {'link_data': '10.1.4.1',
                                                                                'link_id': '10.1.4.4',
                                                                                'num_mtid_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'}},
                                                                        'num_of_links': 3}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 742,
                                                                    'checksum': '0x6228',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '8000003D',
                                                                    'type': 1}}}}}}}}}}}}}}}}

    # 'show ip ospf database external'
    ShowIpOspfDatabaseExternal = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas':
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.21.33.33 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.21.33.33',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'external': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'external_route_tag': 0,
                                                                                'flags': 'E',
                                                                                'forwarding_address': '0.0.0.0',
                                                                                'metric': 20,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1595,
                                                                    'checksum': '0x7F60',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC, Upward',
                                                                    'seq_num': '80000001',
                                                                    'type': 5}}}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'database': 
                                            {'lsa_types': 
                                                {5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.94.44.44 10.64.4.4': 
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.94.44.44',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'external': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'external_route_tag': 0,
                                                                                'flags': 'E',
                                                                                'forwarding_address': '0.0.0.0',
                                                                                'metric': 20,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 1595,
                                                                    'checksum': '0x7F60',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC, Upward',
                                                                    'seq_num': '80000001',
                                                                    'type': 5}}}}}}}}}}}}}}}}

    # 'show ip ospf database network'
    ShowIpOspfDatabaseNetwork = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.166.7.6 10.84.66.66': 
                                                            {'adv_router': '10.84.66.66',
                                                            'lsa_id': '10.166.7.6',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.84.66.66': {},
                                                                            '10.1.77.77': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.84.66.66',
                                                                    'age': 1845,
                                                                    'checksum': '0x980A',
                                                                    'length': 32,
                                                                    'lsa_id': '10.166.7.6',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '8000002A',
                                                                    'type': 2}}}}}}}}}}}}}},

            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'database': 
                                            {'lsa_types': 
                                                {2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.3.4.4 10.64.4.4': 
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.3.4.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.36.3.3': {},
                                                                            '10.64.4.4': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 992,
                                                                    'checksum': '0xF0DA',
                                                                    'length': 32,
                                                                    'lsa_id': '10.3.4.4',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '8000002E',
                                                                    'type': 2}}}}}}}}}}}}}}}}

    # 'show ip ospf database summary'
    ShowIpOspfDatabaseSummary = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.64.4.4 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.64.4.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 65576,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 130,
                                                                    'checksum': '0xEF09',
                                                                    'length': 28,
                                                                    'lsa_id': '10.64.4.4',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC, Upward',
                                                                    'seq_num': '80000002',
                                                                    'type': 3}}}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'database': 
                                            {'lsa_types': 
                                                {3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.186.3.0 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.186.3.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 1,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 422,
                                                                    'checksum': '0x43DC',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.3.0',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC, Upward',
                                                                    'seq_num': '80000001',
                                                                    'type': 3}}}}}}}}}}}}}}}}

    # 'show ip ospf database opaque-area'
    ShowIpOspfDatabaseOpaqueArea = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.2 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.0.2',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'igp_metric': 1,
                                                                                'link_id': '10.1.2.1',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': {'10.1.2.1': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'total_priority': 8,
                                                                                'unreserved_bandwidths': 
                                                                                    {'0 93750000': 
                                                                                        {'priority': 0,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '1 93750000': 
                                                                                        {'priority': 1,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '2 93750000': 
                                                                                        {'priority': 2,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '3 93750000': 
                                                                                        {'priority': 3,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '4 93750000': 
                                                                                        {'priority': 4,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '5 93750000': 
                                                                                        {'priority': 5,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '6 93750000': 
                                                                                        {'priority': 6,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '7 93750000': 
                                                                                        {'priority': 7,
                                                                                        'unreserved_bandwidth': 93750000}}}},
                                                                        'num_of_links': 1}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 370,
                                                                    'checksum': '0xB43D',
                                                                    'fragment_number': 2,
                                                                    'length': 124,
                                                                    'lsa_id': '10.1.0.2',
                                                                    'opaque_id': 2,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'database': 
                                            {'lsa_types': 
                                                {10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.0.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'igp_metric': 1,
                                                                                'link_id': '10.1.4.4',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.1.4.1': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': 
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'total_priority': 8,
                                                                                'unreserved_bandwidths': 
                                                                                    {'0 93750000': 
                                                                                        {'priority': 0,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '1 93750000': 
                                                                                        {'priority': 1,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '2 93750000': 
                                                                                        {'priority': 2,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '3 93750000': 
                                                                                        {'priority': 3,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '4 93750000': 
                                                                                        {'priority': 4,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '5 93750000': 
                                                                                        {'priority': 5,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '6 93750000': 
                                                                                        {'priority': 6,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '7 93750000': 
                                                                                        {'priority': 7,
                                                                                        'unreserved_bandwidth': 93750000}}}},
                                                                        'num_of_links': 1}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 370,
                                                                    'checksum': '0x6586',
                                                                    'fragment_number': 1,
                                                                    'length': 124,
                                                                    'lsa_id': '10.1.0.1',
                                                                    'opaque_id': 1,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}}}}}}}}}}}

    # 'show ip ospf mpls traffic-eng link'
    ShowIpOspfMplsLdpInterface = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces': 
                                            {'GigabitEthernet3': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.1',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'up'}}},
                                            'OSPF_SL1': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.1',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'up'}}}}}},
                                'mpls': 
                                    {'ldp': 
                                        {'autoconfig': False,
                                        'autoconfig_area_id': '0.0.0.1',
                                        'igp_sync': False}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'interfaces': 
                                            {'GigabitEthernet1': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'up'}}},
                                            'GigabitEthernet2': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'up'}}},
                                            'TenGigabitEthernet3/0/1': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'down'}}},
                                            'Loopback1': 
                                                {'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'holddown_timer': False,
                                                        'igp_sync': False,
                                                        'state': 'up'}}}}}},
                                'mpls': 
                                    {'ldp': 
                                        {'autoconfig': False,
                                        'autoconfig_area_id': '0.0.0.0',
                                        'igp_sync': False}}}}}}}}}

    ShowIpOspfMplsLdpInterface_custom = {
        'vrf':
            {'default':
                 {'address_family':
                      {'ipv4':
                           {'instance':
                                {'1':
                                     {'areas':
                                          {'0.0.0.0':
                                               {'interfaces':
                                                    {'GigabitEthernet1':
                                                         {'mpls':
                                                              {'ldp':
                                                                   {'autoconfig': False,
                                                                    'autoconfig_area_id': '0.0.0.0',
                                                                    'holddown_timer':
                                                                        False,
                                                                    'igp_sync': False,
                                                                    'state': 'up'}}},
                                                     }}},
                                      'mpls':
                                          {'ldp':
                                               {'autoconfig': False,
                                                'autoconfig_area_id': '0.0.0.0',
                                                'igp_sync': False}}}}}}}}}

    # 'show ip ospf mpls traffic-eng link'
    ShowIpOspfMplsTrafficEngLink = {
        'vrf': 
            {'default':
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'mpls': 
                                            {'te': 
                                                {'area_instance': 2,
                                                'enable': True,
                                                'link_hash_bucket': 
                                                    {8: 
                                                        {'link_fragments': 
                                                            {2: 
                                                                {'affinity_bit': '0x0',
                                                                'igp_admin_metric': 1,
                                                                'interface_address': '10.1.2.1',
                                                                'link_id': '10.1.2.1',
                                                                'link_instance': 2,
                                                                'max_bandwidth': 125000000,
                                                                'max_reservable_bandwidth': 93750000,
                                                                'network_type': 'broadcast network',
                                                                'te_admin_metric': 1,
                                                                'total_priority': 8,
                                                                'unreserved_bandwidths': 
                                                                    {'0 93750000': 
                                                                        {'priority': 0,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '1 93750000': 
                                                                        {'priority': 1,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '2 93750000': 
                                                                        {'priority': 2,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '3 93750000': 
                                                                        {'priority': 3,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '4 93750000': 
                                                                        {'priority': 4,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '5 93750000': 
                                                                        {'priority': 5,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '6 93750000': 
                                                                        {'priority': 6,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '7 93750000': 
                                                                        {'priority': 7,
                                                                        'unreserved_bandwidth': 93750000}}}}},
                                                    9: 
                                                        {'link_fragments': 
                                                            {1: 
                                                                {'affinity_bit': '0x0',
                                                                'igp_admin_metric': 1,
                                                                'interface_address': '10.1.4.1',
                                                                'link_id': '10.1.4.4',
                                                                'link_instance': 2,
                                                                'max_bandwidth': 125000000,
                                                                'max_reservable_bandwidth': 93750000,
                                                                'network_type': 'broadcast network',
                                                                'te_admin_metric': 1,
                                                                'total_priority': 8,
                                                                'unreserved_bandwidths': 
                                                                    {'0 93750000': 
                                                                        {'priority': 0,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '1 93750000': 
                                                                        {'priority': 1,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '2 93750000': 
                                                                        {'priority': 2,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '3 93750000': 
                                                                        {'priority': 3,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '4 93750000': 
                                                                        {'priority': 4,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '5 93750000': 
                                                                        {'priority': 5,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '6 93750000': 
                                                                        {'priority': 6,
                                                                        'unreserved_bandwidth': 93750000},
                                                                    '7 93750000': 
                                                                        {'priority': 7,
                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                'total_links': 2}}}},
                                'mpls': 
                                    {'te': 
                                        {'router_id': '10.4.1.1'}}}}}}},
            'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'mpls': 
                                            {'te': 
                                                {'enable': False}}}},
                                'mpls': 
                                    {'te': {'router_id': '10.229.11.11'}}}}}}}}}


    ############################################################################
    #                               OSPF INFO
    ############################################################################

    OspfInfo = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'2': 
                                {'adjacency_stagger': 
                                    {'initial_number': 300,
                                    'maximum_number': 300},
                                'areas': 
                                    {'0.0.0.1': 
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'normal',
                                        'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                    'lsas': 
                                                        {'10.1.77.77 10.1.77.77': 
                                                            {'adv_router': '10.1.77.77',
                                                            'lsa_id': '10.1.77.77',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.19.7.7': 
                                                                                {'link_data': '10.19.7.7',
                                                                                'link_id': '10.19.7.7',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.166.7.6': 
                                                                                {'link_data': '10.166.7.7',
                                                                                'link_id': '10.166.7.6',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 30,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.77.77': 
                                                                                {'link_data': '255.255.255.255',
                                                                                'link_id': '10.1.77.77',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'stub network'}},
                                                                        'num_of_links': 3}},
                                                                'header': 
                                                                    {'adv_router': '10.1.77.77',
                                                                    'age': 288,
                                                                    'checksum': '0x1379',
                                                                    'length': 60,
                                                                    'lsa_id': '10.1.77.77',
                                                                    'option': 'None',
                                                                    'seq_num': '80000030',
                                                                    'type': 1}}}}},
                                                2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.166.7.6 10.84.66.66': 
                                                            {'adv_router': '10.84.66.66',
                                                            'lsa_id': '10.166.7.6',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.84.66.66': {},
                                                                            '10.1.77.77': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.84.66.66',
                                                                    'age': 1845,
                                                                    'checksum': '0x980A',
                                                                    'length': 32,
                                                                    'lsa_id': '10.166.7.6',
                                                                    'option': 'None',
                                                                    'seq_num': '8000002A',
                                                                    'type': 2}}}}},
                                                3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.64.4.4 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.64.4.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 65576,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 130,
                                                                    'checksum': '0xEF09',
                                                                    'length': 28,
                                                                    'lsa_id': '10.64.4.4',
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 3}}}}},
                                                5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.21.33.33 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.21.33.33',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'external': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'external_route_tag': 0,
                                                                                'flags': 'E',
                                                                                'forwarding_address': '0.0.0.0',
                                                                                'metric': 20,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1595,
                                                                    'checksum': '0x7F60',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': 'None',
                                                                    'seq_num': '80000001',
                                                                    'type': 5}}}}},
                                                10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.2 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.0.2',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'link_id': '10.1.2.1',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.1.2.1': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': 
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'unreserved_bandwidths': 
                                                                                    {'0 93750000': 
                                                                                        {'priority': 0,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '1 93750000': 
                                                                                        {'priority': 1,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '2 93750000': 
                                                                                        {'priority': 2,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '3 93750000': 
                                                                                        {'priority': 3,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '4 93750000': 
                                                                                        {'priority': 4,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '5 93750000': 
                                                                                        {'priority': 5,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '6 93750000': 
                                                                                        {'priority': 6,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '7 93750000': 
                                                                                        {'priority': 7,
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 370,
                                                                    'checksum': '0xB43D',
                                                                    'length': 124,
                                                                    'lsa_id': '10.1.0.2',
                                                                    'opaque_id': 2,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}},
                                        'interfaces': 
                                            {'GigabitEthernet3': 
                                                {'bdr_ip_addr': '10.186.5.5',
                                                'bdr_router_id': '10.115.55.55',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.186.5.1',
                                                'dr_router_id': '10.229.11.11',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'interface_type': 'broadcast',
                                                'lls': True,
                                                'name': 'GigabitEthernet3',
                                                'neighbors': 
                                                    {'10.115.55.55': 
                                                        {'address': '10.186.5.5',
                                                        'bdr_ip_addr': '10.186.5.5',
                                                        'dead_timer': '00:00:34',
                                                        'dr_ip_addr': '10.186.5.1',
                                                        'neighbor_router_id': '10.115.55.55',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'dr',
                                                'transmit_delay': 1,
                                                'ttl_security': {'enable': True,
                                                                'hops': 30}}},
                                        'mpls': 
                                            {'te': 
                                                {'enable': False}},
                                        'ranges': 
                                            {'10.4.1.0/24': 
                                                {'advertise': True,
                                                'prefix': '10.4.1.0/24'}},
                                        'sham_links': 
                                            {'10.229.11.11 10.151.22.22': 
                                                {'bdr_ip_addr': '10.186.7.7',
                                                'bdr_router_id': '10.246.57.57',
                                                'cost': 111,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'dr_ip_addr': '10.1.2.2',
                                                'dr_router_id': '10.229.11.11',
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'local_id': '10.229.11.11',
                                                'name': 'SL0',
                                                'neighbors': 
                                                    {'10.151.22.22': 
                                                        {'address': '10.151.22.22',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'neighbor_router_id': '10.151.22.22',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'remote_id': '10.151.22.22',
                                                'state': 'point_to_point',
                                                'transit_area_id': '0.0.0.1'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x053FED',
                                            'area_scope_lsa_count': 11,
                                            'spf_runs_count': 97},
                                        'virtual_links': 
                                            {'0.0.0.1 10.36.3.3': 
                                                {'bdr_ip_addr': '10.196.6.6',
                                                'bdr_router_id': '10.49.56.56',
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'dr_ip_addr': '10.1.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'name': 'VL0',
                                                'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'address': '10.229.3.3',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:41',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 12,
                                                            'nbr_retrans_qlen': 0}}},
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1}}}},
                                'auto_cost': 
                                    {'enable': False},
                                'bfd': 
                                    {'enable': True},
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': False,
                                        'type': 'cisco'},
                                    'ietf': 
                                        {'enable': False,
                                        'type': 'ietf'}},
                                'mpls': 
                                    {'ldp': 
                                        {'autoconfig': False,
                                        'autoconfig_area_id': '0.0.0.1',
                                        'igp_sync': False}},
                                'nsr': 
                                    {'enable': True},
                                'redistribution': 
                                    {'bgp': 
                                    {'bgp_id': 100}},
                                'router_id': '10.229.11.11',
                                'spf_control': 
                                    {'throttle': 
                                        {'lsa': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'stub_router': 
                                    {'always': 
                                        {'always': False,
                                        'external_lsa': False,
                                        'include_stub': False,
                                        'summary_lsa': False}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'adjacency_stagger': 
                                    {'initial_number': 300,
                                    'maximum_number': 300},
                                'areas': 
                                    {'0.0.0.0': 
                                        {'area_id': '0.0.0.0',
                                        'area_type': 'normal',
                                        'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                    'lsas': 
                                                        {'10.4.1.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.4.1.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.4.1.1': 
                                                                                {'link_data': '255.255.255.255',
                                                                                'link_id': '10.4.1.1',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0},
                                                                                    32: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 32},
                                                                                    33: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 33}},
                                                                                'type': 'stub network'},
                                                                            '10.1.2.1': 
                                                                                {'link_data': '10.1.2.1',
                                                                                'link_id': '10.1.2.1',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.4.4': 
                                                                                {'link_data': '10.1.4.1',
                                                                                'link_id': '10.1.4.4',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'}},
                                                                        'num_of_links': 3}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 742,
                                                                    'checksum': '0x6228',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': 'None',
                                                                    'seq_num': '8000003D',
                                                                    'type': 1}}}}},
                                                2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.3.4.4 10.64.4.4': 
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.3.4.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.36.3.3': {},
                                                                            '10.64.4.4': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 992,
                                                                    'checksum': '0xF0DA',
                                                                    'length': 32,
                                                                    'lsa_id': '10.3.4.4',
                                                                    'option': 'None',
                                                                    'seq_num': '8000002E',
                                                                    'type': 2}}}}},
                                                3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.186.3.0 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.186.3.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 1,
                                                                                'mt_id': 0}}}},
                                                                        'header': 
                                                                            {'adv_router': '10.4.1.1',
                                                                            'age': 422,
                                                                            'checksum': '0x43DC',
                                                                            'length': 28,
                                                                            'lsa_id': '10.186.3.0',
                                                                            'option': 'None',
                                                                            'seq_num': '80000001',
                                                                            'type': 3}}}}},
                                                5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.94.44.44 10.64.4.4': 
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.94.44.44',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'external': 
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'external_route_tag': 0,
                                                                                'flags': 'E',
                                                                                'forwarding_address': '0.0.0.0',
                                                                                'metric': 20,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 1595,
                                                                    'checksum': '0x7F60',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': 'None',
                                                                    'seq_num': '80000001',
                                                                    'type': 5}}}}},
                                                10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.0.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'link_id': '10.1.4.4',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.1.4.1': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': 
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'unreserved_bandwidths': 
                                                                                    {'0 93750000': 
                                                                                        {'priority': 0,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '1 93750000': 
                                                                                        {'priority': 1,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '2 93750000': 
                                                                                        {'priority': 2,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '3 93750000': 
                                                                                        {'priority': 3,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '4 93750000': 
                                                                                        {'priority': 4,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '5 93750000': 
                                                                                        {'priority': 5,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '6 93750000': 
                                                                                        {'priority': 6,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '7 93750000': 
                                                                                        {'priority': 7,
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 370,
                                                                    'checksum': '0x6586',
                                                                    'length': 124,
                                                                    'lsa_id': '10.1.0.1',
                                                                    'opaque_id': 1,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}},
                                        'interfaces': 
                                            {'GigabitEthernet1': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'md5'}},
                                                'bdr_ip_addr': '10.1.4.1',
                                                'bdr_router_id': '10.4.1.1',
                                                'bfd': {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.1.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'interface_type': 'broadcast',
                                                'lls': True,
                                                'name': 'GigabitEthernet1',
                                                'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'address': '10.1.4.4',
                                                        'bdr_ip_addr': '10.1.4.1',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '10.1.4.4',
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'transmit_delay': 1},
                                            'GigabitEthernet2': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'simple'}},
                                                'bdr_ip_addr': '10.1.2.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.1.2.1',
                                                'dr_router_id': '10.4.1.1',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:05',
                                                'interface_type': 'broadcast',
                                                'lls': True,
                                                'name': 'GigabitEthernet2',
                                                'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'address': '10.1.2.2',
                                                        'bdr_ip_addr': '10.1.2.2',
                                                        'dead_timer': '00:00:33',
                                                        'dr_ip_addr': '10.1.2.1',
                                                        'neighbor_router_id': '10.16.2.2',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'dr',
                                                'transmit_delay': 1},
                                            'Loopback0': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'demand_circuit': False,
                                                'enable': True,
                                                'interface_type': 'loopback',
                                                'name': 'Loopback0'}},
                                        'mpls': 
                                            {'te': 
                                                {'enable': True}},
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': True,
                                                'cost': 10,
                                                'prefix': '10.4.0.0/16'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x07CF20',
                                            'area_scope_lsa_count': 19,
                                            'spf_runs_count': 41}}},
                                'auto_cost': 
                                    {'enable': False},
                                'bfd': 
                                    {'enable': True,
                                    'strict_mode': True},
                                'database_control': 
                                    {'max_lsa': 123},
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': False,
                                        'type': 'cisco'},
                                    'ietf': 
                                        {'enable': False,
                                        'type': 'ietf'}},
                                'mpls': 
                                    {'ldp': 
                                        {'autoconfig': False,
                                        'autoconfig_area_id': '0.0.0.0',
                                        'igp_sync': False}},
                                'nsr': 
                                    {'enable': False},
                                'preference': 
                                    {'multi_values': 
                                        {'external': 114,
                                        'granularity': 
                                            {'detail': 
                                                {'inter_area': 113,
                                                'intra_area': 112}}},
                                    'single_value': {'all': 110}},
                                'router_id': '10.4.1.1',
                                'spf_control': 
                                    {'paths': 4,
                                    'throttle': 
                                        {'lsa': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'stub_router': 
                                    {'always': 
                                        {'always': False,
                                        'external_lsa': False,
                                        'include_stub': False,
                                        'summary_lsa': False}}}}}}}}}
    OspfInfo_custom = {
        'vrf':
            {'default':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'adjacency_stagger':
                                    {'initial_number': 300,
                                    'maximum_number': 300},
                                'areas':
                                    {'0.0.0.0':
                                        {'area_id': '0.0.0.0',
                                        'area_type': 'normal',
                                        'database':
                                            {'lsa_types':
                                                {1:
                                                    {'lsa_type': 1,
                                                    'lsas':
                                                        {'10.4.1.1 10.4.1.1':
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.4.1.1',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'router':
                                                                        {'links':
                                                                            {'10.4.1.1':
                                                                                {'link_data': '255.255.255.255',
                                                                                'link_id': '10.4.1.1',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0},
                                                                                    32:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 32},
                                                                                    33:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 33}},
                                                                                'type': 'stub network'},
                                                                            '10.1.2.1':
                                                                                {'link_data': '10.1.2.1',
                                                                                'link_id': '10.1.2.1',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.4.4':
                                                                                {'link_data': '10.1.4.1',
                                                                                'link_id': '10.1.4.4',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'}},
                                                                        'num_of_links': 3}},
                                                                'header':
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 742,
                                                                    'checksum': '0x6228',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': 'None',
                                                                    'seq_num': '8000003D',
                                                                    'type': 1}}}}},
                                                2:
                                                    {'lsa_type': 2,
                                                    'lsas':
                                                        {'10.3.4.4 10.64.4.4':
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.3.4.4',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'network':
                                                                        {'attached_routers':
                                                                            {'10.36.3.3': {},
                                                                            '10.64.4.4': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header':
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 992,
                                                                    'checksum': '0xF0DA',
                                                                    'length': 32,
                                                                    'lsa_id': '10.3.4.4',
                                                                    'option': 'None',
                                                                    'seq_num': '8000002E',
                                                                    'type': 2}}}}},
                                                3:
                                                    {'lsa_type': 3,
                                                    'lsas':
                                                        {'10.186.3.0 10.4.1.1':
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.186.3.0',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'summary':
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies':
                                                                            {0:
                                                                                {'metric': 1,
                                                                                'mt_id': 0}}}},
                                                                        'header':
                                                                            {'adv_router': '10.4.1.1',
                                                                            'age': 422,
                                                                            'checksum': '0x43DC',
                                                                            'length': 28,
                                                                            'lsa_id': '10.186.3.0',
                                                                            'option': 'None',
                                                                            'seq_num': '80000001',
                                                                            'type': 3}}}}},
                                                5:
                                                    {'lsa_type': 5,
                                                    'lsas':
                                                        {'10.94.44.44 10.64.4.4':
                                                            {'adv_router': '10.64.4.4',
                                                            'lsa_id': '10.94.44.44',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'external':
                                                                        {'network_mask': '255.255.255.255',
                                                                        'topologies':
                                                                            {0:
                                                                                {'external_route_tag': 0,
                                                                                'flags': 'E',
                                                                                'forwarding_address': '0.0.0.0',
                                                                                'metric': 20,
                                                                                'mt_id': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 1595,
                                                                    'checksum': '0x7F60',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': 'None',
                                                                    'seq_num': '80000001',
                                                                    'type': 5}}}}},
                                                10:
                                                    {'lsa_type': 10,
                                                    'lsas':
                                                        {'10.1.0.1 10.4.1.1':
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.0.1',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'opaque':
                                                                        {'link_tlvs':
                                                                            {1:
                                                                                {'admin_group': '0x0',
                                                                                'link_id': '10.1.4.4',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs':
                                                                                    {'10.1.4.1': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs':
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'unreserved_bandwidths':
                                                                                    {'0 93750000':
                                                                                        {'priority': 0,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '1 93750000':
                                                                                        {'priority': 1,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '2 93750000':
                                                                                        {'priority': 2,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '3 93750000':
                                                                                        {'priority': 3,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '4 93750000':
                                                                                        {'priority': 4,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '5 93750000':
                                                                                        {'priority': 5,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '6 93750000':
                                                                                        {'priority': 6,
                                                                                        'unreserved_bandwidth': 93750000},
                                                                                    '7 93750000':
                                                                                        {'priority': 7,
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header':
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 370,
                                                                    'checksum': '0x6586',
                                                                    'length': 124,
                                                                    'lsa_id': '10.1.0.1',
                                                                    'opaque_id': 1,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}},
                                        'interfaces':
                                            {'GigabitEthernet1':
                                                {'authentication':
                                                    {'auth_trailer_key':
                                                        {'crypto_algorithm': 'md5'}},
                                                'bdr_ip_addr': '10.1.4.1',
                                                'bdr_router_id': '10.4.1.1',
                                                'bfd': {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.1.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:08',
                                                'interface_type': 'broadcast',
                                                'lls': True,
                                                'name': 'GigabitEthernet1',
                                                'neighbors':
                                                    {'10.64.4.4':
                                                        {'address': '10.1.4.4',
                                                        'bdr_ip_addr': '10.1.4.1',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '10.1.4.4',
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'transmit_delay': 1},
                                            },
                                        'mpls':
                                            {'te':
                                                {'enable': True}},
                                        'ranges':
                                            {'10.4.0.0/16':
                                                {'advertise': True,
                                                'cost': 10,
                                                'prefix': '10.4.0.0/16'}},
                                        'statistics':
                                            {'area_scope_lsa_cksum_sum': '0x07CF20',
                                            'area_scope_lsa_count': 19,
                                            'spf_runs_count': 41}}},
                                'auto_cost':
                                    {'enable': False},
                                'bfd':
                                    {'enable': True,
                                    'strict_mode': True},
                                'database_control':
                                    {'max_lsa': 123},
                                'graceful_restart':
                                    {'cisco':
                                        {'enable': False,
                                        'type': 'cisco'},
                                    'ietf':
                                        {'enable': False,
                                        'type': 'ietf'}},
                                'mpls':
                                    {'ldp':
                                        {'autoconfig': False,
                                        'autoconfig_area_id': '0.0.0.0',
                                        'igp_sync': False}},
                                'nsr':
                                    {'enable': False},
                                'preference':
                                    {'multi_values':
                                        {'external': 114,
                                        'granularity':
                                            {'detail':
                                                {'inter_area': 113,
                                                'intra_area': 112}}},
                                    'single_value': {'all': 110}},
                                'router_id': '10.4.1.1',
                                'spf_control':
                                    {'paths': 4,
                                    'throttle':
                                        {'lsa':
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50},
                                        'spf':
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'stub_router':
                                    {'always':
                                        {'always': False,
                                        'external_lsa': False,
                                        'include_stub': False,
                                        'summary_lsa': False}}}}}}}}}
