import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_routing_route_attrs


class TestVerifyRoutingRouteAttrs(unittest.TestCase):

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

    def test_verify_routing_route_attrs(self):
        result = verify_routing_route_attrs(self.device, '20.20.20.20/32',
                                            vrf_name=None, max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None, max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None, next_hop_info={
                'next_hop': '192.168.203.1',
                'outgoing_interface': 'BDI103',
            },
                                            max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None, next_hop_info={
                'next_hop': '192.168.103.1',
                'outgoing_interface': 'BDI103',
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None,
                                            route_attrs={
                'source_protocol_codes': 'O',
            },
                                            next_hop_info={
                'next_hop': '192.168.103.1',
                'outgoing_interface': 'BDI103',
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None,
                                            route_attrs={
                'source_protocol_codes': 'C',
            },
                                            next_hop_info={
                'next_hop': '192.168.103.1',
                'outgoing_interface': 'BDI103',
            },
                                            max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '10.10.10.10/32',
                                            vrf_name=None, next_hop_info={},
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '0.0.0.0/0',
                                            vrf_name='red',
                                            route_attrs={
                'source_protocol_codes': 'S*',
            },
                                            next_hop_info={
                'next_hop': '192.168.103.254',
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '0.0.0.0/0',
                                            vrf_name='nonexist',
                                            route_attrs={
                'source_protocol_codes': 'S*',
            },
                                            next_hop_info={
                'next_hop': '192.168.103.254',
            },
                                            max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '192.168.103.101/32',
                                            vrf_name='red',
                                            route_attrs={
                'source_protocol_codes': 'L',
            },
                                            next_hop_info={
                'outgoing_interface': 'Ethernet0/0.103',
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '2001:103::/64',
                                            address_family='ipv6',
                                            vrf_name='red',
                                            route_attrs={
                'source_protocol_codes': 'NDp',
            },
                                            next_hop_info={
                'outgoing_interface': 'Ethernet0/0.103'
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '0.0.0.0/0',
                                            vrf_name='red',
                                            route_attrs={},
                                            next_hop_info={
                'next_hop': '192.168.103.254',
            },
                                            max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_routing_route_attrs(self.device, '0.0.0.0/0',
                                            vrf_name='red',
                                            route_attrs={
                'source_protocol_codes': 'C',
            },
                                            next_hop_info={
                'next_hop': '192.168.103.254',
            },
                                            max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)
