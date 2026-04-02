from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_outside_rule

class TestUnconfigureStaticNatOutsideRule(TestCase):

    def test_unconfigure_static_nat_outside_rule(self):
        device = Mock()
        result = unconfigure_static_nat_outside_rule(
            device, '193.168.128.2', '20.20.20.1', 'tcp', 34, 34, True, '255.255.0.0', True, True, 'VRF2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat outside source static tcp 193.168.128.2 34 20.20.20.1 34 vrf VRF2 extendable add-route',)
        )

    def test_unconfigure_static_nat_outside_rule_1(self):
        device = Mock()
        result = unconfigure_static_nat_outside_rule(
            device, '193.168.128.2', '20.20.20.1', None, None, None, False, None, True, True, 'VRF2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat outside source static 193.168.128.2 20.20.20.1 vrf VRF2 extendable add-route',)
        )

    def test_unconfigure_static_nat_outside_rule_2(self):
        device = Mock()
        result = unconfigure_static_nat_outside_rule(
            device, '193.168.128.2', '20.20.20.1', 'tcp', 34, 34, False, None, False, False, 'VRF2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat outside source static tcp 193.168.128.2 34 20.20.20.1 34 vrf VRF2',)
        )