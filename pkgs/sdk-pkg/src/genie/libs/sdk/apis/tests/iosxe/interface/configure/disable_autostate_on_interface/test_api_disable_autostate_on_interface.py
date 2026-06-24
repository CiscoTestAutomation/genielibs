import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import disable_autostate_on_interface


class TestDisableAutostateOnInterface(TestCase):

    def test_disable_autostate_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = disable_autostate_on_interface(
            device,
            "Vlan200",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Vlan200",
                "no autostate",
            ],
        )


if __name__ == "__main__":
    unittest.main()