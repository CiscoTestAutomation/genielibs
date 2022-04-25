import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.static_routing.verify import verify_static_routing_route_attrs


class TestVerifyStaticRoutingRouteAttrs(unittest.TestCase):

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

    def test_verify_static_routing_route_attrs(self):
        result = verify_static_routing_route_attrs(self.device, '2.2.2.2.0/24',
                                                   vrf_name=None, max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1.1.1.0/24',
                                                   vrf_name=None, max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1.1.1.0/24',
                                                   vrf_name=None, next_hop_info={
                'active': False,
                'next_hop': '2.2.2.254',
                'preference': 1,
                'owner_code': 'M',
            },
                                                   max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1.1.1.0/24',
                                                   vrf_name=None, next_hop_info={
                'active': False,
                'next_hop': '1.1.1.254',
                'preference': 1,
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1.1.1.0/24',
                                                   vrf_name=None, next_hop_info={
                'active': False,
                'next_hop': '1.1.1.254',
                'preference': 1,
                'owner_code': 'M',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1.1.1.0/24',
                                                   vrf_name=None, next_hop_info={},
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '0.0.0.0/0',
                                                   vrf_name='red', next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '0.0.0.0/0',
                                                   vrf_name='nonexist', next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '192.168.103.1/32',
                                                   vrf_name='red', next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'outgoing_interface': 'Ethernet0/0.103',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '1:1:1:1::/64',
                                                   address_family='ipv6',
                                                   vrf_name='red', next_hop_info={
                'active': False,
                'next_hop': '1:1:1:1::254',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '0.0.0.0/0',
                                                   vrf_name='red',
                                                   route_attrs={
              'route': '0.0.0.0/0',
            },
                                                   next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '0.0.0.0/0',
                                                   vrf_name='red',
                                                   route_attrs={},
                                                   next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = True
        self.assertEqual(result, expected_output)

        result = verify_static_routing_route_attrs(self.device, '0.0.0.0/0',
                                                   vrf_name='red',
                                                   route_attrs={
              'route': '1.1.1.1/32',
            },
                                                   next_hop_info={
                'active': True,
                'next_hop': '192.168.103.254',
                'owner_code': 'D',
            },
                                                   max_time=1)
        expected_output = False
        self.assertEqual(result, expected_output)
