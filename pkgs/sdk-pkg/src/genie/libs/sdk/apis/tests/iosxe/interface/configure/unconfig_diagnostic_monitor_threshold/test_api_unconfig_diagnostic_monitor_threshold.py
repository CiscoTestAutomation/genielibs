import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_diagnostic_monitor_threshold


class TestUnconfigDiagnosticMonitorThreshold(TestCase):

    def test_unconfig_diagnostic_monitor_threshold(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_diagnostic_monitor_threshold(
            device,
            2,
            6,
            4,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no diagnostic monitor threshold switch 2 test 6 failure count 4",
        )


if __name__ == "__main__":
    unittest.main()