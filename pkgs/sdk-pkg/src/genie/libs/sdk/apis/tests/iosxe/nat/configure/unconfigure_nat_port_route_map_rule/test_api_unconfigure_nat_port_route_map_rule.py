from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_port_route_map_rule

class TestUnconfigureNatPortRouteMapRule(TestCase):

    def test_unconfigure_nat_port_route_map_rule(self):
        device = Mock()
        result = unconfigure_nat_port_route_map_rule(
            device, 'tcp', '11.12.13.14', 23, '11.12.14.30', 23, 'static_rm'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat inside source static tcp 11.12.13.14 23 11.12.14.30 23 route-map static_rm'],)
        )