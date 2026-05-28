from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.interface.configure import configure_ipv6_dhcp_client_pd_on_interface


class TestConfigureIpv6DhcpClientPdOnInterface(TestCase):

    def test_configure_ipv6_dhcp_client_pd_on_interface(self):
        self.device = Mock()
        configure_ipv6_dhcp_client_pd_on_interface(
            self.device, 'GigabitEthernet0/0', 'PREFIX1'
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ipv6 dhcp client pd PREFIX1",
            ]
        )

    def test_configure_ipv6_dhcp_client_pd_on_interface_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ipv6_dhcp_client_pd_on_interface(
                self.device, 'GigabitEthernet0/0', 'PREFIX1'
            )
