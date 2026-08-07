import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_profile_on_tunnel_interface,
)


class TestUnconfigureProfileOnTunnelInterface(TestCase):

    def test_unconfigure_profile_on_tunnel_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_profile_on_tunnel_interface(
            device,
            "Tunnel1",
            "ipsec",
            "P1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface Tunnel1",
            sent_commands,
        )
        self.assertIn(
            "no tunnel protection ipsec profile P1",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()