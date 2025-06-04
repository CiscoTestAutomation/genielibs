from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_information_option_allow_untrusted_global
from unittest.mock import Mock


class TestUnconfigureIpDhcpSnoopingInformationOptionAllowUntrustedGlobal(TestCase):
    def test_unconfigure_ip_dhcp_snooping_information_option_allow_untrusted_global(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_information_option_allow_untrusted_global(self.device)
        self.assertEqual(
        self.device.configure.mock_calls[0].args,
        ('no ip dhcp snooping information option allow-untrusted',))
        
