import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import disable_switchport_trunk_on_interface


class TestDisableSwitchportTrunkOnInterface(TestCase):

    def test_disable_switchport_trunk_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = disable_switchport_trunk_on_interface(
            device,
            "TwentyFiveGigE1/0/37",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/37",
                "no switchport mode trunk",
            ],
        )


if __name__ == "__main__":
    unittest.main()