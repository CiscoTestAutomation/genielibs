import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import (
    unconfigure_lacp_system_priority,
)


class TestUnconfigureLacpSystemPriority(TestCase):

    def test_unconfigure_lacp_system_priority(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_lacp_system_priority(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "no lacp system-priority",
        )


if __name__ == "__main__":
    unittest.main()
