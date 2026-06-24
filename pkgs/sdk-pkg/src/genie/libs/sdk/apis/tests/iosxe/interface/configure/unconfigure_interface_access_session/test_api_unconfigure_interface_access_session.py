import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_access_session


class TestUnconfigureInterfaceAccessSession(TestCase):

    def test_unconfigure_interface_access_session(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_access_session(
            device,
            "GigabitEthernet1/0/3",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/3",
                "no access-session closed",
            ],
        )


if __name__ == "__main__":
    unittest.main()