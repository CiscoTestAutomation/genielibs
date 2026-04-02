from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_dynamic_nat_rule

class TestUnconfigureDynamicNatRule(TestCase):

    def test_unconfigure_dynamic_nat_rule(self):
        device = Mock()
        result = unconfigure_dynamic_nat_rule(device, 'acl_n', 'pool_n')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat inside source list acl_n pool pool_n'],)
        )