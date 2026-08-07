import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import (
    configure_port_channel_mode,
)


class TestConfigurePortChannelMode(TestCase):

    def test_configure_port_channel_mode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_port_channel_mode(
            device,
            "load-balance",
            "dst-mac",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "port-channel load-balance dst-mac",
            ],
        )


if __name__ == "__main__":
    unittest.main()
