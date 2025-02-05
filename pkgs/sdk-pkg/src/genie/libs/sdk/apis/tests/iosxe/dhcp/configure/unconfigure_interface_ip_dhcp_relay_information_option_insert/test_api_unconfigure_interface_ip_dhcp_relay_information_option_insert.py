from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_relay_information_option_insert
from unittest.mock import Mock


class TestUnconfigureInterfaceIpDhcpRelayInformationOptionInsert(TestCase):

    def test_unconfigure_interface_ip_dhcp_relay_information_option_insert(self):
        self.device = Mock()
        result = unconfigure_interface_ip_dhcp_relay_information_option_insert(self.device, 'GigabitEthernet1/0/8')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'no ip dhcp relay information option-insert'],)
        )
