import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import unconfigure_port_channel_mode


class TestUnconfigurePortChannelMode(TestCase):

    def test_unconfigure_port_channel_mode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_port_channel_mode(
            device,
            "load-balance",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no port-channel load-balance",
        )


if __name__ == "__main__":
    unittest.main()