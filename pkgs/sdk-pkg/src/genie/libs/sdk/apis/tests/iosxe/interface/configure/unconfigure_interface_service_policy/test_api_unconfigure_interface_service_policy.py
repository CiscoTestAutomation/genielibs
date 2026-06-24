import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_service_policy


class TestUnconfigureInterfaceServicePolicy(TestCase):

    def test_unconfigure_interface_service_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_service_policy(
            device,
            "GigabitEthernet1/0/1",
            "pm-tb1",
            "input",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/1",
                "no service-policy input pm-tb1",
            ],
        )


if __name__ == "__main__":
    unittest.main()