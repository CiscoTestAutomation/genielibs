import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ipv6_enable


class TestUnconfigureIpv6Enable(TestCase):

    def test_unconfigure_ipv6_enable(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ipv6_enable(
            device,
            "GigabitEthernet10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet10",
            sent_commands,
        )
        self.assertIn(
            "no ipv6 enable",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()