import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import no_shut_sub_interface_range


class TestNoShutSubInterfaceRange(TestCase):

    def test_no_shut_sub_interface_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = no_shut_sub_interface_range(
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
                "no shut",
            ],
        )


if __name__ == "__main__":
    unittest.main()