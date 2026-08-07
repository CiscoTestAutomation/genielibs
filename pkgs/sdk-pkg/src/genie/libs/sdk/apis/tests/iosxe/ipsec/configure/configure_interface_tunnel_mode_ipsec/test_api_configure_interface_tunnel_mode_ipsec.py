import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_interface_tunnel_mode_ipsec,
)


class TestConfigureInterfaceTunnelModeIpsec(TestCase):

    def test_configure_interface_tunnel_mode_ipsec(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_tunnel_mode_ipsec(
            device,
            "Gi1/0/10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gi1/0/10",
                "tunnel mode ipsec ipv4",
            ],
        )


if __name__ == "__main__":
    unittest.main()