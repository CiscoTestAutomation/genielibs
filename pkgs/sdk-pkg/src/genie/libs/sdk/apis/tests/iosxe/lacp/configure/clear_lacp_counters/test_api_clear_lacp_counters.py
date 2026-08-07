import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import clear_lacp_counters


class TestClearLacpCounters(TestCase):

    def test_clear_lacp_counters(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_lacp_counters(
            device,
            1,
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "clear lacp 1 counters",
        )

    def test_clear_lacp_counters_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.execute.return_value = None

        result = clear_lacp_counters(
            device,
            None,
        )

        self.assertIsNone(result)
        device.execute.assert_called_once()

        sent_command = device.execute.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "clear lacp counters",
        )


if __name__ == "__main__":
    unittest.main()
