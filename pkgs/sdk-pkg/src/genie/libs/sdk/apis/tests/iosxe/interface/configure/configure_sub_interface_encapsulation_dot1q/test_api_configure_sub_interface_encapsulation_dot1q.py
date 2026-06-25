import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_sub_interface_encapsulation_dot1q


class TestConfigureSubInterfaceEncapsulationDot1q(TestCase):

    def test_configure_sub_interface_encapsulation_dot1q(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_sub_interface_encapsulation_dot1q(
            device,
            "GigabitEthernet5/0/33",
            "2",
            "5.1.2.2",
            "255.255.255.0",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet5/0/33.2",
                "encapsulation dot1q 2",
                "ip address 5.1.2.2 255.255.255.0",
            ],
        )


if __name__ == "__main__":
    unittest.main()