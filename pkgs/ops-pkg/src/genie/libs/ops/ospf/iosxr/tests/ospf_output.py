''' 
OSPF Genie Ops Object Outputs for IOSXR.
'''


class OspfOutput(object):

    ############################################################################
    #                           OSPF INFO OUTPUTS
    ############################################################################

    # 'show protocols afi-all all'
    ShowProtocolsAfiAllAll = {
        'protocols': 
            {'bgp': 
                {'address_family': 
                    {'vpnv4 unicast': 
                        {'distance': 
                            {'external': 20,
                            'internal': 200,
                            'local': 200},
                        'neighbors': 
                            {'10.64.4.4': 
                                {'gr_enable': 'No',
                                'last_update': '00:01:28',
                                'nsr_state': 'None'}}},
                    'vpnv6 unicast': 
                        {'distance': 
                            {'external': 20,
                            'internal': 200,
                            'local': 200},
                        'neighbors': 
                            {'10.64.4.4': 
                                {'gr_enable': 'No',
                                'last_update': '00:01:28',
                                'nsr_state': 'None'}}}},
                'bgp_pid': 100,
                'graceful_restart': 
                    {'enable': False},
                'nsr': 
                    {'current_state': 'active ready',
                    'enable': True}},
            'ospf': 
                {'vrf': 
                    {'default': 
                        {'address_family': 
                            {'ipv4': 
                                {'instance': 
                                    {'1': 
                                        {'areas': 
                                            {'0.0.0.0': 
                                                {'interfaces': ['Loopback0', 'GigabitEthernet0/0/0/0', 'GigabitEthernet0/0/0/2'],
                                                'mpls': 
                                                    {'te': 
                                                        {'enable': True}}}},
                                                'nsf': False,
                                        'preference': 
                                            {'multi_values': 
                                                {'external': 114,
                                                'granularity': 
                                                    {'detail': 
                                                        {'inter_area': 113,
                                                        'intra_area': 112}}},
                                            'single_value': 
                                                {'all': 110}},
                                        'redistribution': 
                                            {'bgp': 
                                                {'bgp_id': 100,
                                                'metric': 111},
                                            'connected': 
                                                {'enabled': True},
                                            'isis': 
                                                {'isis_pid': '10',
                                                'metric': 3333},
                                            'static': 
                                                {'enabled': True,
                                                'metric': 10}},
                                        'router_id': '10.36.3.3'}}}}}}}}}

    # 'show ospf vrf all-inclusive'
    ShowOspfVrfAllInclusive = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'adjacency_stagger': 
                                    {'disable': False,
                                    'initial_number': 2,
                                    'maximum_number': 64,
                                    'nbrs_forming': 0,
                                    'nbrs_full': 1},
                                'areas': 
                                    {'0.0.0.1': 
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'stub',
                                        'summary': True,
                                        'default_cost': 111,
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': True,
                                                'prefix': '10.4.0.0/16'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x04f437',
                                            'area_scope_lsa_count': 11,
                                            'area_scope_opaque_lsa_cksum_sum': '00000000',
                                            'area_scope_opaque_lsa_count': 0,
                                            'dcbitless_lsa_count': 1,
                                            'donotage_lsa_count': 0,
                                            'flood_list_length': 0,
                                            'indication_lsa_count': 0,
                                            'interfaces_count': 2,
                                            'lfa_interface_count': 0,
                                            'lfa_per_prefix_interface_count': 0,
                                            'lfa_revision': 0,
                                            'nbrs_full': 1,
                                            'nbrs_staggered_mode': 0,
                                            'spf_runs_count': 79}}},
                                'database_control': 
                                    {'max_lsa': 123},
                                'external_flood_list_length': 0,
                                'flags': 
                                    {'abr': True,
                                    'asbr': True},
                                'flood_pacing_interval_msec': 33,
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': True,
                                        'type': 'ietf'}},
                                'lsd_revision': 1,
                                'lsd_state': 'connected, registered, bound',
                                'maximum_interfaces': 1024,
                                'nsr': 
                                    {'enable': True},
                                'numbers': 
                                    {'dc_bitless': 0,
                                    'do_not_age': 0,
                                    'external_lsa': 0,
                                    'external_lsa_checksum': '00000000',
                                    'opaque_as_lsa': 0,
                                    'opaque_as_lsa_checksum': '00000000'},
                                'redistribution': 
                                    {'bgp': 
                                        {'bgp_id': 100,
                                        'metric': 111},
                                    'connected': 
                                        {'enabled': True,
                                        'metric': 10},
                                    'isis': 
                                        {'isis_pid': '10',
                                        'metric': 3333},
                                    'max_prefix': 
                                        {'num_of_prefix': 4000,
                                        'prefix_thld': 70,
                                        'warn_only': False},
                                    'static': 
                                        {'enabled': True}},
                                'retransmission_pacing_interval': 66,
                                'role': 'primary active',
                                'router_id': '10.36.3.3',
                                'segment_routing_global_block_default': '16000-23999',
                                'segment_routing_global_block_status': 'not allocated',
                                'snmp_trap': False,
                                'spf_control': 
                                    {'throttle': 
                                        {'lsa': 
                                            {'arrival': 100,
                                            'hold': 200,
                                            'interval': 200,
                                            'maximum': 5000,
                                            'refresh_interval': 1800,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'strict_spf': True,
                                'total_areas': 1,
                                'total_normal_areas': 1,
                                'total_nssa_areas': 0,
                                'total_stub_areas': 0,
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
                                    {'disable': False,
                                    'initial_number': 2,
                                    'maximum_number': 64,
                                    'nbrs_forming': 0,
                                    'nbrs_full': 2},
                                'areas': 
                                    {'0.0.0.0': 
                                        {'area_type': 'normal',
                                        'area_id': '0.0.0.0',
                                        'rrr_enabled': True,
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x0a2fb5',
                                            'area_scope_lsa_count': 19,
                                            'area_scope_opaque_lsa_cksum_sum': '00000000',
                                            'area_scope_opaque_lsa_count': 0,
                                            'dcbitless_lsa_count': 5,
                                            'donotage_lsa_count': 0,
                                            'flood_list_length': 0,
                                            'indication_lsa_count': 0,
                                            'interfaces_count': 3,
                                            'lfa_interface_count': 0,
                                            'lfa_per_prefix_interface_count': 0,
                                            'lfa_revision': 0,
                                            'nbrs_full': 2,
                                            'nbrs_staggered_mode': 0,
                                            'spf_runs_count': 26},
                                        'topology_version': 15}},
                                'external_flood_list_length': 0,
                                'flood_pacing_interval_msec': 33,
                                'lsd_revision': 1,
                                'lsd_state': 'connected, registered, bound',
                                'maximum_interfaces': 1024,
                                'mpls': 
                                    {'ldp': 
                                        {'ldp_igp_sync': True,
                                        'ldp_sync_status': 'not achieved'}},
                                'nsr': 
                                    {'enable': True},
                                'numbers': 
                                    {'dc_bitless': 0,
                                    'do_not_age': 0,
                                    'external_lsa': 1,
                                    'external_lsa_checksum': '0x00607f',
                                    'opaque_as_lsa': 0,
                                    'opaque_as_lsa_checksum': '00000000'},
                                'retransmission_pacing_interval': 66,
                                'role': 'primary active',
                                'router_id': '10.36.3.3',
                                'segment_routing_global_block_default': '16000-23999',
                                'segment_routing_global_block_status': 'not allocated',
                                'snmp_trap': True,
                                'spf_control': 
                                    {'throttle': 
                                        {'lsa': 
                                            {'arrival': 100,
                                            'hold': 200,
                                            'interval': 200,
                                            'maximum': 5000,
                                            'refresh_interval': 1800,
                                            'start': 50},
                                        'spf': 
                                            {'hold': 200,
                                            'maximum': 5000,
                                            'start': 50}}},
                                'strict_spf': True,
                                'total_areas': 1,
                                'total_normal_areas': 1,
                                'total_nssa_areas': 0,
                                'total_stub_areas': 0,
                                'stub_router': 
                                    {'always': 
                                        {'always': True,
                                        'external_lsa': True,
                                        'external_lsa_metric': 16711680,
                                        'include_stub': True,
                                        'state': 'active',
                                        'summary_lsa': True,
                                        'summary_lsa_metric': 16711680},
                                    'on_startup': 
                                        {'on_startup': 5,
                                        'external_lsa': True,
                                        'external_lsa_metric': 16711680,
                                        'include_stub': True,
                                        'state': 'inactive',
                                        'summary_lsa': True,
                                        'summary_lsa_metric': 16711680},
                                    'on_switchover': 
                                        {'on_switchover': 10,
                                        'external_lsa': True,
                                        'external_lsa_metric': 16711680,
                                        'include_stub': True,
                                        'state': 'inactive',
                                        'summary_lsa': True,
                                        'summary_lsa_metric': 16711680}}}}}}}}}

    ShowOspfVrfAllInclusive_custom = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'ipv4':
                           {'instance':
                                {'1':
                                     {'adjacency_stagger':
                                          {'disable': False,
                                           'initial_number': 2,
                                           'maximum_number': 64,
                                           'nbrs_forming': 0,
                                           'nbrs_full': 1},
                                      'areas':
                                          {'0.0.0.1':
                                               {'area_id': '0.0.0.1',
                                                'area_type': 'stub',
                                                'summary': True,
                                                'default_cost': 111,
                                                'ranges':
                                                    {'10.4.0.0/16':
                                                         {'advertise': True,
                                                          'prefix': '10.4.0.0/16'}},
                                                'statistics':
                                                    {
                                                        'area_scope_lsa_cksum_sum':
                                                            '0x04f437',
                                                        'area_scope_lsa_count': 11,
                                                        'area_scope_opaque_lsa_cksum_sum': '00000000',
                                                        'area_scope_opaque_lsa_count': 0,
                                                        'dcbitless_lsa_count': 1,
                                                        'donotage_lsa_count': 0,
                                                        'flood_list_length': 0,
                                                        'indication_lsa_count': 0,
                                                        'interfaces_count': 2,
                                                        'lfa_interface_count': 0,
                                                        'lfa_per_prefix_interface_count': 0,
                                                        'lfa_revision': 0,
                                                        'nbrs_full': 1,
                                                        'nbrs_staggered_mode': 0,
                                                        'spf_runs_count': 79}}},
                                      'database_control':
                                          {'max_lsa': 123},
                                      'external_flood_list_length': 0,
                                      'flags':
                                          {'abr': True,
                                           'asbr': True},
                                      'flood_pacing_interval_msec': 33,
                                      'graceful_restart':
                                          {'cisco':
                                               {'enable': True,
                                                'type': 'ietf'}},
                                      'lsd_revision': 1,
                                      'lsd_state': 'connected, registered, bound',
                                      'maximum_interfaces': 1024,
                                      'nsr':
                                          {'enable': True},
                                      'numbers':
                                          {'dc_bitless': 0,
                                           'do_not_age': 0,
                                           'external_lsa': 0,
                                           'external_lsa_checksum': '00000000',
                                           'opaque_as_lsa': 0,
                                           'opaque_as_lsa_checksum': '00000000'},
                                      'redistribution':
                                          {'bgp':
                                               {'bgp_id': 100,
                                                'metric': 111},
                                           'connected':
                                               {'enabled': True,
                                                'metric': 10},
                                           'isis':
                                               {'isis_pid': '10',
                                                'metric': 3333},
                                           'max_prefix':
                                               {'num_of_prefix': 4000,
                                                'prefix_thld': 70,
                                                'warn_only': False},
                                           'static':
                                               {'enabled': True}},
                                      'retransmission_pacing_interval': 66,
                                      'role': 'primary active',
                                      'router_id': '10.36.3.3',
                                      'segment_routing_global_block_default':
                                          '16000-23999',
                                      'segment_routing_global_block_status': 'not '
                                                                             'allocated',
                                      'snmp_trap': False,
                                      'spf_control':
                                          {'throttle':
                                               {'lsa':
                                                    {'arrival': 100,
                                                     'hold': 200,
                                                     'interval': 200,
                                                     'maximum': 5000,
                                                     'refresh_interval': 1800,
                                                     'start': 50},
                                                'spf':
                                                    {'hold': 200,
                                                     'maximum': 5000,
                                                     'start': 50}}},
                                      'strict_spf': True,
                                      'total_areas': 1,
                                      'total_normal_areas': 1,
                                      'total_nssa_areas': 0,
                                      'total_stub_areas': 0,
                                      'stub_router':
                                          {'always':
                                               {'always': False,
                                                'external_lsa': False,
                                                'include_stub': False,
                                                'summary_lsa': False}}}}}}},
            }}

    ShowOspfMplsTrafficEngLink = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'mpls': 
                                            {'te': 
                                                {'area_instance': 2,
                                                'enable': True,
                                                'total_links': 2}}}},
                                'mpls': 
                                    {'te': 
                                        {'router_id': '10.36.3.3'}}}}}}},
            'default': 
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
                                                'link_fragments': 
                                                    {1: 
                                                        {'affinity_bit': 0,
                                                        'extended_admin_groups': 
                                                            {0: {'value': 0},
                                                            1: {'value': 0},
                                                            2: {'value': 0},
                                                            3: {'value': 0},
                                                            4: {'value': 0},
                                                            5: {'value': 0},
                                                            6: {'value': 0},
                                                            7: {'value': 0}},
                                                        'interface_address': '10.3.4.3',
                                                        'link_id': '10.3.4.4',
                                                        'link_instance': 2,
                                                        'maximum_bandwidth': 125000000,
                                                        'maximum_reservable_bandwidth': 93750000,
                                                        'network_type': 'broadcast',
                                                        'out_interface_id': 4,
                                                        'te_admin_metric': 1,
                                                        'total_extended_admin_group': 8,
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
                                                                'unreserved_bandwidth': 93750000}}},
                                                    2: 
                                                        {'affinity_bit': 0,
                                                        'extended_admin_groups': 
                                                            {0: {'value': 0},
                                                            1: {'value': 0},
                                                            2: {'value': 0},
                                                            3: {'value': 0},
                                                            4: {'value': 0},
                                                            5: {'value': 0},
                                                            6: {'value': 0},
                                                            7: {'value': 0}},
                                                        'interface_address': '10.2.3.3',
                                                        'link_id': '10.2.3.3',
                                                        'link_instance': 2,
                                                        'maximum_bandwidth': 125000000,
                                                        'maximum_reservable_bandwidth': 93750000,
                                                        'network_type': 'broadcast',
                                                        'out_interface_id': 6,
                                                        'te_admin_metric': 1,
                                                        'total_extended_admin_group': 8,
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
                                                'total_links': 2}}}},
                                'mpls': 
                                    {'te': 
                                        {'router_id': '10.36.3.3'}}}}}}}}}

    # 'show ospf vrf all-inclusive sham-links'
    ShowOspfVrfAllInclusiveShamLinks = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'sham_links': 
                                            {'10.21.33.33 10.151.22.22': 
                                                {'cost': 111,
                                                'dcbitless_lsa_count': 1,
                                                'donotage_lsa': 'not allowed',
                                                'dead_interval': 13,
                                                'demand_circuit': True,
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:00:772',
                                                'if_index': 2,
                                                'local_id': '10.21.33.33',
                                                'name': 'SL0',
                                                'link_state': 'up',
                                                'remote_id': '10.151.22.22',
                                                'retransmit_interval': 5,
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7,
                                                'wait_interval': 13}}}}}}}}}}}

    # 'show ospf vrf all-inclusive virtual-links'
    ShowOspfVrfAllInclusiveVirtualLinks = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'virtual_links': 
                                            {'0.0.0.1 10.16.2.2': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'simple'}},
                                                'cost': 65535,
                                                'dcbitless_lsa_count': 1,
                                                'donotage_lsa': 'not allowed',
                                                'dead_interval': 16,
                                                'demand_circuit': True,
                                                'hello_interval': 4,
                                                'hello_timer': '00:00:03:179',
                                                'interface': 'GigabitEthernet0/0/0/3',
                                                'name': 'VL0',
                                                'link_state': 'up',
                                                'nsf': 
                                                    {'enable': True,
                                                    'last_restart': '00:18:16'},
                                                'retransmit_interval': 44,
                                                'router_id': '10.16.2.2',
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 5,
                                                'wait_interval': 16}}}}}}}}}}}

    # 'show ospf vrf all-inclusive database router'
    ShowOspfVrfAllInclusiveDatabaseRouter = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                    'lsas': 
                                                        {'10.229.11.11 10.229.11.11': 
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.229.11.11',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.186.5.1': 
                                                                                {'link_data': '10.186.5.1',
                                                                                'link_id': '10.186.5.1',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22': 
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'another router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1713,
                                                                    'area_border_router': True,
                                                                    'as_boundary_router': True,
                                                                    'checksum': '0x9ce3',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '8000003e',
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
                                                                                'num_tos_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'stub network'},
                                                                            '10.1.2.1': 
                                                                                {'link_data': '10.1.2.1',
                                                                                'link_id': '10.1.2.1',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.1.4.4': 
                                                                                {'link_data': '10.1.4.1',
                                                                                'link_id': '10.1.4.4',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'}},
                                                                        'num_of_links': 3}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 1802,
                                                                    'checksum': '0x6228',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '8000003d',
                                                                    'type': 1}}}}}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive database external'
    ShowOspfVrfAllInclusiveDatabaseExternal = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.115.55.55 10.100.5.5': 
                                                            {'adv_router': '10.100.5.5',
                                                            'lsa_id': '10.115.55.55',
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
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.100.5.5',
                                                                    'age': 520,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.115.55.55',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '90000006',
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
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.64.4.4',
                                                                    'age': 608,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '80000002',
                                                                    'type': 5}}}}}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive database network'
    ShowOspfVrfAllInclusiveDatabaseNetwork = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.186.5.1 10.229.11.11':
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.186.5.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 522,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '80000033',
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
                                                        {'10.1.2.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.2.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.4.1.1': {},
                                                                            '10.16.2.2': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 1844,
                                                                    'checksum': '0x3dd0',
                                                                    'length': 32,
                                                                    'lsa_id': '10.1.2.1',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '8000000f',
                                                                    'type': 2}}}}}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive database summary'
    ShowOspfVrfAllInclusiveDatabaseSummary = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.186.4.0 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.186.4.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 75565,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 608,
                                                                    'checksum': '0xaa4a',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.4.0',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '90000001',
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
                                                        {'10.186.3.0 10.16.2.2': 
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.186.3.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 65575,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 520,
                                                                    'checksum': '0xaa4a',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.3.0',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '80000001',
                                                                    'type': 3}}}}}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive database opaque-area'
    ShowOspfVrfAllInclusiveDatabaseOpaqueArea = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'database': 
                                            {'lsa_types': 
                                                {10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.7 10.16.2.2': 
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.0.7',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'igp_metric': 1,
                                                                                'link_id': '10.3.2.2',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.3.2.2': {}},
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
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header': 
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 420,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.7',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '90000002',
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
                                                        {'10.1.0.6 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.6',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0',
                                                                                'extended_admin_group': 
                                                                                    {'groups': 
                                                                                        {0: {'value': 0},
                                                                                        1: {'value': 0},
                                                                                        2: {'value': 0},
                                                                                        3: {'value': 0},
                                                                                        4: {'value': 0},
                                                                                        5: {'value': 0},
                                                                                        6: {'value': 0},
                                                                                        7: {'value': 0}},
                                                                                    'length': 8},
                                                                                'igp_metric': 1,
                                                                                'link_id': '10.2.3.3',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.2.3.3': {}},
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
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header': 
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1175,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.6',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive interface'
    ShowOspfVrfAllInclusiveInterface = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces': 
                                            {'GigabitEthernet0/0/0/1': 
                                                {'bdr_ip_addr': '10.19.7.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd': 
                                                    {'enable': True,
                                                    'interval': 12345,
                                                    'mode': 'default',
                                                    'multiplier': 50},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.19.7.7',
                                                'dr_router_id': '10.1.77.77',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:03:040',
                                                'hello_interval': 10,
                                                'index': '1/1',
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.19.7.3/24',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'high_water_mark': 11,
                                                'max_flood_scan_length': 5,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 1500,
                                                'name': 'GigabitEthernet0/0/0/1',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'bdr',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0,
                                                    'multi_area_intf_count': 0,
                                                    },
                                                'neighbors': 
                                                    {'10.1.77.77': 
                                                        {'dr_router_id': '10.1.77.77'},
                                                    },
                                                }},
                                        'virtual_links': 
                                            {'0.0.0.1 10.16.2.2': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'donotage_lsa': False,
                                                'enable': False,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:01:281',
                                                'hello_interval': 10,
                                                'high_water_mark': 20,
                                                'index': '4/7',
                                                'interface_type': 'virtual-link',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 7,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'max_flood_scan_length': 7,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 0,
                                                'name': 'VL0',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.16.2.2',
                                                'state': 'point-to-point',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'total_dcbitless_lsa': 7,
                                                'neighbors': 
                                                    {'10.64.4.4': {},
                                                    },
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 1,
                                                    'multi_area_intf_count': 0,
                                                    }}}},
                                        'sham_links': 
                                            {'10.21.33.33 10.151.22.22': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 111,
                                                'dead_interval': 13,
                                                'demand_circuit': True,
                                                'donotage_lsa': False,
                                                'enable': False,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:00:864',
                                                'hello_interval': 3,
                                                'high_water_mark': 9,
                                                'index': '2/2',
                                                'interface_type': 'sham-link',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'max_flood_scan_length': 7,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 0,
                                                'name': 'SL0',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'transmit_delay': 7,
                                                'wait_interval': 13,
                                                'statistics': 
                                                    {'adj_nbr_count': 0,
                                                    'nbr_count': 0,
                                                    'num_nbrs_suppress_hello': 0,
                                                    'multi_area_intf_count': 0,
                                                    },
                                                'total_dcbitless_lsa': 1,
                                                }}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'interfaces': 
                                            {'GigabitEthernet0/0/0/0': 
                                                {'bdr_ip_addr': '10.3.4.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.3.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:07:171',
                                                'hello_interval': 10,
                                                'index': '1/1',
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.3.4.3/24',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'high_water_mark': 5,
                                                'max_flood_scan_length': 3,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 1500,
                                                'name': 'GigabitEthernet0/0/0/0',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'bdr',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'statistics': 
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0,
                                                    'multi_area_intf_count': 0,
                                                    },
                                                'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'dr_router_id': '10.64.4.4'},
                                                    },
                                                },
                                            'GigabitEthernet0/0/0/2': 
                                                {'bdr_router_id': '10.16.2.2',
                                                'bdr_ip_addr': '10.2.3.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.2.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:07:587',
                                                'hello_interval': 10,
                                                'index': '2/2',
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.2.3.3/24',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'high_water_mark': 7,
                                                'max_flood_scan_length': 3,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 1500,
                                                'name': 'GigabitEthernet0/0/0/2',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'dr',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'statistics': 
                                                    {'nbr_count': 1,
                                                    'adj_nbr_count': 1,
                                                    'multi_area_intf_count': 0,
                                                    'num_nbrs_suppress_hello': 0,
                                                    },
                                                'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'bdr_router_id': '10.16.2.2'},
                                                    },
                                                },
                                            'Loopback0': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'demand_circuit': False,
                                                'enable': True,
                                                'interface_type': 'loopback',
                                                'ip_address': '10.36.3.3/32',
                                                'line_protocol': True,
                                                'name': 'Loopback0',
                                                'process_id': '1',
                                                'router_id': '10.36.3.3'},
                                            'tunnel-te31': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'hello_interval': 10,
                                                'index': '0/0',
                                                'interface_type': 'point-to-point',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 0,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'high_water_mark': 0,
                                                'max_flood_scan_length': 0,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 576,
                                                'mtu': 0,
                                                'name': 'tunnel-te31',
                                                'next': '0(0)/0(0)',
                                                'passive': True,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'transmit_delay': 1,
                                                'wait_interval': 0,
                                                'statistics': 
                                                    {'adj_nbr_count': 0,
                                                    'multi_area_intf_count': 0,
                                                    'nbr_count': 0,
                                                    'num_nbrs_suppress_hello': 0}}}}}}}}}}}}

    # 'show ospf vrf all-inclusive neighbor detail'
    ShowOspfVrfAllInclusiveNeighborDetail = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'total_neighbor_count': 2,
                                        'virtual_links': 
                                            {'0.0.0.1 10.16.2.2': 
                                                {'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'address': '10.229.4.4',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:21',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '1/3,',
                                                        'lls_options': '0x1 (LR)',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.16.2.2',
                                                        'neighbor_uptime': '04:58:24',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x72',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 7,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 0,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 0,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0}}}}},
                                        'interfaces': 
                                            {'GigabitEthernet0/0/0/1': 
                                                {'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'address': '10.229.3.3',
                                                        'bdr_ip_addr': '10.229.3.2',
                                                        'dead_timer': '00:00:31',
                                                        'dr_ip_addr': '10.229.3.3',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '2/2,',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'neighbor_uptime': '05:00:13',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x42',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 2,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 1,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 1,
                                                            'last_retrans_scan_time_msec': 0}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'total_neighbor_count': 1,
                                        'interfaces':
                                            {'GigabitEthernet0/0/0/0': 
                                                {'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'address': '10.229.4.4',
                                                        'bdr_ip_addr': '10.229.4.2',
                                                        'dead_timer': '00:00:32',
                                                        'dr_ip_addr': '10.229.4.4',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '1/1,',
                                                        'lls_options': '0x1 (LR)',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'neighbor_uptime': '05:00:21',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x52',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,    
                                                            'total_retransmission': 0,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 0,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0}}}},
                                            'GigabitEthernet0/0/0/2': 
                                                {'neighbors': 
                                                    {'10.144.6.6': 
                                                        {'address': '10.229.4.4',
                                                        'bdr_ip_addr': '10.229.4.2',
                                                        'dead_timer': '00:00:32',
                                                        'dr_ip_addr': '10.229.4.4',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '1/1,',
                                                        'lls_options': '0x1 (LR)',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.144.6.6',
                                                        'neighbor_uptime': '05:00:21',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x52',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,    
                                                            'total_retransmission': 0,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 0,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0}}}}}}}}}}}}}}
    # 'show ospf vrf all-inclusive database router'
    ShowOspfVrfAllInclusiveDatabaseRouter_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'database':
                                            {'lsa_types':
                                                {1:
                                                    {'lsa_type': 1,
                                                    'lsas':
                                                        {'10.229.11.11 10.229.11.11':
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.229.11.11',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'router':
                                                                        {'links':
                                                                            {'10.186.5.1':
                                                                                {'link_data': '10.186.5.1',
                                                                                'link_id': '10.186.5.1',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22':
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'num_tos_metrics': 0,
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0,
                                                                                        'tos': 0}},
                                                                                'type': 'another router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1713,
                                                                    'area_border_router': True,
                                                                    'as_boundary_router': True,
                                                                    'checksum': '0x9ce3',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '8000003e',
                                                                    'type': 1}}}}}}}}}}}}}},
            }}

    # 'show ospf vrf all-inclusive database external'
    ShowOspfVrfAllInclusiveDatabaseExternal_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'database':
                                            {'lsa_types':
                                                {5:
                                                    {'lsa_type': 5,
                                                    'lsas':
                                                        {'10.115.55.55 10.100.5.5':
                                                            {'adv_router': '10.100.5.5',
                                                            'lsa_id': '10.115.55.55',
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
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.100.5.5',
                                                                    'age': 520,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.115.55.55',
                                                                    'option': 'None',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '90000006',
                                                                    'type': 5}}}}}}}}}}}}}},
           }}

    # 'show ospf vrf all-inclusive database network'
    ShowOspfVrfAllInclusiveDatabaseNetwork_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'database':
                                            {'lsa_types':
                                                {2:
                                                    {'lsa_type': 2,
                                                    'lsas':
                                                        {'10.186.5.1 10.229.11.11':
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.186.5.1',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'network':
                                                                        {'attached_routers':
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 522,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'routing_bit_enable': True,
                                                                    'seq_num': '80000033',
                                                                    'type': 2}}}}}}}}}}}}}},
           }}

    # 'show ospf vrf all-inclusive database summary'
    ShowOspfVrfAllInclusiveDatabaseSummary_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'database':
                                            {'lsa_types':
                                                {3:
                                                    {'lsa_type': 3,
                                                    'lsas':
                                                        {'10.186.4.0 10.36.3.3':
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.186.4.0',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'summary':
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies':
                                                                            {0:
                                                                                {'metric': 75565,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 608,
                                                                    'checksum': '0xaa4a',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.4.0',
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '90000001',
                                                                    'type': 3}}}}}}}}}}}}}},
            }}

    # 'show ospf vrf all-inclusive database opaque-area'
    ShowOspfVrfAllInclusiveDatabaseOpaqueArea_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'database':
                                            {'lsa_types':
                                                {10:
                                                    {'lsa_type': 10,
                                                    'lsas':
                                                        {'10.1.0.7 10.16.2.2':
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.0.7',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'opaque':
                                                                        {'link_tlvs':
                                                                            {1:
                                                                                {'igp_metric': 1,
                                                                                'link_id': '10.3.2.2',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs':
                                                                                    {'10.3.2.2': {}},
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
                                                                                        'unreserved_bandwidth': 93750000}}}}}},
                                                                'header':
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 420,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.7',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'option_desc': 'No '
                                                                    'TOS-capability, '
                                                                    'DC',
                                                                    'seq_num': '90000002',
                                                                    'type': 10}}}}}}}}}}}}}},
            }}

    # 'show ospf vrf all-inclusive interface'
    ShowOspfVrfAllInclusiveInterface_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'interfaces':
                                            {'GigabitEthernet0/0/0/1':
                                                {'bdr_ip_addr': '10.19.7.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd':
                                                    {'enable': True,
                                                    'interval': 12345,
                                                    'mode': 'default',
                                                    'multiplier': 50},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.19.7.7',
                                                'dr_router_id': '10.1.77.77',
                                                'enable': True,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:03:040',
                                                'hello_interval': 10,
                                                'index': '1/1',
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.19.7.3/24',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'high_water_mark': 11,
                                                'max_flood_scan_length': 5,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 1500,
                                                'name': 'GigabitEthernet0/0/0/1',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'priority': 1,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'bdr',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'statistics':
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 0,
                                                    'multi_area_intf_count': 0,
                                                    },
                                                }},
                                        'virtual_links':
                                            {'0.0.0.1 10.16.2.2':
                                                {'bfd':
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': True,
                                                'donotage_lsa': False,
                                                'enable': False,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:01:281',
                                                'hello_interval': 10,
                                                'high_water_mark': 20,
                                                'index': '4/7',
                                                'interface_type': 'virtual-link',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 7,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'max_flood_scan_length': 7,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 0,
                                                'name': 'VL0',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.16.2.2',
                                                'state': 'point-to-point',
                                                'transmit_delay': 1,
                                                'wait_interval': 40,
                                                'total_dcbitless_lsa': 7,
                                                'neighbors':
                                                    {'10.64.4.4': {},
                                                    },
                                                'statistics':
                                                    {'adj_nbr_count': 1,
                                                    'nbr_count': 1,
                                                    'num_nbrs_suppress_hello': 1,
                                                    'multi_area_intf_count': 0,
                                                    }}}},
                                        'sham_links':
                                            {'10.21.33.33 10.151.22.22':
                                                {'bfd':
                                                    {'enable': False},
                                                'cost': 111,
                                                'dead_interval': 13,
                                                'demand_circuit': True,
                                                'donotage_lsa': False,
                                                'enable': False,
                                                'flood_queue_length': 0,
                                                'hello_timer': '00:00:00:864',
                                                'hello_interval': 3,
                                                'high_water_mark': 9,
                                                'index': '2/2',
                                                'interface_type': 'sham-link',
                                                'ip_address': '0.0.0.0/0',
                                                'last_flood_scan_length': 1,
                                                'last_flood_scan_time_msec': 0,
                                                'line_protocol': True,
                                                'ls_ack_list': 'current',
                                                'ls_ack_list_length': 0,
                                                'max_flood_scan_length': 7,
                                                'max_flood_scan_time_msec': 0,
                                                'max_pkt_sz': 1500,
                                                'mtu': 0,
                                                'name': 'SL0',
                                                'next': '0(0)/0(0)',
                                                'passive': False,
                                                'process_id': '1',
                                                'retransmit_interval': 5,
                                                'router_id': '10.36.3.3',
                                                'state': 'point-to-point',
                                                'transmit_delay': 7,
                                                'wait_interval': 13,
                                                'statistics':
                                                    {'adj_nbr_count': 0,
                                                    'nbr_count': 0,
                                                    'num_nbrs_suppress_hello': 0,
                                                    'multi_area_intf_count': 0,
                                                    },
                                                'total_dcbitless_lsa': 1,
                                                }}}}}}}},
            }}

    # 'show ospf vrf all-inclusive neighbor detail'
    ShowOspfVrfAllInclusiveNeighborDetail_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'total_neighbor_count': 2,
                                        'virtual_links':
                                            {'0.0.0.1 10.16.2.2':
                                                {'neighbors':
                                                    {'10.16.2.2':
                                                        {'address': '10.229.4.4',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:21',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '1/3,',
                                                        'lls_options': '0x1 (LR)',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.16.2.2',
                                                        'neighbor_uptime': '04:58:24',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x72',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 7,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 0,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 0,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 0,
                                                            'last_retrans_scan_time_msec': 0}}}}},
                                        'interfaces':
                                            {'GigabitEthernet0/0/0/1':
                                                {'neighbors':
                                                    {'10.36.3.3':
                                                        {'address': '10.229.3.3',
                                                        'bdr_ip_addr': '10.229.3.2',
                                                        'dead_timer': '00:00:31',
                                                        'dr_ip_addr': '10.229.3.3',
                                                        'first': '0(0)/0(0)',
                                                        'high_water_mark': 0,
                                                        'index': '2/2,',
                                                        'ls_ack_list': 'NSR-sync',
                                                        'ls_ack_list_pending': 0,
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'neighbor_uptime': '05:00:13',
                                                        'next': '0(0)/0(0)',
                                                        'options': '0x42',
                                                        'priority': 1,
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0,
                                                            'total_retransmission': 2,
                                                            'total_dbd_retrans': 0,
                                                            'last_retrans_max_scan_length': 1,
                                                            'last_retrans_max_scan_time_msec': 0,
                                                            'last_retrans_scan_length': 1,
                                                            'last_retrans_scan_time_msec': 0}}}}}}}}}}}},
            }}
    ############################################################################
    #                               OSPF INFO
    ############################################################################

    OspfInfo = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'adjacency_stagger': 
                                    {'disable': False,
                                    'initial_number': 2,
                                    'maximum_number': 64},
                                'areas': 
                                    {'0.0.0.1': 
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'stub',
                                        'database': 
                                            {'lsa_types': 
                                                {1: 
                                                    {'lsa_type': 1,
                                                    'lsas': 
                                                        {'10.229.11.11 10.229.11.11': 
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.229.11.11',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'router': 
                                                                        {'links': 
                                                                            {'10.186.5.1': 
                                                                                {'link_data': '10.186.5.1',
                                                                                'link_id': '10.186.5.1',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22': 
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0}},
                                                                                'type': 'another router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1713,
                                                                    'checksum': '0x9ce3',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': 'None',
                                                                    'seq_num': '8000003e',
                                                                    'type': 1}}}}},
                                                2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.186.5.1 10.229.11.11': 
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.186.5.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 522,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': 'None',
                                                                    'seq_num': '80000033',
                                                                    'type': 2}}}}},
                                                3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.186.4.0 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.186.4.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 75565,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 608,
                                                                    'checksum': '0xaa4a',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.4.0',
                                                                    'option': 'None',
                                                                    'seq_num': '90000001',
                                                                    'type': 3}}}}},
                                                5: 
                                                    {'lsa_type': 5,
                                                    'lsas': 
                                                        {'10.115.55.55 10.100.5.5': 
                                                            {'adv_router': '10.100.5.5',
                                                            'lsa_id': '10.115.55.55',
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
                                                                    {'adv_router': '10.100.5.5',
                                                                    'age': 520,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.115.55.55',
                                                                    'option': 'None',
                                                                    'seq_num': '90000006',
                                                                    'type': 5}}}}},
                                                10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.7 10.16.2.2': 
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.0.7',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'link_id': '10.3.2.2',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.3.2.2': {}},
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
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 420,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.7',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '90000002',
                                                                    'type': 10}}}}}}},
                                        'default_cost': 111,
                                        'interfaces': 
                                            {'GigabitEthernet0/0/0/1': 
                                                {'bdr_ip_addr': '10.19.7.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd': 
                                                    {'enable': True,
                                                    'interval': 12345,
                                                    'multiplier': 50},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.19.7.7',
                                                'dr_router_id': '10.1.77.77',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:03:040',
                                                'interface_type': 'broadcast',
                                                'name': 'GigabitEthernet0/0/0/1',
                                                'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'neighbor_router_id': '10.36.3.3',
                                                        'address': '10.229.3.3',
                                                        'bdr_ip_addr': '10.229.3.2',
                                                        'dead_timer': '00:00:31',
                                                        'dr_ip_addr': '10.229.3.3',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'transmit_delay': 1}},
                                        'mpls': 
                                            {'te': 
                                                {'enable': True}},
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': True,
                                                'prefix': '10.4.0.0/16'}},
                                        'sham_links': 
                                            {'10.21.33.33 10.151.22.22': 
                                                {'cost': 111,
                                                'dead_interval': 13,
                                                'demand_circuit': True,
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:00:772',
                                                'local_id': '10.21.33.33',
                                                'name': 'SL0',
                                                'remote_id': '10.151.22.22',
                                                'retransmit_interval': 5,
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x04f437',
                                            'area_scope_lsa_count': 11,
                                            'spf_runs_count': 79},
                                        'summary': True,
                                        'virtual_links': 
                                            {'0.0.0.1 10.16.2.2': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'simple'}},
                                                'cost': 65535,
                                                'dead_interval': 16,
                                                'demand_circuit': True,
                                                'hello_interval': 4,
                                                'hello_timer': '00:00:03:179',
                                                'name': 'VL0',
                                                'neighbors': 
                                                    {'10.16.2.2': 
                                                        {'neighbor_router_id': '10.16.2.2',
                                                        'address': '10.229.4.4',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:21',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 7,
                                                            'nbr_retrans_qlen': 0}}},
                                                'retransmit_interval': 44,
                                                'router_id': '10.16.2.2',
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 5}}}},
                                'database_control': 
                                    {'max_lsa': 123},
                                'graceful_restart': 
                                    {'cisco': 
                                        {'enable': True,
                                        'type': 'ietf'}},
                                'maximum_interfaces': 1024,
                                'mpls': 
                                    {'te': 
                                        {'router_id': '10.36.3.3'}},
                                'nsr': 
                                    {'enable': True},
                                'redistribution': 
                                    {'bgp': 
                                        {'bgp_id': 100,
                                        'metric': 111},
                                    'connected': 
                                        {'enabled': True,
                                        'metric': 10},
                                    'isis': 
                                        {'isis_pid': '10',
                                        'metric': 3333},
                                    'max_prefix': 
                                        {'num_of_prefix': 4000,
                                        'prefix_thld': 70,
                                        'warn_only': False},
                                    'static': 
                                        {'enabled': True}},
                                'router_id': '10.36.3.3',
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
                                    {'disable': False,
                                    'initial_number': 2,
                                    'maximum_number': 64},
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
                                                                                        'mt_id': 0}},
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
                                                                    'age': 1802,
                                                                    'checksum': '0x6228',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': 'None',
                                                                    'seq_num': '8000003d',
                                                                    'type': 1}}}}},
                                                2: 
                                                    {'lsa_type': 2,
                                                    'lsas': 
                                                        {'10.1.2.1 10.4.1.1': 
                                                            {'adv_router': '10.4.1.1',
                                                            'lsa_id': '10.1.2.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.4.1.1': {},
                                                                            '10.16.2.2': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 1844,
                                                                    'checksum': '0x3dd0',
                                                                    'length': 32,
                                                                    'lsa_id': '10.1.2.1',
                                                                    'option': 'None',
                                                                    'seq_num': '8000000f',
                                                                    'type': 2}}}}},
                                                3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.186.3.0 10.16.2.2': 
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.186.3.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 65575,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 520,
                                                                    'checksum': '0xaa4a',
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
                                                                    'age': 608,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 5}}}}},
                                                10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.6 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.6',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0',
                                                                                'link_id': '10.2.3.3',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.2.3.3': {}},
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
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1175,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.6',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '80000002',
                                                                    'type': 10}}}}}}},
                                        'interfaces': 
                                            {'GigabitEthernet0/0/0/0': 
                                                {'bdr_ip_addr': '10.3.4.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.3.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07:171',
                                                'interface_type': 'broadcast',
                                                'name': 'GigabitEthernet0/0/0/0',
                                                'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'neighbor_router_id': '10.64.4.4',
                                                        'address': '10.229.4.4',
                                                        'bdr_ip_addr': '10.229.4.2',
                                                        'dead_timer': '00:00:32',
                                                        'dr_ip_addr': '10.229.4.4',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'transmit_delay': 1},
                                            'GigabitEthernet0/0/0/2': 
                                                {'bdr_ip_addr': '10.2.3.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.2.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07:587',
                                                'interface_type': 'broadcast',
                                                'name': 'GigabitEthernet0/0/0/2',
                                                'neighbors': 
                                                    {'10.144.6.6': 
                                                        {'neighbor_router_id': '10.144.6.6',
                                                        'address': '10.229.4.4',
                                                        'bdr_ip_addr': '10.229.4.2',
                                                        'dead_timer': '00:00:32',
                                                        'dr_ip_addr': '10.229.4.4',
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
                                                    'name': 'Loopback0'},
                                            'tunnel-te31': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'enable': True,
                                                'hello_interval': 10,
                                                'interface_type': 'point-to-point',
                                                'name': 'tunnel-te31',
                                                'passive': True,
                                                'retransmit_interval': 5,
                                                'state': 'point-to-point',
                                                'transmit_delay': 1}},
                                        'mpls': 
                                            {'te': 
                                                {'enable': True}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '0x0a2fb5',
                                            'area_scope_lsa_count': 19,
                                            'spf_runs_count': 26}}},
                                'maximum_interfaces': 1024,
                                'mpls': 
                                    {'ldp': 
                                        {'ldp_igp_sync': True},
                                    'te': 
                                        {'router_id': '10.36.3.3'}},
                                'nsr': 
                                    {'enable': True},
                                'preference': 
                                    {'multi_values': 
                                        {'external': 114,
                                        'granularity': 
                                            {'detail': 
                                                {'inter_area': 113,
                                                'intra_area': 112}}},
                                    'single_value': 
                                        {'all': 110}},
                                'router_id': '10.36.3.3',
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
                                        {'always': True,
                                        'external_lsa': True,
                                        'include_stub': True,
                                        'summary_lsa': True},
                                    'on_startup': 
                                        {'external_lsa': True,
                                        'include_stub': True,
                                        'on_startup': 5,
                                        'summary_lsa': True},
                                    'on_switchover': 
                                        {'external_lsa': True,
                                        'include_stub': True,
                                        'on_switchover': 10,
                                        'summary_lsa': True}}}}}}}}}
    OspfInfo_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'adjacency_stagger':
                                    {'disable': False,
                                    'initial_number': 2,
                                    'maximum_number': 64},
                                'areas':
                                    {'0.0.0.1':
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'stub',
                                        'database':
                                            {'lsa_types':
                                                {1:
                                                    {'lsa_type': 1,
                                                    'lsas':
                                                        {'10.229.11.11 10.229.11.11':
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.229.11.11',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'router':
                                                                        {'links':
                                                                            {'10.186.5.1':
                                                                                {'link_data': '10.186.5.1',
                                                                                'link_id': '10.186.5.1',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22':
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0}},
                                                                                'type': 'another router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1713,
                                                                    'checksum': '0x9ce3',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': 'None',
                                                                    'seq_num': '8000003e',
                                                                    'type': 1}}}}},
                                                2:
                                                    {'lsa_type': 2,
                                                    'lsas':
                                                        {'10.186.5.1 10.229.11.11':
                                                            {'adv_router': '10.229.11.11',
                                                            'lsa_id': '10.186.5.1',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'network':
                                                                        {'attached_routers':
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 522,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': 'None',
                                                                    'seq_num': '80000033',
                                                                    'type': 2}}}}},
                                                3:
                                                    {'lsa_type': 3,
                                                    'lsas':
                                                        {'10.186.4.0 10.36.3.3':
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.186.4.0',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'summary':
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies':
                                                                            {0:
                                                                                {'metric': 75565,
                                                                                'mt_id': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 608,
                                                                    'checksum': '0xaa4a',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.4.0',
                                                                    'option': 'None',
                                                                    'seq_num': '90000001',
                                                                    'type': 3}}}}},
                                                5:
                                                    {'lsa_type': 5,
                                                    'lsas':
                                                        {'10.115.55.55 10.100.5.5':
                                                            {'adv_router': '10.100.5.5',
                                                            'lsa_id': '10.115.55.55',
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
                                                                    {'adv_router': '10.100.5.5',
                                                                    'age': 520,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.115.55.55',
                                                                    'option': 'None',
                                                                    'seq_num': '90000006',
                                                                    'type': 5}}}}},
                                                10:
                                                    {'lsa_type': 10,
                                                    'lsas':
                                                        {'10.1.0.7 10.16.2.2':
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.0.7',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'opaque':
                                                                        {'link_tlvs':
                                                                            {1:
                                                                                {'link_id': '10.3.2.2',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs':
                                                                                    {'10.3.2.2': {}},
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
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 420,
                                                                    'checksum': '0x5ec',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.7',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': 'None',
                                                                    'seq_num': '90000002',
                                                                    'type': 10}}}}}}},
                                        'default_cost': 111,
                                        'interfaces':
                                            {'GigabitEthernet0/0/0/1':
                                                {'bdr_ip_addr': '10.19.7.3',
                                                'bdr_router_id': '10.36.3.3',
                                                'bfd':
                                                    {'enable': True,
                                                    'interval': 12345,
                                                    'multiplier': 50},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'demand_circuit': False,
                                                'dr_ip_addr': '10.19.7.7',
                                                'dr_router_id': '10.1.77.77',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:03:040',
                                                'interface_type': 'broadcast',
                                                'name': 'GigabitEthernet0/0/0/1',
                                                'neighbors':
                                                    {'10.36.3.3':
                                                        {'neighbor_router_id': '10.36.3.3',
                                                        'address': '10.229.3.3',
                                                        'bdr_ip_addr': '10.229.3.2',
                                                        'dead_timer': '00:00:31',
                                                        'dr_ip_addr': '10.229.3.3',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 6,
                                                            'nbr_retrans_qlen': 0}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'transmit_delay': 1}},
                                        'mpls':
                                            {'te':
                                                {'enable': True}},
                                        'ranges':
                                            {'10.4.0.0/16':
                                                {'advertise': True,
                                                'prefix': '10.4.0.0/16'}},
                                        'sham_links':
                                            {'10.21.33.33 10.151.22.22':
                                                {'cost': 111,
                                                'dead_interval': 13,
                                                'demand_circuit': True,
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:00:772',
                                                'local_id': '10.21.33.33',
                                                'name': 'SL0',
                                                'remote_id': '10.151.22.22',
                                                'retransmit_interval': 5,
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7}},
                                        'statistics':
                                            {'area_scope_lsa_cksum_sum': '0x04f437',
                                            'area_scope_lsa_count': 11,
                                            'spf_runs_count': 79},
                                        'summary': True,
                                        'virtual_links':
                                            {'0.0.0.1 10.16.2.2':
                                                {'authentication':
                                                    {'auth_trailer_key':
                                                        {'crypto_algorithm': 'simple'}},
                                                'cost': 65535,
                                                'dead_interval': 16,
                                                'demand_circuit': True,
                                                'hello_interval': 4,
                                                'hello_timer': '00:00:03:179',
                                                'name': 'VL0',
                                                'neighbors':
                                                    {'10.16.2.2':
                                                        {'neighbor_router_id': '10.16.2.2',
                                                        'address': '10.229.4.4',
                                                        'bdr_ip_addr': '0.0.0.0',
                                                        'dead_timer': '00:00:21',
                                                        'dr_ip_addr': '0.0.0.0',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 7,
                                                            'nbr_retrans_qlen': 0}}},
                                                'retransmit_interval': 44,
                                                'router_id': '10.16.2.2',
                                                'state': 'point-to-point,',
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 5}}}},
                                'database_control':
                                    {'max_lsa': 123},
                                'graceful_restart':
                                    {'cisco':
                                        {'enable': True,
                                        'type': 'ietf'}},
                                'maximum_interfaces': 1024,
                                'mpls':
                                    {'te':
                                        {'router_id': '10.36.3.3'}},
                                'nsr':
                                    {'enable': True},
                                'redistribution':
                                    {'bgp':
                                        {'bgp_id': 100,
                                        'metric': 111},
                                    'connected':
                                        {'enabled': True,
                                        'metric': 10},
                                    'isis':
                                        {'isis_pid': '10',
                                        'metric': 3333},
                                    'max_prefix':
                                        {'num_of_prefix': 4000,
                                        'prefix_thld': 70,
                                        'warn_only': False},
                                    'static':
                                        {'enabled': True}},
                                'router_id': '10.36.3.3',
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
            }}
