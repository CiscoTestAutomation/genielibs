from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_setting_gatekeeper_size
from unittest.mock import Mock


class TestConfigureNatSettingGatekeeperSize(TestCase):

    def test_configure_nat_setting_gatekeeper_size(self):
        self.device = Mock()
        result = configure_nat_setting_gatekeeper_size(self.device, '1024', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip nat settings gatekeeper-size 1024',)
        )
