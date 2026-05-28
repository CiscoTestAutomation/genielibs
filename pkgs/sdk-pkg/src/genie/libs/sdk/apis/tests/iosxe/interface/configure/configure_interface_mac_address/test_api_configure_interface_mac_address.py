import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_mac_address


class TestConfigureInterfaceMacAddress(TestCase):

    def test_configure_interface_mac_address(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_mac_address(
            device=device,
            interface="ten1/0/7",
            mac="0000.1111.2222",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface ten1/0/7", sent_commands)
        self.assertIn("mac-address 0000.1111.2222", sent_commands)


if __name__ == "__main__":
    unittest.main()