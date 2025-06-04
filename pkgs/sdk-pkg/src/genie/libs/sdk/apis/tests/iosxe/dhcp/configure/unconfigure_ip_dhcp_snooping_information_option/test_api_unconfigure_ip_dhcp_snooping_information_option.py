from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_ip_dhcp_snooping_information_option
from unittest.mock import Mock


class TestUnconfigureIpDhcpSnoopingInformationOption(TestCase):
    def test_unconfigure_ip_dhcp_snooping_information_option(self):
        self.device = Mock()
        unconfigure_ip_dhcp_snooping_information_option(self.device)
        self.assertEqual(
        self.device.configure.mock_calls[0].args,
        ('no ip dhcp snooping information option',))
