import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ipv6_address_on_hsrp_interface,
)


class TestConfigureIpv6AddressOnHsrpInterface(TestCase):

    def test_configure_ipv6_address_on_hsrp_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_address_on_hsrp_interface(
            device,
            "Vlan600",
            3,
            2,
            "2001:db8:10::100/64",
            "100",
            "10",
            "10",
            "20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Vlan600", sent_commands)
        self.assertIn("standby version 2", sent_commands)
        self.assertIn("standby 3 ipv6 2001:db8:10::100/64", sent_commands)
        self.assertIn("standby 3  priority 100", sent_commands)
        self.assertIn("standby 3  preempt delay sync 10", sent_commands)
        self.assertIn("standby 3 timers 10 20", sent_commands)


if __name__ == "__main__":
    unittest.main()