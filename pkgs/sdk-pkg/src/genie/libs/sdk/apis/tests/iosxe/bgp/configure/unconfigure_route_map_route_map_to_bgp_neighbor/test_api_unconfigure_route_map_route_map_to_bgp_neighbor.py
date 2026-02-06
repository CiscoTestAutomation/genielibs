from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_route_map_route_map_to_bgp_neighbor

class TestUnconfigureRouteMapRouteMapToBgpNeighbor(TestCase):

    def test_unconfigure_route_map_route_map_to_bgp_neighbor(self):
        device = Mock()
        result = unconfigure_route_map_route_map_to_bgp_neighbor(
            device,
            65000,
            'vpnv4',
            [{'direction': 'in', 'neighbor': '1.1.1.4', 'route_map': 'test'}],
            '',
            ''
        )
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('router bgp 65000\naddress-family vpnv4\nno neighbor 1.1.1.4 route-map test in\n',)
        )