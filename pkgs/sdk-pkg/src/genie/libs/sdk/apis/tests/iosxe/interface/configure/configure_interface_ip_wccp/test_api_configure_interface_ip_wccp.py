import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_wccp


class TestConfigureInterfaceIpWccp(TestCase):

    def test_configure_interface_ip_wccp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_wccp(
            device,
            "Tw1/0/10",
            100,
            "in",
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tw1/0/10", sent_commands)
        self.assertIn("no switchport", sent_commands)
        self.assertIn("ip wccp 100 redirect in", sent_commands)
        self.assertIn("ip wccp 100 group-listen", sent_commands)

    def test_configure_interface_ip_wccp_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_wccp(
            device,
            "Tw1/0/10",
            90,
            "out",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tw1/0/10", sent_commands)
        self.assertIn("ip wccp 90 redirect out", sent_commands)

    def test_configure_interface_ip_wccp_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_wccp(
            device,
            "Tw1/0/10",
            90,
            None,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Tw1/0/10", sent_commands)
        self.assertIn("no switchport", sent_commands)
        self.assertIn("ip wccp 90 group-listen", sent_commands)


if __name__ == "__main__":
    unittest.main()