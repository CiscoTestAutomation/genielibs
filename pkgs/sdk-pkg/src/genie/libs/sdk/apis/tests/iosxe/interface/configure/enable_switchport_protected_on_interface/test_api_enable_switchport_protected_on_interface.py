import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import enable_switchport_protected_on_interface


class TestEnableSwitchportProtectedOnInterface(TestCase):

    def test_enable_switchport_protected_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = enable_switchport_protected_on_interface(
            device,
            "GigabitEthernet1/0/2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/2",
                "switchport protected",
            ],
        )


if __name__ == "__main__":
    unittest.main()