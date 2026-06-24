import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_port_channel_lacp_max_bundle,
)


class TestConfigurePortChannelLacpMaxBundle(TestCase):

    def test_configure_port_channel_lacp_max_bundle(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_port_channel_lacp_max_bundle(
            device,
            "100",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Port-channel 100", sent_commands)
        self.assertIn("lacp max-bundle 1", sent_commands)


if __name__ == "__main__":
    unittest.main()