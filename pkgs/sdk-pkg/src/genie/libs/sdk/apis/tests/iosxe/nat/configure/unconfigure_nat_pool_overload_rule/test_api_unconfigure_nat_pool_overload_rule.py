from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_pool_overload_rule

class TestUnconfigureNatPoolOverloadRule(TestCase):

    def test_unconfigure_nat_pool_overload_rule(self):
        device = Mock()
        result = unconfigure_nat_pool_overload_rule(device, 'acl1', 'pool1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ip nat inside source list acl1 pool pool1 overload'],)
        )