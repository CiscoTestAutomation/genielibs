import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.icmp.configure import unconfigure_icmp_ip_reachables


class TestUnconfigureIcmpIpReachables(TestCase):

    def test_unconfigure_icmp_ip_reachables(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_icmp_ip_reachables(
            device,
            "Te1/0/10",
            "connected to interface",
            "50.1.1.2",
            "255.255.0.0",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Te1/0/10", sent_commands)
        self.assertIn("description connected to interface", sent_commands)
        self.assertIn("ip address 50.1.1.2 255.255.0.0", sent_commands)
        self.assertIn("no ip unreachables", sent_commands)
        self.assertIn("no switchport", sent_commands)


if __name__ == "__main__":
    unittest.main()