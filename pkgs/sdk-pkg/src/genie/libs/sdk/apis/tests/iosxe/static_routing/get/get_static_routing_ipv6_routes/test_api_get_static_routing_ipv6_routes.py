import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.static_routing.get import get_static_routing_ipv6_routes


class TestGetStaticRoutingIpv6Routes(unittest.TestCase):

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

    def test_get_static_routing_ipv6_routes(self):
        result = get_static_routing_ipv6_routes(self.device, vrf=None)
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_ipv6_routes(self.device, vrf=None)
        expected_output = {
            '2001:4::/48': {
                'next_hop': {
                    'outgoing_interface': {
                        'Null0': {
                            'active': True,
                            'outgoing_interface': 'Null0',
                            'preference': 1
                        }
                    }
                },
                'route': '2001:4::/48',
            }
        }
        print(result)
        print(expected_output)
        self.assertEqual(result, expected_output)

        result = get_static_routing_ipv6_routes(self.device, vrf='nonexist')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_ipv6_routes(self.device, vrf='red')
        expected_output = None
        self.assertEqual(result, expected_output)

        result = get_static_routing_ipv6_routes(self.device, vrf='red')
        expected_output = {
            '1:1:1:1::/64': {
                'next_hop': {
                    'next_hop_list': {
                        1: {
                            'active': False,
                            'index': 1,
                            'next_hop': '1:1:1:1::254',
                            'preference': 1
                        }
                    }
                },
                'route': '1:1:1:1::/64'
            }
        }
        self.assertEqual(result, expected_output)
