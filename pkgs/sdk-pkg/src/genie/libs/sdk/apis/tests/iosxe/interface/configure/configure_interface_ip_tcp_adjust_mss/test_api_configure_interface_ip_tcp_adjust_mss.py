import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_ip_tcp_adjust_mss,
)


class TestConfigureInterfaceIpTcpAdjustMss(TestCase):

    def test_configure_interface_ip_tcp_adjust_mss(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_tcp_adjust_mss(
            device,
            "Te1/0/7",
            "1400",
            "False",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Te1/0/7", sent_commands)
        self.assertIn("no switchport", sent_commands)
        self.assertIn("ip tcp adjust-mss 1400", sent_commands)


if __name__ == "__main__":
    unittest.main()