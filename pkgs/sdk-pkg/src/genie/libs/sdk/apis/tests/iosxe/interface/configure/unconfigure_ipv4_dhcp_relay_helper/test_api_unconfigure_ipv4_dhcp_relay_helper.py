import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_ipv4_dhcp_relay_helper,
)


class TestUnconfigureIpv4DhcpRelayHelper(TestCase):

    def test_unconfigure_ipv4_dhcp_relay_helper(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipv4_dhcp_relay_helper(
            device,
            "Vlan110",
            "4.4.4.4",
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
            "no ip helper-address 4.4.4.4",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()