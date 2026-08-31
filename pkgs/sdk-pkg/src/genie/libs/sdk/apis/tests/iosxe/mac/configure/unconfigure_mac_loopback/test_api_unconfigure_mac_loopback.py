import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    unconfigure_mac_loopback,
)


class TestUnconfigureMacLoopback(TestCase):

    def test_unconfigure_mac_loopback(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_mac_loopback(
            device,
            "TenGigabitEthernet0/1/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TenGigabitEthernet0/1/1",
                "no loopback mac",
            ],
        )


if __name__ == "__main__":
    unittest.main()
