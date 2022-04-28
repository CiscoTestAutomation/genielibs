import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_routing_ipv6_routes


class TestGetRoutingIpv6Routes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          router1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_routing_ipv6_routes(self):
        result = get_routing_ipv6_routes(self.device, vrf=None)
        expected_output = {
            '2001:103::/64': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'BDI103': {
                            'outgoing_interface': 'BDI103'
                        }
                    }
                },
                'route': '2001:103::/64',
                'route_preference': 0,
                'source_protocol': 'connected',
                'source_protocol_codes': 'C'
            },
            '2001:103::254/128': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'BDI103': {
                            'outgoing_interface': 'BDI103'
                        }
                    }
                },
                'route': '2001:103::254/128',
                'route_preference': 0,
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            },
            '2001:10::/128': {
                'active': True,
                'metric': 0,
                'next_hop': {
                  'outgoing_interface': {
                        'Loopback0': {
                            'outgoing_interface': 'Loopback0'
                        }
                    }
                },
                'route': '2001:10::/128',
                'route_preference': 0,
                'source_protocol': 'local_connected',
                'source_protocol_codes': 'LC'
            },
            '2001:10::10/128': {
                'active': True,
                'metric': 1,
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'index': 1,
                            'next_hop': 'FE80::A8BB:CCFF:FE00:6900',
                            'outgoing_interface': 'BDI103'
                        }
                    }
                },
                'route': '2001:10::10/128',
                'route_preference': 110,
                'source_protocol': 'ospf',
                'source_protocol_codes': 'O'
            },
            'FF00::/8': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'Null0': {
                            'outgoing_interface': 'Null0'
                        }
                    }
                },
                'route': 'FF00::/8',
                'route_preference': 0,
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            }
        }
        self.assertEqual(result, expected_output)

        result = get_routing_ipv6_routes(self.device, vrf='red')
        expected_output = {
            '2001:103::/64': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'Ethernet0/0.103': {
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '2001:103::/64',
                'route_preference': 2,
                'source_protocol': 'nd',
                'source_protocol_codes': 'NDp'
            },
            '2001:103::A8BB:1FF:FE03:11/128': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'Ethernet0/0.103': {
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '2001:103::A8BB:1FF:FE03:11/128',
                'route_preference': 0,
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            },
            '2001:103::C8F5:BBA:F6AF:B287/128': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'Ethernet0/0.103': {
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '2001:103::C8F5:BBA:F6AF:B287/128',
                'route_preference': 0,
                'source_protocol': 'local_connected',
                'source_protocol_codes': 'LC'
            },
            '::/0': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'index': 1,
                            'next_hop': 'FE80::A8BB:CCFF:FE00:6900',
                            'outgoing_interface': 'Ethernet0/0.103'
                        },
                        2: {
                            'index': 2,
                            'next_hop': 'FE80::A8BB:CCFF:FE80:8EFF',
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '::/0',
                'route_preference': 2,
                'source_protocol': 'nd',
                'source_protocol_codes': 'ND'
            },
            'FF00::/8': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'outgoing_interface': {
                        'Null0': {
                            'outgoing_interface': 'Null0'
                        }
                    }
                },
                'route': 'FF00::/8',
                'route_preference': 0,
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            }
        }
        self.assertEqual(result, expected_output)

        result = get_routing_ipv6_routes(self.device, vrf='nonexist')
        expected_output = {}
        self.assertEqual(result, expected_output)
