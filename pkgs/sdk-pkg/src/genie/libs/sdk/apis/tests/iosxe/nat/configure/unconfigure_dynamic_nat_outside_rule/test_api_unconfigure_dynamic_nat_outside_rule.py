from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_dynamic_nat_outside_rule

class TestUnconfigureDynamicNatOutsideRule(TestCase):

    def test_unconfigure_dynamic_nat_outside_rule(self):
        device = Mock()
        result = unconfigure_dynamic_nat_outside_rule(device, 'acl_1', 'pool_1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat outside source list acl_1 pool pool_1 add-route'],)
        )