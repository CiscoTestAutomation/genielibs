import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_port_channel_standalone_disable,
)

class TestUnconfigurePortChannelStandaloneDisable(TestCase):

    def test_unconfigure_port_channel_standalone_disable(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_port_channel_standalone_disable(
            device,
            "15",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Port-channel 15",
            sent_commands,
        )
        self.assertIn(
            "port-channel standalone-disable",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()