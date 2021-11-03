'''
 Vxlan Genie Ops Object Outputs for IOSXE.
'''

class VxlanOutput(object):
    # 'vxlan' Ops output

    ShowRunInterface = {
        "interfaces": {
            "nve1": {
                "member_vni": {
                    "20011": {
                        "ingress_replication": {
                            'enabled': True,
                            'remote_peer_ip': '1.1.1.1'
                        }
                    },
                    "20012": {
                        "ingress_replication": {
                            'enabled': True,
                            'remote_peer_ip': '2.2.2.1'
                        }
                    },
                    "20013": {
                        "mcast_group": "239.1.1.3"
                    },
                    "20014": {
                        "mcast_group": "239.1.1.4"
                    },
                    "30000": {
                        "vrf": "red"
                    }
                },
                "source_interface": "Loopback1"
            },
        }
    }
    ShowNveInterfaceDetail = {
        'admin_state': 'Up',
        'bgp_host_reachability': 'Enabled',
        'encap': 'Vxlan',
        'interface': 'nve1',
        'num_l2vni_cp': 4,
        'num_l2vni_dp': 0,
        'num_l3vni_cp': 1,
        'oper_state': 'Down',
        'src_intf': {
            'Loopback1 ': {
                'primary_ip': '1.1.1.2',
                'vrf': '0',
            },
        },
         'tunnel_intf': {
            'Tunnel0': {
                'counters': {
                    'bytes_in': 11,
                    'bytes_out': 0,
                    'pkts_in': 1,
                    'pkts_out': 0
                },
            }
        },
        'vxlan_dport': 4789,
        }
    ShowNveVni = {
        'nve1': {
            '20011': {
                'cfg': 'CLI',
                'interface': 'nve1',
                'mcast': 'N/A',
                'mode': 'L2CP',
                'vlan': '11',
                'vni': '20011',
                'vni_state': 'Up',
                'vrf': 'N/A'
            },
            '20012': {
                'cfg': 'CLI',
                'interface': 'nve1',
                'mcast': 'N/A',
                'mode': 'L2CP',
                'vlan': '12',
                'vni': '20012',
                'vni_state': 'Up',
                'vrf': 'N/A'
            },
            '20013': {
                'cfg': 'CLI',
                'interface': 'nve1',
                'mcast': '229.1.1.3',
                'mode': 'L2CP',
                'vlan': 'N/A',
                'vni': '20013',
                'vni_state': 'BD Down/Re',
                'vrf': 'N/A'
            },
            '20014': {
                'cfg': 'CLI',
                'interface': 'nve1',
                'mcast': '229.1.1.4',
                'mode': 'L2CP',
                'vlan': 'N/A',
                'vni': '20014',
                'vni_state': 'BD Down/Re',
                'vrf': 'N/A'
            },
        }
    }

    #################################################
    #  Vxlan nve
    #################################################

    VxlanNveOpsOutput = {
        'nve1': {
            'admin_state': 'Up',
            'bgp_host_reachability': 'Enabled',
            'encap': 'Vxlan',
            'num_l2vni_cp': 4,
            'num_l2vni_dp': 0,
            'num_l3vni_cp': 1,
            'oper_state': 'Down',
            'src_intf': {
                'Loopback1 ': {
                    'primary_ip': '1.1.1.2',
                    'vrf': '0'}
                },
            'tunnel_intf': {
                'Tunnel0': {
                    'counters': {
                        'bytes_in': 11,
                        'bytes_out': 0,
                        'pkts_in': 1,
                        'pkts_out': 0
                    },
                }
            },
            'vni': {
                '20011': {
                    'cfg': 'CLI',
                    'ingress_replication': {
                        'enabled': True,
                        'remote_peer_ip': '1.1.1.1'
                    },
                    'mcast': 'N/A',
                    'mode': 'L2CP',
                    'vlan': '11',
                    'vni_state': 'Up',
                    'vrf': 'N/A'
                    },
                '20012': {
                    'cfg': 'CLI',
                    'ingress_replication': {
                        'enabled': True,
                        'remote_peer_ip': '2.2.2.1'
                    },
                    'mcast': 'N/A',
                    'mode': 'L2CP',
                    'vlan': '12',
                    'vni_state': 'Up',
                    'vrf': 'N/A'
                    },
                '20013': {
                    'cfg': 'CLI',
                    'mcast': '229.1.1.3',
                    'mode': 'L2CP',
                    'vlan': 'N/A',
                    'vni_state': 'BD Down/Re',
                    'vrf': 'N/A'
                    },
                '20014': {
                    'cfg': 'CLI',
                    'mcast': '229.1.1.4',
                    'mode': 'L2CP',
                    'vlan': 'N/A',
                    'vni_state': 'BD Down/Re',
                    'vrf': 'N/A'
                    },
                },
            'vxlan_dport': 4789
            }
    }