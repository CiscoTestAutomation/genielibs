import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_ipv6_verify_unicast_source,
)


class TestConfigureInterfaceIpv6VerifyUnicastSource(TestCase):

    def test_configure_interface_ipv6_verify_unicast_source(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_ipv6_verify_unicast_source(
            device,
            "GigabitEthernet1/0/6",
            "any",
            "",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/6", sent_commands)
        self.assertIn(
            "ipv6 verify unicast source reachable-via any",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()