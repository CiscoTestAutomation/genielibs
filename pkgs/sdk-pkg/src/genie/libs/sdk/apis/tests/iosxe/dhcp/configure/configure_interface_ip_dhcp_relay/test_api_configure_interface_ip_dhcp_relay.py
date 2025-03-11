from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_ip_dhcp_relay
from unittest.mock import Mock


class TestConfigureInterfaceIpDhcpRelay(TestCase):

    def test_configure_interface_ip_dhcp_relay(self):
        self.device = Mock()
        result = configure_interface_ip_dhcp_relay(self.device, 'GigabitEthernet0/0', 'option', 'subscriber-id', 'abc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0', 'ip dhcp relay information option subscriber-id abc'],)
        )
