import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_monitor_session


class TestConfigureInterfaceMonitorSession(TestCase):

    def test_configure_interface_monitor_session(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_monitor_session(
            device,
            [
                {
                    "erspan_id": 1001,
                    "interface": "Fif2/0/1 rx",
                    "ipv6_address": "2004::2",
                    "origin_ipv6_address": "2040::1",
                    "session_name": 2,
                    "session_type": "erspan-source",
                }
            ],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("monitor session 2 type erspan-source", sent_commands)
        self.assertIn("source interface Fif2/0/1 rx", sent_commands)
        self.assertIn("destination", sent_commands)
        self.assertIn("erspan-id 1001", sent_commands)
        self.assertIn("ipv6 address 2004::2", sent_commands)
        self.assertIn("origin ipv6 address 2040::1", sent_commands)
        self.assertIn("exit", sent_commands)
        self.assertIn("no shutdown", sent_commands)


if __name__ == "__main__":
    unittest.main()