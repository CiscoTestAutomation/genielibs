from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_ip_address_no_shutdown,
)


class TestConfigureInterfaceIpAddressNoShutdown(TestCase):

    def test_configure_interface_ip_address_no_shutdown(self):
        self.device = Mock()
        interface = 'GigabitEthernet1'
        ip_address = '192.168.1.1'
        mask = '255.255.255.0'

        configure_interface_ip_address_no_shutdown(
            self.device,
            interface=interface,
            ip_address=ip_address,
            mask=mask
        )

        expected_cmds = [
            f"interface {interface}",
            f"ip address {ip_address} {mask}",
            "no shutdown",
        ]
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_cmds,)
        )
