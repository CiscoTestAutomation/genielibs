import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_ipv6_enable


class TestConfigureIpv6Enable(TestCase):

    def test_configure_ipv6_enable(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_enable(device, "GigabitEthernet10")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet10", sent_commands)
        self.assertIn("ipv6 enable", sent_commands)


if __name__ == "__main__":
    unittest.main()