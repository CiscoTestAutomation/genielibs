import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_ipv6_dhcp_relay,
)


class TestUnconfigureIpv6DhcpRelay(TestCase):

    def test_unconfigure_ipv6_dhcp_relay(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipv6_dhcp_relay(
            device,
            "Vlan110",
            "2001::2",
            "Vlan110",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Vlan110",
            sent_commands,
        )
        self.assertIn(
            "no ipv6 dhcp relay destination 2001::2 Vlan110",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()