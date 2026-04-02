from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import force_unconfigure_static_nat_route_map_rule

class TestForceUnconfigureStaticNatRouteMapRule(TestCase):

    def test_force_unconfigure_static_nat_route_map_rule(self):
        device = Mock()
        result = force_unconfigure_static_nat_route_map_rule(device, '35.0.0.1', '135.0.0.1', 'rm1', 60)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat inside source static 35.0.0.1 135.0.0.1 route-map rm1'],)
        )