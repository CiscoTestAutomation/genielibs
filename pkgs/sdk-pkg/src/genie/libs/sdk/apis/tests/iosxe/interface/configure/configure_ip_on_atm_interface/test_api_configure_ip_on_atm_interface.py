import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ip_on_atm_interface,
)


class TestConfigureIpOnAtmInterface(TestCase):

    def test_configure_ip_on_atm_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_on_atm_interface(
            device,
            "ATM0/2/0",
            "10/100",
            "10",
            "10.10.11.11",
            "255.255.255.0",
            "5000::1/64",
            "aal5snap",
            "ppp",
            "1",
            "vbr-rt",
            500,
            "500",
            "1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface ATM0/2/0.10 point-to-point", sent_commands)
        self.assertIn("ip address 10.10.11.11 255.255.255.0", sent_commands)
        self.assertIn("ipv6 address 5000::1/64", sent_commands)
        self.assertIn("ipv6 enable", sent_commands)
        self.assertIn("pvc 10/100", sent_commands)
        self.assertIn("encapsulation aal5snap", sent_commands)
        self.assertIn("protocol ppp  dialer", sent_commands)
        self.assertIn("dialer pool-member 1", sent_commands)
        self.assertIn("vbr-rt 500 500 1", sent_commands)


if __name__ == "__main__":
    unittest.main()