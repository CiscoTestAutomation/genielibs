from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_static_nat_route_map_no_alias_rule

class TestConfigureStaticNatRouteMapNoAliasRule(TestCase):

    def test_configure_static_nat_route_map_no_alias_rule(self):
        device = Mock()
        result = configure_static_nat_route_map_no_alias_rule(
            device, 'inside', '192.168.1.10', '192.168.21.1', False
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat inside source static 192.168.1.10 192.168.21.1 no-alias'],)
        )

    def test_configure_static_nat_route_map_no_alias_rule_1(self):
        device = Mock()
        result = configure_static_nat_route_map_no_alias_rule(
            device, 'outside', '3.3.33.3', '5.5.5.5', True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat outside source static 5.5.5.5 3.3.33.3 no-alias add-route'],)
        )