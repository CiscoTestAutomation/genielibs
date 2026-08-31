import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    unconfigure_logging_buffered,
)


class TestUnconfigureLoggingBuffered(TestCase):

    def test_unconfigure_logging_buffered(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_logging_buffered(
            device,
            "alerts",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no logging buffered alerts",
        )


if __name__ == "__main__":
    unittest.main()
