import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_verify_unicast_notification


class TestConfigureInterfaceIpVerifyUnicastNotification(TestCase):

    def test_configure_interface_ip_verify_unicast_notification(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_verify_unicast_notification(
            device,
            "te1/0/5",
            1,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface te1/0/5", sent_commands)
        self.assertIn("no switchport", sent_commands)
        self.assertIn(
            "ip verify unicast notification threshold 1",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()