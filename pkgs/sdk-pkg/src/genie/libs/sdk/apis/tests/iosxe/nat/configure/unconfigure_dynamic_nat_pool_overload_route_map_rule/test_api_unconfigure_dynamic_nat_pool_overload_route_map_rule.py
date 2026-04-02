from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_dynamic_nat_pool_overload_route_map_rule

class TestUnconfigureDynamicNatPoolOverloadRouteMapRule(TestCase):

    def test_unconfigure_dynamic_nat_pool_overload_route_map_rule(self):
        device = Mock()
        result = unconfigure_dynamic_nat_pool_overload_route_map_rule(device, 'static_rm', 'pool_b')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat inside source route-map static_rm pool pool_b overload'],)
        )