from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ipv6_dhcp_client_pd_on_interface
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpClientPdOnInterface(TestCase):

    def test_unconfigure_ipv6_dhcp_client_pd_on_interface(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_client_pd_on_interface(self.device, 'GigabitEthernet0/0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0/0/0', 'no ipv6 dhcp client pd'],)
        )
