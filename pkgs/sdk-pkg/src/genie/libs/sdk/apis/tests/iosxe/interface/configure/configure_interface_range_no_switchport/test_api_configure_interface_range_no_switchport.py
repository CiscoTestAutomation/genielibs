import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_range_no_switchport


class TestConfigureInterfaceRangeNoSwitchport(TestCase):

    def test_configure_interface_range_no_switchport(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_range_no_switchport(
            device,
            "Gi1/0/38",
            "41",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface range Gi1/0/38 - 41",
            sent_commands,
        )
        self.assertIn("no switchport", sent_commands)


if __name__ == "__main__":
    unittest.main()