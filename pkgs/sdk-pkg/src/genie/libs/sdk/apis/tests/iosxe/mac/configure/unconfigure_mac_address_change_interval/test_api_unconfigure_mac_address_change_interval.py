import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_address_change_interval,
)


class TestUnconfigureMacAddressChangeInterval(TestCase):

    def test_unconfigure_mac_address_change_interval(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_address_change_interval(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "no mac-address notification change interval",
            ],
        )


if __name__ == "__main__":
    unittest.main()
