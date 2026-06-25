import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_ip_domain_lookup


class TestUnconfigIpDomainLookup(TestCase):

    def test_unconfig_ip_domain_lookup(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_ip_domain_lookup(
            device,
            "Hu1/0/7",
            "14",
        )

        self.assertIsNone(result)
        self.assertEqual(device.configure.call_count, 2)

        first_command = device.configure.mock_calls[0].args[0]
        self.assertIsInstance(first_command, str)
        self.assertEqual(
            first_command,
            "no ip domain lookup source-interface Hu1/0/7",
        )

        second_command = device.configure.mock_calls[1].args[0]
        self.assertIsInstance(second_command, str)
        self.assertEqual(
            second_command,
            "no ip domain lookup source-interface vlan 14",
        )


if __name__ == "__main__":
    unittest.main()