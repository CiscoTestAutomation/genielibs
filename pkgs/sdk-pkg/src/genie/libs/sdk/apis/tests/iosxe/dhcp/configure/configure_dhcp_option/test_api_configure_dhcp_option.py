from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_option
from unittest.mock import Mock


class TestConfigureDhcpOption(TestCase):

    def test_configure_dhcp_option(self):
        self.device = Mock()
        result = configure_dhcp_option(self.device, 'test_pool', 'ascii', '60', 'ArubaAP')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp pool test_pool', 'option 60 ascii ArubaAP'],)
        )
