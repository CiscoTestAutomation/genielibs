import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ipv6_prefix_name_on_interface,
)


class TestConfigureIpv6PrefixNameOnInterface(TestCase):

    def test_configure_ipv6_prefix_name_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_prefix_name_on_interface(
            device,
            "loopback1",
            "pool1",
            "::1/64",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface loopback1", sent_commands)
        self.assertIn("ipv6 address pool1 ::1/64", sent_commands)


if __name__ == "__main__":
    unittest.main()