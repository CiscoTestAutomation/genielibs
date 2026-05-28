import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_macro_auto_port_sticky


class TestConfigureInterfaceMacroAutoPortSticky(TestCase):

    def test_configure_interface_macro_auto_port_sticky(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_macro_auto_port_sticky(
            device,
            "te1/0/6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface te1/0/6", sent_commands)
        self.assertIn("macro auto port sticky", sent_commands)


if __name__ == "__main__":
    unittest.main()