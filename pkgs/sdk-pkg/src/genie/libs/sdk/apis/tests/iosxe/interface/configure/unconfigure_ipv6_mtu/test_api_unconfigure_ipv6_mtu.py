import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ipv6_mtu


class TestUnconfigureIpv6Mtu(TestCase):

    def test_unconfigure_ipv6_mtu(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipv6_mtu(
            device,
            "HundredGigE1/0/29",
            "2000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface HundredGigE1/0/29",
            sent_commands,
        )
        self.assertIn(
            "no ipv6 mtu 2000",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()