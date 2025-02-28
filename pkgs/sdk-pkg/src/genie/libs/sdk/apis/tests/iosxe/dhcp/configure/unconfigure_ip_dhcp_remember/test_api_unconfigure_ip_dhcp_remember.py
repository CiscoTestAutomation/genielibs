from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_remember
from unittest.mock import Mock


class TestUnconfigureIpDhcpRemember(TestCase):

    def test_unconfigure_ip_dhcp_remember(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_remember(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp remember',)
        )
