import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipv6_ra_dhcp_guard.configure import (
    configure_dhcpv6_guard_policy,
)


class TestConfigureDhcpv6GuardPolicy(TestCase):

    def test_configure_dhcpv6_guard_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_dhcpv6_guard_policy(
            device,
            "test2",
            "client",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ipv6 dhcp guard policy test2",
                "device-role client",
            ],
        )


if __name__ == "__main__":
    unittest.main()
