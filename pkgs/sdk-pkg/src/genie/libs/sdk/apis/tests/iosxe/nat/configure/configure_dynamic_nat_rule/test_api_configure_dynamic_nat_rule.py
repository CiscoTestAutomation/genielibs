from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_dynamic_nat_rule

class TestConfigureDynamicNatRule(TestCase):

    def test_configure_dynamic_nat_rule(self):
        device = Mock()
        result = configure_dynamic_nat_rule(device, 'acl_n', 'pool_n')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ip nat inside source list acl_n pool pool_n'],)
        )