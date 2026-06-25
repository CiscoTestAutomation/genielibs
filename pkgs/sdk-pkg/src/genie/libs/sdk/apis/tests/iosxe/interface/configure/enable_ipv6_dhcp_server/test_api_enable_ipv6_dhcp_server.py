import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import enable_ipv6_dhcp_server


class TestEnableIpv6DhcpServer(TestCase):

    def test_enable_ipv6_dhcp_server(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = enable_ipv6_dhcp_server(
            device,
            "TenGigabitEthernet1/0/3",
            None,
            "False",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TenGigabitEthernet1/0/3",
                "ipv6 dhcp server",
            ],
        )


if __name__ == "__main__":
    unittest.main()