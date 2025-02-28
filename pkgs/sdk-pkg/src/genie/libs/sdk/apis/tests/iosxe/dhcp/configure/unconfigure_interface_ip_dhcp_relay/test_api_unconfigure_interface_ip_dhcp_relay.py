from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_ip_dhcp_relay
from unittest.mock import Mock


class TestUnconfigureInterfaceIpDhcpRelay(TestCase):

    def test_unconfigure_interface_ip_dhcp_relay(self):
        self.device = Mock()
        result = unconfigure_interface_ip_dhcp_relay(self.device, 'GigabitEthernet0/0', 'option', 'subscriber-id', 'abc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0', 'no ip dhcp relay information option subscriber-id abc'],)
        )
