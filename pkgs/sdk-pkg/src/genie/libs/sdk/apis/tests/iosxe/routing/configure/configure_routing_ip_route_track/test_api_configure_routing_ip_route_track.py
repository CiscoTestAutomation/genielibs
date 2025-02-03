from unittest import TestCase
from genie.libs.sdk.apis.iosxe.routing.configure import configure_routing_ip_route_track
from unittest.mock import Mock


class TestConfigureRoutingIpRouteTrack(TestCase):

    def test_configure_routing_ip_route_track(self):
        self.device = Mock()
        result = configure_routing_ip_route_track(self.device, '0.0.0.0', '0.0.0.0', 'Vlan301', '172.32.24.17', 'dist001-mgmt', '301', 'FACTORY_VRF')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip route vrf FACTORY_VRF 0.0.0.0 0.0.0.0 Vlan301 172.32.24.17 name dist001-mgmt track 301'],)
        )
