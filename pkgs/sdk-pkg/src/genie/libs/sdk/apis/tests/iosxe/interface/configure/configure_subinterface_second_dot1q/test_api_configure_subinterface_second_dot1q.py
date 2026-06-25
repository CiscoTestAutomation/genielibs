import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_subinterface_second_dot1q


class TestConfigureSubinterfaceSecondDot1q(TestCase):

    def test_configure_subinterface_second_dot1q(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_subinterface_second_dot1q(
            device,
            "GigabitEthernet0/0/0",
            "2",
            "20",
            "30",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/0/0.2",
                "encapsulation dot1q 20 second-dot1q 30",
            ],
        )


if __name__ == "__main__":
    unittest.main()