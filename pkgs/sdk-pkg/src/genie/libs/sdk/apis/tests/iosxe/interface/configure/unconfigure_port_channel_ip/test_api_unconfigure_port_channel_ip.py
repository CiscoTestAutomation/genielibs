import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_port_channel_ip


class TestUnconfigurePortChannelIp(TestCase):

    def test_unconfigure_port_channel_ip(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_port_channel_ip(
            device,
            5,
            "ip",
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Port-channel 5",
            sent_commands,
        )
        self.assertIn(
            "no ip address",
            sent_commands,
        )
        self.assertIn(
            "shutdown",
            sent_commands,
        )

    def test_unconfigure_port_channel_ip_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_port_channel_ip(
            device,
            5,
            "ip",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Port-channel 5",
            sent_commands,
        )
        self.assertIn(
            "no ip address",
            sent_commands,
        )
        self.assertNotIn(
            "shutdown",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()