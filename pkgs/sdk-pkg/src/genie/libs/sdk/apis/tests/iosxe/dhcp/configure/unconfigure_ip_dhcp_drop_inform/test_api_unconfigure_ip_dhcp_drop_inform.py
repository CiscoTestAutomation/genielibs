from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_drop_inform
from unittest.mock import Mock


class TestUnconfigureIpDhcpDropInform(TestCase):

    def test_unconfigure_ip_dhcp_drop_inform(self):
        self.device = Mock()
        result = unconfigure_ip_dhcp_drop_inform(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ip dhcp drop-inform'],)
        )
