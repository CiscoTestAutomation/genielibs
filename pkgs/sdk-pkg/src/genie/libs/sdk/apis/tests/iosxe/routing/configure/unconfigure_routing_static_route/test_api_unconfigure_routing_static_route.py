from unittest import TestCase
from genie.libs.sdk.apis.iosxe.routing.configure import unconfigure_routing_static_route
from unittest.mock import Mock


class TestUnconfigureRoutingStaticRoute(TestCase):

    def test_unconfigure_routing_static_route(self):
        self.device = Mock()
        result = unconfigure_routing_static_route(self.device, '0.0.0.0', '0.0.0.0', 'WAN_VRF', None, '17.17.17.1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip route vrf WAN_VRF 0.0.0.0 0.0.0.0 17.17.17.1'],)
        )
