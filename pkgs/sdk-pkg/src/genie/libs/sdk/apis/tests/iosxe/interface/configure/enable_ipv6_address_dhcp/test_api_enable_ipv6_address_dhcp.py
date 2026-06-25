import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import enable_ipv6_address_dhcp


class TestEnableIpv6AddressDhcp(TestCase):

    def test_enable_ipv6_address_dhcp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = enable_ipv6_address_dhcp(
            device=device,
            interface="HundredGigE1/0/20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface HundredGigE1/0/20",
                "ipv6 enable",
                "ipv6 address dhcp",
            ],
        )


if __name__ == "__main__":
    unittest.main()