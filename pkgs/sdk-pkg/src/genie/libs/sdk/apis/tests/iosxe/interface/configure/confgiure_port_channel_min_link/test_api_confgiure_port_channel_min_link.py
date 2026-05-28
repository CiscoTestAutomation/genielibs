import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    confgiure_port_channel_min_link,
)


class TestConfgiurePortChannelMinLink(TestCase):

    def test_confgiure_port_channel_min_link(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = confgiure_port_channel_min_link(device, "1", 4)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface port-channel 1", sent_commands)
        self.assertIn("port-channel min-links 4", sent_commands)


if __name__ == "__main__":
    unittest.main()