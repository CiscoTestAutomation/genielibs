import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_macro_auto_port_sticky


class TestUnconfigureInterfaceMacroAutoPortSticky(TestCase):

    def test_unconfigure_interface_macro_auto_port_sticky(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_macro_auto_port_sticky(
            device,
            "te1/0/6",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface te1/0/6",
                "no macro auto port sticky",
            ],
        )


if __name__ == "__main__":
    unittest.main()