''' 
BGP Genie Ops Object Outputs for IOSXE.
'''


class BgpOutput(object):

    ShowBgpAllSummary = {
        'bgp_id': 100,
        'vrf':
            {'default':
                {'neighbor': {'10.4.6.6': {'address_family': {'vpnv4 unicast': {'activity_paths': '120/30',
                                                                                    'activity_prefixes': '85/25',
                                                                                    'as': 300,
                                                                                    'attribute_entries': '6/4',
                                                                                    'bgp_table_version': 1,
                                                                                    'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                      'total_entries': 0},
                                                                                                      'route-map': {'memory_usage': 0,
                                                                                                                    'total_entries': 0}},
                                                                                    'community_entries': {'memory_usage': 96,
                                                                                                          'total_entries': 4},
                                                                                    'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                            'total_entries': 3},
                                                                                                'rrinfo': {'memory_usage': 48,
                                                                                                           'total_entries': 2}},
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 68,
                                                                                    'msg_sent': 75,
                                                                                    'output_queue': 0,
                                                                                    'path': {'memory_usage': 3600,
                                                                                             'total_entries': 45},
                                                                                    'prefixes': {'memory_usage': 4560,
                                                                                                 'total_entries': 30},
                                                                                    'route_identifier': '4.4.4.4',
                                                                                    'routing_table_version': 56,
                                                                                    'scan_interval': 60,
                                                                                    'state_pfxrcd': '5',
                                                                                    'tbl_ver': 1,
                                                                                    'total_memory': 9384,
                                                                                    'up_down': '01:03:23',
                                                                                    'version': 4}}},
                                  '2.2.2.2': {'address_family': {'vpnv4 unicast': {'activity_paths': '120/30',
                                                                                   'activity_prefixes': '85/25',
                                                                                   'as': 100,
                                                                                   'attribute_entries': '6/4',
                                                                                   'bgp_table_version': 1,
                                                                                   'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                     'total_entries': 0},
                                                                                                     'route-map': {'memory_usage': 0,
                                                                                                                   'total_entries': 0}},
                                                                                   'community_entries': {'memory_usage': 96,
                                                                                                         'total_entries': 4},
                                                                                   'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                           'total_entries': 3},
                                                                                               'rrinfo': {'memory_usage': 48,
                                                                                                          'total_entries': 2}},
                                                                                   'input_queue': 0,
                                                                                   'local_as': 100,
                                                                                   'msg_rcvd': 82,
                                                                                   'msg_sent': 88,
                                                                                   'output_queue': 0,
                                                                                   'path': {'memory_usage': 3600,
                                                                                            'total_entries': 45},
                                                                                   'prefixes': {'memory_usage': 4560,
                                                                                                'total_entries': 30},
                                                                                   'route_identifier': '4.4.4.4',
                                                                                   'routing_table_version': 56,
                                                                                   'scan_interval': 60,
                                                                                   'state_pfxrcd': '10',
                                                                                   'tbl_ver': 1,
                                                                                   'total_memory': 9384,
                                                                                   'up_down': '01:12:00',
                                                                                   'version': 4},
                                                                 'vpnv6 unicast': {'activity_paths': '120/30',
                                                                                   'activity_prefixes': '85/25',
                                                                                   'as': 100,
                                                                                   'attribute_entries': '6/4',
                                                                                   'bgp_table_version': 1,
                                                                                   'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                     'total_entries': 0},
                                                                                                     'route-map': {'memory_usage': 0,
                                                                                                                   'total_entries': 0}},
                                                                                   'community_entries': {'memory_usage': 96,
                                                                                                         'total_entries': 4},
                                                                                   'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                           'total_entries': 3},
                                                                                               'rrinfo': {'memory_usage': 48,
                                                                                                          'total_entries': 2}},
                                                                                   'input_queue': 0,
                                                                                   'local_as': 100,
                                                                                   'msg_rcvd': 82,
                                                                                   'msg_sent': 88,
                                                                                   'output_queue': 0,
                                                                                   'path': {'memory_usage': 4860,
                                                                                            'total_entries': 45},
                                                                                   'prefixes': {'memory_usage': 5280,
                                                                                                'total_entries': 30},
                                                                                   'route_identifier': '4.4.4.4',
                                                                                   'routing_table_version': 66,
                                                                                   'scan_interval': 60,
                                                                                   'state_pfxrcd': '10',
                                                                                   'tbl_ver': 1,
                                                                                   'total_memory': 11364,
                                                                                   'up_down': '01:12:00',
                                                                                   'version': 4}}},
                                  '20.4.6.6': {'address_family': {'vpnv4 unicast': {'activity_paths': '120/30',
                                                                                    'activity_prefixes': '85/25',
                                                                                    'as': 400,
                                                                                    'attribute_entries': '6/4',
                                                                                    'bgp_table_version': 1,
                                                                                    'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                      'total_entries': 0},
                                                                                                      'route-map': {'memory_usage': 0,
                                                                                                                    'total_entries': 0}},
                                                                                    'community_entries': {'memory_usage': 96,
                                                                                                          'total_entries': 4},
                                                                                    'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                            'total_entries': 3},
                                                                                                'rrinfo': {'memory_usage': 48,
                                                                                                           'total_entries': 2}},
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 67,
                                                                                    'msg_sent': 72,
                                                                                    'output_queue': 0,
                                                                                    'path': {'memory_usage': 3600,
                                                                                             'total_entries': 45},
                                                                                    'prefixes': {'memory_usage': 4560,
                                                                                                 'total_entries': 30},
                                                                                    'route_identifier': '4.4.4.4',
                                                                                    'routing_table_version': 56,
                                                                                    'scan_interval': 60,
                                                                                    'state_pfxrcd': '5',
                                                                                    'tbl_ver': 1,
                                                                                    'total_memory': 9384,
                                                                                    'up_down': '01:03:14',
                                                                                    'version': 4}}},
                                  '200.0.1.1': {'address_family': {'ipv4 unicast': {'activity_paths': '66/39',
                                                                                    'activity_prefixes': '47/20',
                                                                                    'as': 100,
                                                                                    'attribute_entries': '1/1',
                                                                                    'bgp_table_version': 28,
                                                                                    'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                      'total_entries': 0},
                                                                                                      'route-map': {'memory_usage': 0,
                                                                                                                    'total_entries': 0}},
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 0,
                                                                                    'msg_sent': 0,
                                                                                    'output_queue': 0,
                                                                                    'path': {'memory_usage': 3672,
                                                                                             'total_entries': 27},
                                                                                    'prefixes': {'memory_usage': 6696,
                                                                                                 'total_entries': 27},
                                                                                    'route_identifier': '200.0.1.1',
                                                                                    'routing_table_version': 28,
                                                                                    'scan_interval': 60,
                                                                                    'state_pfxrcd': 'Idle',
                                                                                    'tbl_ver': 1,
                                                                                    'total_memory': 10648,
                                                                                    'up_down': '01:07:38',
                                                                                    'version': 4}}},
                                  '200.0.2.1': {'address_family': {'ipv4 unicast': {'activity_paths': '66/39',
                                                                                    'activity_prefixes': '47/20',
                                                                                    'as': 100,
                                                                                    'attribute_entries': '1/1',
                                                                                    'bgp_table_version': 28,
                                                                                    'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                      'total_entries': 0},
                                                                                                      'route-map': {'memory_usage': 0,
                                                                                                                    'total_entries': 0}},
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 0,
                                                                                    'msg_sent': 0,
                                                                                    'output_queue': 0,
                                                                                    'path': {'memory_usage': 3672,
                                                                                             'total_entries': 27},
                                                                                    'prefixes': {'memory_usage': 6696,
                                                                                                 'total_entries': 27},
                                                                                    'route_identifier': '200.0.1.1',
                                                                                    'routing_table_version': 28,
                                                                                    'scan_interval': 60,
                                                                                    'state_pfxrcd': 'Idle',
                                                                                    'tbl_ver': 1,
                                                                                    'total_memory': 10648,
                                                                                    'up_down': 'never',
                                                                                    'version': 4}}},
                                  '200.0.4.1': {'address_family': {'ipv4 unicast': {'activity_paths': '66/39',
                                                                                    'activity_prefixes': '47/20',
                                                                                    'as': 100,
                                                                                    'attribute_entries': '1/1',
                                                                                    'bgp_table_version': 28,
                                                                                    'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                      'total_entries': 0},
                                                                                                      'route-map': {'memory_usage': 0,
                                                                                                                    'total_entries': 0}},
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 0,
                                                                                    'msg_sent': 0,
                                                                                    'output_queue': 0,
                                                                                    'path': {'memory_usage': 3672,
                                                                                             'total_entries': 27},
                                                                                    'prefixes': {'memory_usage': 6696,
                                                                                                 'total_entries': 27},
                                                                                    'route_identifier': '200.0.1.1',
                                                                                    'routing_table_version': 28,
                                                                                    'scan_interval': 60,
                                                                                    'state_pfxrcd': 'Idle',
                                                                                    'tbl_ver': 1,
                                                                                    'total_memory': 10648,
                                                                                    'up_down': '01:07:38',
                                                                                    'version': 4}}},
                                  '2000::1:1': {'address_family': {'ipv6 unicast': {'as': 100,
                                                                                    'bgp_table_version': 1,
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 0,
                                                                                    'msg_sent': 0,
                                                                                    'output_queue': 0,
                                                                                    'route_identifier': '200.0.1.1',
                                                                                    'routing_table_version': 1,
                                                                                    'state_pfxrcd': 'Idle',
                                                                                    'tbl_ver': 1,
                                                                                    'up_down': '01:07:38',
                                                                                    'version': 4}}},
                                  '2000::4:1': {'address_family': {'ipv6 unicast': {'as': 100,
                                                                                    'bgp_table_version': 1,
                                                                                    'input_queue': 0,
                                                                                    'local_as': 100,
                                                                                    'msg_rcvd': 0,
                                                                                    'msg_sent': 0,
                                                                                    'output_queue': 0,
                                                                                    'route_identifier': '200.0.1.1',
                                                                                    'routing_table_version': 1,
                                                                                    'state_pfxrcd': 'Idle',
                                                                                    'tbl_ver': 1,
                                                                                    'up_down': '01:07:38',
                                                                                    'version': 4}}},
                                  '2001::14:4': {'address_family': {'ipv6 unicast': {'as': 200,
                                                                                     'bgp_table_version': 1,
                                                                                     'input_queue': 0,
                                                                                     'local_as': 100,
                                                                                     'msg_rcvd': 0,
                                                                                     'msg_sent': 0,
                                                                                     'output_queue': 0,
                                                                                     'route_identifier': '200.0.1.1',
                                                                                     'routing_table_version': 1,
                                                                                     'state_pfxrcd': 'Idle',
                                                                                     'tbl_ver': 1,
                                                                                     'up_down': 'never',
                                                                                     'version': 4}}},
                                  '2001::26:2': {'address_family': {'ipv6 unicast': {'as': 300,
                                                                                     'bgp_table_version': 1,
                                                                                     'input_queue': 0,
                                                                                     'local_as': 100,
                                                                                     'msg_rcvd': 0,
                                                                                     'msg_sent': 0,
                                                                                     'output_queue': 0,
                                                                                     'route_identifier': '200.0.1.1',
                                                                                     'routing_table_version': 1,
                                                                                     'state_pfxrcd': 'Idle',
                                                                                     'tbl_ver': 1,
                                                                                     'up_down': '01:07:38',
                                                                                     'version': 4}}},
                                  '2001:DB8:20:4:6::6': {'address_family': {'vpnv6 unicast': {'activity_paths': '120/30',
                                                                                              'activity_prefixes': '85/25',
                                                                                              'as': 400,
                                                                                              'attribute_entries': '6/4',
                                                                                              'bgp_table_version': 66,
                                                                                              'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                                'total_entries': 0},
                                                                                                                'route-map': {'memory_usage': 0,
                                                                                                                              'total_entries': 0}},
                                                                                              'community_entries': {'memory_usage': 96,
                                                                                                                    'total_entries': 4},
                                                                                              'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                                      'total_entries': 3},
                                                                                                          'rrinfo': {'memory_usage': 48,
                                                                                                                     'total_entries': 2}},
                                                                                              'input_queue': 0,
                                                                                              'local_as': 100,
                                                                                              'msg_rcvd': 67,
                                                                                              'msg_sent': 73,
                                                                                              'output_queue': 0,
                                                                                              'path': {'memory_usage': 4860,
                                                                                                       'total_entries': 45},
                                                                                              'prefixes': {'memory_usage': 5280,
                                                                                                           'total_entries': 30},
                                                                                              'route_identifier': '4.4.4.4',
                                                                                              'routing_table_version': 66,
                                                                                              'scan_interval': 60,
                                                                                              'state_pfxrcd': '5',
                                                                                              'tbl_ver': 1,
                                                                                              'total_memory': 11364,
                                                                                              'up_down': '01:03:11',
                                                                                              'version': 4}}},
                                  '2001:DB8:4:6::6': {'address_family': {'vpnv6 unicast': {'activity_paths': '120/30',
                                                                                           'activity_prefixes': '85/25',
                                                                                           'as': 300,
                                                                                           'attribute_entries': '6/4',
                                                                                           'bgp_table_version': 1,
                                                                                           'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                             'total_entries': 0},
                                                                                                             'route-map': {'memory_usage': 0,
                                                                                                                           'total_entries': 0}},
                                                                                           'community_entries': {'memory_usage': 96,
                                                                                                                 'total_entries': 4},
                                                                                           'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                                   'total_entries': 3},
                                                                                                       'rrinfo': {'memory_usage': 48,
                                                                                                                  'total_entries': 2}},
                                                                                           'input_queue': 0,
                                                                                           'local_as': 100,
                                                                                           'msg_rcvd': 67,
                                                                                           'msg_sent': 75,
                                                                                           'output_queue': 0,
                                                                                           'path': {'memory_usage': 4860,
                                                                                                    'total_entries': 45},
                                                                                           'prefixes': {'memory_usage': 5280,
                                                                                                        'total_entries': 30},
                                                                                           'route_identifier': '4.4.4.4',
                                                                                           'routing_table_version': 66,
                                                                                           'scan_interval': 60,
                                                                                           'state_pfxrcd': '5',
                                                                                           'tbl_ver': 1,
                                                                                           'total_memory': 11364,
                                                                                           'up_down': '01:03:19',
                                                                                           'version': 4}}},
                                  '201.0.14.4': {'address_family': {'ipv4 unicast': {'activity_paths': '66/39',
                                                                                     'activity_prefixes': '47/20',
                                                                                     'as': 200,
                                                                                     'attribute_entries': '1/1',
                                                                                     'bgp_table_version': 28,
                                                                                     'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                       'total_entries': 0},
                                                                                                       'route-map': {'memory_usage': 0,
                                                                                                                     'total_entries': 0}},
                                                                                     'input_queue': 0,
                                                                                     'local_as': 100,
                                                                                     'msg_rcvd': 0,
                                                                                     'msg_sent': 0,
                                                                                     'output_queue': 0,
                                                                                     'path': {'memory_usage': 3672,
                                                                                              'total_entries': 27},
                                                                                     'prefixes': {'memory_usage': 6696,
                                                                                                  'total_entries': 27},
                                                                                     'route_identifier': '200.0.1.1',
                                                                                     'routing_table_version': 28,
                                                                                     'scan_interval': 60,
                                                                                     'state_pfxrcd': 'Idle',
                                                                                     'tbl_ver': 1,
                                                                                     'total_memory': 10648,
                                                                                     'up_down': 'never',
                                                                                     'version': 4}}},
                                  '201.0.26.2': {'address_family': {'ipv4 unicast': {'activity_paths': '66/39',
                                                                                     'activity_prefixes': '47/20',
                                                                                     'as': 300,
                                                                                     'attribute_entries': '1/1',
                                                                                     'bgp_table_version': 28,
                                                                                     'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                       'total_entries': 0},
                                                                                                       'route-map': {'memory_usage': 0,
                                                                                                                     'total_entries': 0}},
                                                                                     'input_queue': 0,
                                                                                     'local_as': 100,
                                                                                     'msg_rcvd': 0,
                                                                                     'msg_sent': 0,
                                                                                     'output_queue': 0,
                                                                                     'path': {'memory_usage': 3672,
                                                                                              'total_entries': 27},
                                                                                     'prefixes': {'memory_usage': 6696,
                                                                                                  'total_entries': 27},
                                                                                     'route_identifier': '200.0.1.1',
                                                                                     'routing_table_version': 28,
                                                                                     'scan_interval': 60,
                                                                                     'state_pfxrcd': 'Idle',
                                                                                     'tbl_ver': 1,
                                                                                     'total_memory': 10648,
                                                                                     'up_down': '01:07:38',
                                                                                     'version': 4}}},
                                  '3.3.3.3': {'address_family': {'vpnv4 unicast': {'activity_paths': '120/30',
                                                                                   'activity_prefixes': '85/25',
                                                                                   'as': 100,
                                                                                   'attribute_entries': '6/4',
                                                                                   'bgp_table_version': 1,
                                                                                   'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                     'total_entries': 0},
                                                                                                     'route-map': {'memory_usage': 0,
                                                                                                                   'total_entries': 0}},
                                                                                   'community_entries': {'memory_usage': 96,
                                                                                                         'total_entries': 4},
                                                                                   'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                           'total_entries': 3},
                                                                                               'rrinfo': {'memory_usage': 48,
                                                                                                          'total_entries': 2}},
                                                                                   'input_queue': 0,
                                                                                   'local_as': 100,
                                                                                   'msg_rcvd': 0,
                                                                                   'msg_sent': 0,
                                                                                   'output_queue': 0,
                                                                                   'path': {'memory_usage': 3600,
                                                                                            'total_entries': 45},
                                                                                   'prefixes': {'memory_usage': 4560,
                                                                                                'total_entries': 30},
                                                                                   'route_identifier': '200.0.1.1',
                                                                                   'routing_table_version': 1,
                                                                                   'scan_interval': 60,
                                                                                   'state_pfxrcd': 'Idle',
                                                                                   'tbl_ver': 1,
                                                                                   'total_memory': 9384,
                                                                                   'up_down': 'never',
                                                                                   'version': 4},
                                                                 'vpnv6 unicast': {'activity_paths': '120/30',
                                                                                   'activity_prefixes': '85/25',
                                                                                   'as': 100,
                                                                                   'attribute_entries': '6/4',
                                                                                   'bgp_table_version': 1,
                                                                                   'cache_entries': {'filter-list': {'memory_usage': 0,
                                                                                                                     'total_entries': 0},
                                                                                                     'route-map': {'memory_usage': 0,
                                                                                                                   'total_entries': 0}},
                                                                                   'community_entries': {'memory_usage': 96,
                                                                                                         'total_entries': 4},
                                                                                   'entries': {'AS-PATH': {'memory_usage': 120,
                                                                                                           'total_entries': 3},
                                                                                               'rrinfo': {'memory_usage': 48,
                                                                                                          'total_entries': 2}},
                                                                                   'input_queue': 0,
                                                                                   'local_as': 100,
                                                                                   'msg_rcvd': 0,
                                                                                   'msg_sent': 0,
                                                                                   'output_queue': 0,
                                                                                   'path': {'memory_usage': 4860,
                                                                                            'total_entries': 45},
                                                                                   'prefixes': {'memory_usage': 5280,
                                                                                                'total_entries': 30},
                                                                                   'route_identifier': '200.0.1.1',
                                                                                   'routing_table_version': 1,
                                                                                   'scan_interval': 60,
                                                                                   'state_pfxrcd': 'Idle',
                                                                                   'tbl_ver': 1,
                                                                                   'total_memory': 11364,
                                                                                   'up_down': 'never',
                                                                                   'version': 4}}}}}}}

    ShowBgpAllClusterIds = {'vrf': {'default': {'cluster_id': '4.4.4.4',
                     'configured_id': '0.0.0.0',
                     'list_of_cluster_ids': {'192.168.1.1': {'client_to_client_reflection_configured': 'disabled',
                                                             'client_to_client_reflection_used': 'disabled',
                                                             'num_neighbors': 2},
                                             '192.168.2.2': {'client_to_client_reflection_configured': 'disabled',
                                                             'client_to_client_reflection_used': 'disabled',
                                                             'num_neighbors': 2}},
                     'reflection_all_configured': 'enabled',
                     'reflection_intra_cluster_configured': 'enabled',
                     'reflection_intra_cluster_used': 'enabled'},
         'vrf1': {'cluster_id': '4.4.4.4',
                  'configured_id': '0.0.0.0',
                  'list_of_cluster_ids': {'192.168.1.1': {'client_to_client_reflection_configured': 'disabled',
                                                          'client_to_client_reflection_used': 'disabled',
                                                          'num_neighbors': 2},
                                          '192.168.2.2': {'client_to_client_reflection_configured': 'disabled',
                                                          'client_to_client_reflection_used': 'disabled',
                                                          'num_neighbors': 2}},
                  'reflection_all_configured': 'enabled',
                  'reflection_intra_cluster_configured': 'enabled',
                  'reflection_intra_cluster_used': 'enabled'},
         'vrf2': {'cluster_id': '4.4.4.4',
                  'configured_id': '0.0.0.0',
                  'list_of_cluster_ids': {'192.168.1.1': {'client_to_client_reflection_configured': 'disabled',
                                                          'client_to_client_reflection_used': 'disabled',
                                                          'num_neighbors': 2},
                                          '192.168.2.2': {'client_to_client_reflection_configured': 'disabled',
                                                          'client_to_client_reflection_used': 'disabled',
                                                          'num_neighbors': 2}},
                  'reflection_all_configured': 'enabled',
                  'reflection_intra_cluster_configured': 'enabled',
                  'reflection_intra_cluster_used': 'enabled'}}}


    ShowIpBgpTemplatePeerPolicy = {'peer_policy': {'PEER-POLICY': {'allowas_in': True,
                                 'allowas_in_as_number': 9,
                                 'as_override': True,
                                 'default_originate': True,
                                 'default_originate_route_map': 'test',
                                 'index': 1,
                                 'inherited_disable_polices': '0x0',
                                 'inherited_polices': '0x0',
                                 'inherited_policies': {'as_override': True,
                                                        'soo': 'SoO:100:100'},
                                 'local_disable_policies': '0x0',
                                 'local_policies': '0x8002069C603',
                                 'maximum_prefix_max_prefix_no': 5555,
                                 'maximum_prefix_restart': 300,
                                 'maximum_prefix_threshold': 70,
                                 'next_hop_self': True,
                                 'route_map_name_in': 'test',
                                 'route_map_name_out': 'test2',
                                 'route_reflector_client': True,
                                 'send_community': 'both',
                                 'soft_reconfiguration': True,
                                 'soo': 'SoO:100:100'},
                 'PEER-POLICY2': {'allowas_in': True,
                                  'allowas_in_as_number': 10,
                                  'index': 2,
                                  'inherited_disable_polices': '0x0',
                                  'inherited_polices': '0x0',
                                  'local_disable_policies': '0x0',
                                  'local_policies': '0x200000'}}}

    ShowBgpAllNeighbors = {
        'list_of_neighbors':['2.2.2.2', '3.3.3.3'],
        'vrf':
            {'default':
                {'neighbor':
                        {'2.2.2.2':
                             {'remote_as': 100,
                              'link': 'internal',
                              'bgp_version': 4,
                              'router_id': '2.2.2.2',
                              'session_state': 'established',
                              'bgp_negotiated_keepalive_timers':
                                  {
                                   'keepalive_interval': 60,
                                   'hold_time': 180,
                                   },
                              'bgp_session_transport':
                                  {
                                      'connection':
                                      {
                                          'last_reset': 'never',
                                          'established': 1,
                                          'dropped': 0,
                                      },
                                      'transport':
                                      {
                                           'local_host': '4.4.4.4',
                                           'local_port': '35281',
                                           'foreign_host': '2.2.2.2',
                                           'foreign_port': '179',
                                      },
                                      'min_time_between_advertisement_runs': 0,
                                      'address_tracking_status': 'enabled' ,
                                      'rib_route_ip': '2.2.2.2',
                                      'tcp_path_mtu_discovery': 'enabled',
                                      'graceful_restart': 'disabled',
                                      'connection_state': 'estab',
                                      'io_status': 1,
                                      'unread_input_bytes': 0,
                                      'ecn_connection': 'disabled',
                                      'minimum_incoming_ttl': 0,
                                      'outgoing_ttl': 255,
                                      'connection_tableid': 0,
                                      'maximum_output_segment_queue_size': 50,
                                      'enqueued_packets':
                                          {
                                              'retransmit_packet': 0,
                                              'input_packet': 0,
                                              'mis_ordered_packet': 0,
                                          },

                                      'iss': 55023811,
                                      'snduna': 55027115,
                                      'sndnxt': 55027115,
                                      'irs': 109992783,
                                      'rcvnxt':109995158,
                                      'sndwnd': 16616,
                                      'snd_scale': 0,
                                      'maxrcvwnd': 16384,
                                      'rcvwnd': 16327,
                                      'rcv_scale':0 ,
                                      'delrcvwnd': 57,
                                      'srtt': 1000 ,
                                      'rtto': 1003,
                                      'rtv': 3,
                                      'krtt': 0,
                                      'min_rtt': 4 ,
                                      'max_rtt': 1000,
                                      'ack_hold': 200,
                                      'uptime': 4239741  ,
                                      'sent_idletime': 7832 ,
                                      'receive_idletime': 8032  ,
                                      'status_flags': 'active open',
                                      'option_flags': 'nagle, path mtu capable',
                                      'ip_precedence_value': 6,
                                      'datagram':
                                          {
                                              'datagram_sent':
                                                  {
                                                      'value': 166,
                                                      'retransmit':0 ,
                                                      'fastretransmit':0 ,
                                                      'partialack': 0,
                                                      'second_congestion':0 ,
                                                      'with_data':87 ,
                                                      'total_data': 3303,
                                                  },
                                              'datagram_received':
                                                  {
                                                      'value':164 ,
                                                      'out_of_order':0,
                                                      'with_data': 80,
                                                      'total_data': 2374,
                                                  },

                                          },
                                      'packet_fast_path': 0,
                                      'packet_fast_processed': 0,
                                      'packet_slow_path':0 ,
                                      'fast_lock_acquisition_failures':0,
                                      'lock_slow_path': 0,
                                      'tcp_semaphore': '0x1286E7EC',
                                      'tcp_semaphore_status': 'FREE',

                                  },
                              'bgp_neighbor_counters':
                                  {'messages':
                                      {
                                          'sent':
                                              {
                                                  'opens': 1,
                                                  'updates': 11,
                                                  'notifications': 0,
                                                  'keepalives': 75,
                                                  'route_refresh': 0,
                                                  'total': 87,
                                              },
                                          'received':
                                              {
                                                  'opens': 1,
                                                  'updates': 6,
                                                  'notifications': 0,
                                                  'keepalives': 74,
                                                  'route_refresh': 0,
                                                  'total': 81,
                                              },
                                          'in_queue_depth': 0,
                                          'out_queue_depth': 0,
                                      },

                                  },
                              'bgp_negotiated_capabilities':
                                  {'route_refresh': 'advertised and received(new)',
                                   'vpnv4_unicast': 'advertised and received',
                                   'vpnv6_unicast': 'advertised and received',
                                   'graceful_restart': 'received',
                                   'enhanced_refresh': 'advertised',
                                   'four_octets_asn': 'advertised and received',
                                   'stateful_switchover': 'NO for session 1',
                                   'graceful_restart_af_advertised_by_peer':
                                       'VPNv4 Unicast (was not preserved, VPNv6 Unicast (was not preserved',
                                   'graceful_remote_restart_timer':120,
                                   },
                              'bgp_event_timer':
                                  {
                                      'starts':
                                          {
                                              'retrans': 86,
                                              'timewait': 0,
                                              'ackhold': 80,
                                              'sendwnd': 0,
                                              'keepalive': 0,
                                              'giveup': 0,
                                              'pmtuager': 1,
                                              'deadwait': 0,
                                              'linger': 0,
                                              'processq': 0,
                                          },
                                      'wakeups':
                                          {
                                              'retrans': 0,
                                              'timewait': 0,
                                              'ackhold': 72,
                                              'sendwnd': 0,
                                              'keepalive': 0,
                                              'giveup': 0,
                                              'pmtuager': 1,
                                              'deadwait': 0,
                                              'linger': 0,
                                              'processq': 0,
                                          },
                                      'next':
                                          {
                                              'retrans': '0x0',
                                              'timewait': '0x0',
                                              'ackhold': '0x0',
                                              'sendwnd': '0x0',
                                              'keepalive': '0x0',
                                              'giveup': '0x0',
                                              'pmtuager': '0x0',
                                              'deadwait': '0x0',
                                              'linger': '0x0',
                                              'processq': '0x0',
                                          },

                                  },
                              'address_family':
                                  {'vpnv4 unicast':
                                      {
                                          'last_read': '00:00:04',
                                          'last_write': '00:00:09',
                                          'session_state': 'established',
                                          'up_time': '01:10:35',
                                          'current_time': '0x530449',
                                      },
                                  'vpnv6 unicast':
                                      {
                                          'last_read': '00:00:07',
                                          'last_write': '00:00:12',
                                          'session_state': 'established',
                                          'up_time': '01:10:38',
                                          'current_time': '0x530FF5',
                                      },

                                  },
                              },
                        '3.3.3.3':
                             {'remote_as': 100,
                              'link': 'internal',
                              'bgp_version': 4,
                              'router_id': '3.3.3.3',
                              'session_state': 'established',
                              'bgp_negotiated_keepalive_timers':
                                  {
                                   'keepalive_interval': 60,
                                   'hold_time': 180,
                                   },
                              'bgp_session_transport':
                                  {'connection':
                                      {
                                          'last_reset': 'never',
                                          'established': 1,
                                          'dropped': 0,
                                      },
                                      'transport':
                                          {'local_host': '4.4.4.4',
                                           'local_port': '56031',
                                           'foreign_host': '3.3.3.3',
                                           'foreign_port': '179',
                                           },
                                      'min_time_between_advertisement_runs': 0,
                                      'address_tracking_status': 'enabled',
                                      'rib_route_ip': '3.3.3.3',
                                      'tcp_path_mtu_discovery': 'enabled',
                                      'graceful_restart': 'disabled',
                                      'connection_state': 'estab',
                                      'io_status': 1,
                                      'unread_input_bytes': 0,
                                      'ecn_connection': 'disabled',
                                      'minimum_incoming_ttl': 0,
                                      'outgoing_ttl': 255,
                                      'connection_tableid': 0,
                                      'maximum_output_segment_queue_size': 50,
                                      'enqueued_packets':
                                          {
                                              'retransmit_packet': 0,
                                              'input_packet': 0,
                                              'mis_ordered_packet': 0,
                                          },
                                      'iss': 2116369173,
                                      'snduna': 2116372477,
                                      'sndnxt': 2116372477,
                                      'irs': 4033842748,
                                      'rcvnxt': 4033845123,
                                      'sndwnd': 16616,
                                      'snd_scale':0,
                                      'maxrcvwnd': 16384,
                                      'rcvwnd': 16327,
                                      'rcv_scale': 0,
                                      'delrcvwnd': 57,
                                      'srtt': 1000,
                                      'rtto': 1003,
                                      'rtv': 3,
                                      'krtt': 0,
                                      'min_rtt': 3,
                                      'max_rtt': 1000,
                                      'ack_hold': 200,
                                      'uptime': 4246385,
                                      'sent_idletime': 8367,
                                      'receive_idletime': 8567,
                                      'status_flags': 'active open',
                                      'option_flags': 'nagle, path mtu capable',
                                      'ip_precedence_value': 6,
                                      'datagram':
                                          {
                                              'datagram_sent':
                                                  {
                                                      'value': 167,
                                                      'retransmit': 0,
                                                      'fastretransmit': 0,
                                                      'partialack': 0,
                                                      'second_congestion': 0,
                                                      'with_data': 87,
                                                      'total_data': 3303,
                                                  },
                                              'datagram_received':
                                                  {
                                                      'value': 165,
                                                      'out_of_order': 0,
                                                      'with_data': 80,
                                                      'total_data': 2374,
                                                  },

                                          },
                                      'packet_fast_path': 0,
                                      'packet_fast_processed': 0,
                                      'packet_slow_path': 0,
                                      'fast_lock_acquisition_failures': 0,
                                      'lock_slow_path': 0,
                                      'tcp_semaphore': '0x1286E85C',
                                      'tcp_semaphore_status': 'FREE',
                                  },
                              'bgp_neighbor_counters':
                                  {'messages':
                                      {
                                          'sent':
                                              {
                                                  'opens': 1,
                                                  'updates': 11,
                                                  'notifications': 0,
                                                  'keepalives': 75,
                                                  'route_refresh': 0,
                                                  'total': 87,
                                              },
                                          'received':
                                              {
                                                  'opens': 1,
                                                  'updates': 6,
                                                  'notifications': 0,
                                                  'keepalives': 74,
                                                  'route_refresh': 0,
                                                  'total': 81,
                                              },
                                          'in_queue_depth': 0,
                                          'out_queue_depth': 0,
                                      },

                                  },
                              'bgp_negotiated_capabilities':
                                  {'route_refresh': 'advertised and received(new)',
                                   'vpnv4_unicast': 'advertised and received',
                                   'vpnv6_unicast': 'advertised and received',
                                   'graceful_restart': 'received',
                                   'enhanced_refresh': 'advertised',
                                   'four_octets_asn': 'advertised and received',
                                   'stateful_switchover': 'NO for session 1',
                                   'graceful_restart_af_advertised_by_peer':
                                       'VPNv4 Unicast (was not preserved, VPNv6 Unicast (was not preserved',
                                   'graceful_remote_restart_timer': 120,
                                   },
                              'bgp_event_timer':
                                  {
                                      'starts':
                                          {
                                              'retrans': 86,
                                              'timewait': 0,
                                              'ackhold': 80,
                                              'sendwnd': 0,
                                              'keepalive': 0,
                                              'giveup': 0,
                                              'pmtuager': 1,
                                              'deadwait': 0,
                                              'linger': 0,
                                              'processq': 0,
                                          },
                                      'wakeups':
                                          {
                                              'retrans': 0,
                                              'timewait': 0,
                                              'ackhold': 73,
                                              'sendwnd': 0,
                                              'keepalive': 0,
                                              'giveup': 0,
                                              'pmtuager': 1,
                                              'deadwait': 0,
                                              'linger': 0,
                                              'processq': 0,
                                          },
                                      'next':
                                          {
                                              'retrans': '0x0',
                                              'timewait': '0x0',
                                              'ackhold': '0x0',
                                              'sendwnd': '0x0',
                                              'keepalive': '0x0',
                                              'giveup': '0x0',
                                              'pmtuager': '0x0',
                                              'deadwait': '0x0',
                                              'linger': '0x0',
                                              'processq': '0x0',
                                          },
                                  },
                              'address_family':
                                  {'vpnv4 unicast':
                                      {
                                          'last_read': '00:00:04',
                                          'last_write': '00:00:43',
                                          'session_state': 'established',
                                          'up_time': '01:10:41',
                                          'current_time': '0x530638',
                                      },
                                  'vpnv6 unicast':
                                      {
                                          'last_read': '00:00:08',
                                          'last_write': '00:00:47',
                                          'session_state': 'established',
                                          'up_time': '01:10:44',
                                          'current_time': '0x5313D8',
                                      },
                                  },
                              },
                        },
                },
            },
    }

    ShowIpBgpAllDampeningParameters = {'vrf': {'VRF1': {'address_family': {'vpnv4 unicast': {'dampening': True,
                                                       'dampening_decay_time': 2320,
                                                       'dampening_half_life_time': 900,
                                                       'dampening_max_suppress_penalty': 12000,
                                                       'dampening_max_suppress_time': 3600,
                                                       'dampening_reuse_time': 750,
                                                       'dampening_suppress_time': 2000}}},
         'default': {'address_family': {'ipv4 unicast': {'dampening': True,
                                                         'dampening_decay_time': 4200,
                                                         'dampening_half_life_time': 2100,
                                                         'dampening_max_suppress_penalty': 800,
                                                         'dampening_max_suppress_time': 4200,
                                                         'dampening_reuse_time': 200,
                                                         'dampening_suppress_time': 200},
                                        'ipv6 unicast': {'dampening': True,
                                                         'dampening_decay_time': 4235,
                                                         'dampening_half_life_time': 2160,
                                                         'dampening_max_suppress_penalty': 788,
                                                         'dampening_max_suppress_time': 4260,
                                                         'dampening_reuse_time': 201,
                                                         'dampening_suppress_time': 201},
                                        'vpnv4 unicast': {'dampening': True,
                                                          'dampening_decay_time': 2320,
                                                          'dampening_half_life_time': 900,
                                                          'dampening_max_suppress_penalty': 12000,
                                                          'dampening_max_suppress_time': 3600,
                                                          'dampening_reuse_time': 750,
                                                          'dampening_suppress_time': 2000}}}}}

    ShowIpBgpTemplatePeerSession = {'peer_session': {'PEER-SESSION': {'description': 'desc1!',
                                   'disable_connected_check': True,
                                   'ebgp_multihop_enable': True,
                                   'ebgp_multihop_max_hop': 254,
                                   'fall_over_bfd': True,
                                   'holdtime': 30,
                                   'index': 1,
                                   'inherited_polices': '0x0',
                                   'inherited_session_commands': {'holdtime': 30,
                                                                  'keepalive_interval': 10},
                                   'keepalive_interval': 10,
                                   'local_as_as_no': 255,
                                   'local_policies': '0x5025FD',
                                   'password_text': 'is configured',
                                   'remote_as': 321,
                                   'shutdown': True,
                                   'suppress_four_byte_as_capability': True,
                                   'transport_connection_mode': 'passive',
                                   'update_source': 'Loopback0'},
                  'PEER-SESSION2': {'fall_over_bfd': True,
                                    'index': 2,
                                    'inherited_polices': '0x0',
                                    'local_policies': '0x100000'}}}

    ShowBgpAllDetail = {'instance':
        {'default':
            {'vrf':
                {'EVPN-BGP-Table':
                    {'address_family':
                        {'vpnv4 unicast RD 65535:1':
                            {'default_vrf': 'evpn1',
                                                                         'prefixes': {'100.1.1.0/17': {'available_path': '1',
                                                                                                       'best_path': '1',
                                                                                                       'index': {1: {'evpn': {'encap': ':8',
                                                                                                                              'evpn_esi': '00000000000000000000',
                                                                                                                              'ext_community': 'RT:65535:1',
                                                                                                                              'gateway_address': '0.0.0.0',
                                                                                                                              'label': 30000,
                                                                                                                              'local_vtep': '33.33.33.33',
                                                                                                                              'router_mac': 'MAC:001E.7A13.E9BF'},
                                                                                                                     'gateway': '0.0.0.0',
                                                                                                                     'localpref': 100,
                                                                                                                     'metric': 0,
                                                                                                                     'next_hop': '0.0.0.0',
                                                                                                                     'next_hop_via': 'vrf '
                                                                                                                                     'evpn1',
                                                                                                                     'origin_codes': '?',
                                                                                                                     'originator': '33.33.33.33',
                                                                                                                     'recipient_pathid': 0,
                                                                                                                     'refresh_epoch': 1,
                                                                                                                     'route_info': 'Local, '
                                                                                                                                   'imported '
                                                                                                                                   'path '
                                                                                                                                   'from '
                                                                                                                                   'base',
                                                                                                                     'status_codes': '*>',
                                                                                                                     'transfer_pathid': '0x0',
                                                                                                                     'weight': '32768'}},
                                                                                                       'paths': '(1 '
                                                                                                                'available, '
                                                                                                                'best '
                                                                                                                '#1, '
                                                                                                                'table '
                                                                                                                'EVPN-BGP-Table)',
                                                                                                       'table_version': '4'},
                                                                                      '3.3.3.0/17': {'available_path': '2',
                                                                                                     'best_path': '1',
                                                                                                     'index': {1: {'evpn': {'encap': ':8',
                                                                                                                            'evpn_esi': '00000000000000000000',
                                                                                                                            'ext_community': 'RT:65535:1',
                                                                                                                            'gateway_address': '0.0.0.0',
                                                                                                                            'label': 30000,
                                                                                                                            'local_vtep': '33.33.33.33',
                                                                                                                            'router_mac': 'MAC:001E.7A13.E9BF'},
                                                                                                                   'gateway': '0.0.0.0',
                                                                                                                   'localpref': 100,
                                                                                                                   'metric': 0,
                                                                                                                   'next_hop': '0.0.0.0',
                                                                                                                   'next_hop_via': 'vrf '
                                                                                                                                   'evpn1',
                                                                                                                   'origin_codes': '?',
                                                                                                                   'originator': '33.33.33.33',
                                                                                                                   'recipient_pathid': 0,
                                                                                                                   'refresh_epoch': 1,
                                                                                                                   'route_info': 'Local, '
                                                                                                                                 'imported '
                                                                                                                                 'path '
                                                                                                                                 'from '
                                                                                                                                 'base',
                                                                                                                   'status_codes': '*>',
                                                                                                                   'transfer_pathid': '0x0',
                                                                                                                   'weight': '32768'},
                                                                                                               2: {'evpn': {'encap': ':8',
                                                                                                                            'evpn_esi': '00000000000000000000',
                                                                                                                            'ext_community': 'RT:65535:1',
                                                                                                                            'gateway_address': '0.0.0.0',
                                                                                                                            'label': 30000,
                                                                                                                            'local_vtep': '33.33.33.33',
                                                                                                                            'router_mac': 'MAC:001E.7A13.E9BF'},
                                                                                                                   'gateway': '3.3.3.254',
                                                                                                                   'localpref': 100,
                                                                                                                   'metric': 0,
                                                                                                                   'next_hop': '3.3.3.254',
                                                                                                                   'next_hop_igp_metric': 111,
                                                                                                                   'update_groups': 3,
                                                                                                                   'paths': '(1 '
                                                                                                                            'available, '
                                                                                                                            'best '
                                                                                                                            '#1, '
                                                                                                                            'table '
                                                                                                                            'default)',
                                                                                                                   'next_hop_via': 'vrf '
                                                                                                                                   'evpn1',
                                                                                                                   'origin_codes': '?',
                                                                                                                   'originator': '33.33.33.22',
                                                                                                                   'refresh_epoch': 1,
                                                                                                                   'route_info': '65530, '
                                                                                                                                 'imported '
                                                                                                                                 'path '
                                                                                                                                 'from '
                                                                                                                                 'base',
                                                                                                                   'status_codes': '* '}},
                                                                                                     'paths': '(2 '
                                                                                                              'available, '
                                                                                                              'best '
                                                                                                              '#1, '
                                                                                                              'table '
                                                                                                              'EVPN-BGP-Table)',
                                                                                                     'table_version': '3'}},
                                                                         'route_distinguisher': '65535:1'}}},
      'VRF1': {'address_family': {'vpnv4 unicast RD 100:100': {'default_vrf': 'VRF1',
                                                               'prefixes': {'11.11.11.11/32': {'available_path': '1',
                                                                                               'best_path': '1',
                                                                                               'index': {1: {'gateway': '0.0.0.0',
                                                                                                             'localpref': 100,
                                                                                                             'metric': 0,
                                                                                                             'next_hop': '0.0.0.0',
                                                                                                             'next_hop_via': 'vrf '
                                                                                                                             'VRF1',
                                                                                                             'origin_codes': '?',
                                                                                                             'originator': '10.1.1.1',
                                                                                                             'recipient_pathid': 0,
                                                                                                             'refresh_epoch': 1,
                                                                                                             'route_info': 'Local',
                                                                                                             'status_codes': '*>',
                                                                                                             'transfer_pathid': '0x0',
                                                                                                             'weight': '32768'}},
                                                                                               'paths': '(1 '
                                                                                                        'available, '
                                                                                                        'best '
                                                                                                        '#1, '
                                                                                                        'table '
                                                                                                        'VRF1)',
                                                                                               'table_version': '2'}},
                                                               'route_distinguisher': '100:100'},
                                  'vpnv6 unicast RD 100:100': {'default_vrf': 'VRF1',
                                                               'prefixes': {'2001:11:11::11/128': {'available_path': '1',
                                                                                                   'best_path': '1',
                                                                                                   'index': {1: {'gateway': '0.0.0.0',
                                                                                                                 'localpref': 100,
                                                                                                                 'metric': 0,
                                                                                                                 'next_hop': '::',
                                                                                                                 'next_hop_via': 'vrf '
                                                                                                                                 'VRF1',
                                                                                                                 'origin_codes': '?',
                                                                                                                 'originator': '10.1.1.1',
                                                                                                                 'recipient_pathid': 0,
                                                                                                                 'refresh_epoch': 1,
                                                                                                                 'route_info': 'Local',
                                                                                                                 'status_codes': '*>',
                                                                                                                 'transfer_pathid': '0x0',
                                                                                                                 'weight': '32768'}},
                                                                                                   'paths': '(1 '
                                                                                                            'available, '
                                                                                                            'best '
                                                                                                            '#1, '
                                                                                                            'table '
                                                                                                            'VRF1)',
                                                                                                   'table_version': '2'}},
                                                               'route_distinguisher': '100:100'}}},
      'default': {'address_family': {'ipv4 unicast': {'prefixes': {'1.1.1.1/32': {'available_path': '1',
                                                                                  'best_path': '1',
                                                                                  'index': {1: {'gateway': '0.0.0.0',
                                                                                                'localpref': 100,
                                                                                                'metric': 0,
                                                                                                'next_hop': '0.0.0.0',
                                                                                                'origin_codes': '?',
                                                                                                'originator': '10.1.1.1',
                                                                                                'recipient_pathid': 0,
                                                                                                'refresh_epoch': 1,
                                                                                                'route_info': 'Local',
                                                                                                'status_codes': '*>',
                                                                                                'transfer_pathid': '0x0',
                                                                                                'update_group': 3,
                                                                                                'weight': '32768'}},
                                                                                  'paths': '(1 '
                                                                                           'available, '
                                                                                           'best '
                                                                                           '#1, '
                                                                                           'table '
                                                                                           'default)',
                                                                                  'table_version': '4'},
                                                                   '10.1.1.0/24': {'available_path': '2',
                                                                                   'best_path': '1',
                                                                                   'index': {1: {'gateway': '0.0.0.0',
                                                                                                 'localpref': 100,
                                                                                                 'metric': 0,
                                                                                                 'next_hop': '0.0.0.0',
                                                                                                 'origin_codes': '?',
                                                                                                 'originator': '10.1.1.1',
                                                                                                 'recipient_pathid': 0,
                                                                                                 'refresh_epoch': 1,
                                                                                                 'route_info': 'Local',
                                                                                                 'status_codes': '*>',
                                                                                                 'transfer_pathid': '0x0',
                                                                                                 'update_group': 3,
                                                                                                 'weight': '32768'},
                                                                                             2: {'gateway': '10.1.1.2',
                                                                                                 'localpref': 100,
                                                                                                 'metric': 0,
                                                                                                 'next_hop': '10.1.1.2',
                                                                                                 'origin_codes': '?',
                                                                                                 'originator': '10.1.1.2',
                                                                                                 'refresh_epoch': 1,
                                                                                                 'route_info': 'Local',
                                                                                                 'status_codes': '* '
                                                                                                                 'i',
                                                                                                 'update_group': 3}},
                                                                                   'paths': '(2 '
                                                                                            'available, '
                                                                                            'best '
                                                                                            '#1, '
                                                                                            'table '
                                                                                            'default)',
                                                                                   'table_version': '5'},
                                                                   '2.2.2.2/32': {'available_path': '1',
                                                                                  'best_path': '1',
                                                                                  'index': {1: {'gateway': '10.1.1.2',
                                                                                                'localpref': 100,
                                                                                                'metric': 0,
                                                                                                'next_hop': '10.1.1.2',
                                                                                                'origin_codes': '?',
                                                                                                'originator': '10.1.1.2',
                                                                                                'recipient_pathid': 0,
                                                                                                'refresh_epoch': 1,
                                                                                                'route_info': 'Local',
                                                                                                'status_codes': '*>',
                                                                                                'transfer_pathid': '0x0'}},
                                                                                  'paths': '(1 '
                                                                                           'available, '
                                                                                           'best '
                                                                                           '#1, '
                                                                                           'table '
                                                                                           'default)',
                                                                                  'table_version': '2'}}},
                                     'ipv6 unicast': {'prefixes': {'2001:1:1:1::1/128': {'available_path': '1',
                                                                                         'best_path': '1',
                                                                                         'index': {1: {'gateway': '0.0.0.0',
                                                                                                       'localpref': 100,
                                                                                                       'metric': 0,
                                                                                                       'next_hop': '::',
                                                                                                       'origin_codes': '?',
                                                                                                       'originator': '10.1.1.1',
                                                                                                       'recipient_pathid': 0,
                                                                                                       'refresh_epoch': 1,
                                                                                                       'route_info': 'Local',
                                                                                                       'status_codes': '*>',
                                                                                                       'transfer_pathid': '0x0',
                                                                                                       'update_group': 1,
                                                                                                       'weight': '32768'}},
                                                                                         'paths': '(1 '
                                                                                                  'available, '
                                                                                                  'best '
                                                                                                  '#1, '
                                                                                                  'table '
                                                                                                  'default)',
                                                                                         'table_version': '4'},
                                                                   '2001:2:2:2::2/128': {'available_path': '2',
                                                                                         'best_path': '1',
                                                                                         'index': {1: {'gateway': '2001:DB8:1:1::2',
                                                                                                       'localpref': 100,
                                                                                                       'metric': 0,
                                                                                                       'next_hop': '2001:DB8:1:1::2',
                                                                                                       'origin_codes': '?',
                                                                                                       'originator': '10.1.1.2',
                                                                                                       'recipient_pathid': 0,
                                                                                                       'refresh_epoch': 1,
                                                                                                       'route_info': 'Local',
                                                                                                       'status_codes': '* '
                                                                                                                       'i',
                                                                                                       'transfer_pathid': '0x0'}},
                                                                                         'paths': '(2 '
                                                                                                  'available, '
                                                                                                  'best '
                                                                                                  '#1, '
                                                                                                  'table '
                                                                                                  'default)',
                                                                                         'table_version': '2'},
                                                                   '2001:DB8:1:1::/64': {'available_path': '3',
                                                                                         'best_path': '1',
                                                                                         'index': {1: {'gateway': '0.0.0.0',
                                                                                                       'localpref': 100,
                                                                                                       'metric': 0,
                                                                                                       'next_hop': '::',
                                                                                                       'origin_codes': '?',
                                                                                                       'originator': '10.1.1.1',
                                                                                                       'recipient_pathid': 0,
                                                                                                       'refresh_epoch': 1,
                                                                                                       'route_info': 'Local',
                                                                                                       'status_codes': '*>',
                                                                                                       'transfer_pathid': '0x0',
                                                                                                       'update_group': 1,
                                                                                                       'weight': '32768'},
                                                                                                   2: {'gateway': '2001:DB8:1:1::2',
                                                                                                       'localpref': 100,
                                                                                                       'metric': 0,
                                                                                                       'next_hop': '2001:DB8:1:1::2',
                                                                                                       'origin_codes': '?',
                                                                                                       'originator': '10.1.1.2',
                                                                                                       'refresh_epoch': 1,
                                                                                                       'route_info': 'Local',
                                                                                                       'status_codes': '* '
                                                                                                                       'i',
                                                                                                       'update_group': 1}},
                                                                                         'paths': '(3 '
                                                                                                  'available, '
                                                                                                  'best '
                                                                                                  '#1, '
                                                                                                  'table '
                                                                                                  'default)',
                                                                                         'table_version': '5'}}}}},
      'evpn1': {'address_family': {'vpnv4 unicast RD 65535:1': {'default_vrf': 'evpn1',
                                                                'prefixes': {'100.1.1.0/24': {'available_path': '1',
                                                                                              'best_path': '1',
                                                                                              'index': {1: {'gateway': '0.0.0.0',
                                                                                                            'local_vxlan_vtep': {'bdi': 'BDI200',
                                                                                                                                 'encap': '8',
                                                                                                                                 'local_router_mac': '001E.7A13.E9BF',
                                                                                                                                 'vni': '30000',
                                                                                                                                 'vrf': 'evpn1',
                                                                                                                                 'vtep_ip': '33.33.33.33'},
                                                                                                            'localpref': 100,
                                                                                                            'metric': 0,
                                                                                                            'next_hop': '0.0.0.0',
                                                                                                            'next_hop_via': 'vrf '
                                                                                                                            'evpn1',
                                                                                                            'origin_codes': '?',
                                                                                                            'originator': '33.33.33.33',
                                                                                                            'recipient_pathid': 0,
                                                                                                            'refresh_epoch': 1,
                                                                                                            'route_info': 'Local',
                                                                                                            'status_codes': '*>',
                                                                                                            'transfer_pathid': '0x0',
                                                                                                            'update_group': 1,
                                                                                                            'weight': '32768'}},
                                                                                              'paths': '(1 '
                                                                                                       'available, '
                                                                                                       'best '
                                                                                                       '#1, '
                                                                                                       'table '
                                                                                                       'evpn1)',
                                                                                              'table_version': '5'},
                                                                             '3.3.3.0/24': {'available_path': '2',
                                                                                            'best_path': '2',
                                                                                            'index': {1: {'gateway': '3.3.3.254',
                                                                                                          'local_vxlan_vtep': {'bdi': 'BDI200',
                                                                                                                               'encap': '8',
                                                                                                                               'local_router_mac': '001E.7A13.E9BF',
                                                                                                                               'vni': '30000',
                                                                                                                               'vrf': 'evpn1',
                                                                                                                               'vtep_ip': '33.33.33.33'},
                                                                                                          'localpref': 100,
                                                                                                          'metric': 0,
                                                                                                          'next_hop': '3.3.3.254',
                                                                                                          'next_hop_via': 'vrf '
                                                                                                                          'evpn1',
                                                                                                          'origin_codes': '?',
                                                                                                          'originator': '33.33.33.22',
                                                                                                          'refresh_epoch': 1,
                                                                                                          'route_info': '65530',
                                                                                                          'status_codes': '* ',
                                                                                                          'update_group': 1},
                                                                                                      2: {'gateway': '0.0.0.0',
                                                                                                          'local_vxlan_vtep': {'bdi': 'BDI200',
                                                                                                                               'encap': '8',
                                                                                                                               'local_router_mac': '001E.7A13.E9BF',
                                                                                                                               'vni': '30000',
                                                                                                                               'vrf': 'evpn1',
                                                                                                                               'vtep_ip': '33.33.33.33'},
                                                                                                          'localpref': 100,
                                                                                                          'metric': 0,
                                                                                                          'next_hop': '0.0.0.0',
                                                                                                          'next_hop_via': 'vrf '
                                                                                                                          'evpn1',
                                                                                                          'origin_codes': '?',
                                                                                                          'originator': '33.33.33.33',
                                                                                                          'recipient_pathid': 0,
                                                                                                          'refresh_epoch': 1,
                                                                                                          'route_info': 'Local',
                                                                                                          'status_codes': '*>',
                                                                                                          'transfer_pathid': '0x0',
                                                                                                          'update_group': 1,
                                                                                                          'weight': '32768'}},
                                                                                            'paths': '(2 '
                                                                                                     'available, '
                                                                                                     'best '
                                                                                                     '#2, '
                                                                                                     'table '
                                                                                                     'evpn1)',
                                                                                            'table_version': '4'}},
                                                                'route_distinguisher': '65535:1'}}}}}}}

    ShowBgpAll = {'vrf': {'VRF1': {'address_family': {'vpnv4 unicast RD 300:1': {'bgp_table_version': 56,
                                                                'default_vrf': 'VRF1',
                                                                'route_distinguisher': '300:1',
                                                                'route_identifier': '4.4.4.4',
                                                                'routes': {'15.1.1.0/24': {'index': {1: {'localpref': 100,
                                                                                                         'metric': 2219,
                                                                                                         'next_hop': '1.1.1.1',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '200 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '* '
                                                                                                                         'i',
                                                                                                         'weight': 0},
                                                                                                     2: {'localpref': 100,
                                                                                                         'metric': 2219,
                                                                                                         'next_hop': '1.1.1.1',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '200 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>i',
                                                                                                         'weight': 0}}},
                                                                           '15.1.2.0/24': {'index': {1: {'localpref': 100,
                                                                                                         'metric': 2219,
                                                                                                         'next_hop': '1.1.1.1',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '200 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '* '
                                                                                                                         'i',
                                                                                                         'weight': 0},
                                                                                                     2: {'localpref': 100,
                                                                                                         'metric': 2219,
                                                                                                         'next_hop': '1.1.1.1',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '200 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>i',
                                                                                                         'weight': 0}}},
                                                                           '46.1.1.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '10.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '300 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.1.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '10.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '300 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.1.3.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '10.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '300 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.1.4.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '10.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '300 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.1.5.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '10.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '300 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.2.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}}},
                                                                'vrf_route_identifier': '44.44.44.44'}}},
         'VRF2': {'address_family': {'vpnv4 unicast RD 400:1': {'bgp_table_version': 56,
                                                                'default_vrf': 'VRF2',
                                                                'route_distinguisher': '400:1',
                                                                'route_identifier': '4.4.4.4',
                                                                'routes': {'46.2.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.2.3.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.2.4.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.2.5.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '46.2.6.0/24': {'index': {1: {'metric': 2219,
                                                                                                         'next_hop': '20.4.6.6',
                                                                                                         'origin_codes': 'e',
                                                                                                         'path': '400 '
                                                                                                                 '33299 '
                                                                                                                 '51178 '
                                                                                                                 '47751 '
                                                                                                                 '{27016}',
                                                                                                         'status_codes': '*>',
                                                                                                         'weight': 0}}},
                                                                           '615:11:11:1::/64': {'index': {1: {'localpref': 100,
                                                                                                              'metric': 2219,
                                                                                                              'next_hop': '::FFFF:1.1.1.1',
                                                                                                              'origin_codes': 'e',
                                                                                                              'path': '400 '
                                                                                                                      '33299 '
                                                                                                                      '51178 '
                                                                                                                      '47751 '
                                                                                                                      '{27016}',
                                                                                                              'status_codes': '* '
                                                                                                                              'i',
                                                                                                              'weight': 0},
                                                                                                          2: {'localpref': 100,
                                                                                                              'metric': 2219,
                                                                                                              'next_hop': '::FFFF:1.1.1.1',
                                                                                                              'origin_codes': 'e',
                                                                                                              'path': '400 '
                                                                                                                      '33299 '
                                                                                                                      '51178 '
                                                                                                                      '47751 '
                                                                                                                      '{27016}',
                                                                                                              'status_codes': '*>i',
                                                                                                              'weight': 0}}},
                                                                           '615:11:11::/64': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '::FFFF:1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '400 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '::FFFF:1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '400 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0}}}},
                                                                'vrf_route_identifier': '44.44.44.44'}}},
         'default': {'address_family': {'vpnv4 unicast RD 200:1': {'bgp_table_version': 56,
                                                                   'default_vrf': 'default',
                                                                   'route_distinguisher': '200:1',
                                                                   'route_identifier': '4.4.4.4',
                                                                   'routes': {'15.1.1.0/24': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0}}},
                                                                              '15.1.2.0/24': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0}}}}},
                                        'vpnv4 unicast RD 200:2': {'bgp_table_version': 56,
                                                                   'default_vrf': 'default',
                                                                   'route_distinguisher': '200:2',
                                                                   'route_identifier': '4.4.4.4',
                                                                   'routes': {'15.1.1.0/24': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0}}},
                                                                              '15.1.2.0/24': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0}}},
                                                                              '15.1.3.0/24': {'index': {1: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '*>i',
                                                                                                            'weight': 0},
                                                                                                        2: {'localpref': 100,
                                                                                                            'metric': 2219,
                                                                                                            'next_hop': '1.1.1.1',
                                                                                                            'origin_codes': 'e',
                                                                                                            'path': '200 '
                                                                                                                    '33299 '
                                                                                                                    '51178 '
                                                                                                                    '47751 '
                                                                                                                    '{27016}',
                                                                                                            'status_codes': '* '
                                                                                                                            'i',
                                                                                                            'weight': 0}}}}}}},
         'evpn1': {'address_family': {'l2vpn e-vpn RD 65535:1': {'bgp_table_version': 4,
                                                                 'default_vrf': 'evpn1',
                                                                 'route_distinguisher': '65535:1',
                                                                 'route_identifier': '33.33.33.33',
                                                                 'routes': {'[5][65535:1][0][24][100.1.1.0]/17': {'index': {1: {'metric': 0,
                                                                                                                                'next_hop': '0.0.0.0',
                                                                                                                                'origin_codes': '?',
                                                                                                                                'status_codes': '*>',
                                                                                                                                'weight': 32768}}},
                                                                            '[5][65535:1][0][24][3.3.3.0]/17': {'index': {1: {'metric': 0,
                                                                                                                              'next_hop': '0.0.0.0',
                                                                                                                              'origin_codes': '?',
                                                                                                                              'status_codes': '*>',
                                                                                                                              'weight': 32768},
                                                                                                                          2: {'metric': 0,
                                                                                                                              'next_hop': '3.3.3.254',
                                                                                                                              'origin_codes': '?',
                                                                                                                              'path': '65530',
                                                                                                                              'status_codes': '*',
                                                                                                                              'weight': 0}}}}},
                                      'vpnv4 unicast RD 65535:1': {'af_private_import_to_address_family': 'L2VPN '
                                                                                                          'E-VPN',
                                                                   'bgp_table_version': 5,
                                                                   'default_vrf': 'evpn1',
                                                                   'pfx_count': 2,
                                                                   'pfx_limit': 1000,
                                                                   'route_distinguisher': '65535:1',
                                                                   'route_identifier': '33.33.33.33',
                                                                   'routes': {'100.1.1.0/24': {'index': {1: {'metric': 0,
                                                                                                             'next_hop': '0.0.0.0',
                                                                                                             'origin_codes': '?',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 32768}}},
                                                                              '3.3.3.0/24': {'index': {1: {'metric': 0,
                                                                                                           'next_hop': '3.3.3.254',
                                                                                                           'origin_codes': '?',
                                                                                                           'path': '65530',
                                                                                                           'status_codes': '*',
                                                                                                           'weight': 0},
                                                                                                       2: {'metric': 0,
                                                                                                           'next_hop': '0.0.0.0',
                                                                                                           'origin_codes': '?',
                                                                                                           'status_codes': '*>',
                                                                                                           'weight': 32768}}}}}}}}}

    nbr1_bgp_policy = '''\
        R4_iosv#show bgp all neighbors 2.2.2.2 policy
         Neighbor: 2.2.2.2, Address-Family: VPNv4 Unicast (VRF1)
         Locally configured policies:
          route-map test in
          route-map test out
        '''

    nbr1_bgp_all_neighbors = '''\
      R4# show bgp all neighbors | i BGP neighbor
      BGP neighbor is 2.2.2.2,  remote AS 100, internal link
        '''

    nbr1_advertised_routes = '''\
        R4# show bgp all neighbors 2.2.2.2 advertised-routes

        For address family: IPv4 Unicast
        BGP table version is 648438, local router ID is 44.44.44.44
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i15.1.1.0/24        1.1.1.1               2219        100          0 200 33299 51178 47751 {27016} e
        *>i15.1.2.0/24        1.1.1.1               2219        100          0 200 33299 51178 47751 {27016} e
        *>i15.1.3.0/24        1.1.1.1               2219        100          0 200 33299 51178 47751 {27016} e
        *>i15.1.4.0/24        1.1.1.1               2219        100          0 200 33299 51178 47751 {27016} e
        *>i15.1.5.0/24        1.1.1.1               2219        100          0 200 33299 51178 47751 {27016} e
        *>e46.2.2.0/24        20.4.6.6               100                     0 400 33299 51178 {47751} e
        *>e46.2.3.0/24        20.4.6.6               100                     0 400 33299 51178 {47751} e
        *>e46.2.4.0/24        20.4.6.6               100                     0 400 33299 51178 {47751} e
        *>e46.2.5.0/24        20.4.6.6               100                     0 400 33299 51178 {47751} e
        *>e46.2.6.0/24        20.4.6.6               100                     0 400 33299 51178 {47751} e

        For address family: IPv4 Multicast

        For address family: IPv6 Unicast
        BGP table version is 256028, local router ID is 44.44.44.44
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        For address family: IPv6 Multicast

        For address family: VPNv4 Unicast

        For address family: VPNv6 Unicast

        For address family: IPv4 MDT

        For address family: IPv6 Label Unicast

        For address family: L2VPN VPLS

        For address family: IPv4 MVPN

        For address family: IPv6 MVPN

        For address family: IPv4 Label Unicast
        '''

    nbr1_routes = '''\
        R4# show bgp all neighbors 2.2.2.2 routes 

        For address family: IPv4 Unicast
        BGP table version is 773961, local router ID is 44.44.44.44
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>e46.1.1.0/24        21.0.0.2              2219                     0 300 33299 51178 47751 {27016} e
        *>e46.1.2.0/24        21.0.0.2              2219                     0 300 33299 51178 47751 {27016} e
        *>e46.1.3.0/24        21.0.0.2              2219                     0 300 33299 51178 47751 {27016} e
        *>e46.1.4.0/24        21.0.0.2              2219                     0 300 33299 51178 47751 {27016} e
        *>e46.1.5.0/24        21.0.0.2              2219                     0 300 33299 51178 47751 {27016} e

        For address family: IPv4 Multicast

        For address family: IPv6 Unicast
        BGP table version is 256033, local router ID is 44.44.44.44
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        For address family: IPv6 Multicast

        For address family: VPNv4 Unicast

        For address family: VPNv6 Unicast

        For address family: IPv4 MDT

        For address family: IPv6 Label Unicast

        For address family: L2VPN VPLS

        For address family: IPv4 MVPN

        For address family: IPv6 MVPN

        For address family: IPv4 Label Unicast
            '''

    nbr1_received_routes = '''\
        R4_iosv#show bgp all neighbors 2.2.2.2 received-routes 
        For address family: VPNv4 Unicast
        BGP table version is 66, local router ID is 4.4.4.4
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                      r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                      x best-external, a additional-path, c RIB-compressed, 
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

             Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 44.44.44.44
         *   46.1.1.0/24      21.0.0.2              2219             0 300 33299 51178 47751 {27016} e
         *   46.1.2.0/24      21.0.0.2              2219             0 300 33299 51178 47751 {27016} e
         *   46.1.3.0/24      21.0.0.2              2219             0 300 33299 51178 47751 {27016} e
         *   46.1.4.0/24      21.0.0.2              2219             0 300 33299 51178 47751 {27016} e
         *   46.1.5.0/24      21.0.0.2              2219             0 300 33299 51178 47751 {27016} e

        Total number of prefixes 5
        '''

    nbr2_bgp_policy = '''\
        R4_iosv#show bgp all neighbors 3.3.3.3 policy
         Neighbor: 3.3.3.3, Address-Family: VPNv4 Unicast (VRF1)
         Locally configured policies:
          route-map test in
          route-map test out
        '''

    nbr2_bgp_all_neighbors = '''\
      R4# show bgp all neighbors | i BGP neighbor
      BGP neighbor is 3.3.3.3,  remote AS 100, internal link
        '''

    nbr2_advertised_routes = '''\
        R4# show bgp all neighbors 3.3.3.3 advertised-routes
        For address family: VPNv4 Unicast
        BGP table version is 56, local router ID is 4.4.4.4
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                      r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                      x best-external, a additional-path, c RIB-compressed, 
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

             Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 44.44.44.44
         *>  46.1.1.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
         *>  46.1.2.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
         *>  46.1.3.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
         *>  46.1.4.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
         *>  46.1.5.0/24      10.4.6.6              2219             0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1 (default for vrf VRF2) VRF Router ID 44.44.44.44
         *>  46.2.2.0/24      20.4.6.6              2219             0 400 33299 51178 47751 {27016} e
         *>  46.2.3.0/24      20.4.6.6              2219             0 400 33299 51178 47751 {27016} e
         *>  46.2.4.0/24      20.4.6.6              2219             0 400 33299 51178 47751 {27016} e
         *>  46.2.5.0/24      20.4.6.6              2219             0 400 33299 51178 47751 {27016} e
         *>  46.2.6.0/24      20.4.6.6              2219             0 400 33299 51178 47751 {27016} e

        Total number of prefixes 10 

        For address family: VPNv6 Unicast
        BGP table version is 66, local router ID is 4.4.4.4
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                      r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                      x best-external, a additional-path, c RIB-compressed, 
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

             Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 44.44.44.44
         *>  646:11:11::/64   2001:DB8:4:6::6       2219             0 300 33299 51178 47751 {27016} e
         *>  646:11:11:1::/64 2001:DB8:4:6::6       2219             0 300 33299 51178 47751 {27016} e
         *>  646:11:11:2::/64 2001:DB8:4:6::6       2219             0 300 33299 51178 47751 {27016} e
         *>  646:11:11:3::/64 2001:DB8:4:6::6       2219             0 300 33299 51178 47751 {27016} e
         *>  646:11:11:4::/64 2001:DB8:4:6::6       2219             0 300 33299 51178 47751 {27016} e
        Route Distinguisher: 400:1 (default for vrf VRF2) VRF Router ID 44.44.44.44
         *>  646:22:22::/64   2001:DB8:20:4:6::6
                                                     2219             0 400 33299 51178 47751 {27016} e
         *>  646:22:22:1::/64 2001:DB8:20:4:6::6
                                                     2219             0 400 33299 51178 47751 {27016} e
         *>  646:22:22:2::/64 2001:DB8:20:4:6::6
                                                     2219             0 400 33299 51178 47751 {27016} e
         *>  646:22:22:3::/64 2001:DB8:20:4:6::6
                                                     2219             0 400 33299 51178 47751 {27016} e
         *>  646:22:22:4::/64 2001:DB8:20:4:6::6
                                                     2219             0 400 33299 51178 47751 {27016} e

        Total number of prefixes 10
        '''

    nbr2_routes = '''\
        R4# show bgp all neighbors 3.3.3.3 routes 
        For address family: VPNv4 Unicast
        BGP table version is 56, local router ID is 4.4.4.4
        Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
                      r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
                      x best-external, a additional-path, c RIB-compressed, 
        Origin codes: i - IGP, e - EGP, ? - incomplete
        RPKI validation codes: V valid, I invalid, N Not found

             Network          Next Hop            Metric LocPrf Weight Path
        Route Distinguisher: 200:1
         *>i 15.1.1.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.2.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.3.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.4.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.5.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
        Route Distinguisher: 200:2
         *>i 15.1.1.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.2.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.3.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.4.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i 15.1.5.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
        Route Distinguisher: 300:1 (default for vrf VRF1) VRF Router ID 44.44.44.44
         * i 15.1.1.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i                  3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         * i 15.1.2.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i                  3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         * i 15.1.3.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i                  3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         * i 15.1.4.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i                  3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         * i 15.1.5.0/24      3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e
         *>i                  3.3.3.3               2219    100      0 200 33299 51178 47751 {27016} e

        Total number of prefixes 20
            '''

    nbr2_received_routes = '''\
        R4_iosv#show bgp all neighbors 3.3.3.3 received-routes
        For address family: IPv4 Unicast
        BGP table version is 174, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        * i1.1.1.0/24         3.3.3.3            2222        100          0 1 2 3 65000 23 i
        * i1.1.2.0/24         3.3.3.3            2222        100          0 1 2 3 65000 23 i
        *>i1.6.0.0/16         3.3.3.3                        100          0 10 20 30 40 50 60 70 80 90 i


        For address family: IPv4 Multicast
        BGP table version is 175, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i1.2.1.0/24         3.3.3.3                        100          0 2 3 4 i
        *>i1.2.2.0/24         3.3.3.3                        100          0 2 3 4 i


        For address family: IPv6 Unicast
        BGP table version is 173, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        For address family: IPv6 Multicast
        BGP table version is 6, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        For address family: VPNv4 Unicast
        BGP table version is 183, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 0:0

        Route Distinguisher: 101:100
        * i1.3.1.0/24         3.3.3.3            4444        100          0 3 10 20 4 5 6 3 10 20 4 5 6 i
        * i1.3.2.0/24         3.3.3.3            4444        100          0 3 10 20 4 5 6 3 10 20 4 5 6 i

        Route Distinguisher: 102:100


        For address family: VPNv6 Unicast
        BGP table version is 13, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 100:200
        *>iaaaa:1::/113       ::ffff:3.3.3.3
                                                    4444        100          0 i
        *>iaaaa:1::8000/113   ::ffff:3.3.3.3
                                                    4444        100          0 i

        Route Distinguisher: 0xbb00010000000000


        For address family: Link-State
        BGP table version is 173, Local Router ID is 20.0.0.6
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i[2]:[77][7,0][9.9.9.9,1,151587081][29.1.1.1,22][3.3.3.3,29.0.1.30]/616
                              3.3.3.3            4444        100          0 3 10 20 30 40 50 60 70 80 90 i
        *>i[2]:[77][7,0][9.9.9.9,2,151587081][29.1.1.1,22][3.3.3.3,29.0.1.31]/616
                              3.3.3.3            4444        100          0 3 10 20 30 40 50 60 70 80 90 i
        '''

    BgpOpsOutput_info = {'instance': {'default': {'bgp_id': 100,
                          'peer_policy': {'PEER-POLICY': {'allowas_in': True,
                                                          'as_override': True,
                                                          'default_originate': True,
                                                          'default_originate_route_map': 'test',
                                                          'maximum_prefix_max_prefix_no': 5555,
                                                          'next_hop_self': True,
                                                          'route_map_name_in': 'test',
                                                          'route_map_name_out': 'test2',
                                                          'route_reflector_client': True,
                                                          'send_community': 'both',
                                                          'soft_reconfiguration': True,
                                                          'soo': 'SoO:100:100'},
                                          'PEER-POLICY2': {'allowas_in': True}},
                          'peer_session': {'PEER-SESSION': {'description': 'desc1!',
                                                            'disable_connected_check': True,
                                                            'ebgp_multihop_enable': True,
                                                            'ebgp_multihop_max_hop': 254,
                                                            'fall_over_bfd': True,
                                                            'holdtime': 30,
                                                            'keepalive_interval': 10,
                                                            'local_as_as_no': 255,
                                                            'password_text': 'is '
                                                                             'configured',
                                                            'remote_as': 321,
                                                            'shutdown': True,
                                                            'suppress_four_byte_as_capability': True,
                                                            'transport_connection_mode': 'passive',
                                                            'update_source': 'Loopback0'},
                                           'PEER-SESSION2': {'fall_over_bfd': True}},
                          'vrf': {'VRF1': {'address_family': {'vpnv4 unicast': {'dampening': True,
                                                                                'dampening_half_life_time': 900,
                                                                                'dampening_max_suppress_time': 3600,
                                                                                'dampening_reuse_time': 750,
                                                                                'dampening_suppress_time': 2000}},
                                           'neighbor': {'3.3.3.3': {'address_family': {'vpnv4 unicast': {'route_map_name_in': 'test',
                                                                                                         'route_map_name_out': 'test'}}},
                                                        '2.2.2.2': {'address_family': {'vpnv4 unicast': {'route_map_name_in': 'test',
                                                                                                         'route_map_name_out': 'test'}}}}},
                                  'default': {'address_family': {'ipv4 unicast': {'dampening': True,
                                                                                  'dampening_half_life_time': 2100,
                                                                                  'dampening_max_suppress_time': 4200,
                                                                                  'dampening_reuse_time': 200,
                                                                                  'dampening_suppress_time': 200},
                                                                 'ipv6 unicast': {'dampening': True,
                                                                                  'dampening_half_life_time': 2160,
                                                                                  'dampening_max_suppress_time': 4260,
                                                                                  'dampening_reuse_time': 201,
                                                                                  'dampening_suppress_time': 201},
                                                                 'vpnv4 unicast': {'dampening': True,
                                                                                   'dampening_half_life_time': 900,
                                                                                   'dampening_max_suppress_time': 3600,
                                                                                   'dampening_reuse_time': 750,
                                                                                   'dampening_suppress_time': 2000}},
                                              'cluster_id': '4.4.4.4',
                                              'neighbor': {'10.4.6.6': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 1,
                                                                                                             'path': {'memory_usage': 3600,
                                                                                                                      'total_entries': 45},
                                                                                                             'prefixes': {'memory_usage': 4560,
                                                                                                                          'total_entries': 30},
                                                                                                             'routing_table_version': 56,
                                                                                                             'total_memory': 9384}}},
                                                           '2.2.2.2': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 1,
                                                                                                            'path': {'memory_usage': 3600,
                                                                                                                     'total_entries': 45},
                                                                                                            'prefixes': {'memory_usage': 4560,
                                                                                                                         'total_entries': 30},
                                                                                                            'routing_table_version': 56,
                                                                                                            'total_memory': 9384},
                                                                                          'vpnv6 unicast': {'bgp_table_version': 1,
                                                                                                            'path': {'memory_usage': 4860,
                                                                                                                     'total_entries': 45},
                                                                                                            'prefixes': {'memory_usage': 5280,
                                                                                                                         'total_entries': 30},
                                                                                                            'routing_table_version': 66,
                                                                                                            'total_memory': 11364}},
                                                                       'bgp_negotiated_capabilities': {'enhanced_refresh': 'advertised',
                                                                                                       'four_octets_asn': 'advertised '
                                                                                                                          'and '
                                                                                                                          'received',
                                                                                                       'graceful_restart': 'received',
                                                                                                       'route_refresh': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received(new)',
                                                                                                       'stateful_switchover': 'NO '
                                                                                                                              'for '
                                                                                                                              'session '
                                                                                                                              '1',
                                                                                                       'vpnv4_unicast': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received',
                                                                                                       'vpnv6_unicast': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received'},
                                                                       'bgp_negotiated_keepalive_timers': {'hold_time': 180,
                                                                                                           'keepalive_interval': 60},
                                                                       'bgp_neighbor_counters': {'messages': {'received': {'keepalives': 74,
                                                                                                                           'notifications': 0,
                                                                                                                           'opens': 1,
                                                                                                                           'updates': 6},
                                                                                                              'sent': {'keepalives': 75,
                                                                                                                       'notifications': 0,
                                                                                                                       'opens': 1,
                                                                                                                       'updates': 11}}},
                                                                       'bgp_session_transport': {'connection': {'last_reset': 'never',
                                                                                                                'state': 'established'},
                                                                                                 'transport': {'foreign_host': '2.2.2.2',
                                                                                                               'foreign_port': '179',
                                                                                                               'local_host': '4.4.4.4',
                                                                                                               'local_port': '35281'}},
                                                                       'bgp_version': 4,
                                                                       'remote_as': 100,
                                                                       'session_state': 'established'},
                                                           '20.4.6.6': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 1,
                                                                                                             'path': {'memory_usage': 3600,
                                                                                                                      'total_entries': 45},
                                                                                                             'prefixes': {'memory_usage': 4560,
                                                                                                                          'total_entries': 30},
                                                                                                             'routing_table_version': 56,
                                                                                                             'total_memory': 9384}}},
                                                           '200.0.1.1': {'address_family': {'ipv4 unicast': {'bgp_table_version': 28,
                                                                                                             'path': {'memory_usage': 3672,
                                                                                                                      'total_entries': 27},
                                                                                                             'prefixes': {'memory_usage': 6696,
                                                                                                                          'total_entries': 27},
                                                                                                             'routing_table_version': 28,
                                                                                                             'total_memory': 10648}}},
                                                           '200.0.2.1': {'address_family': {'ipv4 unicast': {'bgp_table_version': 28,
                                                                                                             'path': {'memory_usage': 3672,
                                                                                                                      'total_entries': 27},
                                                                                                             'prefixes': {'memory_usage': 6696,
                                                                                                                          'total_entries': 27},
                                                                                                             'routing_table_version': 28,
                                                                                                             'total_memory': 10648}}},
                                                           '200.0.4.1': {'address_family': {'ipv4 unicast': {'bgp_table_version': 28,
                                                                                                             'path': {'memory_usage': 3672,
                                                                                                                      'total_entries': 27},
                                                                                                             'prefixes': {'memory_usage': 6696,
                                                                                                                          'total_entries': 27},
                                                                                                             'routing_table_version': 28,
                                                                                                             'total_memory': 10648}}},
                                                           '2000::1:1': {'address_family': {'ipv6 unicast': {'bgp_table_version': 1,
                                                                                                             'routing_table_version': 1}}},
                                                           '2000::4:1': {'address_family': {'ipv6 unicast': {'bgp_table_version': 1,
                                                                                                             'routing_table_version': 1}}},
                                                           '2001::14:4': {'address_family': {'ipv6 unicast': {'bgp_table_version': 1,
                                                                                                              'routing_table_version': 1}}},
                                                           '2001::26:2': {'address_family': {'ipv6 unicast': {'bgp_table_version': 1,
                                                                                                              'routing_table_version': 1}}},
                                                           '2001:DB8:20:4:6::6': {'address_family': {'vpnv6 unicast': {'bgp_table_version': 66,
                                                                                                                       'path': {'memory_usage': 4860,
                                                                                                                                'total_entries': 45},
                                                                                                                       'prefixes': {'memory_usage': 5280,
                                                                                                                                    'total_entries': 30},
                                                                                                                       'routing_table_version': 66,
                                                                                                                       'total_memory': 11364}}},
                                                           '2001:DB8:4:6::6': {'address_family': {'vpnv6 unicast': {'bgp_table_version': 1,
                                                                                                                    'path': {'memory_usage': 4860,
                                                                                                                             'total_entries': 45},
                                                                                                                    'prefixes': {'memory_usage': 5280,
                                                                                                                                 'total_entries': 30},
                                                                                                                    'routing_table_version': 66,
                                                                                                                    'total_memory': 11364}}},
                                                           '201.0.14.4': {'address_family': {'ipv4 unicast': {'bgp_table_version': 28,
                                                                                                              'path': {'memory_usage': 3672,
                                                                                                                       'total_entries': 27},
                                                                                                              'prefixes': {'memory_usage': 6696,
                                                                                                                           'total_entries': 27},
                                                                                                              'routing_table_version': 28,
                                                                                                              'total_memory': 10648}}},
                                                           '201.0.26.2': {'address_family': {'ipv4 unicast': {'bgp_table_version': 28,
                                                                                                              'path': {'memory_usage': 3672,
                                                                                                                       'total_entries': 27},
                                                                                                              'prefixes': {'memory_usage': 6696,
                                                                                                                           'total_entries': 27},
                                                                                                              'routing_table_version': 28,
                                                                                                              'total_memory': 10648}}},
                                                           '3.3.3.3': {'address_family': {'vpnv4 unicast': {'bgp_table_version': 1,
                                                                                                            'path': {'memory_usage': 3600,
                                                                                                                     'total_entries': 45},
                                                                                                            'prefixes': {'memory_usage': 4560,
                                                                                                                         'total_entries': 30},
                                                                                                            'routing_table_version': 1,
                                                                                                            'total_memory': 9384},
                                                                                          'vpnv6 unicast': {'bgp_table_version': 1,
                                                                                                            'path': {'memory_usage': 4860,
                                                                                                                     'total_entries': 45},
                                                                                                            'prefixes': {'memory_usage': 5280,
                                                                                                                         'total_entries': 30},
                                                                                                            'routing_table_version': 1,
                                                                                                            'total_memory': 11364}},
                                                                       'bgp_negotiated_capabilities': {'enhanced_refresh': 'advertised',
                                                                                                       'four_octets_asn': 'advertised '
                                                                                                                          'and '
                                                                                                                          'received',
                                                                                                       'graceful_restart': 'received',
                                                                                                       'route_refresh': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received(new)',
                                                                                                       'stateful_switchover': 'NO '
                                                                                                                              'for '
                                                                                                                              'session '
                                                                                                                              '1',
                                                                                                       'vpnv4_unicast': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received',
                                                                                                       'vpnv6_unicast': 'advertised '
                                                                                                                        'and '
                                                                                                                        'received'},
                                                                       'bgp_negotiated_keepalive_timers': {'hold_time': 180,
                                                                                                           'keepalive_interval': 60},
                                                                       'bgp_neighbor_counters': {'messages': {'received': {'keepalives': 74,
                                                                                                                           'notifications': 0,
                                                                                                                           'opens': 1,
                                                                                                                           'updates': 6},
                                                                                                              'sent': {'keepalives': 75,
                                                                                                                       'notifications': 0,
                                                                                                                       'opens': 1,
                                                                                                                       'updates': 11}}},
                                                                       'bgp_session_transport': {'connection': {'last_reset': 'never',
                                                                                                                'state': 'established'},
                                                                                                 'transport': {'foreign_host': '3.3.3.3',
                                                                                                               'foreign_port': '179',
                                                                                                               'local_host': '4.4.4.4',
                                                                                                               'local_port': '56031'}},
                                                                       'bgp_version': 4,
                                                                       'remote_as': 100,
                                                                       'session_state': 'established'}}},
                                  'vrf1': {'cluster_id': '4.4.4.4'},
                                  'vrf2': {'cluster_id': '4.4.4.4'}}}}}

    BgpOpsOutput_table = {'instance': {'default': {'vrf': {'EVPN-BGP-Table': {'address_family': {'vpnv4 unicast RD 65535:1': {'prefixes': {'100.1.1.0/17': {'index': {1: {'ext_community': 'RT:65535:1',
                                                                                                                                                 'gateway': '0.0.0.0',
                                                                                                                                                 'localpref': 100,
                                                                                                                                                 'metric': 0,
                                                                                                                                                 'next_hop': '0.0.0.0',
                                                                                                                                                 'origin_codes': '?',
                                                                                                                                                 'originator': '33.33.33.33',
                                                                                                                                                 'status_codes': '*>',
                                                                                                                                                 'weight': '32768'}},
                                                                                                                                   'table_version': '4'},
                                                                                                                  '3.3.3.0/17': {'index': {1: {'ext_community': 'RT:65535:1',
                                                                                                                                               'gateway': '0.0.0.0',
                                                                                                                                               'localpref': 100,
                                                                                                                                               'metric': 0,
                                                                                                                                               'next_hop': '0.0.0.0',
                                                                                                                                               'origin_codes': '?',
                                                                                                                                               'originator': '33.33.33.33',
                                                                                                                                               'status_codes': '*>',
                                                                                                                                               'weight': '32768'},
                                                                                                                                           2: {'ext_community': 'RT:65535:1',
                                                                                                                                               'gateway': '3.3.3.254',
                                                                                                                                               'localpref': 100,
                                                                                                                                               'metric': 0,
                                                                                                                                               'next_hop': '3.3.3.254',
                                                                                                                                               'next_hop_igp_metric': 111,
                                                                                                                                               'origin_codes': '?',
                                                                                                                                               'originator': '33.33.33.22',
                                                                                                                                               'status_codes': '* '}},
                                                                                                                                 'table_version': '3'}}}}},
                                  'VRF1': {'address_family': {'vpnv4 unicast RD 100:100': {'paths': '(1 '
                                                                                                    'available, '
                                                                                                    'best '
                                                                                                    '#1, '
                                                                                                    'table '
                                                                                                    'VRF1)',
                                                                                           'prefixes': {'11.11.11.11/32': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                                         'localpref': 100,
                                                                                                                                         'metric': 0,
                                                                                                                                         'next_hop': '0.0.0.0',
                                                                                                                                         'origin_codes': '?',
                                                                                                                                         'originator': '10.1.1.1',
                                                                                                                                         'status_codes': '*>',
                                                                                                                                         'weight': '32768'}},
                                                                                                                           'table_version': '2'}}},
                                                              'vpnv4 unicast RD 300:1': {'bgp_table_version': 56,
                                                                                         'default_vrf': 'VRF1',
                                                                                         'route_distinguisher': '300:1',
                                                                                         'route_identifier': '4.4.4.4'},
                                                              'vpnv6 unicast RD 100:100': {'paths': '(1 '
                                                                                                    'available, '
                                                                                                    'best '
                                                                                                    '#1, '
                                                                                                    'table '
                                                                                                    'VRF1)',
                                                                                           'prefixes': {'2001:11:11::11/128': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                                             'localpref': 100,
                                                                                                                                             'metric': 0,
                                                                                                                                             'next_hop': '::',
                                                                                                                                             'origin_codes': '?',
                                                                                                                                             'originator': '10.1.1.1',
                                                                                                                                             'status_codes': '*>',
                                                                                                                                             'weight': '32768'}},
                                                                                                                               'table_version': '2'}}}}},
                                  'VRF2': {'address_family': {'vpnv4 unicast RD 400:1': {'bgp_table_version': 56,
                                                                                         'default_vrf': 'VRF2',
                                                                                         'route_distinguisher': '400:1',
                                                                                         'route_identifier': '4.4.4.4'}}},
                                  'default': {'address_family': {'ipv4 unicast': {'prefixes': {'1.1.1.1/32': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                            'localpref': 100,
                                                                                                                            'metric': 0,
                                                                                                                            'next_hop': '0.0.0.0',
                                                                                                                            'origin_codes': '?',
                                                                                                                            'originator': '10.1.1.1',
                                                                                                                            'status_codes': '*>',
                                                                                                                            'update_group': 3,
                                                                                                                            'weight': '32768'}},
                                                                                                              'table_version': '4'},
                                                                                               '10.1.1.0/24': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                             'localpref': 100,
                                                                                                                             'metric': 0,
                                                                                                                             'next_hop': '0.0.0.0',
                                                                                                                             'origin_codes': '?',
                                                                                                                             'originator': '10.1.1.1',
                                                                                                                             'status_codes': '*>',
                                                                                                                             'update_group': 3,
                                                                                                                             'weight': '32768'},
                                                                                                                         2: {'gateway': '10.1.1.2',
                                                                                                                             'localpref': 100,
                                                                                                                             'metric': 0,
                                                                                                                             'next_hop': '10.1.1.2',
                                                                                                                             'origin_codes': '?',
                                                                                                                             'originator': '10.1.1.2',
                                                                                                                             'status_codes': '* '
                                                                                                                                             'i',
                                                                                                                             'update_group': 3}},
                                                                                                               'table_version': '5'},
                                                                                               '2.2.2.2/32': {'index': {1: {'gateway': '10.1.1.2',
                                                                                                                            'localpref': 100,
                                                                                                                            'metric': 0,
                                                                                                                            'next_hop': '10.1.1.2',
                                                                                                                            'origin_codes': '?',
                                                                                                                            'originator': '10.1.1.2',
                                                                                                                            'status_codes': '*>'}},
                                                                                                              'table_version': '2'}}},
                                                                 'ipv6 unicast': {'prefixes': {'2001:1:1:1::1/128': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                                   'localpref': 100,
                                                                                                                                   'metric': 0,
                                                                                                                                   'next_hop': '::',
                                                                                                                                   'origin_codes': '?',
                                                                                                                                   'originator': '10.1.1.1',
                                                                                                                                   'status_codes': '*>',
                                                                                                                                   'update_group': 1,
                                                                                                                                   'weight': '32768'}},
                                                                                                                     'table_version': '4'},
                                                                                               '2001:2:2:2::2/128': {'index': {1: {'gateway': '2001:DB8:1:1::2',
                                                                                                                                   'localpref': 100,
                                                                                                                                   'metric': 0,
                                                                                                                                   'next_hop': '2001:DB8:1:1::2',
                                                                                                                                   'origin_codes': '?',
                                                                                                                                   'originator': '10.1.1.2',
                                                                                                                                   'status_codes': '* '
                                                                                                                                                   'i'}},
                                                                                                                     'table_version': '2'},
                                                                                               '2001:DB8:1:1::/64': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                                   'localpref': 100,
                                                                                                                                   'metric': 0,
                                                                                                                                   'next_hop': '::',
                                                                                                                                   'origin_codes': '?',
                                                                                                                                   'originator': '10.1.1.1',
                                                                                                                                   'status_codes': '*>',
                                                                                                                                   'update_group': 1,
                                                                                                                                   'weight': '32768'},
                                                                                                                               2: {'gateway': '2001:DB8:1:1::2',
                                                                                                                                   'localpref': 100,
                                                                                                                                   'metric': 0,
                                                                                                                                   'next_hop': '2001:DB8:1:1::2',
                                                                                                                                   'origin_codes': '?',
                                                                                                                                   'originator': '10.1.1.2',
                                                                                                                                   'status_codes': '* '
                                                                                                                                                   'i',
                                                                                                                                   'update_group': 1}},
                                                                                                                     'table_version': '5'}}},
                                                                 'vpnv4 unicast RD 200:1': {'bgp_table_version': 56,
                                                                                            'default_vrf': 'default',
                                                                                            'route_distinguisher': '200:1',
                                                                                            'route_identifier': '4.4.4.4'},
                                                                 'vpnv4 unicast RD 200:2': {'bgp_table_version': 56,
                                                                                            'default_vrf': 'default',
                                                                                            'route_distinguisher': '200:2',
                                                                                            'route_identifier': '4.4.4.4'}}},
                                  'evpn1': {'address_family': {'l2vpn e-vpn RD 65535:1': {'bgp_table_version': 4,
                                                                                          'default_vrf': 'evpn1',
                                                                                          'route_distinguisher': '65535:1',
                                                                                          'route_identifier': '33.33.33.33'},
                                                               'vpnv4 unicast RD 65535:1': {'bgp_table_version': 5,
                                                                                            'default_vrf': 'evpn1',
                                                                                            'prefixes': {'100.1.1.0/24': {'index': {1: {'gateway': '0.0.0.0',
                                                                                                                                        'localpref': 100,
                                                                                                                                        'metric': 0,
                                                                                                                                        'next_hop': '0.0.0.0',
                                                                                                                                        'origin_codes': '?',
                                                                                                                                        'originator': '33.33.33.33',
                                                                                                                                        'status_codes': '*>',
                                                                                                                                        'update_group': 1,
                                                                                                                                        'weight': '32768'}},
                                                                                                                          'table_version': '5'},
                                                                                                         '3.3.3.0/24': {'index': {1: {'gateway': '3.3.3.254',
                                                                                                                                      'localpref': 100,
                                                                                                                                      'metric': 0,
                                                                                                                                      'next_hop': '3.3.3.254',
                                                                                                                                      'origin_codes': '?',
                                                                                                                                      'originator': '33.33.33.22',
                                                                                                                                      'status_codes': '* ',
                                                                                                                                      'update_group': 1},
                                                                                                                                  2: {'gateway': '0.0.0.0',
                                                                                                                                      'localpref': 100,
                                                                                                                                      'metric': 0,
                                                                                                                                      'next_hop': '0.0.0.0',
                                                                                                                                      'origin_codes': '?',
                                                                                                                                      'originator': '33.33.33.33',
                                                                                                                                      'status_codes': '*>',
                                                                                                                                      'update_group': 1,
                                                                                                                                      'weight': '32768'}},
                                                                                                                        'table_version': '4'}},
                                                                                            'route_distinguisher': '65535:1',
                                                                                            'route_identifier': '33.33.33.33'}}}}}}}

    BgpOpsOutput_routesperpeer = {'instance': {'default': {'vrf': {'default': {'neighbor': {'10.4.6.6': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 68,
                                                                                                             'msg_sent': 75,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': '5',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:03:23'}}},
                                                           '2.2.2.2': {'address_family': {'ipv4 unicast': {'advertised': {'15.1.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                        'metric': 2219,
                                                                                                                                                        'next_hop': '1.1.1.1',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '200 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '47751 '
                                                                                                                                                                '{27016}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '15.1.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                        'metric': 2219,
                                                                                                                                                        'next_hop': '1.1.1.1',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '200 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '47751 '
                                                                                                                                                                '{27016}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '15.1.3.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                        'metric': 2219,
                                                                                                                                                        'next_hop': '1.1.1.1',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '200 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '47751 '
                                                                                                                                                                '{27016}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '15.1.4.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                        'metric': 2219,
                                                                                                                                                        'next_hop': '1.1.1.1',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '200 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '47751 '
                                                                                                                                                                '{27016}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '15.1.5.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                        'metric': 2219,
                                                                                                                                                        'next_hop': '1.1.1.1',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '200 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '47751 '
                                                                                                                                                                '{27016}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '46.2.2.0/24': {'index': {1: {'metric': 100,
                                                                                                                                                        'next_hop': '20.4.6.6',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '400 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '{47751}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '46.2.3.0/24': {'index': {1: {'metric': 100,
                                                                                                                                                        'next_hop': '20.4.6.6',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '400 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '{47751}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '46.2.4.0/24': {'index': {1: {'metric': 100,
                                                                                                                                                        'next_hop': '20.4.6.6',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '400 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '{47751}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '46.2.5.0/24': {'index': {1: {'metric': 100,
                                                                                                                                                        'next_hop': '20.4.6.6',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '400 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '{47751}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}},
                                                                                                                          '46.2.6.0/24': {'index': {1: {'metric': 100,
                                                                                                                                                        'next_hop': '20.4.6.6',
                                                                                                                                                        'origin_codes': 'e',
                                                                                                                                                        'path': '400 '
                                                                                                                                                                '33299 '
                                                                                                                                                                '51178 '
                                                                                                                                                                '{47751}',
                                                                                                                                                        'status_codes': '*>',
                                                                                                                                                        'weight': 0}}}},
                                                                                                           'routes': {'46.1.1.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                    'next_hop': '21.0.0.2',
                                                                                                                                                    'origin_codes': 'e',
                                                                                                                                                    'path': '300 '
                                                                                                                                                            '33299 '
                                                                                                                                                            '51178 '
                                                                                                                                                            '47751 '
                                                                                                                                                            '{27016}',
                                                                                                                                                    'status_codes': '*>',
                                                                                                                                                    'weight': 0}}},
                                                                                                                      '46.1.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                    'next_hop': '21.0.0.2',
                                                                                                                                                    'origin_codes': 'e',
                                                                                                                                                    'path': '300 '
                                                                                                                                                            '33299 '
                                                                                                                                                            '51178 '
                                                                                                                                                            '47751 '
                                                                                                                                                            '{27016}',
                                                                                                                                                    'status_codes': '*>',
                                                                                                                                                    'weight': 0}}},
                                                                                                                      '46.1.3.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                    'next_hop': '21.0.0.2',
                                                                                                                                                    'origin_codes': 'e',
                                                                                                                                                    'path': '300 '
                                                                                                                                                            '33299 '
                                                                                                                                                            '51178 '
                                                                                                                                                            '47751 '
                                                                                                                                                            '{27016}',
                                                                                                                                                    'status_codes': '*>',
                                                                                                                                                    'weight': 0}}},
                                                                                                                      '46.1.4.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                    'next_hop': '21.0.0.2',
                                                                                                                                                    'origin_codes': 'e',
                                                                                                                                                    'path': '300 '
                                                                                                                                                            '33299 '
                                                                                                                                                            '51178 '
                                                                                                                                                            '47751 '
                                                                                                                                                            '{27016}',
                                                                                                                                                    'status_codes': '*>',
                                                                                                                                                    'weight': 0}}},
                                                                                                                      '46.1.5.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                    'next_hop': '21.0.0.2',
                                                                                                                                                    'origin_codes': 'e',
                                                                                                                                                    'path': '300 '
                                                                                                                                                            '33299 '
                                                                                                                                                            '51178 '
                                                                                                                                                            '47751 '
                                                                                                                                                            '{27016}',
                                                                                                                                                    'status_codes': '*>',
                                                                                                                                                    'weight': 0}}}}},
                                                                                          'ipv6 unicast': {'advertised': {},
                                                                                                           'routes': {}},
                                                                                          'vpnv4 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 82,
                                                                                                            'msg_sent': 88,
                                                                                                            'output_queue': 0,
                                                                                                            'received_routes': {},
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 1,
                                                                                                            'up_down': '01:12:00'},
                                                                                          'vpnv4 unicast RD 300:1': {'received_routes': {'46.1.1.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '21.0.0.2',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                         '46.1.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '21.0.0.2',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                         '46.1.3.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '21.0.0.2',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                         '46.1.4.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '21.0.0.2',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                         '46.1.5.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '21.0.0.2',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*',
                                                                                                                                                                       'weight': 0}}}}},
                                                                                          'vpnv6 unicast': {'input_queue': 0,
                                                                                                            'msg_rcvd': 82,
                                                                                                            'msg_sent': 88,
                                                                                                            'output_queue': 0,
                                                                                                            'state_pfxrcd': '10',
                                                                                                            'tbl_ver': 1,
                                                                                                            'up_down': '01:12:00'}},
                                                                       'remote_as': 100},
                                                           '20.4.6.6': {'address_family': {'vpnv4 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 67,
                                                                                                             'msg_sent': 72,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': '5',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:03:14'}}},
                                                           '200.0.1.1': {'address_family': {'ipv4 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 0,
                                                                                                             'msg_sent': 0,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': 'Idle',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:07:38'}}},
                                                           '200.0.2.1': {'address_family': {'ipv4 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 0,
                                                                                                             'msg_sent': 0,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': 'Idle',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': 'never'}}},
                                                           '200.0.4.1': {'address_family': {'ipv4 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 0,
                                                                                                             'msg_sent': 0,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': 'Idle',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:07:38'}}},
                                                           '2000::1:1': {'address_family': {'ipv6 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 0,
                                                                                                             'msg_sent': 0,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': 'Idle',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:07:38'}}},
                                                           '2000::4:1': {'address_family': {'ipv6 unicast': {'input_queue': 0,
                                                                                                             'msg_rcvd': 0,
                                                                                                             'msg_sent': 0,
                                                                                                             'output_queue': 0,
                                                                                                             'state_pfxrcd': 'Idle',
                                                                                                             'tbl_ver': 1,
                                                                                                             'up_down': '01:07:38'}}},
                                                           '2001::14:4': {'address_family': {'ipv6 unicast': {'input_queue': 0,
                                                                                                              'msg_rcvd': 0,
                                                                                                              'msg_sent': 0,
                                                                                                              'output_queue': 0,
                                                                                                              'state_pfxrcd': 'Idle',
                                                                                                              'tbl_ver': 1,
                                                                                                              'up_down': 'never'}}},
                                                           '2001::26:2': {'address_family': {'ipv6 unicast': {'input_queue': 0,
                                                                                                              'msg_rcvd': 0,
                                                                                                              'msg_sent': 0,
                                                                                                              'output_queue': 0,
                                                                                                              'state_pfxrcd': 'Idle',
                                                                                                              'tbl_ver': 1,
                                                                                                              'up_down': '01:07:38'}}},
                                                           '2001:DB8:20:4:6::6': {'address_family': {'vpnv6 unicast': {'input_queue': 0,
                                                                                                                       'msg_rcvd': 67,
                                                                                                                       'msg_sent': 73,
                                                                                                                       'output_queue': 0,
                                                                                                                       'state_pfxrcd': '5',
                                                                                                                       'tbl_ver': 1,
                                                                                                                       'up_down': '01:03:11'}}},
                                                           '2001:DB8:4:6::6': {'address_family': {'vpnv6 unicast': {'input_queue': 0,
                                                                                                                    'msg_rcvd': 67,
                                                                                                                    'msg_sent': 75,
                                                                                                                    'output_queue': 0,
                                                                                                                    'state_pfxrcd': '5',
                                                                                                                    'tbl_ver': 1,
                                                                                                                    'up_down': '01:03:19'}}},
                                                           '201.0.14.4': {'address_family': {'ipv4 unicast': {'input_queue': 0,
                                                                                                              'msg_rcvd': 0,
                                                                                                              'msg_sent': 0,
                                                                                                              'output_queue': 0,
                                                                                                              'state_pfxrcd': 'Idle',
                                                                                                              'tbl_ver': 1,
                                                                                                              'up_down': 'never'}}},
                                                           '201.0.26.2': {'address_family': {'ipv4 unicast': {'input_queue': 0,
                                                                                                              'msg_rcvd': 0,
                                                                                                              'msg_sent': 0,
                                                                                                              'output_queue': 0,
                                                                                                              'state_pfxrcd': 'Idle',
                                                                                                              'tbl_ver': 1,
                                                                                                              'up_down': '01:07:38'}}},
                                                           '3.3.3.3': {'address_family': {'ipv4 multicast': {'received_routes': {'1.2.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'i',
                                                                                                                                                              'path': '2 '
                                                                                                                                                                      '3 '
                                                                                                                                                                      '4',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                 '1.2.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'i',
                                                                                                                                                              'path': '2 '
                                                                                                                                                                      '3 '
                                                                                                                                                                      '4',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}}}},
                                                                                          'ipv4 unicast': {'received_routes': {'1.1.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                            'metric': 2222,
                                                                                                                                                            'next_hop': '3.3.3.3',
                                                                                                                                                            'origin_codes': 'i',
                                                                                                                                                            'path': '1 '
                                                                                                                                                                    '2 '
                                                                                                                                                                    '3 '
                                                                                                                                                                    '65000 '
                                                                                                                                                                    '23',
                                                                                                                                                            'status_codes': '*',
                                                                                                                                                            'weight': 0}}},
                                                                                                                               '1.1.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                            'metric': 2222,
                                                                                                                                                            'next_hop': '3.3.3.3',
                                                                                                                                                            'origin_codes': 'i',
                                                                                                                                                            'path': '1 '
                                                                                                                                                                    '2 '
                                                                                                                                                                    '3 '
                                                                                                                                                                    '65000 '
                                                                                                                                                                    '23',
                                                                                                                                                            'status_codes': '*',
                                                                                                                                                            'weight': 0}}},
                                                                                                                               '1.6.0.0/16': {'index': {1: {'localprf': 100,
                                                                                                                                                            'next_hop': '3.3.3.3',
                                                                                                                                                            'origin_codes': 'i',
                                                                                                                                                            'path': '10 '
                                                                                                                                                                    '20 '
                                                                                                                                                                    '30 '
                                                                                                                                                                    '40 '
                                                                                                                                                                    '50 '
                                                                                                                                                                    '60 '
                                                                                                                                                                    '70 '
                                                                                                                                                                    '80 '
                                                                                                                                                                    '90',
                                                                                                                                                            'status_codes': '*>',
                                                                                                                                                            'weight': 0}}}}},
                                                                                          'ipv6 multicast': {'received_routes': {}},
                                                                                          'ipv6 unicast': {'received_routes': {}},
                                                                                          'link-state': {'received_routes': {'[2]:[77][7,0][9.9.9.9,1,151587081][29.1.1.1,22][3.3.3.3,29.0.1.30]/616': {'index': {1: {'localprf': 100,
                                                                                                                                                                                                                      'metric': 4444,
                                                                                                                                                                                                                      'next_hop': '3.3.3.3',
                                                                                                                                                                                                                      'origin_codes': 'i',
                                                                                                                                                                                                                      'path': '3 '
                                                                                                                                                                                                                              '10 '
                                                                                                                                                                                                                              '20 '
                                                                                                                                                                                                                              '30 '
                                                                                                                                                                                                                              '40 '
                                                                                                                                                                                                                              '50 '
                                                                                                                                                                                                                              '60 '
                                                                                                                                                                                                                              '70 '
                                                                                                                                                                                                                              '80 '
                                                                                                                                                                                                                              '90',
                                                                                                                                                                                                                      'status_codes': '*>',
                                                                                                                                                                                                                      'weight': 0}}},
                                                                                                                             '[2]:[77][7,0][9.9.9.9,2,151587081][29.1.1.1,22][3.3.3.3,29.0.1.31]/616': {'index': {1: {'localprf': 100,
                                                                                                                                                                                                                      'metric': 4444,
                                                                                                                                                                                                                      'next_hop': '3.3.3.3',
                                                                                                                                                                                                                      'origin_codes': 'i',
                                                                                                                                                                                                                      'path': '3 '
                                                                                                                                                                                                                              '10 '
                                                                                                                                                                                                                              '20 '
                                                                                                                                                                                                                              '30 '
                                                                                                                                                                                                                              '40 '
                                                                                                                                                                                                                              '50 '
                                                                                                                                                                                                                              '60 '
                                                                                                                                                                                                                              '70 '
                                                                                                                                                                                                                              '80 '
                                                                                                                                                                                                                              '90',
                                                                                                                                                                                                                      'status_codes': '*>',
                                                                                                                                                                                                                      'weight': 0}}}}},
                                                                                          'vpnv4 unicast': {'advertised': {},
                                                                                                            'input_queue': 0,
                                                                                                            'msg_rcvd': 0,
                                                                                                            'msg_sent': 0,
                                                                                                            'output_queue': 0,
                                                                                                            'received_routes': {},
                                                                                                            'routes': {},
                                                                                                            'state_pfxrcd': 'Idle',
                                                                                                            'tbl_ver': 1,
                                                                                                            'up_down': 'never'},
                                                                                          'vpnv4 unicast RD 0:0': {'received_routes': {}},
                                                                                          'vpnv4 unicast RD 101:100': {'received_routes': {'1.3.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                                        'metric': 4444,
                                                                                                                                                                        'next_hop': '3.3.3.3',
                                                                                                                                                                        'origin_codes': 'i',
                                                                                                                                                                        'path': '3 '
                                                                                                                                                                                '10 '
                                                                                                                                                                                '20 '
                                                                                                                                                                                '4 '
                                                                                                                                                                                '5 '
                                                                                                                                                                                '6 '
                                                                                                                                                                                '3 '
                                                                                                                                                                                '10 '
                                                                                                                                                                                '20 '
                                                                                                                                                                                '4 '
                                                                                                                                                                                '5 '
                                                                                                                                                                                '6',
                                                                                                                                                                        'status_codes': '*',
                                                                                                                                                                        'weight': 0}}},
                                                                                                                                           '1.3.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                                        'metric': 4444,
                                                                                                                                                                        'next_hop': '3.3.3.3',
                                                                                                                                                                        'origin_codes': 'i',
                                                                                                                                                                        'path': '3 '
                                                                                                                                                                                '10 '
                                                                                                                                                                                '20 '
                                                                                                                                                                                '4 '
                                                                                                                                                                                '5 '
                                                                                                                                                                                '6 '
                                                                                                                                                                                '3 '
                                                                                                                                                                                '10 '
                                                                                                                                                                                '20 '
                                                                                                                                                                                '4 '
                                                                                                                                                                                '5 '
                                                                                                                                                                                '6',
                                                                                                                                                                        'status_codes': '*',
                                                                                                                                                                        'weight': 0}}}}},
                                                                                          'vpnv4 unicast RD 102:100': {'received_routes': {}},
                                                                                          'vpnv4 unicast RD 200:1': {'routes': {'15.1.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.3.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.4.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.5.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}}}},
                                                                                          'vpnv4 unicast RD 200:2': {'routes': {'15.1.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.3.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.4.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.5.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                              'weight': 0}}}}},
                                                                                          'vpnv4 unicast RD 300:1': {'advertised': {'46.1.1.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                  'next_hop': '10.4.6.6',
                                                                                                                                                                  'origin_codes': 'e',
                                                                                                                                                                  'path': '300 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}',
                                                                                                                                                                  'status_codes': '*>',
                                                                                                                                                                  'weight': 0}}},
                                                                                                                                    '46.1.2.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                  'next_hop': '10.4.6.6',
                                                                                                                                                                  'origin_codes': 'e',
                                                                                                                                                                  'path': '300 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}',
                                                                                                                                                                  'status_codes': '*>',
                                                                                                                                                                  'weight': 0}}},
                                                                                                                                    '46.1.3.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                  'next_hop': '10.4.6.6',
                                                                                                                                                                  'origin_codes': 'e',
                                                                                                                                                                  'path': '300 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}',
                                                                                                                                                                  'status_codes': '*>',
                                                                                                                                                                  'weight': 0}}},
                                                                                                                                    '46.1.4.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                  'next_hop': '10.4.6.6',
                                                                                                                                                                  'origin_codes': 'e',
                                                                                                                                                                  'path': '300 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}',
                                                                                                                                                                  'status_codes': '*>',
                                                                                                                                                                  'weight': 0}}},
                                                                                                                                    '46.1.5.0/24': {'index': {1: {'metric': 2219,
                                                                                                                                                                  'next_hop': '10.4.6.6',
                                                                                                                                                                  'origin_codes': 'e',
                                                                                                                                                                  'path': '300 '
                                                                                                                                                                          '33299 '
                                                                                                                                                                          '51178 '
                                                                                                                                                                          '47751 '
                                                                                                                                                                          '{27016}',
                                                                                                                                                                  'status_codes': '*>',
                                                                                                                                                                  'weight': 0}}}},
                                                                                                                     'default_vrf': 'VRF1',
                                                                                                                     'route_distinguisher': '300:1',
                                                                                                                     'routes': {'15.1.1.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0},
                                                                                                                                                          2: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.2.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0},
                                                                                                                                                          2: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.3.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0},
                                                                                                                                                          2: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.4.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0},
                                                                                                                                                          2: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0}}},
                                                                                                                                '15.1.5.0/24': {'index': {1: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0},
                                                                                                                                                          2: {'localprf': 100,
                                                                                                                                                              'metric': 2219,
                                                                                                                                                              'next_hop': '3.3.3.3',
                                                                                                                                                              'origin_codes': 'e',
                                                                                                                                                              'path': '200 '
                                                                                                                                                                      '33299 '
                                                                                                                                                                      '51178 '
                                                                                                                                                                      '47751 '
                                                                                                                                                                      '{27016}',
                                                                                                                                                              'status_codes': '*',
                                                                                                                                                              'weight': 0}}}}},
                                                                                          'vpnv4 unicast RD 400:1':
                                                                                            {'advertised':
                                                                                                {'46.2.2.0/24':
                                                                                                    {'index':
                                                                                                        {1:
                                                                                                            {'metric': 2219,
                                                                                                             'next_hop': '20.4.6.6',
                                                                                                             'origin_codes': 'e',
                                                                                                             'path': '400 '
                                                                                                                     '33299 '
                                                                                                                     '51178 '
                                                                                                                     '47751 '
                                                                                                                     '{27016}',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 0}}},
                                                                                                '46.2.3.0/24':
                                                                                                    {'index':
                                                                                                        {1:
                                                                                                            {'metric': 2219,
                                                                                                             'next_hop': '20.4.6.6',
                                                                                                             'origin_codes': 'e',
                                                                                                             'path': '400 '
                                                                                                                     '33299 '
                                                                                                                     '51178 '
                                                                                                                     '47751 '
                                                                                                                     '{27016}',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 0}}},
                                                                                                '46.2.4.0/24':
                                                                                                    {'index':
                                                                                                        {1:
                                                                                                            {'metric': 2219,
                                                                                                             'next_hop': '20.4.6.6',
                                                                                                             'origin_codes': 'e',
                                                                                                             'path': '400 '
                                                                                                                     '33299 '
                                                                                                                     '51178 '
                                                                                                                     '47751 '
                                                                                                                     '{27016}',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 0}}},
                                                                                                '46.2.5.0/24':
                                                                                                    {'index':
                                                                                                        {1:
                                                                                                            {'metric': 2219,
                                                                                                             'next_hop': '20.4.6.6',
                                                                                                             'origin_codes': 'e',
                                                                                                             'path': '400 '
                                                                                                                     '33299 '
                                                                                                                     '51178 '
                                                                                                                     '47751 '
                                                                                                                     '{27016}',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 0}}},
                                                                                                '46.2.6.0/24':
                                                                                                    {'index':
                                                                                                        {1:
                                                                                                            {'metric': 2219,
                                                                                                             'next_hop': '20.4.6.6',
                                                                                                             'origin_codes': 'e',
                                                                                                             'path': '400 '
                                                                                                                     '33299 '
                                                                                                                     '51178 '
                                                                                                                     '47751 '
                                                                                                                     '{27016}',
                                                                                                             'status_codes': '*>',
                                                                                                             'weight': 0}}}},
                                                                                            'default_vrf': 'VRF2',
                                                                                            'route_distinguisher': '400:1'},
                                                                                          'vpnv6 unicast': {'advertised': {},
                                                                                                            'input_queue': 0,
                                                                                                            'msg_rcvd': 0,
                                                                                                            'msg_sent': 0,
                                                                                                            'output_queue': 0,
                                                                                                            'received_routes': {},
                                                                                                            'state_pfxrcd': 'Idle',
                                                                                                            'tbl_ver': 1,
                                                                                                            'up_down': 'never'},
                                                                                          'vpnv6 unicast RD 0xbb00010000000000': {'received_routes': {}},
                                                                                          'vpnv6 unicast RD 100:200': {'received_routes': {'aaaa:1::/113': {'index': {1: {'localprf': 100,
                                                                                                                                                                          'next_hop': '4444',
                                                                                                                                                                          'origin_codes': 'i',
                                                                                                                                                                          'status_codes': '*>',
                                                                                                                                                                          'weight': 0}}},
                                                                                                                                           'aaaa:1::8000/113': {'index': {1: {'localprf': 100,
                                                                                                                                                                              'next_hop': '4444',
                                                                                                                                                                              'origin_codes': 'i',
                                                                                                                                                                              'status_codes': '*>',
                                                                                                                                                                              'weight': 0}}}}},
                                                                                          'vpnv6 unicast RD 300:1': {'advertised': {'646:11:11:1::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:11:11:2::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:11:11:3::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:11:11:4::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '300 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:11:11::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                     'next_hop': '2001:DB8:4:6::6',
                                                                                                                                                                     'origin_codes': 'e',
                                                                                                                                                                     'path': '300 '
                                                                                                                                                                             '33299 '
                                                                                                                                                                             '51178 '
                                                                                                                                                                             '47751 '
                                                                                                                                                                             '{27016}',
                                                                                                                                                                     'status_codes': '*>',
                                                                                                                                                                     'weight': 0}}}},
                                                                                                                     'default_vrf': 'VRF1',
                                                                                                                     'route_distinguisher': '300:1'},
                                                                                          'vpnv6 unicast RD 400:1': {'advertised': {'646:22:22:1::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:20:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '400 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:22:22:2::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:20:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '400 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:22:22:3::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:20:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '400 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:22:22:4::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                       'next_hop': '2001:DB8:20:4:6::6',
                                                                                                                                                                       'origin_codes': 'e',
                                                                                                                                                                       'path': '400 '
                                                                                                                                                                               '33299 '
                                                                                                                                                                               '51178 '
                                                                                                                                                                               '47751 '
                                                                                                                                                                               '{27016}',
                                                                                                                                                                       'status_codes': '*>',
                                                                                                                                                                       'weight': 0}}},
                                                                                                                                    '646:22:22::/64': {'index': {1: {'metric': 2219,
                                                                                                                                                                     'next_hop': '2001:DB8:20:4:6::6',
                                                                                                                                                                     'origin_codes': 'e',
                                                                                                                                                                     'path': '400 '
                                                                                                                                                                             '33299 '
                                                                                                                                                                             '51178 '
                                                                                                                                                                             '47751 '
                                                                                                                                                                             '{27016}',
                                                                                                                                                                     'status_codes': '*>',
                                                                                                                                                                     'weight': 0}}}},
                                                                                                                     'default_vrf': 'VRF2',
                                                                                                                     'route_distinguisher': '400:1'}},
                                                                       'remote_as': 100}}}}}}}
