import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_tunnel_with_ipsec


class TestConfigureTunnelWithIpsec(TestCase):

    def test_configure_tunnel_with_ipsec(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_tunnel_with_ipsec(
            device,
            "Tunnel1",
            "ipv4",
            "1.1.1.1",
            "255.255.255.255",
            "Te0/0/2",
            "17.17.17.2",
            None,
            None,
            "1::1",
            128,
            "gre",
            "ipsec",
            "IPSEC_PROFILE",
            None,
            None,
            None,
            1,
            True,
            "virtual-template 1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tunnel1",
                "ip address 1.1.1.1 255.255.255.255",
                "ipv6 enable",
                "ipv6 address 1::1/128",
                "tunnel mode gre ip",
                "tunnel source Te0/0/2",
                "tunnel destination 17.17.17.2",
                "tunnel protection ipsec profile IPSEC_PROFILE",
                "ip nhrp network-id 1",
                "ip nhrp redirect",
                "ip nhrp shortcut virtual-template 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()