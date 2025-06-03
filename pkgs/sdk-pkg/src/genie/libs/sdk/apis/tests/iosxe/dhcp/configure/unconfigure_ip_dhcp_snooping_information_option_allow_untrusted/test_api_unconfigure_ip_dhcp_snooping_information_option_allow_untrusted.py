from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_information_option_allow_untrusted
from unittest.mock import Mock

class TestUnconfigureIpDhcpSnoopingInformationOptionAllowUntrusted(TestCase):
    def test_unconfigure_ip_dhcp_snooping_information_option_allow_untrusted(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_information_option_allow_untrusted(self.device, 'Port-channel 93')
        self.assertEqual(
        self.device.configure.mock_calls[0].args,
        (['interface Port-channel 93','no ip dhcp snooping information option allow-untrusted'],))
