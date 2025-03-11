from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_drop_inform
from unittest.mock import Mock


class TestConfigureIpDhcpDropInform(TestCase):

    def test_configure_ip_dhcp_drop_inform(self):
        self.device = Mock()
        result = configure_ip_dhcp_drop_inform(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip dhcp drop-inform'],)
        )
