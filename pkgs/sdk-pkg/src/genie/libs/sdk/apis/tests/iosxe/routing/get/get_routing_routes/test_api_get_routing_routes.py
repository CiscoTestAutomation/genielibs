import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_routing_routes


class TestGetRoutingRoutes(unittest.TestCase):

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

    def test_get_routing_routes(self):
        result = get_routing_routes(self.device, vrf=None, address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_routing_routes(self.device, vrf=None, address_family='ipv4')
        expected_output = {
            '10.10.10.0/32': {
                'active': True,
                'next_hop': {
                    'outgoing_interface': {
                        'Loopback0': {
                            'outgoing_interface': 'Loopback0'
                        }
                    }
                },
                'route': '10.10.10.0/32',
                'source_protocol': 'connected',
                'source_protocol_codes': 'C'
            },
            '10.10.10.10/32': {
                'active': True,
                'metric': 1,
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'index': 1,
                            'next_hop': '192.168.103.1',
                            'outgoing_interface': 'BDI103',
                            'updated': '13:13:12'
                        }
                    }
                },
                'route': '10.10.10.10/32',
                'route_preference': 110,
                'source_protocol': 'ospf',
                'source_protocol_codes': 'O'
            },
            '192.168.103.0/24': {
                'active': True,
                'next_hop': {
                    'outgoing_interface': {
                        'BDI103': {
                            'outgoing_interface': 'BDI103'
                        }
                    }
                },
                'route': '192.168.103.0/24',
                'source_protocol': 'connected',
                'source_protocol_codes': 'C'},
            '192.168.103.254/32': {
                'active': True,
                'next_hop': {
                    'outgoing_interface': {
                        'BDI103': {
                            'outgoing_interface': 'BDI103'
                        }
                    }
                },
                'route': '192.168.103.254/32',
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            }
        }
        self.assertEqual(result, expected_output)

        result = get_routing_routes(self.device, vrf='red', address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_routing_routes(self.device, vrf='red', address_family='ipv4')
        expected_output = {
            '0.0.0.0/0': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'index': 1,
                            'next_hop': '192.168.103.254'
                        }
                    }
                },
                'route': '0.0.0.0/0',
                'route_preference': 254,
                'source_protocol': 'static',
                'source_protocol_codes': 'S*'
            },
            '192.168.103.0/24': {
                'active': True,
                'next_hop': {
                    'outgoing_interface': {
                        'Ethernet0/0.103': {
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '192.168.103.0/24',
                'source_protocol': 'connected',
                'source_protocol_codes': 'C'
            },
            '192.168.103.1/32': {
                'active': True,
                'metric': 0,
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'index': 1,
                            'next_hop': '192.168.103.254',
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '192.168.103.1/32',
                'route_preference': 254,
                'source_protocol': 'static',
                'source_protocol_codes': 'S'
            },
            '192.168.103.101/32': {
                'active': True,
                'next_hop': {
                    'outgoing_interface': {
                        'Ethernet0/0.103': {
                            'outgoing_interface': 'Ethernet0/0.103'
                        }
                    }
                },
                'route': '192.168.103.101/32',
                'source_protocol': 'local',
                'source_protocol_codes': 'L'
            }
        }
        self.assertEqual(result, expected_output)

        result = get_routing_routes(self.device, vrf='nonexist', address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)
