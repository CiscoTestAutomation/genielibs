''' 
BGP Genie Ops Object Outputs for NXOS.
'''

import xml.etree.ElementTree as ET

class BgpOutput(object):

    ShowVrf = {
        'vrfs':
            {'VRF1':
                {'reason': '--',
                'vrf_id': 3,
                'vrf_state': 'Up'},
            'default':
                {'reason': '--',
                'vrf_id': 1,
                'vrf_state': 'Up'}}}
    ShowVrf_vrf1 = {
        'vrfs':
            {'VRF1':
                 {'reason': '--',
                  'vrf_id': 3,
                  'vrf_state': 'Up'},}}
    ShowRoutingVrfAll = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'vpnv4 unicast':
                        {'bgp_distance_internal_as': 33,
                        'bgp_distance_local': 55,
                        'ip/mask':
                            {'10.121.0.0/8':
                                {'ubest_num': '1',
                                'mbest_num': '0',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'Null0':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '55',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'discard',
                                                        'tag': '100'}}}}}}},
                            '10.21.33.33/32':
                                {'ubest_num': '1',
                                'mbest_num': '1',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'10.36.3.3':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '33',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'internal',
                                                        'route_table': 'default',
                                                        'tag': '100 (mpls-vpn)'}}}}},
                                    'multicast':
                                        {'nexthop':
                                            {'10.36.3.3':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '33',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'internal',
                                                        'route_table': 'default',
                                                        'tag': '100 (mpls-vpn)'}}}}}}},
                            '10.229.11.11/32':
                                {'ubest_num': '2',
                                'mbest_num': '0',
                                'attach': 'attached',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'10.229.11.11':
                                                {'protocol':
                                                    {'local':
                                                        {'uptime': '5w4d',
                                                        'preference': '0',
                                                        'metric': '0',
                                                        'interface': 'Lo1'},
                                                    'direct':
                                                        {'uptime': '5w4d',
                                                        'preference': '0',
                                                        'metric': '0',
                                                        'interface': 'Lo1'}}}}}}}}}}},
            'default':
                {'address_family':
                    {'ipv4 unicast':
                        {'bgp_distance_extern_as': 20,
                        'bgp_distance_internal_as': 200,
                        'ip/mask':
                            {'10.106.0.0/8':
                                {'ubest_num': '1',
                                'mbest_num': '0',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'vrf default':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '18:11:28',
                                                        'preference': '20',
                                                        'metric': '0',
                                                        'protocol_id': '333',
                                                        'attribute': 'external',
                                                        'tag': '333',
                                                        'interface': 'Null0'}}}}}}},
                            '10.16.1.0/24':
                                {'ubest_num': '1',
                                'mbest_num': '0',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'2001:db8:8b05::1002':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '15:57:39',
                                                        'preference': '200',
                                                        'metric': '4444',
                                                        'protocol_id': '333',
                                                        'attribute': 'internal',
                                                        'route_table': 'default',
                                                        'tag': '333',
                                                        'interface': 'Eth1/1'}}}}}}},
                            '10.106.0.5/8':
                                {'ubest_num': '1',
                                'mbest_num': '0',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'Null0':
                                                {'protocol':
                                                    {'static':
                                                        {'uptime': '18:47:42',
                                                        'preference': '1',
                                                        'metric': '0'}}}}}}}}}}}}}
    ShowRoutingVrfAll_vrf1 = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'vpnv4 unicast':
                        {'bgp_distance_internal_as': 33,
                        'bgp_distance_local': 55,
                        'ip/mask':
                            {'10.121.0.0/8':
                                {'ubest_num': '1',
                                'mbest_num': '0',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'Null0':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '55',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'discard',
                                                        'tag': '100'}}}}}}},
                            '10.21.33.33/32':
                                {'ubest_num': '1',
                                'mbest_num': '1',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'10.36.3.3':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '33',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'internal',
                                                        'route_table': 'default',
                                                        'tag': '100 (mpls-vpn)'}}}}},
                                    'multicast':
                                        {'nexthop':
                                            {'10.36.3.3':
                                                {'protocol':
                                                    {'bgp':
                                                        {'uptime': '5w0d',
                                                        'preference': '33',
                                                        'metric': '0',
                                                        'protocol_id': '100',
                                                        'attribute': 'internal',
                                                        'route_table': 'default',
                                                        'tag': '100 (mpls-vpn)'}}}}}}},
                            '10.229.11.11/32':
                                {'ubest_num': '2',
                                'mbest_num': '0',
                                'attach': 'attached',
                                'best_route':
                                    {'unicast':
                                        {'nexthop':
                                            {'10.229.11.11':
                                                {'protocol':
                                                    {'local':
                                                        {'uptime': '5w4d',
                                                        'preference': '0',
                                                        'metric': '0',
                                                        'interface': 'Lo1'},
                                                    'direct':
                                                        {'uptime': '5w4d',
                                                        'preference': '0',
                                                        'metric': '0',
                                                        'interface': 'Lo1'}}}}}}}}}}},
            }}

    ShowBgpProcessVrfAll = {
        'bgp_as_path_entries': 0,
        'bgp_memory_state': 'ok',
        'bgp_paths_per_hwm_attr': 1,
        'bgp_pid': 29474,
        'bgp_protocol_state': 'running',
        'bgp_protocol_status': 'started',
        'bgp_protocol_status_reason': 'configuration',
        'bgp_tag': '100',
        'bytes_used': 368,
        'bytes_used_as_path_entries': 0,
        'entries_pending_delete': 0,
        'hwm_attr_entries': 5,
        'hwm_entries_pending_delete': 0,
        'num_attr_entries': 4,
        'vrf': 
            {'VRF1': {
                'address_family': 
                    {'ipv4 unicast': 
                        {'aggregate_label': '492287',
                        'export_rt_list': '100:100',
                        'import_rt_list': '100:100',
                        'label_mode': 'per-prefix',
                        'peers': 
                            {1: 
                                {'active_peers': 0,
                                 'aggregates': 2,
                                 'networks': 1,
                                 'paths': 5,
                                 'routes': 5}},
                        'redistribution': 
                            {'direct': 
                                {'route_map': 'genie_redistribution'},
                             'eigrp': 
                                {'route_map': 'test-map'},
                             'static': 
                                {'route_map': 'genie_redistribution'}},
                        'table_id': 10,
                        'table_state': 'up'},
                    'ipv6 unicast': {
                        'aggregate_label': '492288',
                        'export_rt_list': '100:100',
                        'import_rt_list': '100:100',
                        'label_mode': 'per-prefix',
                        'peers': 
                            {0: 
                                {'active_peers': 0,
                                 'aggregates': 1,
                                 'networks': 1,
                                 'paths': 4,
                                 'routes': 4}},
                        'redistribution': 
                            {'direct': 
                                {'route_map': 'genie_redistribution'},
                             'static': 
                                {'route_map': 'genie_redistribution'}},
                        'table_id': 80000010,
                        'table_state': 'up'}},
                'cluster_id': '0.0.0.0',
                'conf_router_id': '0.0.0.0',
                'confed_id': 0,
                'num_conf_peers': 1,
                'num_established_peers': 0,
                'num_pending_conf_peers': 0,
                'router_id': '10.229.11.11',
                'vrf_id': '3',
                'vrf_rd': '100:100',
                'vrf_state': 'up'},
             'default': 
                {'address_family': 
                    {'ipv4 unicast': 
                        {'peers': 
                            {1: 
                                {'active_peers': 0,
                                'aggregates': 0,
                                'networks': 0,
                                'paths': 0,
                                'routes': 0}},
                         'table_id': 1,
                         'table_state': 'up'},
                    'ipv6 labeled-unicast': 
                        {'peers': 
                            {0: 
                                {'active_peers': 0,
                                 'aggregates': 0,
                                 'networks': 0,
                                 'paths': 0,
                                 'routes': 0}},
                         'table_id': 80000001,
                         'table_state': 'up'},
                    'ipv6 unicast': 
                        {'peers': 
                            {0: 
                                {'active_peers': 0,
                                'aggregates': 0,
                                'networks': 0,
                                'paths': 0,
                                'routes': 0}},
                         'table_id': 80000001,
                         'table_state': 'up'},
                    'vpnv4 unicast': 
                        {'peers': 
                            {1: 
                                {'active_peers': 1,
                                 'aggregates': 0,
                                 'networks': 0,
                                 'paths': 5,
                                 'routes': 5}},
                         'table_id': 1,
                         'table_state': 'up'},
                    'vpnv6 unicast': 
                        {'peers': 
                            {1: 
                                {'active_peers': 1,
                                'aggregates': 0,
                                 'networks': 0,
                                 'paths': 4,
                                 'routes': 4}},
                         'table_id': 80000001,
                         'table_state': 'up'}},
                 'cluster_id': '0.0.0.0',
                 'conf_router_id': '10.4.1.1',
                 'confed_id': 0,
                 'num_conf_peers': 3,
                 'num_established_peers': 1,
                 'num_pending_conf_peers': 0,
                 'router_id': '10.4.1.1',
                 'vrf_id': '1',
                 'vrf_rd': 'not configured',
                 'vrf_state': 'up'}}}
    ShowBgpProcessVrfAll_vrf1 = {
        'bgp_as_path_entries': 0,
        'bgp_memory_state': 'ok',
        'bgp_paths_per_hwm_attr': 1,
        'bgp_pid': 29474,
        'bgp_protocol_state': 'running',
        'bgp_protocol_status': 'started',
        'bgp_protocol_status_reason': 'configuration',
        'bgp_tag': '100',
        'bytes_used': 368,
        'bytes_used_as_path_entries': 0,
        'entries_pending_delete': 0,
        'hwm_attr_entries': 5,
        'hwm_entries_pending_delete': 0,
        'num_attr_entries': 4,
        'vrf':
            {'VRF1': {
                'address_family':
                    {'ipv4 unicast':
                        {'aggregate_label': '492287',
                        'export_rt_list': '100:100',
                        'import_rt_list': '100:100',
                        'label_mode': 'per-prefix',
                        'peers':
                            {1:
                                {'active_peers': 0,
                                 'aggregates': 2,
                                 'networks': 1,
                                 'paths': 5,
                                 'routes': 5}},
                        'redistribution':
                            {'direct':
                                {'route_map': 'genie_redistribution'},
                             'eigrp':
                                {'route_map': 'test-map'},
                             'static':
                                {'route_map': 'genie_redistribution'}},
                        'table_id': 10,
                        'table_state': 'up'},
                    },
                'cluster_id': '0.0.0.0',
                'conf_router_id': '0.0.0.0',
                'confed_id': 0,
                'num_conf_peers': 1,
                'num_established_peers': 0,
                'num_pending_conf_peers': 0,
                'router_id': '10.229.11.11',
                'vrf_id': '3',
                'vrf_rd': '100:100',
                'vrf_state': 'up'},
             }}

    ShowBgpProcessVrfAll_all = '''
        BGP Process Information
        BGP Process ID                 : 29474
        BGP Protocol Started, reason:  : configuration
        BGP Protocol Tag               : 100
        BGP Performance Mode:          : No
        BGP Protocol State             : Running
        BGP Isolate Mode               : No
        BGP MMODE                      : Initialized
        BGP Memory State               : OK
        BGP asformat                   : asplain
        Segment Routing Global Block   : 10000-25000

        BGP attributes information
        Number of attribute entries    : 4
        HWM of attribute entries       : 5
        Bytes used by entries          : 368
        Entries pending delete         : 0
        HWM of entries pending delete  : 0
        BGP paths per attribute HWM    : 1
        BGP AS path entries            : 0
        Bytes used by AS path entries  : 0

        Confcheck capabilities in use:
          1. CAP_FEATURE_BGP_5_2_1 (refcount = 7)

        Information regarding configured VRFs:

        BGP Information for VRF VRF1
        VRF Id                         : 3
        VRF state                      : UP
        Router-ID                      : 10.229.11.11
        Configured Router-ID           : 0.0.0.0
        Confed-ID                      : 0
        Cluster-ID                     : 0.0.0.0
        No. of configured peers        : 1
        No. of pending config peers    : 0
        No. of established peers       : 0
        VRF RD                         : 100:100

            Information for address family IPv4 Unicast in VRF VRF1
            Table Id                   : 10
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            1          0               5          5          1          2

            Redistribution
                direct, route-map genie_redistribution
                static, route-map genie_redistribution
                eigrp, route-map test-map

            Export RT list: 100:100
            Import RT list: 100:100
            Label mode: per-prefix
            Aggregate label: 492287

            Information for address family IPv6 Unicast in VRF VRF1
            Table Id                   : 0x80000010
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            0          0               4          4          1          1

            Redistribution
                direct, route-map genie_redistribution
                static, route-map genie_redistribution

            Export RT list: 100:100
            Import RT list: 100:100
            Label mode: per-prefix
            Aggregate label: 492288

            Nexthop trigger-delay
                critical 3000 ms
                non-critical 10000 ms

        BGP Information for VRF default
        VRF Id                         : 1
        VRF state                      : UP
        Router-ID                      : 10.4.1.1
        Configured Router-ID           : 10.4.1.1
        Confed-ID                      : 0
        Cluster-ID                     : 0.0.0.0
        No. of configured peers        : 3
        No. of pending config peers    : 0
        No. of established peers       : 1
        VRF RD                         : Not configured

            Information for address family IPv4 Unicast in VRF default
            Table Id                   : 1
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            1          0               0          0          0          0

            Redistribution
                None


            Information for address family IPv6 Unicast in VRF default
            Table Id                   : 80000001
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            0          0               0          0          0          0

            Redistribution
                None


            Information for address family VPNv4 Unicast in VRF default
            Table Id                   : 1
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            1          1               5          5          0          0

            Redistribution
                None

            Retain RT: enabled all

            Information for address family VPNv6 Unicast in VRF default
            Table Id                   : 80000001
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            1          1               4          4          0          0

            Redistribution
                None


            Information for address family IPv6 Label Unicast in VRF default
            Table Id                   : 80000001
            Table state                : UP
            Peers      Active-peers    Routes     Paths      Networks   Aggregates
            0          0               0          0          0          0

            Redistribution
                None
        '''
    ShowBgpPeerSession = {
        'peer_session': 
            {'PEER-SESSION': 
                {'bfd': True,
                 'description': 'PEER-SESSION',
                 'disable_connectivity_check': True,
                 'ebgp_multihop_enable': True,
                 'ebgp_multihop_limit': 255,
                 'holdtime': 111,
                 'inherited_vrf_default': '10.16.2.5',
                 'keepalive': 222,
                 'local_as': True,
                 'transport_connection_mode': 'Passive',
                 'password': True,
                 'remote_as': True,
                 'shutdown': True,
                 'suppress_capabilities': True,
                 'update_source': 'interface: '
                                 'loopback0'}}}

    ShowBgpPeerPolicy = {
        'peer_policy': {
            'PEER-POLICY': {
                'allowas_in': True,
                'as_override': True,
                'default_originate': True,
                'default_originate_route_map': 'test',
                'inherited_vrf_default': '10.16.2.5',
                'maximum_prefix_max_prefix_no': 300,
                'route_map_name_in': 'test-map',
                'route_map_name_out': 'test-map',
                'route_reflector_client': True,
                'send_community': True,
                'send_ext_community': True,
                'site_of_origin': True,
                'soft_reconfiguration': True}}}

    ShowBgpPeerTemplate = {
        'peer_template':
            {'PEER':
                {'bfd_live_detection': True,
                'disable_connected_check': True,
                'description': 'DESC',
                'holdtime': 26,
                'inherit_template': 'PEER-SESSION',
                'keepalive_interval': 13,
                'nbr_transport_connection_mode': 'Passive',
                'num_hops_bgp_peer': 255,
                'private_as_updates': False,
                'remote_as': 500,
                'tcp_md5_auth': 'enabled',
                'update_source': 'loopback1'}}}

    ShowBgpVrfAllAll = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4 unicast':
                        {'aggregate_address_as_set': True,
                        'aggregate_address_ipv4_address': '10.121.0.0',
                        'aggregate_address_ipv4_mask': '8',
                        'aggregate_address_summary_only': True,
                        'bgp_table_version': 35,
                        'local_router_id': '10.229.11.11',
                        'prefixes':
                            {'10.121.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768},
                                    2:
                                        {'next_hop': '10.64.4.4',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': 'e',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768},
                                    3:
                                        {'next_hop': '10.144.6.6',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': 'e',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                                    '10.229.11.11/32':
                                        {'index':
                                            {1:
                                            {'next_hop': '0.0.0.0',
                                            'localprf': 100,
                                            'metric': 0,
                                            'origin_codes': '?',
                                            'path_type': 'r',
                                            'status_codes': '*>',
                                            'weight': 32768}}},
                            '10.84.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': 'None',
                                        'weight': 32768}}},
                            '10.21.33.33/32':
                                {'index':
                                    {1:
                                        {'next_hop': '10.36.3.3',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'i',
                                        'status_codes': '*>',
                                        'weight': 0}}},
                            '10.34.34.0/24':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'l',
                                        'status_codes': 'None',
                                        'weight': 32768}}}}},
                    'ipv6 unicast':
                        {'bgp_table_version': 28,
                        'local_router_id': '10.229.11.11',
                        'prefixes':
                            {'2001:db8:400::/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '2001:111:222::/64':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'l',
                                        'status_codes': 'None',
                                        'weight': 32768}}},
                            '2001::11/128':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'r',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '2001::33/128':
                                {'index':
                                    {1:
                                        {'next_hop': '::ffff:10.36.3.3',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'i',
                                        'status_codes': '*>',
                                        'weight': 0}}}},
                        'v6_aggregate_address_as_set': True,
                        'v6_aggregate_address_ipv6_address': '2001:db8:400::/8',
                        'v6_aggregate_address_summary_only': True}}},
            'default':
                {'address_family':
                    {'vpnv4 unicast':
                        {'bgp_table_version': 48,
                        'local_router_id': '10.4.1.1'},
                    'vpnv4 unicast RD 100:100':
                        {'aggregate_address_as_set': True,
                        'aggregate_address_ipv4_address': '10.121.0.0',
                        'aggregate_address_ipv4_mask': '8',
                        'aggregate_address_summary_only': True,
                        'bgp_table_version': 48,
                        'default_vrf': 'VRF1',
                        'local_router_id': '10.4.1.1',
                        'prefixes':
                            {'10.121.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '10.229.11.11/32':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'r',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '10.84.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': 'None',
                                        'weight': 32768}}},
                            '10.21.33.33/32':
                                {'index':
                                    {1:
                                        {'next_hop': '10.36.3.3',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'i',
                                        'status_codes': '*>',
                                        'weight': 0}}},
                            '10.34.34.0/24':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'l',
                                        'status_codes': 'None',
                                        'weight': 32768}}}},
                        'route_distinguisher': '100:100'},
                    'vpnv6 unicast':
                        {'bgp_table_version': 41,
                        'local_router_id': '10.4.1.1'},
                    'vpnv6 unicast RD 100:100':
                        {'bgp_table_version': 41,
                        'default_vrf': 'VRF1',
                        'local_router_id': '10.4.1.1',
                        'prefixes':
                            {'2001:db8:400::/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '2001:111:222::/64':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'l',
                                        'status_codes': 'None',
                                        'weight': 32768}}},
                            '2001::11/128':
                                {'index':
                                    {1:
                                        {'next_hop': '0::',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'r',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                            '2001::33/128':
                                {'index':
                                    {1:
                                        {'next_hop': '::ffff:10.36.3.3',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'i',
                                        'status_codes': '*>',
                                        'weight': 0}}}},
                        'route_distinguisher': '100:100',
                        'v6_aggregate_address_as_set': True,
                        'v6_aggregate_address_ipv6_address': '2001:db8:400::/8',
                        'v6_aggregate_address_summary_only': True}}}}}
    ShowBgpVrfAllAll_vrf1 = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4 unicast':
                        {'aggregate_address_as_set': True,
                        'aggregate_address_ipv4_address': '10.121.0.0',
                        'aggregate_address_ipv4_mask': '8',
                        'aggregate_address_summary_only': True,
                        'bgp_table_version': 35,
                        'local_router_id': '10.229.11.11',
                        'prefixes':
                            {'10.121.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768},
                                    2:
                                        {'next_hop': '10.64.4.4',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': 'e',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768},
                                    3:
                                        {'next_hop': '10.144.6.6',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': 'e',
                                        'path_type': 'a',
                                        'status_codes': '*>',
                                        'weight': 32768}}},
                                    '10.229.11.11/32':
                                        {'index':
                                            {1:
                                            {'next_hop': '0.0.0.0',
                                            'localprf': 100,
                                            'metric': 0,
                                            'origin_codes': '?',
                                            'path_type': 'r',
                                            'status_codes': '*>',
                                            'weight': 32768}}},
                            '10.84.0.0/8':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'a',
                                        'status_codes': 'None',
                                        'weight': 32768}}},
                            '10.21.33.33/32':
                                {'index':
                                    {1:
                                        {'next_hop': '10.36.3.3',
                                        'localprf': 100,
                                        'metric': 0,
                                        'origin_codes': '?',
                                        'path_type': 'i',
                                        'status_codes': '*>',
                                        'weight': 0}}},
                            '10.34.34.0/24':
                                {'index':
                                    {1:
                                        {'next_hop': '0.0.0.0',
                                        'localprf': 100,
                                        'origin_codes': 'i',
                                        'path_type': 'l',
                                        'status_codes': 'None',
                                        'weight': 32768}}}}},
                  }},
           }}

    ShowBgpVrfAllAllNextHopDatabase = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'igp_cost': 0,
                        'igp_preference': 0,
                        'igp_route_type': 0,
                        'metric_next_advertise': 'never',
                        'next_hop': '0.0.0.0',
                        'nexthop_last_resolved': 'never',
                        'nexthop_resolved_using': '0.0.0.0/0',
                        'nexthop_trigger_delay_critical': 2222,
                        'nexthop_trigger_delay_non_critical': 3333,
                        'nexthop_type': 'not-attached '
                                        'local '
                                        'unreachable '
                                        'not-labeled',
                        'refcount': 4,
                        'rnh_epoch': 0},
                    'ipv6 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'igp_cost': 0,
                        'igp_preference': 0,
                        'igp_route_type': 0,
                        'metric_next_advertise': 'never',
                        'next_hop': '0::',
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000,
                        'nexthop_type': 'not-attached '
                                        'local '
                                        'unreachable '
                                        'not-labeled',
                        'refcount': 3,
                        'rnh_epoch': 0}}},
            'default':
                {'address_family':
                    {'ipv4 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000},
                    'ipv6 labeled-unicast':
                        {'af_nexthop_trigger_enable': True,
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000},
                    'ipv6 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000},
                    'vpnv4 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'attached_nexthop': '10.1.3.3',
                        'attached_nexthop_interface': 'Ethernet4/2',
                        'igp_cost': 41,
                        'igp_preference': 110,
                        'igp_route_type': 0,
                        'metric_next_advertise': 'never',
                        'next_hop': '10.36.3.3',
                        'nexthop_last_resolved': '5w0d',
                        'nexthop_resolved_using': '10.36.3.3/32',
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000,
                        'nexthop_type': 'not-attached '
                                        'not-local '
                                        'reachable '
                                        'labeled',
                        'refcount': 1,
                        'rnh_epoch': 1},
                    'vpnv6 unicast':
                        {'af_nexthop_trigger_enable': True,
                        'attached_nexthop': '10.1.3.3',
                        'attached_nexthop_interface': 'Ethernet4/2',
                        'igp_cost': 41,
                        'igp_preference': 110,
                        'igp_route_type': 0,
                        'metric_next_advertise': 'never',
                        'next_hop': '::ffff:10.36.3.3',
                        'nexthop_last_resolved': '5w0d',
                        'nexthop_resolved_using': '10.36.3.3/32',
                        'nexthop_trigger_delay_critical': 3000,
                        'nexthop_trigger_delay_non_critical': 10000,
                        'nexthop_type': 'not-attached '
                                        'not-local '
                                        'reachable '
                                        'labeled',
                        'refcount': 1,
                        'rnh_epoch': 1}}}}}

    ShowBgpVrfAllAllSummary = {
        'vrf':
            {'VRF1':
                {'neighbor':
                    {'10.16.2.10':
                        {'address_family':
                            {'ipv4 unicast':
                                {'as': 0,
                                'as_path_entries': '[0/0]',
                                'attribute_entries': '[3/384]',
                                'bgp_table_version': 40,
                                'capable_peers': 0,
                                'clusterlist_entries': '[1/4]',
                                'community_entries': '[0/0]',
                                'config_peers': 1,
                                'dampened_paths': 0,
                                'dampening': True,
                                'history_paths': 0,
                                'inq': 0,
                                'local_as': 100,
                                'msg_rcvd': 0,
                                'msg_sent': 0,
                                'outq': 0,
                                'path': {'memory_usage': 620,
                                        'total_entries': 5},
                                'prefixes':
                                    {'memory_usage': 620,
                                    'total_entries': 5},
                                'route_identifier': '10.64.4.4',
                                'state_pfxrcd': 'Idle',
                                'tbl_ver': 0,
                                'up_down': '5w6d',
                                'v': 4}}}}},
            'default':
                {'neighbor':
                    {'10.16.2.2':
                        {'address_family':
                            {'vpnv4 unicast':
                                {'as': 100,
                                'as_path_entries': '[0/0]',
                                'attribute_entries': '[1/128]',
                                'bgp_table_version': 53,
                                'capable_peers': 1,
                                'clusterlist_entries': '[1/4]',
                                'community_entries': '[0/0]',
                                'config_peers': 1,
                                'dampened_paths': 0,
                                'dampening': True,
                                'history_paths': 0,
                                'inq': 0,
                                'local_as': 100,
                                'msg_rcvd': 108554,
                                'msg_sent': 108566,
                                'outq': 0,
                                'path': {'memory_usage': 620,
                                        'total_entries': 5},
                                'prefixes':
                                    {'memory_usage': 620,
                                    'total_entries': 5},
                                'route_identifier': '10.4.1.1',
                                'state_pfxrcd': '1',
                                'tbl_ver': 53,
                                'up_down': '5w6d',
                                'v': 4},
                            'vpnv6 unicast':
                                {'as': 100,
                                'as_path_entries': '[0/0]',
                                'attribute_entries': '[1/128]',
                                'bgp_table_version': 45,
                                'capable_peers': 1,
                                'clusterlist_entries': '[1/4]',
                                'community_entries': '[0/0]',
                                'config_peers': 1,
                                'dampened_paths': 0,
                                'dampening': True,
                                'history_paths': 0,
                                'inq': 0,
                                'local_as': 100,
                                'msg_rcvd': 108554,
                                'msg_sent': 108566,
                                'outq': 0,
                                'path': {'memory_usage': 544,
                                        'total_entries': 4},
                                'prefixes':
                                    {'memory_usage': 544,
                                    'total_entries': 4},
                                'route_identifier': '10.4.1.1',
                                'state_pfxrcd': '1',
                                'tbl_ver': 45,
                                'up_down': '5w6d',
                                'v': 4}}}}}}}

    ShowBgpVrfAllAllDampeningParameters = {
        'vrf':
            {'VRF1':
                {'address_family':
                    {'ipv4 unicast':
                        {'dampening': 'True',
                        'dampening_route_map': 'dampening1',
                        'dampening_half_life_time': '45',
                        'dampening_reuse_time': '10000',
                        'dampening_suppress_time': '20000',
                        'dampening_max_suppress_time': '255',
                        'dampening_max_suppress_penalty': '507968'},
                    'ipv6 unicast':
                       {'dampening': 'True',
                        'dampening_route_map': 'dampening2',
                        'dampening_half_life_time': '45',
                        'dampening_reuse_time': '9999',
                        'dampening_suppress_time': '19999',
                        'dampening_max_suppress_time': '255',
                        'dampening_max_suppress_penalty': '507917'}}},
        'default':
            {'address_family':
                {'ipv4 unicast':
                    {'dampening': 'True',
                    'dampening_half_life_time': '45',
                    'dampening_reuse_time': '1111',
                    'dampening_suppress_time': '2222',
                    'dampening_max_suppress_time': '255',
                    'dampening_max_suppress_penalty': '56435'},
                'vpnv4 unicast':
                    {'dampening': 'True',
                    'route_distinguisher':
                        {'1:100':
                            {'rd_vrf': 'vpn1',
                            'dampening_half_life_time': '1 mins',
                            'dampening_reuse_time': '10',
                            'dampening_suppress_time': '30',
                            'dampening_max_suppress_time': '2 mins',
                            'dampening_max_suppress_penalty': '40'}}}}}}}

    ShowBgpVrfAllAllNextHopDatabase_vrf1 = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'ipv4 unicast':
                           {'af_nexthop_trigger_enable': True,
                            'igp_cost': 0,
                            'igp_preference': 0,
                            'igp_route_type': 0,
                            'metric_next_advertise': 'never',
                            'next_hop': '0.0.0.0',
                            'nexthop_last_resolved': 'never',
                            'nexthop_resolved_using': '0.0.0.0/0',
                            'nexthop_trigger_delay_critical': 2222,
                            'nexthop_trigger_delay_non_critical': 3333,
                            'nexthop_type': 'not-attached '
                                            'local '
                                            'unreachable '
                                            'not-labeled',
                            'refcount': 4,
                            'rnh_epoch': 0},
                       }},
             }}

    ShowBgpVrfAllAllSummary_vrf1 = {
        'vrf':
            {'VRF1':
                 {'neighbor':
                      {'10.16.2.10':
                           {'address_family':
                                {'ipv4 unicast':
                                     {'as': 0,
                                      'as_path_entries': '[0/0]',
                                      'attribute_entries': '[3/384]',
                                      'bgp_table_version': 40,
                                      'capable_peers': 0,
                                      'clusterlist_entries': '[1/4]',
                                      'community_entries': '[0/0]',
                                      'config_peers': 1,
                                      'dampened_paths': 0,
                                      'dampening': True,
                                      'history_paths': 0,
                                      'inq': 0,
                                      'local_as': 100,
                                      'msg_rcvd': 0,
                                      'msg_sent': 0,
                                      'outq': 0,
                                      'path': {'memory_usage': 620,
                                               'total_entries': 5},
                                      'prefixes':
                                          {'memory_usage': 620,
                                           'total_entries': 5},
                                      'route_identifier': '10.64.4.4',
                                      'state_pfxrcd': 'Idle',
                                      'tbl_ver': 0,
                                      'up_down': '5w6d',
                                      'v': 4}}}}},
            }}

    ShowBgpVrfAllAllDampeningParameters_vrf1 = {
        'vrf':
            {'VRF1':
                 {'address_family':
                      {'ipv4 unicast':
                           {'dampening': 'True',
                            'dampening_route_map': 'dampening1',
                            'dampening_half_life_time': '45',
                            'dampening_reuse_time': '10000',
                            'dampening_suppress_time': '20000',
                            'dampening_max_suppress_time': '255',
                            'dampening_max_suppress_penalty': '507968'},
                       }},
             }}
    # Set output for 'show bgp vrf VRF1 all neighbors' as input to parser
    vrf_vrf1_output = '''\
        N7k# show bgp vrf VRF1 all neighbors 
        BGP neighbor is 10.16.2.10,  remote AS 0, unknown link,  Peer index 1
          BGP version 4, remote router ID 0.0.0.0
          BGP state = Idle, down for 02:19:37, retry in 0.000000
          Last read never, hold time = 180, keepalive interval is 60 seconds
          Last written never, keepalive timer not running
          Received 0 messages, 0 notifications, 0 bytes in queue
          Sent 0 messages, 0 notifications, 0 bytes in queue
          Connections established 0, dropped 0
          Connection attempts 0
          Last reset by us never, due to No error
          Last reset by peer never, due to No error

          Message statistics:
                                      Sent               Rcvd
          Opens:                         0                  0  
          Notifications:                 0                  0  
          Updates:                       0                  0  
          Keepalives:                    0                  0  
          Route Refresh:                 0                  0  
          Capability:                    0                  0  
          Total:                         0                  0  
          Total bytes:                   0                  0  
          Bytes in queue:                0                  0  

          For address family: IPv4 Unicast
          BGP table version 21, neighbor version 0
          0 accepted paths consume 0 bytes of memory
          0 sent paths
          Third-party Nexthop will not be computed.
          Default information originate, route-map SOMENAME, default not sent
          SOO Extcommunity: SOO:100:100

          No established BGP session with peer
        '''

    # Set output for 'show bgp vrf default all neighbors'
    vrf_default_output = '''\
        N7k# show bgp vrf default all neighbors 
        BGP neighbor is 10.16.2.2,  remote AS 100, ibgp link,  Peer index 1
          Description: nei_desc
          BGP version 4, remote router ID 10.16.2.2
          BGP state = Established, up for 02:20:02
          Using loopback0 as update source for this peer
          BFD live-detection is configured
          Neighbor local-as command not active
          Last read 00:00:15, hold time = 99, keepalive interval is 33 seconds
          Last written 00:00:13, keepalive timer expiry due 00:00:19
          Received 261 messages, 0 notifications, 0 bytes in queue
          Sent 263 messages, 0 notifications, 0 bytes in queue
          Connections established 1, dropped 0
          Last reset by us never, due to No error
          Last reset by peer never, due to No error

          Neighbor capabilities:
          Dynamic capability: advertised (mp, refresh, gr) received (mp, refresh, gr)
          Dynamic capability (old): advertised received
          Route refresh capability (new): advertised received 
          Route refresh capability (old): advertised received 
          4-Byte AS capability: disabled 
          Address family VPNv4 Unicast: advertised received 
          Address family VPNv6 Unicast: advertised received 
          Graceful Restart capability: advertised received

          Graceful Restart Parameters:
          Address families advertised to peer:
            VPNv4 Unicast  VPNv6 Unicast  
          Address families received from peer:
            VPNv4 Unicast  VPNv6 Unicast  
          Forwarding state preserved by peer for:
          Restart time advertised to peer: 240 seconds
          Stale time for routes advertised by peer: 600 seconds
          Restart time advertised by peer: 120 seconds

          Message statistics:
                                      Sent               Rcvd
          Opens:                         1                  1  
          Notifications:                 0                  0  
          Updates:                       6                  4  
          Keepalives:                  256                256  
          Route Refresh:                 0                  0  
          Capability:                    0                  0  
          Total:                       263                261  
          Total bytes:                5311               5139  
          Bytes in queue:                0                  0  

          For address family: VPNv4 Unicast
          BGP table version 11, neighbor version 11
          1 accepted paths consume 48 bytes of memory
          2 sent paths
          Community attribute sent to this neighbor
          Extended community attribute sent to this neighbor
          Third-party Nexthop will not be computed.
          Maximum prefixes allowed 300000
          Inbound route-map configured is genie_redistribution, handle obtained
          Outbound route-map configured is genie_redistribution, handle obtained

          For address family: VPNv6 Unicast
          BGP table version 10, neighbor version 10
          1 accepted paths consume 48 bytes of memory
          2 sent paths
          Community attribute sent to this neighbor
          Extended community attribute sent to this neighbor
          Third-party Nexthop will not be computed.

          Local host: 10.4.1.1, Local port: 57144
          Foreign host: 10.16.2.2, Foreign port: 179
          fd = 44
        '''

    nbr1_advertised_routes = '''\
        pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 advertised-routes 
        Can't find neighbor 10.16.2.10

        Peer 10.16.2.10 routes for address family IPv4 Unicast:
        BGP table version is 25, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>l10.4.1.0/24         0.0.0.0                           100      32768 i
        *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.106.0.0/8        0.0.0.0               4444        100      32768 ?
        *>r192.168.51.0/8        0.0.0.0               4444        100      32768 ?


        Peer 10.16.2.10 routes for address family IPv4 Multicast:
        BGP table version is 19, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>r10.4.1.0/24         0.0.0.0               3333        100      32768 ?
        *>r10.9.1.0/24         0.0.0.0               3333        100      32768 ?
        *>r10.4.0.0/8          0.0.0.0               3333        100      32768 ?
        *>r10.204.0.0/8        0.0.0.0               3333        100      32768 ?
        *>r192.168.4.0/8        0.0.0.0               3333        100      32768 ?


        Peer 10.16.2.10 routes for address family IPv6 Unicast:
        BGP table version is 7, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        Peer 10.16.2.10 routes for address family IPv6 Multicast:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.10 routes for address family VPNv4 Unicast:
        BGP table version is 23, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 1:100    (VRF vpn1)

        Route Distinguisher: 2:100    (VRF vpn2)


        Peer 10.16.2.10 routes for address family VPNv6 Unicast:
        BGP table version is 7, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 1:100    (VRF vpn1)

        Route Distinguisher: 2:100    (VRF vpn2)


        Peer 10.16.2.10 routes for address family IPv4 MVPN:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.10 routes for address family IPv6 MVPN:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.10 routes for address family IPv4 Label Unicast:
        BGP table version is 28, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        Peer 10.16.2.10 routes for address family Link-State:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Can't find neighbor 10.16.2.10
        Can't find neighbor 10.16.2.10
        '''
    nbr1_advertised_routes_ipv4 = '''
    pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 advertised-routes 
        Can't find neighbor 10.16.2.10

        Peer 10.16.2.10 routes for address family IPv4 Unicast:
        BGP table version is 25, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>l10.4.1.0/24         0.0.0.0                           100      32768 i
        *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.106.0.0/8        0.0.0.0               4444        100      32768 ?
        *>r192.168.51.0/8        0.0.0.0               4444        100      32768 ?
        '''
    nbr1_routes = '''\
        pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 routes 
            Can't find neighbor 10.16.2.10

            Peer 10.16.2.10 routes for address family IPv4 Unicast:
            BGP table version is 25, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            * i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            * i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.10 routes for address family IPv4 Multicast:
            BGP table version is 19, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            *>i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            *>i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.10 routes for address family IPv6 Unicast:
            BGP table version is 7, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path


            Peer 10.16.2.10 routes for address family IPv6 Multicast:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.10 routes for address family VPNv4 Unicast:
            BGP table version is 23, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Route Distinguisher: 1:100    (VRF vpn1)
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?

            Route Distinguisher: 2:100    (VRF vpn2)


            Peer 10.16.2.10 routes for address family VPNv6 Unicast:
            BGP table version is 7, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Route Distinguisher: 1:100    (VRF vpn1)

            Route Distinguisher: 2:100    (VRF vpn2)


            Peer 10.16.2.10 routes for address family IPv4 MVPN:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.10 routes for address family IPv6 MVPN:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.10 routes for address family IPv4 Label Unicast:
            BGP table version is 28, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            * i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            * i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.10 routes for address family Link-State:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Can't find neighbor 10.16.2.10
            Can't find neighbor 10.16.2.10
            '''
    nbr1_routes_ipv4 = '''
    pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 routes 
        Can't find neighbor 10.16.2.10

        Peer 10.16.2.10 routes for address family IPv4 Unicast:
        BGP table version is 25, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
        * i10.106.0.0/8        10.186.0.2                 0        100          0 ?
        * i192.168.51.0/8        10.186.0.2                 0        100          0 ?
        '''
    nbr1_received_routes = '''\
        pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 received-routes 
        Can't find neighbor 10.16.2.10

        Inbound soft reconfiguration for IPv4 Unicast not performed on 10.16.2.10

        Peer 10.16.2.10 routes for address family IPv4 Multicast:
        BGP table version is 19, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
        *>i10.106.0.0/8        10.186.0.2                 0        100          0 ?
        *>i192.168.51.0/8        10.186.0.2                 0        100          0 ?


        Inbound soft reconfiguration for IPv6 Unicast not performed on 10.16.2.10

        Inbound soft reconfiguration for IPv6 Multicast not performed on 10.16.2.10

        Inbound soft reconfiguration for VPNv4 Unicast not performed on 10.16.2.10

        Inbound soft reconfiguration for VPNv6 Unicast not performed on 10.16.2.10

        Inbound soft reconfiguration for IPv4 MVPN not performed on 10.16.2.10

        Inbound soft reconfiguration for IPv6 MVPN not performed on 10.16.2.10

        Inbound soft reconfiguration for IPv4 Label Unicast not performed on 10.16.2.10

        Inbound soft reconfiguration for Link-State not performed on 10.16.2.10
        Can't find neighbor 10.16.2.10
        Can't find neighbor 10.16.2.10
        '''
    nbr1_received_routes_ipv4 = '''\
            pinxdt-n9kv-2# show bgp vrf VRF1 all neighbors 10.16.2.10 received-routes 
            Can't find neighbor 10.16.2.10

            Inbound soft reconfiguration for IPv4 Unicast not performed on 10.16.2.10
            '''
    nbr2_advertised_routes = '''\
        pinxdt-n9kv-2# show bgp vrf default all neighbors 10.16.2.2 advertised-routes 
        Can't find neighbor 10.16.2.2

        Peer 10.16.2.2 routes for address family IPv4 Unicast:
        BGP table version is 25, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>l10.4.1.0/24         0.0.0.0                           100      32768 i
        *>r10.16.1.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.16.2.0/24         0.0.0.0               4444        100      32768 ?
        *>r10.106.0.0/8        0.0.0.0               4444        100      32768 ?
        *>r192.168.51.0/8        0.0.0.0               4444        100      32768 ?


        Peer 10.16.2.2 routes for address family IPv4 Multicast:
        BGP table version is 19, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>r10.4.1.0/24         0.0.0.0               3333        100      32768 ?
        *>r10.9.1.0/24         0.0.0.0               3333        100      32768 ?
        *>r10.4.0.0/8          0.0.0.0               3333        100      32768 ?
        *>r10.204.0.0/8        0.0.0.0               3333        100      32768 ?
        *>r192.168.4.0/8        0.0.0.0               3333        100      32768 ?


        Peer 10.16.2.2 routes for address family IPv6 Unicast:
        BGP table version is 7, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        Peer 10.16.2.2 routes for address family IPv6 Multicast:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.2 routes for address family VPNv4 Unicast:
        BGP table version is 23, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 1:100    (VRF vpn1)

        Route Distinguisher: 2:100    (VRF vpn2)


        Peer 10.16.2.2 routes for address family VPNv6 Unicast:
        BGP table version is 7, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Route Distinguisher: 1:100    (VRF vpn1)

        Route Distinguisher: 2:100    (VRF vpn2)


        Peer 10.16.2.2 routes for address family IPv4 MVPN:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.2 routes for address family IPv6 MVPN:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path

        Peer 10.16.2.2 routes for address family IPv4 Label Unicast:
        BGP table version is 28, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path


        Peer 10.16.2.2 routes for address family Link-State:
        BGP table version is 2, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        Can't find neighbor 10.16.2.2
        Can't find neighbor 10.16.2.2
        '''

    nbr2_routes = '''\
        pinxdt-n9kv-2# show bgp vrf default all neighbors 10.16.2.2 routes 
            Can't find neighbor 10.16.2.2

            Peer 10.16.2.2 routes for address family IPv4 Unicast:
            BGP table version is 25, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            * i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            * i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.2 routes for address family IPv4 Multicast:
            BGP table version is 19, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            *>i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            *>i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.2 routes for address family IPv6 Unicast:
            BGP table version is 7, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path


            Peer 10.16.2.2 routes for address family IPv6 Multicast:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.2 routes for address family VPNv4 Unicast:
            BGP table version is 23, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Route Distinguisher: 1:100    (VRF vpn1)
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?

            Route Distinguisher: 2:100    (VRF vpn2)


            Peer 10.16.2.2 routes for address family VPNv6 Unicast:
            BGP table version is 7, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Route Distinguisher: 1:100    (VRF vpn1)

            Route Distinguisher: 2:100    (VRF vpn2)


            Peer 10.16.2.2 routes for address family IPv4 MVPN:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.2 routes for address family IPv6 MVPN:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path

            Peer 10.16.2.2 routes for address family IPv4 Label Unicast:
            BGP table version is 28, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
            * i10.106.0.0/8        10.186.0.2                 0        100          0 ?
            * i192.168.51.0/8        10.186.0.2                 0        100          0 ?


            Peer 10.16.2.2 routes for address family Link-State:
            BGP table version is 2, Local Router ID is 10.186.101.1
            Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
            Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
            Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

               Network            Next Hop            Metric     LocPrf     Weight Path
            Can't find neighbor 10.16.2.10
            Can't find neighbor 10.16.2.10
            '''

    nbr2_received_routes = '''\
        pinxdt-n9kv-2# show bgp vrf default all neighbors 10.16.2.2 received-routes 
        Can't find neighbor 10.16.2.2

        Inbound soft reconfiguration for IPv4 Unicast not performed on 10.16.2.2

        Peer 10.16.2.25 routes for address family IPv4 Multicast:
        BGP table version is 19, Local Router ID is 10.186.101.1
        Status: s-suppressed, x-deleted, S-stale, d-dampened, h-history, *-valid, >-best
        Path type: i-internal, e-external, c-confed, l-local, a-aggregate, r-redist, I-injected
        Origin codes: i - IGP, e - EGP, ? - incomplete, | - multipath, & - backup

           Network            Next Hop            Metric     LocPrf     Weight Path
        *>i10.16.0.0/8          10.186.0.2                 0        100          0 ?
        *>i10.106.0.0/8        10.186.0.2                 0        100          0 ?
        *>i192.168.51.0/8        10.186.0.2                 0        100          0 ?


        Inbound soft reconfiguration for IPv6 Unicast not performed on 10.16.2.2

        Inbound soft reconfiguration for IPv6 Multicast not performed on 10.16.2.2

        Inbound soft reconfiguration for VPNv4 Unicast not performed on 10.16.2.2

        Inbound soft reconfiguration for VPNv6 Unicast not performed on 10.16.2.2

        Inbound soft reconfiguration for IPv4 MVPN not performed on 10.16.2.2

        Inbound soft reconfiguration for IPv6 MVPN not performed on 10.16.2.2

        Inbound soft reconfiguration for IPv4 Label Unicast not performed on 10.16.2.2

        Inbound soft reconfiguration for Link-State not performed on 10.16.2.2
        Can't find neighbor 10.16.2.2
        Can't find neighbor 10.16.2.2
        '''

    BgpOpsOutput_info = {
        'instance':
            {'default':
                {'bgp_id': 100,
                'peer_policy':
                    {'PEER-POLICY':
                        {'allowas_in': True,
                        'as_override': True,
                        'default_originate': True,
                        'default_originate_route_map': 'test',
                        'maximum_prefix_max_prefix_no': 300,
                        'route_map_name_in': 'test-map',
                        'route_map_name_out': 'test-map',
                        'route_reflector_client': True,
                        'send_community': True,
                        'soft_reconfiguration': True,
                        'soo': True}},
                'peer_session':
                    {'PEER-SESSION':
                        {'description': 'PEER-SESSION',
                        'disable_connected_check': True,
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'holdtime': 111,
                        'keepalive_interval': 222,
                        'local_as_as_no': True,
                        'password_text': True,
                        'remote_as': True,
                        'shutdown': True,
                        'suppress_four_byte_as_capability': True,
                        'transport_connection_mode': 'Passive',
                        'update_source': 'interface: '
                                         'loopback0'}},
                'protocol_state': 'running',
                'vrf':
                    {'VRF1':
                        {'address_family':
                            {'ipv4 unicast':
                                {'aggregate_address_as_set': True,
                                'aggregate_address_ipv4_address': '10.121.0.0',
                                'aggregate_address_ipv4_mask': '8',
                                'aggregate_address_summary_only': True,
                                'dampening': 'True',
                                'dampening_half_life_time': '45',
                                'dampening_max_suppress_time': '255',
                                'dampening_reuse_time': '10000',
                                'dampening_route_map': 'dampening1',
                                'dampening_suppress_time': '20000',
                                'label_allocation_mode': 'per-prefix',
                                'nexthop_trigger_delay_critical': 2222,
                                'nexthop_trigger_delay_non_critical': 3333,
                                'nexthop_trigger_enable': True},
                            'vpnv4 unicast': 
                                {'distance_internal_as': 33,
                                'distance_local': 55},
                            'ipv6 unicast':
                                {'dampening': 'True',
                                'dampening_half_life_time': '45',
                                'dampening_max_suppress_time': '255',
                                'dampening_reuse_time': '9999',
                                'dampening_route_map': 'dampening2',
                                'dampening_suppress_time': '19999',
                                'label_allocation_mode': 'per-prefix',
                                'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True,
                                'v6_aggregate_address_as_set': True,
                                'v6_aggregate_address_ipv6_address': '2001:db8:400::/8',
                                'v6_aggregate_address_summary_only': True}},
                        'cluster_id': '0.0.0.0',
                        'confederation_identifier': 0,
                        'neighbor':
                            {'10.16.2.10':
                                {'address_family':
                                    {'ipv4 unicast':
                                        {'bgp_table_version': 21,
                                        'default_originate': True,
                                         'session_state':'idle',
                                        'default_originate_route_map': 'SOMENAME',
                                        'soo': 'SOO:100:100'}},
                                'bgp_negotiated_keepalive_timers':
                                    {'hold_time': 180,
                                    'keepalive_interval': 60},
                                'bgp_neighbor_counters':
                                    {'messages':
                                        {'received':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 0,
                                            'notifications': 0,
                                            'opens': 0,
                                            'route_refresh': 0,
                                            'total': 0,
                                            'total_bytes': 0,
                                            'updates': 0},
                                        'sent':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 0,
                                            'notifications': 0,
                                            'opens': 0,
                                            'route_refresh': 0,
                                            'total': 0,
                                            'total_bytes': 0,
                                            'updates': 0}}},
                                'bgp_session_transport':
                                    {'connection':
                                        {'last_reset': 'never',
                                         'reset_reason': 'no '
                                                         'error',
                                         'state': 'idle'}},
                                'bgp_version': 4,
                                'holdtime': 180,
                                'keepalive_interval': 60,
                                'local_as_as_no': 'None',
                                'remote_as': 0,
                                'session_state': 'idle',
                                'shutdown': False,
                                'up_time': '02:19:37'}},
                        'router_id': '10.229.11.11'},
                    'default':
                        {'address_family':
                            {'ipv4 unicast':
                                {'dampening': 'True',
                                'dampening_half_life_time': '45',
                                'dampening_max_suppress_time': '255',
                                'dampening_reuse_time': '1111',
                                'dampening_suppress_time': '2222',
                                'distance_extern_as': 20,
                                'distance_internal_as': 200,
                                'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True},
                            'ipv6 labeled-unicast':
                                {'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True},
                            'ipv6 unicast':
                                {'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True},
                            'vpnv4 unicast':
                                {'aggregate_address_as_set': True,
                                'aggregate_address_ipv4_address': '10.121.0.0',
                                'aggregate_address_ipv4_mask': '8',
                                'aggregate_address_summary_only': True,
                                'dampening': 'True',
                                'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True},
                            'vpnv6 unicast':
                                {'nexthop_trigger_delay_critical': 3000,
                                'nexthop_trigger_delay_non_critical': 10000,
                                'nexthop_trigger_enable': True,
                                'v6_aggregate_address_as_set': True,
                                'v6_aggregate_address_ipv6_address': '2001:db8:400::/8',
                                'v6_aggregate_address_summary_only': True}},
                        'cluster_id': '0.0.0.0',
                        'confederation_identifier': 0,
                        'neighbor':
                            {'10.16.2.2':
                                {'address_family':
                                    {'vpnv4 unicast':
                                        {'bgp_table_version': 11,
                                        'session_state': 'established',
                                        'maximum_prefix_max_prefix_no': 300000,
                                        'route_map_name_in': 'genie_redistribution',
                                        'route_map_name_out': 'genie_redistribution',
                                        'send_community': "both"},
                                    'vpnv6 unicast':
                                        {'bgp_table_version': 10,
                                        'session_state': 'established',
                                        'send_community': "both"}},
                                'bgp_negotiated_capabilities':
                                    {'dynamic_capability': 'advertised '
                                                            '(mp, '
                                                            'refresh, '
                                                            'gr) '
                                                            'received '
                                                            '(mp, '
                                                            'refresh, '
                                                            'gr)',
                                    'dynamic_capability_old': 'advertised '
                                                              'received',
                                    'graceful_restart': 'advertised '
                                                        'received',
                                    'route_refresh': 'advertised '
                                                     'received',
                                    'route_refresh_old': 'advertised '
                                                         'received',
                                    'vpnv4_unicast': 'advertised '
                                                     'received',
                                    'vpnv6_unicast': 'advertised '
                                                     'received'},
                                'bgp_negotiated_keepalive_timers':
                                    {'hold_time': 99,
                                    'keepalive_interval': 33},
                                'bgp_neighbor_counters':
                                    {'messages':
                                        {'received':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 256,
                                            'notifications': 0,
                                            'opens': 1,
                                            'route_refresh': 0,
                                            'total': 261,
                                            'total_bytes': 5139,
                                            'updates': 4},
                                        'sent':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 256,
                                            'notifications': 0,
                                            'opens': 1,
                                            'route_refresh': 0,
                                            'total': 263,
                                            'total_bytes': 5311,
                                            'updates': 6}}},
                                'bgp_session_transport':
                                    {'connection':
                                        {'last_reset': 'never',
                                        'reset_reason': 'no '
                                                        'error',
                                        'state': 'established'},
                                    'transport':
                                        {'foreign_host': '10.16.2.2',
                                        'foreign_port': '179',
                                        'local_host': '10.4.1.1',
                                        'local_port': '57144'}},
                                'bgp_version': 4,
                                'description': 'nei_desc',
                                'fall_over_bfd': True,
                                'holdtime': 99,
                                'keepalive_interval': 33,
                                'local_as_as_no': 'None',
                                'remote_as': 100,
                                'session_state': 'established',
                                'shutdown': False,
                                'suppress_four_byte_as_capability': True,
                                'up_time': '02:20:02',
                                'update_source': 'Loopback0'}},
                        'router_id': '10.4.1.1'}}}}}
    BgpOpsOutput_info_custom = {
        'instance':
            {'default':
                {'bgp_id': 100,
                'peer_policy':
                    {'PEER-POLICY':
                        {'allowas_in': True,
                        'as_override': True,
                        'default_originate': True,
                        'default_originate_route_map': 'test',
                        'maximum_prefix_max_prefix_no': 300,
                        'route_map_name_in': 'test-map',
                        'route_map_name_out': 'test-map',
                        'route_reflector_client': True,
                        'send_community': True,
                        'soft_reconfiguration': True,
                        'soo': True}},
                'peer_session':
                    {'PEER-SESSION':
                        {'description': 'PEER-SESSION',
                        'disable_connected_check': True,
                        'ebgp_multihop_enable': True,
                        'ebgp_multihop_max_hop': 255,
                        'fall_over_bfd': True,
                        'holdtime': 111,
                        'keepalive_interval': 222,
                        'local_as_as_no': True,
                        'password_text': True,
                        'remote_as': True,
                        'shutdown': True,
                        'suppress_four_byte_as_capability': True,
                        'transport_connection_mode': 'Passive',
                        'update_source': 'interface: '
                                         'loopback0'}},
                'protocol_state': 'running',
                'vrf':
                    {'VRF1':
                        {'address_family':
                            {'ipv4 unicast':
                                {'aggregate_address_as_set': True,
                                'aggregate_address_ipv4_address': '10.121.0.0',
                                'aggregate_address_ipv4_mask': '8',
                                'aggregate_address_summary_only': True,
                                'dampening': 'True',
                                'dampening_half_life_time': '45',
                                'dampening_max_suppress_time': '255',
                                'dampening_reuse_time': '10000',
                                'dampening_route_map': 'dampening1',
                                'dampening_suppress_time': '20000',
                                'label_allocation_mode': 'per-prefix',
                                'nexthop_trigger_delay_critical': 2222,
                                'nexthop_trigger_delay_non_critical': 3333,
                                'nexthop_trigger_enable': True},
                            'vpnv4 unicast':
                                {'distance_internal_as': 33,
                                'distance_local': 55},
                            },
                        'cluster_id': '0.0.0.0',
                        'confederation_identifier': 0,
                        'neighbor':
                            {'10.16.2.10':
                                {'address_family':
                                    {'ipv4 unicast':
                                        {'bgp_table_version': 21,
                                        'default_originate': True,
                                         'session_state':'idle',
                                        'default_originate_route_map': 'SOMENAME',
                                        'soo': 'SOO:100:100'}},
                                'bgp_negotiated_keepalive_timers':
                                    {'hold_time': 180,
                                    'keepalive_interval': 60},
                                'bgp_neighbor_counters':
                                    {'messages':
                                        {'received':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 0,
                                            'notifications': 0,
                                            'opens': 0,
                                            'route_refresh': 0,
                                            'total': 0,
                                            'total_bytes': 0,
                                            'updates': 0},
                                        'sent':
                                            {'bytes_in_queue': 0,
                                            'capability': 0,
                                            'keepalives': 0,
                                            'notifications': 0,
                                            'opens': 0,
                                            'route_refresh': 0,
                                            'total': 0,
                                            'total_bytes': 0,
                                            'updates': 0}}},
                                'bgp_session_transport':
                                    {'connection':
                                        {'last_reset': 'never',
                                         'reset_reason': 'no '
                                                         'error',
                                         'state': 'idle'}},
                                'bgp_version': 4,
                                'holdtime': 180,
                                'keepalive_interval': 60,
                                'local_as_as_no': 'None',
                                'remote_as': 0,
                                'session_state': 'idle',
                                'shutdown': False,
                                'up_time': '02:19:37'}},
                        'router_id': '10.229.11.11'},
                    }}
             }
    }


    BgpOpsOutput_table_custom = {
        'instance':
            {'default':
                {'vrf':
                    {'VRF1':
                        {'address_family':
                            {'ipv4 unicast':
                                {'bgp_table_version': 35,
                                'prefixes':
                                    {'10.121.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': '*>',
                                                'weight': 32768},
                                            2:
                                                {'next_hop': '10.64.4.4',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': 'e',
                                                'status_codes': '*>',
                                                'weight': 32768},
                                            3:
                                                {'next_hop': '10.144.6.6',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': 'e',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.229.11.11/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.84.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}},
                                    '10.21.33.33/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '10.36.3.3',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 0}}},
                                    '10.34.34.0/24':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}}}},
                            }},
                   }}}}
    BgpOpsOutput_table = {
        'instance':
            {'default':
                {'vrf':
                    {'VRF1':
                        {'address_family':
                            {'ipv4 unicast':
                                {'bgp_table_version': 35,
                                'prefixes':
                                    {'10.121.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': '*>',
                                                'weight': 32768},
                                            2:
                                                {'next_hop': '10.64.4.4',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': 'e',
                                                'status_codes': '*>',
                                                'weight': 32768},
                                            3:
                                                {'next_hop': '10.144.6.6',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': 'e',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.229.11.11/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.84.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}},
                                    '10.21.33.33/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '10.36.3.3',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 0}}},
                                    '10.34.34.0/24':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}}}},
                            'ipv6 unicast':
                                {'bgp_table_version': 28,
                                'prefixes':
                                    {'2001:db8:400::/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '2001:111:222::/64':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}},
                                    '2001::11/128':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '2001::33/128':
                                        {'index':
                                            {1:
                                                {'next_hop': '::ffff:10.36.3.3',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 0}}}}}}},
                    'default':
                        {'address_family':
                            {'vpnv4 unicast': {'bgp_table_version': 48},
                            'vpnv4 unicast RD 100:100':
                                {'bgp_table_version': 48,
                                'default_vrf': 'VRF1',
                                'prefixes':
                                    {'10.121.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.229.11.11/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '10.84.0.0/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}},
                                    '10.21.33.33/32':
                                        {'index':
                                            {1:
                                                {'next_hop': '10.36.3.3',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 0}}},
                                    '10.34.34.0/24':
                                        {'index':
                                            {1:
                                                {'next_hop': '0.0.0.0',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}}},
                                'route_distinguisher': '100:100'},
                            'vpnv6 unicast': {'bgp_table_version': 41},
                            'vpnv6 unicast RD 100:100':
                                {'bgp_table_version': 41,
                                'default_vrf': 'VRF1',
                                'prefixes':
                                    {'2001:db8:400::/8':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '2001:111:222::/64':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'origin_codes': 'i',
                                                'status_codes': 'None',
                                                'weight': 32768}}},
                                    '2001::11/128':
                                        {'index':
                                            {1:
                                                {'next_hop': '0::',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 32768}}},
                                    '2001::33/128':
                                        {'index':
                                            {1:
                                                {'next_hop': '::ffff:10.36.3.3',
                                                'localpref': 100,
                                                'metric': 0,
                                                'origin_codes': '?',
                                                'status_codes': '*>',
                                                'weight': 0}}}},
                                'route_distinguisher': '100:100'}}}}}}}

    BgpOpsOutput_routesperpeer = {
        'instance':
            {'default':
                {'vrf':
                    {'VRF1':
                        {'neighbor':
                            {'10.16.2.10':
                                {'address_family':
                                    {'ipv4 labeled-unicast':
                                        {'advertised': {},
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'ipv4 multicast':
                                        {'advertised':
                                            {'10.4.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.9.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.204.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.4.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '192.168.4.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}}},
                                        'received_routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}},
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'ipv4 mvpn': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'ipv4 unicast':
                                        {'advertised':
                                            {'10.4.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'origin_codes': 'i',
                                                        'path_type': 'l',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.2.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}}},
                                        'input_queue': 0,
                                        'msg_rcvd': 0,
                                        'msg_sent': 0,
                                        'output_queue': 0,
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}},
                                        'state_pfxrcd': 'Idle',
                                        'tbl_ver': 0,
                                        'up_down': '5w6d'},
                                    'ipv6 multicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'ipv6 mvpn': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'ipv6 unicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'link-state': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'vpnv4 unicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'vpnv4 unicast RD 2:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn2',
                                        'route_distinguisher': '2:100'},
                                    'vpnv6 unicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'vpnv6 unicast RD 1:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn1',
                                        'route_distinguisher': '1:100'},
                                    'vpnv6 unicast RD 2:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn2',
                                        'route_distinguisher': '2:100'},
                                    'vpnv4 unicast RD 1:100':
                                        {'default_vrf': 'vpn1',
                                        'route_distinguisher': '1:100',
                                        'advertised': {},
                                        'routes':
                                            {'10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}}},
                                'remote_as': 0}}},
                    'default':
                        {'neighbor':
                            {'10.16.2.2':
                                {'address_family':
                                    {'ipv4 labeled-unicast':
                                        {'advertised': {},
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'ipv4 multicast':
                                        {'advertised':
                                            {'10.4.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.9.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.204.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.4.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '192.168.4.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 3333,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}}},
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'ipv4 mvpn': {
                                        'advertised': {},
                                        'routes': {}},
                                    'ipv4 unicast':
                                        {'advertised':
                                            {'10.4.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'origin_codes': 'i',
                                                        'path_type': 'l',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.2.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}}},
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'ipv6 multicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'ipv6 mvpn': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'ipv6 unicast': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'link-state': 
                                        {'advertised': {},
                                        'routes': {}},
                                    'vpnv4 unicast':
                                        {'advertised': {},
                                        'routes': {},
                                        'input_queue': 0,
                                        'msg_rcvd': 108554,
                                        'msg_sent': 108566,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 53,
                                        'up_down': '5w6d'},
                                    'vpnv4 unicast RD 1:100': 
                                        {'default_vrf': 'vpn1',
                                        'route_distinguisher': '1:100',
                                        'advertised': {},
                                        'routes':
                                            {'10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}}},
                                    'vpnv4 unicast RD 2:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn2',
                                        'route_distinguisher': '2:100'},
                                    'vpnv6 unicast RD 1:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn1',
                                        'route_distinguisher': '1:100'},
                                    'vpnv6 unicast RD 2:100': 
                                        {'advertised': {},
                                        'routes': {},
                                        'default_vrf': 'vpn2',
                                        'route_distinguisher': '2:100'},
                                    'vpnv6 unicast':
                                        {'advertised': {},
                                        'routes': {},
                                        'input_queue': 0,
                                        'msg_rcvd': 108554,
                                        'msg_sent': 108566,
                                        'output_queue': 0,
                                        'state_pfxrcd': '1',
                                        'tbl_ver': 45,
                                        'up_down': '5w6d'}},
                                'remote_as': 100}}}}}}}
    BgpOpsOutput_routesperpeer_custom = {
        'instance':
            {'default':
                {'vrf':
                    {'VRF1':
                        {'neighbor':
                            {'10.16.2.10':
                                {'address_family':{
                                    'ipv4 unicast':
                                        {'advertised':
                                            {'10.4.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'origin_codes': 'i',
                                                        'path_type': 'l',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.1.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.16.2.0/24':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '0.0.0.0',
                                                        'locprf': 100,
                                                        'metric': 4444,
                                                        'origin_codes': '?',
                                                        'path_type': 'r',
                                                        'status_codes': '*>',
                                                        'weight': 32768}}}},
                                        'input_queue': 0,
                                        'msg_rcvd': 0,
                                        'msg_sent': 0,
                                        'output_queue': 0,
                                        'routes':
                                            {'10.106.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '192.168.51.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '* ',
                                                        'weight': 0}}},
                                            '10.16.0.0/8':
                                                {'index':
                                                    {1:
                                                        {'next_hop': '10.186.0.2',
                                                        'locprf': 100,
                                                        'metric': 0,
                                                        'origin_codes': '?',
                                                        'path_type': 'i',
                                                        'status_codes': '*>',
                                                        'weight': 0}}}},
                                        'state_pfxrcd': 'Idle',
                                        'tbl_ver': 0,
                                        'up_down': '5w6d'},

                                  },
                                'remote_as': 0}}},
                   }}}}

