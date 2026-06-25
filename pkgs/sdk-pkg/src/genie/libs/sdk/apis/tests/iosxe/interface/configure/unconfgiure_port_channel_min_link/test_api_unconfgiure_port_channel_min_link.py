import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfgiure_port_channel_min_link


class TestUnconfgiurePortChannelMinLink(TestCase):

    def test_unconfgiure_port_channel_min_link(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfgiure_port_channel_min_link(
            device,
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface port-channel 1",
                "no port-channel min-links",
            ],
        )


if __name__ == "__main__":
    unittest.main()