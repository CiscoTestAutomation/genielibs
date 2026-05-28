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
                    "erspan_id": 301,
                    "ip_address": "30.1.1.2",
                    "mtu": 344,
                    "origin_ip_address": "30.1.1.1",
                    "session_name": 3,
                    "session_type": "erspan-source",
                    "vlan_id": "100 rx",
                    "vrf": "red",
                }
            ],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertIn("monitor session 3 type erspan-source", sent_commands)
        self.assertIn("source vlan 100 rx", sent_commands)
        self.assertIn("destination", sent_commands)
        self.assertIn("erspan-id 301", sent_commands)
        self.assertIn("ip address 30.1.1.2", sent_commands)
        self.assertIn("origin ip address 30.1.1.1", sent_commands)
        self.assertIn("mtu 344", sent_commands)
        self.assertIn("vrf red", sent_commands)
        self.assertIn("no shutdown", sent_commands)


if __name__ == "__main__":
    unittest.main()