import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_sub_interface_range


class TestConfigureSubInterfaceRange(TestCase):

    def test_configure_sub_interface_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_sub_interface_range(
            device,
            "GigabitEthernet5/0/33",
            2,
            129,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface range GigabitEthernet5/0/33.2 - GigabitEthernet5/0/33.129",
                "logging event subif-link-status",
                "no shut",
            ],
        )


if __name__ == "__main__":
    unittest.main()