# Genie
from genie.ops.base import Base
from genie.metaparser.util.schemaengine import Any

class Interface(Base):

    schema = {
        'interface': {
            'info': {
                Any(): {
                    'description': Any(),
                    'type': Any(),
                    'oper_status': Any(),
                    'last_change': Any(),
                    'phys_address': Any(),
                    'mtu': Any(),
                    'enabled': Any(),
                    'vlan_id': Any(),
                    'access_vlan': Any(),
                    'trunk_vlans': Any(),
                    'mac_address': Any(),
                    'auto_negotiate': Any(),
                    'duplex_mode': Any(),
                    'port_speed': Any(),
                    'switchport_enable': Any(),
                    'switchport_mode': Any(),
                    'medium': Any(),
                    'delay': Any(),
                    'port_channel': {
                        'port_channel_member': Any(),
                        'port_channel_int': Any(),
                        'port_channel_member_intfs': Any(),
                    },
                    'flow_control': {
                        'receive': Any(),
                        'send': Any(),
                    },
                    'bandwidth': Any(),
                    'link_status': Any(),
                    'vrf': Any(),
                    'vrf_downstream': Any(),
                    'accounting': {
                        Any(): {
                            'pkts_in': Any(),
                            'pkts_out': Any(),
                            'chars_in': Any(),
                            'chars_out': Any(),
                        },
                    },
                    'counters': {
                        'rate': {
                            'load_interval': Any(),
                            'in_rate': Any(),
                            'in_rate_pkts': Any(),
                            'out_rate': Any(),
                            'out_rate_pkts': Any(),
                        },
                        'in_pkts': Any(),
                        'in_octets': Any(),
                        'in_unicast_pkts': Any(),
                        'in_broadcast_pkts': Any(),
                        'in_multicast_pkts': Any(),
                        'in_discards': Any(),
                        'in_errors': Any(),
                        'in_unknown_protos': Any(),
                        'in_mac_control_frames': Any(),
                        'in_mac_pause_frames': Any(),
                        'in_oversize_frames': Any(),
                        'in_jabber_frames': Any(),
                        'in_fragment_frames': Any(),
                        'in_8021q_frames': Any(),
                        'in_crc_errors': Any(),
                        'out_pkts': Any(),
                        'out_octets': Any(),
                        'out_unicast_pkts': Any(),
                        'out_broadcast_pkts': Any(),
                        'out_multicast_pkts': Any(),
                        'out_discard': Any(),
                        'out_errors': Any(),
                        'out_mac_control_frames': Any(),
                        'out_mac_pause_frames': Any(),
                        'out_8021q_frames': Any(),
                        'last_clear': Any(),
                    },
                    'encapsulation': {
                        'enacapsulation': Any(),
                        'first_dot1q': Any(),
                        'second_dot1q': Any(),
                        'native_vlan': Any(),
                    },
                    'ipv4': {
                        Any(): {
                            'ip': Any(),
                            'prefix_length': Any(),
                            'origin': Any(),
                            'sedondary': Any(),
                            'route_tag': Any(),
                            'secondary_vrf': Any(),
                        },
                        'unnumbered': {
                            'interface_ref': Any(),
                        },
                    },
                    'ipv6': {
                        Any(): {
                            'ip': Any(),
                            'prefix_length': Any(),
                            'anycast': Any(),
                            'eui_64': Any(),
                            'route_tag': Any(),
                            'origin': Any(),
                            'status': Any(),
                            'autoconf': {
                                'valid_lifetime': Any(),
                                'preferred_lifetime': Any(),
                            },
                        },
                        'unnumbered': {
                            'interface_ref': Any(),
                        },
                        'enabled': Any(),
                    }
                }
            }
        }
    }

    exclude = ['in_discards',
               'in_octets',
               'in_pkts',
               'last_clear',
               'out_octets',
               'out_pkts',
               'in_rate',
               'out_rate',
               'in_errors',
               'in_crc_errors',
               'in_rate_pkts',
               'out_rate_pkts',
               'in_broadcast_pkts',
               'out_broadcast_pkts',
               'in_multicast_pkts',
               'out_multicast_pkts',
               'in_unicast_pkts',
               'out_unicast_pkts',
               'last_change',
               'mac_address',
               'phys_address',
               '((t|T)unnel.*)',
               '(Null.*)',
               'chars_out',
               'chars_in',
               'pkts_out',
               'pkts_in',
               'mgmt0']