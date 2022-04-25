import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.static_routing.get import get_static_routing_routes


class TestGetStaticRoutingRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          host1:
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
        self.device = self.testbed.devices['host1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_static_routing_routes(self):
        result = get_static_routing_routes(self.device, vrf=None, address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_routes(self.device, vrf=None, address_family='ipv4')
        expected_output = {
            '1.1.1.0/24': {
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'active': False,
                            'index': 1,
                            'next_hop': '1.1.1.254',
                            'owner_code': 'M',
                            'preference': 1
                        }
                    }
                },
                'route': '1.1.1.0/24'
            }
        }
        self.assertEqual(result, expected_output)

        result = get_static_routing_routes(self.device, vrf='nonexist', address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_routes(self.device, vrf='red', address_family='ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_routes(self.device, vrf='red', address_family='ipv4')
        expected_output = {
            '0.0.0.0/0': {
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'active': True,
                            'index': 1,
                            'next_hop': '192.168.103.254',
                            'preference': 254,
                            'owner_code': 'D'
                        }
                    }
                },
                'route': '0.0.0.0/0'
            },
            '192.168.103.1/32': {
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'active': True,
                            'index': 1,
                            'next_hop': '192.168.103.254',
                            'outgoing_interface': 'Ethernet0/0.103',
                            'preference': 254,
                            'owner_code': 'D'
                        }
                    }
                },
                'route': '192.168.103.1/32'
            }
        }
        self.assertEqual(result, expected_output)
