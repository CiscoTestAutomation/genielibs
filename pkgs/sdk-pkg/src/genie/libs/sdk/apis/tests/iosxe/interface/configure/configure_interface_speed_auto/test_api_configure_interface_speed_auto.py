import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_speed_auto


class TestConfigureInterfaceSpeedAuto(TestCase):

    def test_configure_interface_speed_auto(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_speed_auto(
            device,
            "TenGigabitEthernet1/0/6",
            "10 100 1000 2500 5000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface TenGigabitEthernet1/0/6", sent_commands)
        self.assertIn(
            "speed auto 10 100 1000 2500 5000",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()