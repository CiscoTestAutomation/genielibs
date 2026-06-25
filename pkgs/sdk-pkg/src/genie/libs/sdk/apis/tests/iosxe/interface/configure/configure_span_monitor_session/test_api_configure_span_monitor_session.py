import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_span_monitor_session


class TestConfigureSpanMonitorSession(TestCase):

    def test_configure_span_monitor_session(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_span_monitor_session(
            device,
            "1",
            "FiftyGigE1/0/3",
            "both",
            "FiftyGigE1/0/9",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "monitor session 1  source interface FiftyGigE1/0/3 both",
                "monitor session 1  destination interface FiftyGigE1/0/9",
            ],
        )

    def test_configure_span_monitor_session_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_span_monitor_session(
            device,
            "10",
            None,
            None,
            None,
            "100",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "monitor session 10  source vlan 100",
            ],
        )


if __name__ == "__main__":
    unittest.main()