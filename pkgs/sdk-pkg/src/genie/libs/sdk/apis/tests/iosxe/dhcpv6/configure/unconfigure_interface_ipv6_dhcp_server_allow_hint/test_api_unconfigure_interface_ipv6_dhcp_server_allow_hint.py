from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_interface_ipv6_dhcp_server_allow_hint
from unittest.mock import Mock


class TestUnconfigureInterfaceIpv6DhcpServerAllowHint(TestCase):

    def test_unconfigure_interface_ipv6_dhcp_server_allow_hint(self):
        self.device = Mock()
        result = unconfigure_interface_ipv6_dhcp_server_allow_hint(self.device, 'GigabitEthernet0/0/1', 'test')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/1', 'no ipv6 dhcp server test allow-hint'],)
        )
