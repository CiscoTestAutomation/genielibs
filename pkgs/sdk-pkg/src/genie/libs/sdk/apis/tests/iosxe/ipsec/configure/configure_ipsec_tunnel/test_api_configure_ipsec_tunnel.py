import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_tunnel


class TestConfigureIpsecTunnel(TestCase):

    def test_configure_ipsec_tunnel(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipsec_tunnel(
            device,
            "Tunnel1",
            "200.2.0.2",
            "255.255.255.0",
            "2001::99:2:4:2",
            "ipv6",
            "2001::99:6:8:8",
            "gre_profile",
            False,
            None,
            None,
            "2001::200:2:8:2/112",
            "pe1_pe3_tunnel",
            "gre",
            "True",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Tunnel1",
                "description pe1_pe3_tunnel",
                "ip address 200.2.0.2 255.255.255.0",
                "ipv6 address 2001::200:2:8:2/112",
                "tunnel mode gre ipv6",
                "tunnel source 2001::99:2:4:2",
                "tunnel destination 2001::99:6:8:8",
                "tunnel protection ipsec profile gre_profile",
                "tunnel path-mtu-discovery",
            ],
        )


if __name__ == "__main__":
    unittest.main()