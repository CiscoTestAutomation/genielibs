from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_dynamic_nat_outside_rule

class TestConfigureDynamicNatOutsideRule(TestCase):

    def test_configure_dynamic_nat_outside_rule(self):
        device = Mock()
        result = configure_dynamic_nat_outside_rule(device, 'acl_1', 'pool_1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat outside source list acl_1 pool pool_1 add-route'],)
        )