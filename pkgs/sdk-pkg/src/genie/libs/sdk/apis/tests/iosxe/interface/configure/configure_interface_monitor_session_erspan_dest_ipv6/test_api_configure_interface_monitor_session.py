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
                    "erspan_id": 101,
                    "interface": "Twe1/0/7",
                    "ipv6_address": "2040::1",
                    "session_name": 6,
                    "session_type": "erspan-destination",
                }
            ],
        )

        self.assertIsNone(result)
        self.assertEqual(device.configure.call_count, 2)

        interface_commands = device.configure.call_args_list[0].args[0]
        self.assertIsInstance(interface_commands, list)
        self.assertIn("interface Twe1/0/7", interface_commands)
        self.assertIn("no shutdown", interface_commands)

        monitor_commands = device.configure.call_args_list[1].args[0]
        self.assertIsInstance(monitor_commands, str)
        self.assertIn("monitor session 6 type erspan-destination", monitor_commands)
        self.assertIn("destination interface Twe1/0/7", monitor_commands)
        self.assertIn("source", monitor_commands)
        self.assertIn("erspan-id 101", monitor_commands)
        self.assertIn("ipv6 address 2040::1", monitor_commands)
        self.assertIn("exit", monitor_commands)
        self.assertIn("no shutdown", monitor_commands)


if __name__ == "__main__":
    unittest.main()