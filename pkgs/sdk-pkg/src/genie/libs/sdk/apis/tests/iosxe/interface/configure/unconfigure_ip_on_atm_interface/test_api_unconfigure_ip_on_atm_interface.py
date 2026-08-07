import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_ip_on_atm_interface,
)


class TestUnconfigureIpOnAtmInterface(TestCase):

    def test_unconfigure_ip_on_atm_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_on_atm_interface(
            device,
            "ATM0/2/0",
            "10/100",
            "10",
            "10.10.11.11",
            "255.255.255.0",
            "5000::1/64",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface ATM0/2/0.10 point-to-point",
            sent_commands,
        )
        self.assertIn(
            "no pvc 10/100",
            sent_commands,
        )
        self.assertIn(
            "no ip address 10.10.11.11 255.255.255.0",
            sent_commands,
        )
        self.assertIn(
            "no ipv6 address 5000::1/64",
            sent_commands,
        )
        self.assertIn(
            "no ipv6 enable",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()