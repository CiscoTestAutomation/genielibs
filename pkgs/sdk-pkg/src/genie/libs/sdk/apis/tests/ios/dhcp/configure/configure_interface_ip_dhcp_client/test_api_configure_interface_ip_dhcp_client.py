from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.dhcp.configure import (
    configure_interface_ip_dhcp_client,
)


class TestConfigureInterfaceIpDhcpClient(TestCase):

    def test_configure_interface_ip_dhcp_client_broadcast_flag(self):
        device = Mock()
        configure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "broadcast-flag", "clear"
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "ip dhcp client broadcast-flag clear",
            ]
        )

    def test_configure_interface_ip_dhcp_client_client_id(self):
        device = Mock()
        configure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "client-id", "ascii", tag="myhost"
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "ip dhcp client client-id ascii",
                "ip dhcp client client-id ascii myhost",
            ]
        )

    def test_configure_interface_ip_dhcp_client_update_dns(self):
        device = Mock()
        configure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "dns", "server", tag="both", is_update=True
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "ip dhcp client dns server",
                "ip dhcp client update dns server both",
            ]
        )

    def test_configure_interface_ip_dhcp_client_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("cli error")
        with self.assertRaises(SubCommandFailure):
            configure_interface_ip_dhcp_client(
                device, "GigabitEthernet0/0", "broadcast-flag", "clear"
            )
