import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_ipv6_nd_suppress_ra,
)


class TestConfigureIpv6NdSuppressRa(TestCase):

    def test_configure_ipv6_nd_suppress_ra(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_nd_suppress_ra(
            device,
            "GigabitEthernet1/0/24",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/24", sent_commands)
        self.assertIn("ipv6 nd suppress-ra", sent_commands)


if __name__ == "__main__":
    unittest.main()