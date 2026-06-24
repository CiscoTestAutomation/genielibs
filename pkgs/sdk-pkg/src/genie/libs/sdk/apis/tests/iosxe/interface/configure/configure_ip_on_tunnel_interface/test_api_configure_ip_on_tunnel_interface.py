import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ip_on_tunnel_interface,
)


class TestConfigureIpOnTunnelInterface(TestCase):

    def test_configure_ip_on_tunnel_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_on_tunnel_interface(
            device,
            "Tunnel10",
            "41.1.1.1",
            "255.255.255.0",
            "42.1.1.1",
            "42.1.1.2",
            10,
            None,
            None,
            None,
            "gre",
            None,
            None,
            None,
            None,
            None,
            None,
            "ip",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tunnel10", sent_commands)
        self.assertIn("ip address 41.1.1.1 255.255.255.0", sent_commands)
        self.assertIn("tunnel mode gre ip", sent_commands)
        self.assertIn("tunnel source 42.1.1.1", sent_commands)
        self.assertIn("tunnel destination 42.1.1.2", sent_commands)
        self.assertIn("keepalive 10", sent_commands)


if __name__ == "__main__":
    unittest.main()