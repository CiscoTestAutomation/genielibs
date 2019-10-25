''' 
OSPF Genie Ops Object Outputs for NXOS.
'''


class OspfOutput(object):

    # ==========================================================================
    #                           DEVICE RAW OUTPUTS
    # ==========================================================================

    # 'show feature'
    ShowFeature = {
        'feature':
            {'ospf':
                {'instance':
                    {'1':
                        {'state': 'enabled'}}}}}

    # 'show ip ospf vrf all'
    ShowIpOspfVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'stub',
                                        'authentication': 'none',
                                        'default_cost': 1,
                                        'existed': '08:30:42',
                                        'numbers': 
                                            {'active_interfaces': 3,
                                            'interfaces': 3,
                                            'loopback_interfaces': 0,
                                            'passive_interfaces': 0},
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': False,
                                                'cost': 31,
                                                'net': 1,
                                                'prefix': '10.4.0.0/16'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '11',
                                            'area_scope_lsa_count': 11,
                                            'spf_last_run_time': 0.000464,
                                            'spf_runs_count': 33}}},
                                'auto_cost': 
                                    {'bandwidth_unit': 'mbps',
                                    'enable': False,
                                    'reference_bandwidth': 40000},
                                'enable': True,
                                'discard_route_external': True,
                                'discard_route_internal': True,
                                'graceful_restart': 
                                    {'ietf': 
                                        {'enable': True,
                                        'exist_status': 'none',
                                        'restart_interval': 60,
                                        'state': 'Inactive',
                                        'type': 'ietf'}},
                                'instance': 1,
                                'nsr': 
                                    {'enable': True},
                                'numbers': 
                                    {'active_areas': 
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1},
                                    'areas': 
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1}},
                                'opaque_lsa_enable': True,
                                'preference': 
                                    {'single_value': 
                                        {'all': 110}},
                                'router_id': '10.151.22.22',
                                'single_tos_routes_enable': True,
                                'spf_control': 
                                    {'paths': 8,
                                    'throttle': 
                                        {'lsa': 
                                            {'group_pacing': 10,
                                            'hold': 5000,
                                            'maximum': 5000,
                                            'minimum': 1000,
                                            'numbers': 
                                                {'external_lsas': 
                                                    {'checksum': '0',
                                                    'total': 0},
                                                'opaque_as_lsas': 
                                                    {'checksum': '0',
                                                    'total': 0}},
                                            'start': 0.0},
                                            'spf': 
                                                {'hold': 1000,
                                                'maximum': 5000,
                                                'start': 200}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'area_id': '0.0.0.0',
                                        'area_type': 'normal',
                                        'authentication': 'none',
                                        'existed': '08:30:42',
                                        'numbers': 
                                            {'active_interfaces': 4,
                                            'interfaces': 4,
                                            'loopback_interfaces': 1,
                                            'passive_interfaces': 0},
                                        'ranges': 
                                            {'10.4.1.0/24': 
                                                {'advertise': True,
                                                'cost': 33,
                                                'net': 0,
                                                'prefix': '10.4.1.0/24'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '19',
                                            'area_scope_lsa_count': 19,
                                            'spf_last_run_time': 0.001386,
                                            'spf_runs_count': 8}}},
                                'auto_cost': 
                                    {'bandwidth_unit': 'mbps',
                                    'enable': False,
                                    'reference_bandwidth': 40000},
                                'bfd': 
                                    {'enable': True,
                                    'strict_mode': True},
                                'database_control': 
                                    {'max_lsa': 123},
                                'enable': True,
                                'discard_route_external': True,
                                'discard_route_internal': True,
                                'graceful_restart': 
                                    {'ietf': 
                                        {'enable': True,
                                        'exist_status': 'none',
                                        'restart_interval': 60,
                                        'state': 'Inactive',
                                        'type': 'ietf'}},
                                'instance': 1,
                                'nsr': 
                                    {'enable': True},
                                'numbers': 
                                    {'active_areas': 
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1},
                                    'areas': 
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1}},
                                'opaque_lsa_enable': True,
                                'preference': 
                                    {'single_value': {'all': 110}},
                                'router_id': '10.16.2.2',
                                'single_tos_routes_enable': True,
                                'spf_control': 
                                    {'paths': 8,
                                    'throttle': 
                                        {'lsa': 
                                            {'group_pacing': 10,
                                            'hold': 5000,
                                            'maximum': 5000,
                                            'minimum': 1000,
                                            'numbers': 
                                                {'external_lsas': 
                                                    {'checksum': '0x7d61',
                                                    'total': 1},
                                                'opaque_as_lsas': 
                                                    {'checksum': '0',
                                                    'total': 0}},
                                            'start': 0.0},
                                            'spf': 
                                                {'hold': 1000,
                                                'maximum': 5000,
                                                'start': 200}}},
                                'stub_router': 
                                    {'always': 
                                        {'always': True}}}}}}}}}
    ShowIpOspfVrfAll_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'area_id': '0.0.0.1',
                                        'area_type': 'stub',
                                        'authentication': 'none',
                                        'default_cost': 1,
                                        'existed': '08:30:42',
                                        'numbers':
                                            {'active_interfaces': 3,
                                            'interfaces': 3,
                                            'loopback_interfaces': 0,
                                            'passive_interfaces': 0},
                                        'ranges':
                                            {'10.4.0.0/16':
                                                {'advertise': False,
                                                'cost': 31,
                                                'net': 1,
                                                'prefix': '10.4.0.0/16'}},
                                        'statistics':
                                            {'area_scope_lsa_cksum_sum': '11',
                                            'area_scope_lsa_count': 11,
                                            'spf_last_run_time': 0.000464,
                                            'spf_runs_count': 33}}},
                                'auto_cost':
                                    {'bandwidth_unit': 'mbps',
                                    'enable': False,
                                    'reference_bandwidth': 40000},
                                'enable': True,
                                'discard_route_external': True,
                                'discard_route_internal': True,
                                'graceful_restart':
                                    {'ietf':
                                        {'enable': True,
                                        'exist_status': 'none',
                                        'restart_interval': 60,
                                        'state': 'Inactive',
                                        'type': 'ietf'}},
                                'instance': 1,
                                'nsr':
                                    {'enable': True},
                                'numbers':
                                    {'active_areas':
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1},
                                    'areas':
                                        {'normal': 1,
                                        'nssa': 0,
                                        'stub': 0,
                                        'total': 1}},
                                'opaque_lsa_enable': True,
                                'preference':
                                    {'single_value':
                                        {'all': 110}},
                                'router_id': '10.151.22.22',
                                'single_tos_routes_enable': True,
                                'spf_control':
                                    {'paths': 8,
                                    'throttle':
                                        {'lsa':
                                            {'group_pacing': 10,
                                            'hold': 5000,
                                            'maximum': 5000,
                                            'minimum': 1000,
                                            'numbers':
                                                {'external_lsas':
                                                    {'checksum': '0',
                                                    'total': 0},
                                                'opaque_as_lsas':
                                                    {'checksum': '0',
                                                    'total': 0}},
                                            'start': 0.0},
                                            'spf':
                                                {'hold': 1000,
                                                'maximum': 5000,
                                                'start': 200}}}}}}}},
            }}

    # 'show ip ospf mpls ldp interface vrf all'
    ShowIpOspfMplsLdpInterfaceVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'mpls': 
                                            {'ldp': 
                                                {'autoconfig': False,
                                                'autoconfig_area_id': '0.0.0.1',
                                                'igp_sync': False}},
                                        'interfaces': 
                                            {'Ethernet2/1': 
                                                {'area': '0.0.0.1',
                                                'interface_type': 'broadcast',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.1',
                                                        'igp_sync': False}},
                                                'name': 'Ethernet2/1',
                                                'state': 'bdr'}},
                                        'sham_links': 
                                            {'10.151.22.22 10.229.11.11': 
                                                {'area': '0.0.0.1',
                                                'interface_type': 'point_to_point',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.1',
                                                        'igp_sync': False}},
                                                'name': '10.151.22.22 10.229.11.11',
                                                'state': 'point_to_point'},
                                            '10.151.22.22 10.21.33.33': 
                                                {'area': '0.0.0.1',
                                                'interface_type': 'point_to_point',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.1',
                                                        'igp_sync': False}},
                                                'name': '10.151.22.22 '
                                                '10.21.33.33',
                                                'state': 'point_to_point'}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'mpls': 
                                            {'ldp': 
                                                {'autoconfig': False,
                                                'autoconfig_area_id': '0.0.0.0',
                                                'igp_sync': False}},
                                        'interfaces': 
                                            {'Ethernet2/2': 
                                                {'area': '0.0.0.0',
                                                'interface_type': 'broadcast',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'igp_sync': False}},
                                                'name': 'Ethernet2/2',
                                                'state': 'bdr'},
                                            'Ethernet2/3': 
                                                {'area': '0.0.0.0',
                                                'interface_type': 'broadcast',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'igp_sync': False}},
                                                'name': 'Ethernet2/3',
                                                'state': 'bdr'},
                                            'Ethernet2/4': 
                                                {'area': '0.0.0.0',
                                                'interface_type': 'broadcast',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'igp_sync': False}},
                                                'name': 'Ethernet2/4',
                                                'state': 'bdr'},
                                            'loopback0': 
                                                {'area': '0.0.0.0',
                                                'interface_type': 'loopback',
                                                'mpls': 
                                                    {'ldp': 
                                                        {'autoconfig': False,
                                                        'autoconfig_area_id': '0.0.0.0',
                                                        'igp_sync': False}},
                                                'name': 'loopback0',
                                                'state': 'loopback'}}}}}}}}}}}
    ShowIpOspfMplsLdpInterfaceVrfAll_custom = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'ipv4':
                           {'instance':
                                {'1':
                                     {'areas':
                                          {'0.0.0.1':
                                               {'mpls':
                                                    {'ldp':
                                                         {'autoconfig': False,
                                                          'autoconfig_area_id': '0.0.0.1',
                                                          'igp_sync': False}},
                                                'interfaces':
                                                    {'Ethernet2/1':
                                                         {'area': '0.0.0.1',
                                                          'interface_type': 'broadcast',
                                                          'mpls':
                                                              {'ldp':
                                                                   {'autoconfig': False,
                                                                    'autoconfig_area_id': '0.0.0.1',
                                                                    'igp_sync': False}},
                                                          'name': 'Ethernet2/1',
                                                          'state': 'bdr'}},
                                                'sham_links':
                                                    {'10.151.22.22 10.229.11.11':
                                                         {'area': '0.0.0.1',
                                                          'interface_type':
                                                              'point_to_point',
                                                          'mpls':
                                                              {'ldp':
                                                                   {'autoconfig': False,
                                                                    'autoconfig_area_id': '0.0.0.1',
                                                                    'igp_sync': False}},
                                                          'name': '10.151.22.22 '
                                                                  '10.229.11.11',
                                                          'state': 'point_to_point'},
                                                     '10.151.22.22 10.21.33.33':
                                                         {'area': '0.0.0.1',
                                                          'interface_type':
                                                              'point_to_point',
                                                          'mpls':
                                                              {'ldp':
                                                                   {'autoconfig': False,
                                                                    'autoconfig_area_id': '0.0.0.1',
                                                                    'igp_sync': False}},
                                                          'name': '10.151.22.22 '
                                                                  '10.21.33.33',
                                                          'state':
                                                              'point_to_point'}}}}}}}}},
             }}
    # 'show ip ospf virtual-links vrf all'
    ShowIpOspfVirtualLinksVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'virtual_links': 
                                            {'0.0.0.1 10.1.8.8': 
                                                {'backbone_area_id': '0.0.0.0',
                                                'cost': 40,
                                                'dead_interval': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:05',
                                                'index': 7,
                                                'interface': 'Ethernet1/5',
                                                'interface_type': 'point_to_point',
                                                'link_state': 'up',
                                                'name': 'VL1',
                                                'nbr_adjs': 1,
                                                'nbr_flood': 1,
                                                'nbr_total': 1,
                                                'neighbors': 
                                                    {'10.1.8.8': 
                                                        {'address': '10.19.4.4',
                                                        'dbd_option': '0x72',
                                                        'dead_timer': '00:00:33',
                                                        'hello_option': '0x32',
                                                        'last_change': '00:07:51',
                                                        'last_non_hello_received': '00:07:49',
                                                        'neighbor_router_id': '10.1.8.8',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}},
                                                'remote_addr': '10.19.4.4',
                                                'retransmit_interval': 5,
                                                'router_id': '10.1.8.8',
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1,
                                                'unnumbered_interface': 'Ethernet1/5',
                                                'unnumbered_ip_address': '10.19.4.3',
                                                'wait_interval': 40}}}}}}}}}}}

    # 'show ip ospf sham-links vrf all'
    ShowIpOspfShamLinksVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'sham_links': 
                                            {'10.151.22.22 10.229.11.11': 
                                                {'backbone_area_id': '0.0.0.0',
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'destination': '10.229.11.11',
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:02',
                                                'index': 6,
                                                'interface_type': 'point_to_point',
                                                'link_state': 'up',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL1',
                                                'nbr_adjs': 1,
                                                'nbr_flood': 1,
                                                'nbr_total': 1,
                                                'neighbors': 
                                                    {'10.229.11.11': 
                                                        {'address': '10.229.11.11',
                                                        'area': '0.0.0.1',
                                                        'backbone_area_id': '0.0.0.0',
                                                        'dbd_option': '0x72',
                                                        'dead_timer': '00:00:38',
                                                        'hello_option': '0x32',
                                                        'instance': '1',
                                                        'last_change': '08:10:01',
                                                        'last_non_hello_received': 'never',
                                                        'local': '10.151.22.22',
                                                        'neighbor_router_id': '10.229.11.11',
                                                        'remote': '10.229.11.11',
                                                        'state': 'full',
                                                        'statistics': {'nbr_event_count': 8}}},
                                                'remote_id': '10.229.11.11',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1,
                                                'unnumbered_interface': 'loopback1',
                                                'unnumbered_ip_address': '10.151.22.22',
                                                'wait_interval': 40},
                                            '10.151.22.22 10.21.33.33': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'simple'},
                                                    'auth_trailer_key_chain': 
                                                        {'key_chain': 'test',
                                                        'status': 'ready'}},
                                                'backbone_area_id': '0.0.0.0',
                                                'cost': 111,
                                                'dead_interval': 13,
                                                'destination': '10.21.33.33',
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:01',
                                                'index': 7,
                                                'nbr_adjs': 0,
                                                'nbr_flood': 0,
                                                'nbr_total': 0,
                                                'interface_type': 'point_to_point',
                                                'link_state': 'up',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL2',
                                                'remote_id': '10.21.33.33',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7,
                                                'unnumbered_interface': 'loopback1',
                                                'unnumbered_ip_address': '10.151.22.22',
                                                'wait_interval': 13}}}}}}}}}}}

    # 'show ip ospf interface vrf all'
    ShowIpOspfInterfaceVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces': 
                                            {'Ethernet2/1': 
                                                {'bdr_ip_addr': '10.229.6.2',
                                                'bdr_router_id': '10.151.22.22',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 40,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.229.6.6',
                                                'dr_router_id': '10.84.66.66',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': True,
                                                'index': 2,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.229.6.2/24',
                                                'line_protocol': 'up',
                                                'name': 'Ethernet2/1',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}},
                                        'sham_links': 
                                            {'10.151.22.22 10.229.11.11': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': False,
                                                'index': 6,
                                                'interface_type': 'p2p',
                                                'ip_address': '10.151.22.22',
                                                'line_protocol': 'up',
                                                'name': 'SL1-0.0.0.0-10.151.22.22-10.229.11.11',
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'state': 'p2p',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            '10.151.22.22 10.21.33.33': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'Simple'},
                                                        'auth_trailer_key_chain': 
                                                            {'key_chain': 'test'}},
                                                    'bfd': 
                                                        {'enable': False},
                                                    'cost': 111,
                                                    'dead_interval': 13,
                                                    'enable': True,
                                                    'hello_interval': 3,
                                                    'hello_timer': '00:00:00',
                                                    'if_cfg': False,
                                                    'index': 7,
                                                    'interface_type': 'p2p',
                                                    'ip_address': '10.151.22.22',
                                                    'line_protocol': 'up',
                                                    'name': 'SL2-0.0.0.0-10.151.22.22-10.21.33.33',
                                                    'passive': False,
                                                    'retransmit_interval': 5,
                                                    'state': 'p2p',
                                                    'statistics': 
                                                        {'link_scope_lsa_cksum_sum': 0,
                                                        'link_scope_lsa_count': 0,
                                                        'num_nbrs_adjacent': 0,
                                                        'num_nbrs_flooding': 0,
                                                        'total_neighbors': 0},
                                                    'transmit_delay': 7,
                                                    'wait_interval': 13}},
                                        'virtual_links': 
                                            {'0.0.0.1 10.1.8.8': 
                                                {'backbone_area_id': '0.0.0.0',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': False,
                                                'index': 6,
                                                'interface_type': 'p2p',
                                                'ip_address': '10.151.22.22',
                                                'line_protocol': 'up',
                                                'name': 'VL1-0.0.0.0-10.1.8.8-10.66.12.12',
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'state': 'p2p',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
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
                                            {'Ethernet2/2': 
                                                {'bdr_ip_addr': '10.2.3.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.2.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:02',
                                                'if_cfg': True,
                                                'index': 3,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.2.3.2/24',
                                                'line_protocol': 'up',
                                                'name': 'Ethernet2/2',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            'Ethernet2/3': 
                                                {'bdr_ip_addr': '10.2.4.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.2.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'if_cfg': True,
                                                'index': 4,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.2.4.2/24',
                                                'line_protocol': 'up',
                                                'name': 'Ethernet2/3',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            'Ethernet2/4': 
                                                {'bdr_ip_addr': '10.1.2.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.1.2.1',
                                                'dr_router_id': '10.4.1.1',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'if_cfg': True,
                                                'index': 5,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.1.2.2/24',
                                                'line_protocol': 'up',
                                                'name': 'Ethernet2/4',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            'loopback0': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'enable': True,
                                                'if_cfg': True,
                                                'index': 1,
                                                'interface_type': 'loopback',
                                                'ip_address': '10.16.2.2/32',
                                                'line_protocol': 'up',
                                                'name': 'loopback0',
                                                'state': 'loopback'}}}}}}}}}}}

    ShowIpOspfInterfaceVrfAll_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'interfaces':
                                            {'Ethernet2/1':
                                                {'bdr_ip_addr': '10.229.6.2',
                                                'bdr_router_id': '10.151.22.22',
                                                'bfd':
                                                    {'enable': False},
                                                'cost': 40,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.229.6.6',
                                                'dr_router_id': '10.84.66.66',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': True,
                                                'index': 2,
                                                'interface_type': 'broadcast',
                                                'ip_address': '10.229.6.2/24',
                                                'line_protocol': 'up',
                                                'name': 'Ethernet2/1',
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}},
                                        'sham_links':
                                            {'10.151.22.22 10.229.11.11':
                                                {'bfd':
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': False,
                                                'index': 6,
                                                'interface_type': 'p2p',
                                                'ip_address': '10.151.22.22',
                                                'line_protocol': 'up',
                                                'name': 'SL1-0.0.0.0-10.151.22.22-10.229.11.11',
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'state': 'p2p',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40},
                                            '10.151.22.22 10.21.33.33':
                                                {'authentication':
                                                    {'auth_trailer_key':
                                                        {'crypto_algorithm': 'Simple'},
                                                        'auth_trailer_key_chain':
                                                            {'key_chain': 'test'}},
                                                    'bfd':
                                                        {'enable': False},
                                                    'cost': 111,
                                                    'dead_interval': 13,
                                                    'enable': True,
                                                    'hello_interval': 3,
                                                    'hello_timer': '00:00:00',
                                                    'if_cfg': False,
                                                    'index': 7,
                                                    'interface_type': 'p2p',
                                                    'ip_address': '10.151.22.22',
                                                    'line_protocol': 'up',
                                                    'name': 'SL2-0.0.0.0-10.151.22.22-10.21.33.33',
                                                    'passive': False,
                                                    'retransmit_interval': 5,
                                                    'state': 'p2p',
                                                    'statistics':
                                                        {'link_scope_lsa_cksum_sum': 0,
                                                        'link_scope_lsa_count': 0,
                                                        'num_nbrs_adjacent': 0,
                                                        'num_nbrs_flooding': 0,
                                                        'total_neighbors': 0},
                                                    'transmit_delay': 7,
                                                    'wait_interval': 13}},
                                        'virtual_links':
                                            {'0.0.0.1 10.1.8.8':
                                                {'backbone_area_id': '0.0.0.0',
                                                'bfd':
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'if_cfg': False,
                                                'index': 6,
                                                'interface_type': 'p2p',
                                                'ip_address': '10.151.22.22',
                                                'line_protocol': 'up',
                                                'name': 'VL1-0.0.0.0-10.1.8.8-10.66.12.12',
                                                'passive': False,
                                                'retransmit_interval': 5,
                                                'state': 'p2p',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0,
                                                    'num_nbrs_adjacent': 1,
                                                    'num_nbrs_flooding': 1,
                                                    'total_neighbors': 1},
                                                'transmit_delay': 1,
                                                'wait_interval': 40}}}}}}}}},
            }}

    # 'show ip ospf neighbor detail vrf all'
    ShowIpOspfNeighborDetailVrfAll = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.1': 
                                        {'interfaces':
                                            {'Ethernet2/1': 
                                                {'neighbors': 
                                                    {'10.84.66.66': 
                                                        {'address': '10.229.6.6',
                                                        'bdr_ip_addr': '10.229.6.2',
                                                        'dbd_options': '0x52',
                                                        'dead_timer': '00:00:38',
                                                        'dr_ip_addr': '10.229.6.6',
                                                        'hello_options': '0x12',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:38:39',
                                                        'priority': 1,
                                                        'neighbor_router_id': '10.84.66.66',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6}}}}},
                                        'sham_links': 
                                            {'10.151.22.22 10.229.11.11': 
                                                {'neighbors': 
                                                    {'10.229.11.11': 
                                                        {'address': '10.229.11.11',
                                                        'dbd_options': '0x72',
                                                        'dead_timer': '00:00:41',
                                                        'hello_options': '0x32',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:16:20',
                                                        'neighbor_router_id': '10.229.11.11',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 8}}}}},

                                        'virtual_links': 
                                            {'0.0.0.1 10.1.8.8': 
                                                {'neighbors': 
                                                    {'10.1.8.8': 
                                                        {'address': '10.19.4.4',
                                                        'dbd_options': '0x72',
                                                        'dead_timer': '00:00:43',
                                                        'hello_options': '0x32',
                                                        'last_non_hello_packet_received': '00:00:18',
                                                        'last_state_change': '00:00:23',
                                                        'neighbor_router_id': '10.1.8.8',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}}}}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
                                    {'0.0.0.0': 
                                        {'interfaces': 
                                            {'Ethernet2/2': 
                                                {'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'address': '10.2.3.3',
                                                        'bdr_ip_addr': '10.2.3.2',
                                                        'dbd_options': '0x52',
                                                        'dead_timer': '00:00:39',
                                                        'dr_ip_addr': '10.2.3.3',
                                                        'hello_options': '0x12',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:38:40',
                                                        'priority': 1,
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}}},
                                            'Ethernet2/3': 
                                                {'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'address': '10.2.4.4',
                                                        'bdr_ip_addr': '10.2.4.2',
                                                        'dbd_options': '0x52',
                                                        'dead_timer': '00:00:33',
                                                        'dr_ip_addr': '10.2.4.4',
                                                        'hello_options': '0x12',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:38:42',
                                                        'priority': 1,
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6}}}},
                                            'Ethernet2/4': 
                                                {'neighbors': 
                                                    {'10.4.1.1': 
                                                        {'address': '10.1.2.1',
                                                        'bdr_ip_addr': '10.1.2.2',
                                                        'dbd_options': '0x52',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '10.1.2.1',
                                                        'hello_options': '0x12',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:38:41',
                                                        'priority': 1,
                                                        'neighbor_router_id': '10.4.1.1',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}}}}}}}}}}}}}

    ShowIpOspfNeighborDetailVrfAll_custom = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
                                    {'0.0.0.1':
                                        {'interfaces':
                                            {'Ethernet2/1':
                                                {'neighbors':
                                                    {'10.84.66.66':
                                                        {'address': '10.229.6.6',
                                                        'bdr_ip_addr': '10.229.6.2',
                                                        'dbd_options': '0x52',
                                                        'dead_timer': '00:00:38',
                                                        'dr_ip_addr': '10.229.6.6',
                                                        'hello_options': '0x12',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:38:39',
                                                        'priority': 1,
                                                        'neighbor_router_id': '10.84.66.66',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 6}}}}},
                                        'sham_links':
                                            {'10.151.22.22 10.229.11.11':
                                                {'neighbors':
                                                    {'10.229.11.11':
                                                        {'address': '10.229.11.11',
                                                        'dbd_options': '0x72',
                                                        'dead_timer': '00:00:41',
                                                        'hello_options': '0x32',
                                                        'last_non_hello_packet_received': 'never',
                                                        'last_state_change': '08:16:20',
                                                        'neighbor_router_id': '10.229.11.11',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 8}}}}},

                                        'virtual_links':
                                            {'0.0.0.1 10.1.8.8':
                                                {'neighbors':
                                                    {'10.1.8.8':
                                                        {'address': '10.19.4.4',
                                                        'dbd_options': '0x72',
                                                        'dead_timer': '00:00:43',
                                                        'hello_options': '0x32',
                                                        'last_non_hello_packet_received': '00:00:18',
                                                        'last_state_change': '00:00:23',
                                                        'neighbor_router_id': '10.1.8.8',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 5}}}}}}}}}}}},
            }}

    # 'show ip ospf database external detail vrf all'
    ShowIpOspfDatabaseExternalDetailVrfAll = {
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
                                                        {'10.21.33.33 10.36.3.3': 
                                                            {'lsa_id': '10.21.33.33',
                                                            'adv_router': '10.36.3.3',
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
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': '0x20',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000002',
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
                                                            {'lsa_id': '10.94.44.44',
                                                            'adv_router': '10.64.4.4',
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
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': '0x20',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000002',
                                                                    'type': 5}}}}}}}}}}}}}}}}
    ShowIpOspfDatabaseExternalDetailVrfAll_custom = {
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
                                                        {'10.21.33.33 10.36.3.3':
                                                            {'lsa_id': '10.21.33.33',
                                                            'adv_router': '10.36.3.3',
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
                                                                    {'adv_router': '10.36.3.3',
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': '0x20',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000002',
                                                                    'type': 5}}}}}}}}}}}}}},
            }}

    # 'show ip ospf database network detail vrf all'
    ShowIpOspfDatabaseNetworkDetailVrfAll = {
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
                                                            {'lsa_id': '10.186.5.1',
                                                            'adv_router': '10.229.11.11',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1454,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000033',
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
                                                            {'lsa_id': '10.1.2.1',
                                                            'adv_router': '10.4.1.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'network': 
                                                                        {'attached_routers': 
                                                                            {'10.4.1.1': {},
                                                                            '10.16.2.2': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 772,
                                                                    'checksum': '0x3bd1',
                                                                    'length': 32,
                                                                    'lsa_id': '10.1.2.1',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000010',
                                                                    'type': 2}}}}}}}}}}}}}}}}
    ShowIpOspfDatabaseNetworkDetailVrfAll_custom = {
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
                                                            {'lsa_id': '10.186.5.1',
                                                            'adv_router': '10.229.11.11',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'network':
                                                                        {'attached_routers':
                                                                            {'10.229.11.11': {},
                                                                            '10.115.55.55': {}},
                                                                        'network_mask': '255.255.255.0'}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 1454,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000033',
                                                                    'type': 2}}}}}}}}}}}}}},
            }}


    # 'show ip ospf database summary detail vrf all'
    ShowIpOspfDatabaseSummaryDetailVrfAll = {
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
                                                        {'10.1.2.0 10.16.2.2': 
                                                            {'lsa_id': '10.1.2.0',
                                                            'adv_router': '10.16.2.2',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 4294,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 788,
                                                                    'checksum': '0xfc54',
                                                                    'length': 28,
                                                                    'lsa_id': '10.1.2.0',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000001',
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
                                                            {'lsa_id': '10.186.3.0',
                                                            'adv_router': '10.4.1.1',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 1,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.4.1.1',
                                                                    'age': 694,
                                                                    'checksum': '0x43dc',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.3.0',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000001',
                                                                    'type': 3}}}}}}}}}}}}}}}}
    ShowIpOspfDatabaseSummaryDetailVrfAll_custom = {
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
                                                        {'10.1.2.0 10.16.2.2':
                                                            {'lsa_id': '10.1.2.0',
                                                            'adv_router': '10.16.2.2',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'summary':
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies':
                                                                            {0:
                                                                                {'metric': 4294,
                                                                                'mt_id': 0,
                                                                                'tos': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 788,
                                                                    'checksum': '0xfc54',
                                                                    'length': 28,
                                                                    'lsa_id': '10.1.2.0',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000001',
                                                                    'type': 3}}}}}}}}}}}}}},
            }}

    # 'show ip ospf database router detail vrf all'
    ShowIpOspfDatabaseRouterDetailVrfAll = {
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
                                                                                                {'metric': 111,
                                                                                                'mt_id': 0,
                                                                                                'tos': 0}},
                                                                                        'type': 'transit network'},
                                                                                    '10.151.22.22': 
                                                                                        {'link_data': '0.0.0.14',
                                                                                        'link_id': '10.151.22.22',
                                                                                        'num_tos_metrics': 0,
                                                                                        'topologies': 
                                                                                            {0: 
                                                                                                {'metric': 1,
                                                                                                'mt_id': 0,
                                                                                                'tos': 0}},
                                                                                        'type': 'router (point-to-point)'}},
                                                                                'num_of_links': 2}},
                                                                    'header': 
                                                                        {'adv_router': '10.229.11.11',
                                                                        'age': 646,
                                                                        'checksum': '0x9ae4',
                                                                        'length': 48,
                                                                        'lsa_id': '10.229.11.11',
                                                                        'option': '0x22',
                                                                        'option_desc': 'No TOS-capability, DC',
                                                                        'seq_num': '0x8000003f',
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
                                                                                        {'mt_id': 0}},
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
                                                                    'age': 723,
                                                                    'checksum': '0x6029',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': '0x22',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x8000003e',
                                                                    'type': 1}}}}}}}}}}}}}}}}
    ShowIpOspfDatabaseRouterDetailVrfAll_custom = {
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
                                                                                                {'metric': 111,
                                                                                                'mt_id': 0,
                                                                                                'tos': 0}},
                                                                                        'type': 'transit network'},
                                                                                    '10.151.22.22':
                                                                                        {'link_data': '0.0.0.14',
                                                                                        'link_id': '10.151.22.22',
                                                                                        'num_tos_metrics': 0,
                                                                                        'topologies':
                                                                                            {0:
                                                                                                {'metric': 1,
                                                                                                'mt_id': 0,
                                                                                                'tos': 0}},
                                                                                        'type': 'router (point-to-point)'}},
                                                                                'num_of_links': 2}},
                                                                    'header':
                                                                        {'adv_router': '10.229.11.11',
                                                                        'age': 646,
                                                                        'checksum': '0x9ae4',
                                                                        'length': 48,
                                                                        'lsa_id': '10.229.11.11',
                                                                        'option': '0x22',
                                                                        'option_desc': 'No TOS-capability, DC',
                                                                        'seq_num': '0x8000003f',
                                                                        'type': 1}}}}}}}}}}}}}}}}

    # 'show ip ospf database opaque-area detail vrf all'
    ShowIpOspfDatabaseOpaqueAreaDetailVrfAll = {
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
                                                        {'10.1.0.6 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.6',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
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
                                                                                'unknown_tlvs': 
                                                                                    {1: 
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2: {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '0 '
                                                                                                '0 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00'}},
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
                                                                'age': 113,
                                                                'checksum': '0x03ed',
                                                                'fragment_number': 6,
                                                                'length': 160,
                                                                'lsa_id': '10.1.0.6',
                                                                'num_links': 1,
                                                                'opaque_id': 6,
                                                                'opaque_type': 1,
                                                                'option': '0x20',
                                                                'option_desc': 'No TOS-capability, DC',
                                                                'seq_num': '0x80000003',
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
                                                        {'10.1.0.4 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'link_id': '10.3.4.4',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.3.4.3': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': 
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'unknown_tlvs': 
                                                                                    {1: 
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2: {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '0 '
                                                                                                '0 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00'}},
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
                                                                    'age': 113,
                                                                    'checksum': '0x8f5e',
                                                                    'fragment_number': 4,
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.4',
                                                                    'num_links': 1,
                                                                    'opaque_id': 4,
                                                                    'opaque_type': 1,
                                                                    'option': '0x20',
                                                                    'option_desc': 'No TOS-capability, DC',
                                                                    'seq_num': '0x80000003',
                                                                    'type': 10}}}}}}}}}}}}}}}}
    ShowIpOspfDatabaseOpaqueAreaDetailVrfAll_custom = {
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
                                                        {'10.1.0.6 10.36.3.3':
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.6',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'opaque':
                                                                        {'link_tlvs':
                                                                            {1:
                                                                                {'admin_group': '0x0',
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
                                                                                'unknown_tlvs':
                                                                                    {1:
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2: {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '0 '
                                                                                                '0 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00 '
                                                                                                '00'}},
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
                                                                'age': 113,
                                                                'checksum': '0x03ed',
                                                                'fragment_number': 6,
                                                                'length': 160,
                                                                'lsa_id': '10.1.0.6',
                                                                'num_links': 1,
                                                                'opaque_id': 6,
                                                                'opaque_type': 1,
                                                                'option': '0x20',
                                                                'option_desc': 'No TOS-capability, DC',
                                                                'seq_num': '0x80000003',
                                                                'type': 10}}}}}}}}}}}}}},
           }}
    # ==========================================================================
    #                               OSPF INFO 
    # ==========================================================================

    OspfInfo = {
        'feature_ospf': True,
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
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
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22': 
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'topologies': 
                                                                                    {0: 
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header': 
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 646,
                                                                    'checksum': '0x9ae4',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x8000003f',
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
                                                                    'age': 1454,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000033',
                                                                    'type': 2}}}}},
                                                3: 
                                                    {'lsa_type': 3,
                                                    'lsas': 
                                                        {'10.1.2.0 10.16.2.2': 
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.2.0',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'summary': 
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies': 
                                                                            {0: 
                                                                                {'metric': 4294,
                                                                                'mt_id': 0}}}},
                                                                'header': 
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 788,
                                                                    'checksum': '0xfc54',
                                                                    'length': 28,
                                                                    'lsa_id': '10.1.2.0',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000001',
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
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000002',
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
                                                                                {'admin_group': '0x0',
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
                                                                                'unknown_tlvs': 
                                                                                    {1: 
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2: 
                                                                                        {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 00 00 00 00 0 0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'}},
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
                                                                    'age': 113,
                                                                    'checksum': '0x03ed',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.6',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000003',
                                                                    'type': 10}}}}}}},
                                        'interfaces': 
                                            {'Ethernet2/1': 
                                                {'bdr_ip_addr': '10.229.6.2',
                                                'bdr_router_id': '10.151.22.22',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 40,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.229.6.6',
                                                'dr_router_id': '10.84.66.66',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'interface_type': 'broadcast',
                                                'name': 'Ethernet2/1',
                                                'neighbors': 
                                                    {'10.84.66.66': 
                                                        {'address': '10.229.6.6',
                                                        'bdr_ip_addr': '10.229.6.2',
                                                        'dead_timer': '00:00:38',
                                                        'dr_ip_addr': '10.229.6.6',
                                                        'last_state_change': '08:38:39',
                                                        'neighbor_router_id': '10.84.66.66',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': {'link_scope_lsa_cksum_sum': 0,
                                                             'link_scope_lsa_count': 0},
                                                'transmit_delay': 1}},
                                        'mpls': 
                                            {'ldp': 
                                                {'auto_config': False,
                                                'sync': False}},
                                        'ranges': 
                                            {'10.4.0.0/16': 
                                                {'advertise': False,
                                                'cost': 31,
                                                'prefix': '10.4.0.0/16'}},
                                        'sham_links': 
                                            {'10.151.22.22 10.229.11.11': 
                                                {'cost': 1,
                                                'dead_interval': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:02',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL1',
                                                'neighbors': 
                                                    {'10.229.11.11': 
                                                        {'address': '10.229.11.11',
                                                        'dead_timer': '00:00:41',
                                                        'neighbor_router_id': '10.229.11.11',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 8}}},
                                                'remote_id': '10.229.11.11',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1},
                                            '10.151.22.22 10.21.33.33': 
                                                {'authentication': 
                                                    {'auth_trailer_key': 
                                                        {'crypto_algorithm': 'Simple'},
                                                    'auth_trailer_key_chain': 
                                                        {'key_chain': 'test'}},
                                                'cost': 111,
                                                'dead_interval': 13,
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:01',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL2',
                                                'remote_id': '10.21.33.33',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '11',
                                            'area_scope_lsa_count': 11,
                                            'spf_runs_count': 33},
                                        'virtual_links': 
                                            {'0.0.0.1 10.1.8.8': 
                                                {'cost': 40,
                                                'dead_interval': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:05',
                                                'name': 'VL1',
                                                'neighbors': 
                                                    {'10.1.8.8': 
                                                        {'address': '10.19.4.4',
                                                        'dead_timer': '00:00:43',
                                                        'neighbor_router_id': '10.1.8.8',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}},
                                                'retransmit_interval': 5,
                                                'router_id': '10.1.8.8',
                                                'state': 'point_to_point',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1}}}},
                                'auto_cost': 
                                    {'enable': False,
                                    'reference_bandwidth': 40000},
                                'enable': True,
                                'graceful_restart': 
                                    {'ietf': 
                                        {'enable': True,
                                        'restart_interval': 60,
                                        'type': 'ietf'}},
                                'nsr': 
                                    {'enable': True},
                                'preference': 
                                    {'single_value': 
                                        {'all': 110}},
                                'router_id': '10.151.22.22',
                                'spf_control': 
                                    {'paths': 8,
                                    'throttle': 
                                        {'lsa': 
                                            {'hold': 5000,
                                            'maximum': 5000,
                                            'start': 0.0},
                                        'spf': 
                                            {'hold': 1000,
                                            'maximum': 5000,
                                            'start': 200}}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'instance': 
                            {'1': 
                                {'areas': 
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
                                                                                        {'mt_id': 0}},
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
                                                                    'age': 723,
                                                                    'checksum': '0x6029',
                                                                    'length': 60,
                                                                    'lsa_id': '10.4.1.1',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x8000003e',
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
                                                                    'age': 772,
                                                                    'checksum': '0x3bd1',
                                                                    'length': 32,
                                                                    'lsa_id': '10.1.2.1',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000010',
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
                                                                    'age': 694,
                                                                    'checksum': '0x43dc',
                                                                    'length': 28,
                                                                    'lsa_id': '10.186.3.0',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000001',
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
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.94.44.44',
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000002',
                                                                    'type': 5}}}}},
                                                10: 
                                                    {'lsa_type': 10,
                                                    'lsas': 
                                                        {'10.1.0.4 10.36.3.3': 
                                                            {'adv_router': '10.36.3.3',
                                                            'lsa_id': '10.1.0.4',
                                                            'ospfv2': 
                                                                {'body': 
                                                                    {'opaque': 
                                                                        {'link_tlvs': 
                                                                            {1: 
                                                                                {'admin_group': '0x0',
                                                                                'link_id': '10.3.4.4',
                                                                                'link_name': 'broadcast network',
                                                                                'link_type': 2,
                                                                                'local_if_ipv4_addrs': 
                                                                                    {'10.3.4.3': {}},
                                                                                'max_bandwidth': 125000000,
                                                                                'max_reservable_bandwidth': 93750000,
                                                                                'remote_if_ipv4_addrs': 
                                                                                    {'0.0.0.0': {}},
                                                                                'te_metric': 1,
                                                                                'unknown_tlvs': 
                                                                                    {1: 
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2: 
                                                                                        {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 00 00 00 00 0 0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'}},
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
                                                                    'age': 113,
                                                                    'checksum': '0x8f5e',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.4',
                                                                    'opaque_id': 4,
                                                                    'opaque_type': 1,
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000003',
                                                                    'type': 10}}}}}}},
                                        'interfaces': 
                                            {'Ethernet2/2': 
                                                {'bdr_ip_addr': '10.2.3.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.2.3.3',
                                                'dr_router_id': '10.36.3.3',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:02',
                                                'interface_type': 'broadcast',
                                                'name': 'Ethernet2/2',
                                                'neighbors': 
                                                    {'10.36.3.3': 
                                                        {'address': '10.2.3.3',
                                                        'bdr_ip_addr': '10.2.3.2',
                                                        'dead_timer': '00:00:39',
                                                        'dr_ip_addr': '10.2.3.3',
                                                        'last_state_change': '08:38:40',
                                                        'neighbor_router_id': '10.36.3.3',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transmit_delay': 1},
                                            'Ethernet2/3': 
                                                {'bdr_ip_addr': '10.2.4.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.2.4.4',
                                                'dr_router_id': '10.64.4.4',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'interface_type': 'broadcast',
                                                'name': 'Ethernet2/3',
                                                'neighbors': 
                                                    {'10.64.4.4': 
                                                        {'address': '10.2.4.4',
                                                        'bdr_ip_addr': '10.2.4.2',
                                                        'dead_timer': '00:00:33',
                                                        'dr_ip_addr': '10.2.4.4',
                                                        "last_state_change": "08:38:42",
                                                        'neighbor_router_id': '10.64.4.4',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 6}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transmit_delay': 1},
                                            'Ethernet2/4': 
                                                {'bdr_ip_addr': '10.1.2.2',
                                                'bdr_router_id': '10.16.2.2',
                                                'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.1.2.1',
                                                'dr_router_id': '10.4.1.1',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:00',
                                                'interface_type': 'broadcast',
                                                'name': 'Ethernet2/4',
                                                'neighbors': 
                                                    {'10.4.1.1': 
                                                        {'address': '10.1.2.1',
                                                        'bdr_ip_addr': '10.1.2.2',
                                                        'dead_timer': '00:00:35',
                                                        'dr_ip_addr': '10.1.2.1',
                                                        'last_state_change': '08:38:41',
                                                        'neighbor_router_id': '10.4.1.1',
                                                        'state': 'full',
                                                        'statistics': 
                                                            {'nbr_event_count': 5}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': 
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transmit_delay': 1},
                                            'loopback0': 
                                                {'bfd': 
                                                    {'enable': False},
                                                'cost': 1,
                                                'enable': True,
                                                'interface_type': 'loopback',
                                                'name': 'loopback0',
                                                'state': 'loopback'}},
                                        'mpls': 
                                            {'ldp': 
                                                {'auto_config': False,
                                                'sync': False}},
                                        'ranges': 
                                            {'10.4.1.0/24': 
                                                {'advertise': True,
                                                'cost': 33,
                                                'prefix': '10.4.1.0/24'}},
                                        'statistics': 
                                            {'area_scope_lsa_cksum_sum': '19',
                                            'area_scope_lsa_count': 19,
                                            'spf_runs_count': 8}}},
                                'auto_cost': 
                                    {'enable': False,
                                    'reference_bandwidth': 40000},
                                'bfd': 
                                    {'enable': True},
                                'database_control': 
                                    {'max_lsa': 123},
                                'enable': True,
                                'graceful_restart': 
                                    {'ietf': 
                                        {'enable': True,
                                        'restart_interval': 60,
                                        'type': 'ietf'}},
                                'nsr': 
                                    {'enable': True},
                                'preference': 
                                    {'single_value': 
                                        {'all': 110}},
                                'router_id': '10.16.2.2',
                                'spf_control': 
                                    {'paths': 8,
                                    'throttle': 
                                        {'lsa': 
                                            {'hold': 5000,
                                            'maximum': 5000,
                                            'start': 0.0},
                                        'spf': 
                                            {'hold': 1000,
                                            'maximum': 5000,
                                            'start': 200}}},
                                'stub_router': 
                                    {'always': 
                                        {'always': True}}}}}}}}}
    OspfInfo_custom = {
        'feature_ospf': True,
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4':
                        {'instance':
                            {'1':
                                {'areas':
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
                                                                                        {'metric': 111,
                                                                                        'mt_id': 0}},
                                                                                'type': 'transit network'},
                                                                            '10.151.22.22':
                                                                                {'link_data': '0.0.0.14',
                                                                                'link_id': '10.151.22.22',
                                                                                'topologies':
                                                                                    {0:
                                                                                        {'metric': 1,
                                                                                        'mt_id': 0}},
                                                                                'type': 'router (point-to-point)'}},
                                                                        'num_of_links': 2}},
                                                                'header':
                                                                    {'adv_router': '10.229.11.11',
                                                                    'age': 646,
                                                                    'checksum': '0x9ae4',
                                                                    'length': 48,
                                                                    'lsa_id': '10.229.11.11',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x8000003f',
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
                                                                    'age': 1454,
                                                                    'checksum': '0xddd9',
                                                                    'length': 32,
                                                                    'lsa_id': '10.186.5.1',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000033',
                                                                    'type': 2}}}}},
                                                3:
                                                    {'lsa_type': 3,
                                                    'lsas':
                                                        {'10.1.2.0 10.16.2.2':
                                                            {'adv_router': '10.16.2.2',
                                                            'lsa_id': '10.1.2.0',
                                                            'ospfv2':
                                                                {'body':
                                                                    {'summary':
                                                                        {'network_mask': '255.255.255.0',
                                                                        'topologies':
                                                                            {0:
                                                                                {'metric': 4294,
                                                                                'mt_id': 0}}}},
                                                                'header':
                                                                    {'adv_router': '10.16.2.2',
                                                                    'age': 788,
                                                                    'checksum': '0xfc54',
                                                                    'length': 28,
                                                                    'lsa_id': '10.1.2.0',
                                                                    'option': '0x22',
                                                                    'seq_num': '0x80000001',
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
                                                                    'age': 1565,
                                                                    'checksum': '0x7d61',
                                                                    'length': 36,
                                                                    'lsa_id': '10.21.33.33',
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000002',
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
                                                                                {'admin_group': '0x0',
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
                                                                                'unknown_tlvs':
                                                                                    {1:
                                                                                        {'length': 4,
                                                                                        'type': 32770,
                                                                                        'value': '00 00 00 01'},
                                                                                    2:
                                                                                        {'length': 32,
                                                                                        'type': 32771,
                                                                                        'value': '00 00 00 00 00 0 0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'}},
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
                                                                    'age': 113,
                                                                    'checksum': '0x03ed',
                                                                    'length': 160,
                                                                    'lsa_id': '10.1.0.6',
                                                                    'opaque_id': 6,
                                                                    'opaque_type': 1,
                                                                    'option': '0x20',
                                                                    'seq_num': '0x80000003',
                                                                    'type': 10}}}}}}},
                                        'interfaces':
                                            {'Ethernet2/1':
                                                {'bdr_ip_addr': '10.229.6.2',
                                                'bdr_router_id': '10.151.22.22',
                                                'bfd':
                                                    {'enable': False},
                                                'cost': 40,
                                                'dead_interval': 40,
                                                'dr_ip_addr': '10.229.6.6',
                                                'dr_router_id': '10.84.66.66',
                                                'enable': True,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:07',
                                                'interface_type': 'broadcast',
                                                'name': 'Ethernet2/1',
                                                'neighbors':
                                                    {'10.84.66.66':
                                                        {'address': '10.229.6.6',
                                                        'bdr_ip_addr': '10.229.6.2',
                                                        'dead_timer': '00:00:38',
                                                        'dr_ip_addr': '10.229.6.6',
                                                        'last_state_change': '08:38:39',
                                                        'neighbor_router_id': '10.84.66.66',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 6}}},
                                                'passive': False,
                                                'priority': 1,
                                                'retransmit_interval': 5,
                                                'state': 'bdr',
                                                'statistics': {'link_scope_lsa_cksum_sum': 0,
                                                             'link_scope_lsa_count': 0},
                                                'transmit_delay': 1}},
                                        'mpls':
                                            {'ldp':
                                                {'auto_config': False,
                                                'sync': False}},
                                        'ranges':
                                            {'10.4.0.0/16':
                                                {'advertise': False,
                                                'cost': 31,
                                                'prefix': '10.4.0.0/16'}},
                                        'sham_links':
                                            {'10.151.22.22 10.229.11.11':
                                                {'cost': 1,
                                                'dead_interval': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:02',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL1',
                                                'neighbors':
                                                    {'10.229.11.11':
                                                        {'address': '10.229.11.11',
                                                        'dead_timer': '00:00:41',
                                                        'neighbor_router_id': '10.229.11.11',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 8}}},
                                                'remote_id': '10.229.11.11',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1},
                                            '10.151.22.22 10.21.33.33':
                                                {'authentication':
                                                    {'auth_trailer_key':
                                                        {'crypto_algorithm': 'Simple'},
                                                    'auth_trailer_key_chain':
                                                        {'key_chain': 'test'}},
                                                'cost': 111,
                                                'dead_interval': 13,
                                                'hello_interval': 3,
                                                'hello_timer': '00:00:01',
                                                'local_id': '10.151.22.22',
                                                'name': 'SL2',
                                                'remote_id': '10.21.33.33',
                                                'retransmit_interval': 5,
                                                'state': 'point_to_point',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 7}},
                                        'statistics':
                                            {'area_scope_lsa_cksum_sum': '11',
                                            'area_scope_lsa_count': 11,
                                            'spf_runs_count': 33},
                                        'virtual_links':
                                            {'0.0.0.1 10.1.8.8':
                                                {'cost': 40,
                                                'dead_interval': 40,
                                                'hello_interval': 10,
                                                'hello_timer': '00:00:05',
                                                'name': 'VL1',
                                                'neighbors':
                                                    {'10.1.8.8':
                                                        {'address': '10.19.4.4',
                                                        'dead_timer': '00:00:43',
                                                        'neighbor_router_id': '10.1.8.8',
                                                        'state': 'full',
                                                        'statistics':
                                                            {'nbr_event_count': 5}}},
                                                'retransmit_interval': 5,
                                                'router_id': '10.1.8.8',
                                                'state': 'point_to_point',
                                                'statistics':
                                                    {'link_scope_lsa_cksum_sum': 0,
                                                    'link_scope_lsa_count': 0},
                                                'transit_area_id': '0.0.0.1',
                                                'transmit_delay': 1}}}},
                                'auto_cost':
                                    {'enable': False,
                                    'reference_bandwidth': 40000},
                                'enable': True,
                                'graceful_restart':
                                    {'ietf':
                                        {'enable': True,
                                        'restart_interval': 60,
                                        'type': 'ietf'}},
                                'nsr':
                                    {'enable': True},
                                'preference':
                                    {'single_value':
                                        {'all': 110}},
                                'router_id': '10.151.22.22',
                                'spf_control':
                                    {'paths': 8,
                                    'throttle':
                                        {'lsa':
                                            {'hold': 5000,
                                            'maximum': 5000,
                                            'start': 0.0},
                                        'spf':
                                            {'hold': 1000,
                                            'maximum': 5000,
                                            'start': 200}}}}}}}},
            }}
