import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import disable_ipv6_dhcp_server


class TestDisableIpv6DhcpServer(TestCase):

    def test_disable_ipv6_dhcp_server(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = disable_ipv6_dhcp_server(
            device=device,
            interface="HundredGigE1/0/21",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface HundredGigE1/0/21",
                "no ipv6 dhcp server",
            ],
        )


if __name__ == "__main__":
    unittest.main()