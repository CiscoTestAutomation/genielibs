import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_print_timestamp_for_show_command


class TestConfigurePrintTimestampForShowCommand(TestCase):

    def test_configure_print_timestamp_for_show_command(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_print_timestamp_for_show_command(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "line console 0",
                "exec prompt timestamp",
            ],
        )


if __name__ == "__main__":
    unittest.main()