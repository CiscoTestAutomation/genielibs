from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.dhcp.configure import (
    unconfigure_interface_ip_dhcp_client,
)


class TestUnconfigureInterfaceIpDhcpClient(TestCase):

    def test_unconfigure_interface_ip_dhcp_client_broadcast_flag(self):
        device = Mock()
        unconfigure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "broadcast-flag", "clear"
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "no ip dhcp client broadcast-flag clear",
            ]
        )

    def test_unconfigure_interface_ip_dhcp_client_client_id(self):
        device = Mock()
        unconfigure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "client-id", "ascii", tag="myhost"
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "no ip dhcp client client-id ascii",
                "no ip dhcp client client-id ascii myhost",
            ]
        )

    def test_unconfigure_interface_ip_dhcp_client_update_dns(self):
        device = Mock()
        unconfigure_interface_ip_dhcp_client(
            device, "GigabitEthernet0/0", "dns", "server", tag="both", is_update=True
        )
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                "no ip dhcp client dns server",
                "no ip dhcp client update dns server both",
            ]
        )

    def test_unconfigure_interface_ip_dhcp_client_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("cli error")
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_ip_dhcp_client(
                device, "GigabitEthernet0/0", "broadcast-flag", "clear"
            )
