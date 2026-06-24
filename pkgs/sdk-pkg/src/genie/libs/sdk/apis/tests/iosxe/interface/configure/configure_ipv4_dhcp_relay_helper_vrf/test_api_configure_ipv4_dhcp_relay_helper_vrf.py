import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ipv4_dhcp_relay_helper_vrf,
)


class TestConfigureIpv4DhcpRelayHelperVrf(TestCase):

    def test_configure_ipv4_dhcp_relay_helper_vrf(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv4_dhcp_relay_helper_vrf(
            device,
            "Vlan100",
            "101.101.0.2",
            "RAGUARD",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Vlan100", sent_commands)
        self.assertIn(
            "ip helper-address vrf RAGUARD 101.101.0.2",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()