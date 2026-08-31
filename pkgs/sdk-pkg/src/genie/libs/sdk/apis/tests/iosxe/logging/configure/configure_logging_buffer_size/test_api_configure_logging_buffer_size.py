import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    configure_logging_buffer_size,
)


class TestConfigureLoggingBufferSize(TestCase):

    def test_configure_logging_buffer_size(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_logging_buffer_size(
            device,
            2147483647,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "logging buffered 2147483647",
        )

    def test_configure_logging_buffer_size_with_severity(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_logging_buffer_size(
            device,
            1000000,
            "debugging",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "logging buffered 1000000 debugging",
        )


if __name__ == "__main__":
    unittest.main()
