from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_verify_mac_address
from unittest.mock import Mock

class TestUnconfigureIpDhcpSnoopingVerifyMacAddress(TestCase):

    def test_unconfigure_ip_dhcp_snooping_verify_mac_address(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_verify_mac_address(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip dhcp snooping verify mac-address',)
        )
        
