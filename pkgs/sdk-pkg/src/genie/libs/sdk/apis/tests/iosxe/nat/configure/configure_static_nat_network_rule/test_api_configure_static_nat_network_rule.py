from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_static_nat_network_rule

class TestConfigureStaticNatNetworkRule(TestCase):

    def test_configure_static_nat_network_rule(self):
        device = Mock()
        result = configure_static_nat_network_rule(device, '35.0.0.0', '81.1.1.0', '255.255.255.0')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip nat inside source static network 35.0.0.0 81.1.1.0 255.255.255.0',)
        )