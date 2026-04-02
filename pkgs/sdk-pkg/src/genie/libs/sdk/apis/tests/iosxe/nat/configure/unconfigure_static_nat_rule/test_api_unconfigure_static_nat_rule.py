from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_rule

class TestUnconfigureStaticNatRule(TestCase):

    def test_unconfigure_static_nat_rule(self):
        device = Mock()
        result = unconfigure_static_nat_rule(device, '193.168.0.2', '10.10.10.1', 'tcp', 22, 22, True, 'VRF2', True)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source static tcp 193.168.0.2 22 10.10.10.1 22 vrf VRF2 extendable no-alias',)
        )

    def test_unconfigure_static_nat_rule_1(self):
        device = Mock()
        result = unconfigure_static_nat_rule(device, '193.168.0.2', '10.10.10.1', None, None, None, True, 'VRF2', True)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source static 193.168.0.2 10.10.10.1 vrf VRF2 extendable no-alias',)
        )

    def test_unconfigure_static_nat_rule_2(self):
        device = Mock()
        result = unconfigure_static_nat_rule(device, '193.168.0.2', '10.10.10.1', 'tcp', 22, 22, False, None, False)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source static tcp 193.168.0.2 22 10.10.10.1 22',)
        )