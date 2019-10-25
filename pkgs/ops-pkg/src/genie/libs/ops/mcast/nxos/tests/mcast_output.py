''' 
Mcast Genie Ops Object Outputs for NXOS.
'''


class McastOutput(object):

    ShowFeature = {
        'feature':
            {'bgp':
                {'instance':
                    {'1':
                        {'state': 'enabled'}}},
            'pim':
                {'instance':
                    {'1':
                        {'state': 'enabled'}}},
            'pim6':
                {'instance':
                    {'1':
                        {'state': 'enabled'}}}}}

    ShowIpMrouteVrfAll = {
        'vrf': 
            {'VRF': 
                {'address_family': 
                    {'ipv4': {}}},
            'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'232.0.0.0/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim '
                                                 'ip',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'oil_count': 0,
                                        'uptime': '3d11h'}}},
                            '239.5.5.5/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp '
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
            'VRF2': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'224.192.1.10/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp '
                                                  'ip '
                                                  'pim',
                                        'incoming_interface_list': 
                                            {'port-channel8': 
                                                {'rpf_nbr': '172.16.189.233'}},
                                       'oil_count': 3,
                                        'outgoing_interface_list': 
                                            {'Vlan803': 
                                                {'oil_flags': 'igmp',
                                                'oil_uptime': '09:15:11'},
                                            'Vlan812': 
                                                {'oil_flags': 'igmp',
                                                'oil_uptime': '09:14:42'},
                                            'Vlan864': 
                                                {'oil_flags': 'igmp',
                                                'oil_uptime': '09:11:22'}},
                                       'uptime': '09:15:11'},
                                    '192.168.112.3/32': 
                                        {'flags': 'pim '
                                                  'ip',
                                        'incoming_interface_list': 
                                            {'Vlan807': 
                                                {'rpf_nbr': '172.16.94.228'}},
                                        'oil_count': 1,
                                        'outgoing_interface_list': 
                                            {'port-channel9': 
                                                {'oil_flags': 'pim',
                                                'oil_uptime': '09:31:16'}},
                                        'uptime': '09:31:16'},
                                    '192.168.112.4/32': 
                                        {'flags': 'pim '
                                                  'ip',
                                        'incoming_interface_list': 
                                            {'Ethernet1/1.10': 
                                                {'rpf_nbr': '172.16.94.228'}},
                                        'oil_count': 1,
                                        'outgoing_interface_list': 
                                            {'Ethernet1/2.20': 
                                                {'oil_flags': 'pim',
                                                'oil_uptime': '09:31:16'}},
                                        'uptime': '09:31:16'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'232.0.0.0/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim '
                                                  'ip',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'oil_count': 0,
                                        'uptime': '00:41:05'}}},
                            '239.1.1.1/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp '
                                                  'pim '
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
            {'VRF': 
                {'address_family': 
                    {'ipv6': {}}},
            'VRF1': 
                {'address_family': 
                    {'ipv6': 
                        {'multicast_group': 
                            {'ff1e:1111::1:0/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'loopback10': 
                                                {'rpf_nbr': '2001:db8:4401:9999::1'}},
                                        'oil_count': '3',
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234, internal'}},
                                        'oil_count': '3',
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 pim6 m6rib',
                                                             'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234, '
                                                                                                                        'internal'}},
                                                             'oil_count': '3',
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
                            'ff1e:1111:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1'}},
                                        'oil_count': '2',
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': {'flags': 'ipv6 pim6 m6rib',
                                                               'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1234, '
                                                                                                                          'internal'}},
                                                               'oil_count': '3',
                                                               'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 pim6 m6rib',
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
                                    '2001::222:1:1:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                               'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1234'}},
                                                               'oil_count': '2',
                                                               'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                               'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234'}},
                                                               'oil_count': '2',
                                                               'outgoing_interface_list': {'Ethernet1/33.11': {'oif_rpf': True,
                                                                                                               'oil_flags': 'm6rib',
                                                                                                               'oil_uptime': '00:04:03'}},
                                                               'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                               'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                                               'oil_count': '1',
                                                               'uptime': '00:04:02'},
                                    '2001::222:2:44:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                                'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                                                'oil_count': '1',
                                                                'uptime': '00:04:02'}}},
                            'ff1e:2222:ffff::1:0/128': 
                                {'source_address': 
                                    {'*': {'flags': 'mld pim6 ipv6',
                                          'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                          'oil_count': '1',
                                          'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': {'flags': 'ipv6 '
                                                                      'm6rib '
                                                                      'pim6',
                                                              'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1234'}},
                                                              'oil_count': '3',
                                                              'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 '
                                                                      'm6rib '
                                                                      'pim6',
                                                              'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234'}},
                                                              'oil_count': '2',
                                                              'outgoing_interface_list': {'Ethernet1/33.11': {'oif_rpf': True,
                                                                                                              'oil_flags': 'm6rib',
                                                                                                              'oil_uptime': '00:04:03'}},
                                                              'uptime': '00:04:03'}}},
                            'ff1e:3333::1:0/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                        'oil_count': '1',
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                             'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1234'}},
                                                             'oil_count': '2',
                                                             'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 m6rib pim6',
                                                             'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234'}},
                                                             'oil_count': '3',
                                                             'outgoing_interface_list': {'Ethernet1/33.11': {'oif_rpf': True,
                                                                                                             'oil_flags': 'm6rib',
                                                                                                             'oil_uptime': '00:04:03'}},
                                                             'uptime': '00:04:03'}}},
                            'ff1e:3333:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                        'oil_count': '1',
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': {'flags': 'ipv6 '
                                                                       'm6rib '
                                                                       'pim6',
                                                               'incoming_interface_list': {'Ethernet1/33.10': {'rpf_nbr': '2001::222:1:1:1234'}},
                                                               'oil_count': '3',
                                                               'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': {'flags': 'ipv6 '
                                                                       'm6rib '
                                                                       'pim6',
                                                               'incoming_interface_list': {'Ethernet1/33.11': {'rpf_nbr': '2001::222:1:2:1234'}},
                                                               'oil_count': '2',
                                                               'outgoing_interface_list': {'Ethernet1/33.11': {'oif_rpf': True,
                                                                                                               'oil_flags': 'm6rib',
                                                                                                               'oil_uptime': '00:04:03'}},
                                                               'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': {'flags': 'ipv6 '
                                                                       'm6rib '
                                                                       'pim6',
                                                               'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                                               'oil_count': '1',
                                                               'uptime': '00:04:01'},
                                    '2001::222:2:44:1234/128': {'flags': 'ipv6 '
                                                                        'm6rib '
                                                                        'pim6',
                                                                'incoming_interface_list': {'Ethernet1/26': {'rpf_nbr': 'fe80::10'}},
                                                                'oil_count': '1',
                                                                'uptime': '00:04:00'}}},
                            'ff30::/12': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim6 ipv6',
                                        'incoming_interface_list': {'Null': {'rpf_nbr': '0::'}},
                                        'oil_count': '0',
                                        'uptime': '19:55:47'}}}}}}},
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

    ShowIpStaticRouteMulticast = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'10.2.2.2/32': 
                                {'path': 
                                    {'0.0.0.0/32%sanity1 Vlan2': 
                                        {'neighbor_address': '0.0.0.0/32%sanity1 '
                                                              'Vlan2',
                                        'urib': True,
                                        'vrf_id': '2'}}},
                            '10.2.2.3/32': 
                                {'path': 
                                    {'0.0.0.0/32%sanity1 Vlan2': 
                                        {'neighbor_address': '0.0.0.0/32%sanity1 '
                                                             'Vlan2',
                                        'urib': True,
                                        'vrf_id': '2'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'10.49.0.0/8': 
                                {'path': 
                                    {'0.0.0.0/32 Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0.0.0.0/32',
                                        'urib': True,
                                        'vrf_id': '1'}}},
                            '192.168.64.0/8': 
                                {'path': 
                                    {'0.0.0.0/32 Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0.0.0.0/32',
                                        'urib': True,
                                        'vrf_id': '1'}}}}}}},
            'management': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'0.0.0.0/0': 
                                {'path': 
                                    {'172.31.200.1/32': 
                                        {'neighbor_address': '172.31.200.1/32',
                                        'urib': True,
                                        'vrf_id': '3'}}}}}}},
            'sanity1': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'10.2.2.2/32': 
                                {'path': 
                                    {'0.0.0.0/32 Vlan2': 
                                        {'interface_name': 'Vlan2',
                                        'neighbor_address': '0.0.0.0/32',
                                        'urib': True,
                                        'vrf_id': '4'}}},
                            '10.2.2.3/32': 
                                {'path': 
                                    {'0.0.0.0/32 Vlan2': 
                                        {'interface_name': 'Vlan2',
                                        'neighbor_address': '0.0.0.0/32',
                                        'urib': True,
                                        'vrf_id': '4'}}}}}}}}}

    ShowIpv6StaticRouteMulticast = {
        'vrf': 
            {'default': 
                {'address_family': 
                    {'ipv6': 
                        {'mroute': 
                            {'2001:db8:51a5::/16': 
                                {'path': 
                                    {'0:: Null0': 
                                        {'bfd_enable': False,
                                        'interface_name': 'Null0',
                                        'mroute_int': 'Null0',
                                        'neighbor_address': '0::',
                                        'nh_vrf': 'default',
                                        'preference': '1',
                                        'reslv_tid': '80000001',
                                        'rnh_status': 'not '
                                                      'installed '
                                                      'in '
                                                      'u6rib',
                                        'vrf_id': '1'}}},
                            '2001:db8:53f2::/16': 
                                {'path': 
                                    {'0:: port-channel8': 
                                        {'bfd_enable': False,
                                        'interface_name': 'port-channel8',
                                        'mroute_int': 'port-channel8',
                                        'neighbor_address': '0::',
                                        'nh_vrf': 'default',
                                        'preference': '2',
                                        'reslv_tid': '80000001',
                                        'rnh_status': 'not '
                                                      'installed '
                                                      'in '
                                                      'u6rib',
                                        'vrf_id': '1'}}},
                            '2001:db8:9da8::/16': 
                                {'path': 
                                    {'0:: Null0': 
                                        {'bfd_enable': False,
                                        'interface_name': 'Null0',
                                        'mroute_int': 'Null0',
                                        'neighbor_address': '0::',
                                        'nh_vrf': 'default',
                                        'preference': '1',
                                        'reslv_tid': '80000001',
                                        'rnh_status': 'not '
                                                      'installed '
                                                      'in '
                                                      'u6rib',
                                        'vrf_id': '1'}}},
                            '2001:db8:a1f5::/16': 
                                {'path': 
                                    {'0:: Ethernet1/2.10': 
                                        {'bfd_enable': False,
                                        'interface_name': 'Ethernet1/2.10',
                                        'mroute_int': 'Ethernet1/2.10',
                                        'neighbor_address': '0::',
                                        'nh_vrf': 'default',
                                        'preference': '3',
                                        'reslv_tid': '80000001',
                                        'rnh_status': 'not '
                                                   'installed '
                                                   'in '
                                                   'u6rib',
                                        'vrf_id': '1'}}}}}}}}}

    McastInfo = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'10.2.2.2/32': 
                                {'path': 
                                    {'0.0.0.0/32%sanity1 Vlan2': 
                                        {'neighbor_address': '0.0.0.0/32%sanity1 '
                                                             'Vlan2'}}},
                            '10.2.2.3/32': 
                                {'path': 
                                    {'0.0.0.0/32%sanity1 Vlan2': 
                                        {'neighbor_address': '0.0.0.0/32%sanity1 '
                                                             'Vlan2'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'enable': True,
                        'mroute': 
                            {'10.49.0.0/8': 
                                {'path': 
                                    {'0.0.0.0/32 Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0.0.0.0/32'}}},
                            '192.168.64.0/8': 
                                {'path': 
                                    {'0.0.0.0/32 Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0.0.0.0/32'}}}}},
                    'ipv6': 
                        {'enable': True,
                        'mroute': 
                            {'2001:db8:51a5::/16': 
                                {'path': 
                                    {'0:: Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0::'}}},
                            '2001:db8:53f2::/16': 
                                {'path': 
                                    {'0:: port-channel8': 
                                        {'interface_name': 'port-channel8',
                                        'neighbor_address': '0::'}}},
                            '2001:db8:9da8::/16': 
                                {'path': 
                                    {'0:: Null0': 
                                        {'interface_name': 'Null0',
                                        'neighbor_address': '0::'}}},
                            '2001:db8:a1f5::/16': 
                                {'path': 
                                    {'0:: Ethernet1/2.10': 
                                        {'interface_name': 'Ethernet1/2.10',
                                        'neighbor_address': '0::'}}}}}}},
            'management': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'0.0.0.0/0': 
                                {'path': 
                                    {'172.31.200.1/32': 
                                        {'neighbor_address': '172.31.200.1/32'}}}}}}},
            'sanity1': 
                {'address_family': 
                    {'ipv4': 
                        {'mroute': 
                            {'10.2.2.2/32': 
                                {'path': 
                                    {'0.0.0.0/32 Vlan2': 
                                        {'interface_name': 'Vlan2',
                                        'neighbor_address': '0.0.0.0/32'}}},
                            '10.2.2.3/32': 
                                {'path': 
                                    {'0.0.0.0/32 Vlan2': 
                                        {'interface_name': 'Vlan2',
                                        'neighbor_address': '0.0.0.0/32'}}}}}}}}}

    McastTable = {
        'vrf': 
            {'VRF1': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'232.0.0.0/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim ip',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'uptime': '3d11h'}}},
                            '239.5.5.5/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp ip pim',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0.0.0.0'}},
                                        'outgoing_interface_list': 
                                            {'loopback1': 
                                                {'flags': 'igmp',
                                                'uptime': '3d11h'}},
                                        'uptime': '3d11h'}}}}},
                    'ipv6': 
                        {'multicast_group': 
                            {'ff1e:1111::1:0/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'loopback10': 
                                                {'rpf_nbr': '2001:db8:4401:9999::1'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234, internal'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234, internal'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': 
                                        {'flags': 'pim6 m6rib ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10, internal'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:44:1234/128': 
                                        {'flags': 'pim6 m6rib ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10, internal'}},
                                        'uptime': '00:04:03'}}},
                            'ff1e:1111:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234, internal'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 pim6 m6rib',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234, internal'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': 
                                        {'flags': 'pim6 m6rib ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10, internal'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:44:1234/128': 
                                        {'flags': 'pim6 m6rib ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10, internal'}},
                                        'uptime': '00:04:03'}}},
                            'ff1e:2222:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                                'uptime': '00:04:02'},
                                    '2001::222:2:44:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:02'}}},
                            'ff1e:2222:ffff::1:0/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'}}},
                            'ff1e:3333::1:0/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'}}},
                            'ff1e:3333:ffff::/128': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'mld pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:1:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.10': 
                                                {'rpf_nbr': '2001::222:1:1:1234'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:1:2:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'rpf_nbr': '2001::222:1:2:1234'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/33.11': 
                                                {'flags': 'm6rib',
                                                'uptime': '00:04:03'}},
                                        'uptime': '00:04:03'},
                                    '2001::222:2:3:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:01'},
                                    '2001::222:2:44:1234/128': 
                                        {'flags': 'ipv6 m6rib pim6',
                                        'incoming_interface_list': 
                                            {'Ethernet1/26': 
                                                {'rpf_nbr': 'fe80::10'}},
                                        'uptime': '00:04:00'}}},
                            'ff30::/12': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0::'}},
                                        'uptime': '19:55:47'}}}}}}},
            'VRF2': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'224.192.1.10/32': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'igmp ip pim',
                                        'incoming_interface_list': 
                                            {'port-channel8': 
                                                {'rpf_nbr': '172.16.189.233'}},
                                        'outgoing_interface_list': 
                                            {'Vlan803': 
                                                {'flags': 'igmp',
                                                'uptime': '09:15:11'},
                                            'Vlan812': 
                                                {'flags': 'igmp',
                                                'uptime': '09:14:42'},
                                            'Vlan864': 
                                                {'flags': 'igmp',
                                                'uptime': '09:11:22'}},
                                        'uptime': '09:15:11'},
                                    '192.168.112.3/32': 
                                        {'flags': 'pim ip',
                                        'incoming_interface_list': 
                                            {'Vlan807': 
                                                {'rpf_nbr': '172.16.94.228'}},
                                        'outgoing_interface_list': 
                                            {'port-channel9': 
                                                {'flags': 'pim',
                                                'uptime': '09:31:16'}},
                                        'uptime': '09:31:16'},
                                    '192.168.112.4/32': 
                                        {'flags': 'pim ip',
                                        'incoming_interface_list': 
                                            {'Ethernet1/1.10': 
                                                {'rpf_nbr': '172.16.94.228'}},
                                        'outgoing_interface_list': 
                                            {'Ethernet1/2.20': 
                                                {'flags': 'pim',
                                                'uptime': '09:31:16'}},
                                        'uptime': '09:31:16'}}}}}}},
            'default': 
                {'address_family': 
                    {'ipv4': 
                        {'multicast_group': 
                            {'232.0.0.0/8': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim ip',
                                        'incoming_interface_list': {'Null': {'rpf_nbr': '0.0.0.0'}},
                                        'uptime': '00:41:05'}}},
                                    '239.1.1.1/32': 
                                        {'source_address': 
                                            {'*': 
                                                {'flags': 'igmp pim ip',
                                                'incoming_interface_list': 
                                                    {'Ethernet9/13': 
                                                        {'rpf_nbr': '10.2.3.2'}},
                                                'outgoing_interface_list': 
                                                    {'loopback2': 
                                                        {'flags': 'igmp',
                                                        'uptime': '3d11h'}},
                                                'uptime': '3d11h'}}}}},
                    'ipv6': 
                        {'multicast_group': 
                            {'ff30::/12': 
                                {'source_address': 
                                    {'*': 
                                        {'flags': 'pim6 ipv6',
                                        'incoming_interface_list': 
                                            {'Null': 
                                                {'rpf_nbr': '0::'}},
                                        'uptime': '00:11:23'}}}}}}}}}
