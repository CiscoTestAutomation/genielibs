import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ip_unnumbered_on_interface,
)


class TestConfigureIpUnnumberedOnInterface(TestCase):

    def test_configure_ip_unnumbered_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_unnumbered_on_interface(
            device,
            "Vlan200",
            "Loopback0",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Vlan200", sent_commands)
        self.assertIn("ip unnumbered Loopback0", sent_commands)

    def test_configure_ipv6_unnumbered_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_unnumbered_on_interface(
            device,
            "Vlan200",
            "Loopback0",
            ipv6=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Vlan200", sent_commands)
        self.assertIn("ipv6 unnumbered Loopback0", sent_commands)


if __name__ == "__main__":
    unittest.main()