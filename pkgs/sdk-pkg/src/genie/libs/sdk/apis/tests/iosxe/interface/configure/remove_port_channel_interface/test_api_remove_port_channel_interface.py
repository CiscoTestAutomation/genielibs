import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import remove_port_channel_interface


class TestRemovePortChannelInterface(TestCase):

    def test_remove_port_channel_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = remove_port_channel_interface(
            device,
            23,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no interface Port-channel 23",
        )


if __name__ == "__main__":
    unittest.main()