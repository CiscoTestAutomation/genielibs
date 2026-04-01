from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_outside_static_nat_rule

class TestUnconfigureOutsideStaticNatRule(TestCase):

    def test_unconfigure_outside_static_nat_rule(self):
        device = Mock()
        result = unconfigure_outside_static_nat_rule(
            device, '2.2.2.2', '1.1.1.1', 'tcp', 650, 860, False, None, False, True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat outside source static tcp 1.1.1.1 650 2.2.2.2 860 add-route',)
        )