from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_route_map_route_map_to_bgp_neighbor
from unittest.mock import Mock

class TestConfigureRouteMapRouteMapToBgpNeighbor(TestCase):

    def test_configure_route_map_route_map_to_bgp_neighbor(self):
        self.device = Mock()
        configure_route_map_route_map_to_bgp_neighbor(self.device, 65000, 'vpnv4', [{'direction': 'in', 'neighbor': '1.1.1.4', 'route_map': 'test'}], '', '')
        self.assertEqual(self.device.configure.mock_calls[0].args, ('router bgp 65000\naddress-family vpnv4\nneighbor 1.1.1.4 route-map test in\n',))


    def test_configure_route_map_route_map_to_bgp_neighbor_1(self):
        self.device = Mock()
        configure_route_map_route_map_to_bgp_neighbor(self.device, 65000, '', [{'direction': 'in', 'neighbor': '99.1.3.1', 'route_map': 'test'}], 'ce1', 'ipv4')
        self.assertEqual(self.device.configure.mock_calls[0].args, ('router bgp 65000\n' 'address-family ipv4 vrf ce1\n''neighbor 99.1.3.1 route-map test in\n',))

