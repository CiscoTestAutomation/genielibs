import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unshut_port_channel


class TestUnshutPortChannel(TestCase):

    def test_unshut_port_channel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unshut_port_channel(
            device,
            "15",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Port-channel 15",
                "no shutdown",
            ],
        )


if __name__ == "__main__":
    unittest.main()