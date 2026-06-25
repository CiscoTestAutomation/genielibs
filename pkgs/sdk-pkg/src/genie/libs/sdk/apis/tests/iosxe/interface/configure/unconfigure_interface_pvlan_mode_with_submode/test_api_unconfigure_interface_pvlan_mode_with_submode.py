import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_pvlan_mode_with_submode


class TestUnconfigureInterfacePvlanModeWithSubmode(TestCase):

    def test_unconfigure_interface_pvlan_mode_with_submode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_pvlan_mode_with_submode(
            device,
            "TwentyFiveGigE1/0/31",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/31",
                "no switchport mode",
            ],
        )


if __name__ == "__main__":
    unittest.main()