from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_network_rule

class TestUnconfigureStaticNatNetworkRule(TestCase):

    def test_unconfigure_static_nat_network_rule(self):
        device = Mock()
        result = unconfigure_static_nat_network_rule(device, '35.0.0.0', '81.1.1.0', '255.255.255.0')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip nat inside source static network 35.0.0.0 81.1.1.0 255.255.255.0',)
        )