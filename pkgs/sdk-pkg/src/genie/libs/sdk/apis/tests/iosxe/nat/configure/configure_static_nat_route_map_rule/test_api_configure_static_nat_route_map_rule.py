from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_static_nat_route_map_rule

class TestConfigureStaticNatRouteMapRule(TestCase):

    def test_configure_static_nat_route_map_rule(self):
        device = Mock()
        result = configure_static_nat_route_map_rule(device, '35.0.0.1', '135.0.0.1', 'rm_1', True)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source static 35.0.0.1 135.0.0.1 route-map rm_1 no-alias',)
        )