from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_dhcp_relay_information_option_insert
from unittest.mock import Mock


class TestConfigureInterfaceIpDhcpRelayInformationOptionInsert(TestCase):

    def test_configure_interface_ip_dhcp_relay_information_option_insert(self):
        self.device = Mock()
        result = configure_interface_ip_dhcp_relay_information_option_insert(self.device, 'GigabitEthernet1/0/8')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/8', 'ip dhcp relay information option-insert'],)
        )
