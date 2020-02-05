'''
 Nd Genie Ops Object Outputs for IOSXE.
'''

class NdOutput(object):
    
    ShowIpv6Neighbors = {
        "interface": {
            "GigabitEthernet2.90": {
                "interface": "GigabitEthernet2.90",
                "neighbors": {
                    "FE80::F816:3EFF:FE0F:B2EC": {
                        "age": "2",
                        "ip": "FE80::F816:3EFF:FE0F:B2EC",
                        "link_layer_address": "fa16.3e0f.b2ec",
                        "neighbor_state": "STALE"
                    }
                }
            }
        }
    }
    
    ShowIpv6Interface = {
        "GigabitEthernet2.90": {
            "enabled": True,
            "oper_status": "up",
            "ipv6": {
                "FE80::F816:3EFF:FE26:1224": {
                    "ip": "FE80::F816:3EFF:FE26:1224",
                    "origin": "link_layer",
                    "status": "valid"
                },
                "2001:10:12:90::1/64": {
                    "ip": "2001:10:12:90::1",
                    "prefix_length": "64",
                    "status": "valid"
                },
                "enabled": True,
                "icmp": {
                    "error_messages_limited": 100,
                    "redirects": True,
                    "unreachables": "sent"
                },
                "nd": {
                    "suppress": False,
                    "dad_enabled": True,
                    "dad_attempts": 1,
                    "reachable_time": 30000,
                    "using_time": 30000,
                    "advertised_reachable_time": 0,
                    "advertised_reachable_time_unspecified": True,
                    "advertised_retransmit_interval": 0,
                    "advertised_retransmit_interval_unspecified": True,
                    "router_advertisements_interval": 200,
                    "router_advertisements_live": 1800,
                    "advertised_default_router_preference": "Medium"
                }
            },
            "joined_group_addresses": [
                "FF02::1",
                "FF02::16",
                "FF02::1:FF00:1",
                "FF02::1:FF26:1224",
                "FF02::2",
                "FF02::A",
                "FF02::D"
            ],
            "mtu": 1500,
            "addresses_config_method": "stateless autoconfig"
        }
    }
    
    ndOpsOutput = {
        'interface':{
            'GigabitEthernet2.90':{
                'interface': 'GigabitEthernet2.90',
                "router_advertisement": {
                    "interval": 200,
                    "suppress": False,
                    "lifetime": 1800,
                },
                'neighbors': {
                    "FE80::F816:3EFF:FE0F:B2EC": {
                        "age": "2",
                        "ip": "FE80::F816:3EFF:FE0F:B2EC",
                        "link_layer_address": "fa16.3e0f.b2ec",
                        "neighbor_state": "STALE",
                    },
                },
            },
        },
    }
