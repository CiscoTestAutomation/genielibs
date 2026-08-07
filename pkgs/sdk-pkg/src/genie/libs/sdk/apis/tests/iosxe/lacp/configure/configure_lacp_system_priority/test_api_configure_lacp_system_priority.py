import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.lacp.configure import (
    configure_lacp_system_priority,
)


class TestConfigureLacpSystemPriority(TestCase):

    def test_configure_lacp_system_priority(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_lacp_system_priority(
            device,
            100,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "lacp system-priority 100",
        )


if __name__ == "__main__":
    unittest.main()
