import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.logging.configure import (
    configure_terminal_exec_prompt_timestamp,
)


class TestConfigureTerminalExecPromptTimestamp(TestCase):

    def test_configure_terminal_exec_prompt_timestamp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = configure_terminal_exec_prompt_timestamp(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "terminal exec prompt timestamp",
        )


if __name__ == "__main__":
    unittest.main()
