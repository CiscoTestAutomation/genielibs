import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_verify_source


class TestConfigureInterfaceIpVerifySource(TestCase):

    def test_configure_interface_ip_verify_source(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ip_verify_source(
            device,
            "g1/0/4",
            "mac-chec",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface g1/0/4", sent_commands)
        self.assertIn("ip verify source mac-chec", sent_commands)


if __name__ == "__main__":
    unittest.main()