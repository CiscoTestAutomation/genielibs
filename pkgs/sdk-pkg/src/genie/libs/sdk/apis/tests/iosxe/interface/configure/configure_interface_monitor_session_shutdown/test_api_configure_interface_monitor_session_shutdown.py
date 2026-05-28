import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session_shutdown


class TestConfigureInterfaceMonitorSessionShutdown(TestCase):

    def test_configure_interface_monitor_session_shutdown(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_monitor_session_shutdown(
            device,
            [
                {
                    "erspan_id": 1,
                    "interface": "TwentyFiveGigE2/1/1",
                    "ip_address": "4.4.4.2",
                    "origin_ip_address": "5.5.5.5",
                    "session_name": 1,
                    "session_type": "erspan-source",
                }
            ],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("monitor session 1 type erspan-source", sent_commands)
        self.assertIn("source interface TwentyFiveGigE2/1/1", sent_commands)
        self.assertIn("destination", sent_commands)
        self.assertIn("erspan-id 1", sent_commands)
        self.assertIn("ip address 4.4.4.2", sent_commands)
        self.assertIn("origin ip address 5.5.5.5", sent_commands)
        self.assertIn("exit", sent_commands)
        self.assertIn("no shutdown", sent_commands)


if __name__ == "__main__":
    unittest.main()